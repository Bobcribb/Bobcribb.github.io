#!/usr/bin/env python3
"""Number approved manuscripts from a fresh main snapshot, before a normal push.

`apply` is local and transactional at the Git commit level. Only publish_main.sh
may commit its result: a rejected push must discard it and allocate again from
the new main. Requests are immutable, and their UUID is the idempotency key.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import uuid

REGISTRY = Path("editorial/numbering.json")
INBOX = Path("editorial/inbox")
HOLDS = Path("editorial/holds.json")
QUARANTINED_INVALID_REQUESTS = {
    "85ed9610-42a9-4b7b-90e0-2aeb8a619d041.json": {
        "sha256": "35fbad6ea7ae497995708c70346a54395ed40cb5692d305db4938e8c954c195f",
        "reason": "Nom UUID historique mal formé (MC-041) : conserver le manuscrit intact sans l'allouer tant qu'il n'est pas réémis sous un UUID canonique.",
    },
}
COLLECTIONS = {
    "origines-du-sacre": ("", "decimal", 0),
    "encyclopedie": ("chapitre-", "decimal", 0),
    "comedies": ("volume-", "decimal", 3),
    "tragedies": ("volume-", "roman", 0),
    "comparatif": ("volume-", "roman", 0),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def roman(number):
    if not 0 < number < 4000:
        raise ValueError("Volume romain hors limites")
    result = ""
    for value, letters in [(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),
                           (100,"C"),(90,"XC"),(50,"L"),(40,"XL"),
                           (10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]:
        while number >= value:
            result += letters
            number -= value
    return result


def number_of(name, collection):
    prefix, style, width = COLLECTIONS[collection]
    token = r"([ivxlcdm]+)" if style == "roman" else r"([0-9]+)"
    match = re.fullmatch(re.escape(prefix) + token + r"-[a-z0-9][a-z0-9-]*\.md", name)
    if not match:
        return None
    value = match[1]
    if style == "decimal":
        number = int(value)
    else:
        digits = {"i":1,"v":5,"x":10,"l":50,"c":100,"d":500,"m":1000}
        number = sum(-digits[c] if i+1 < len(value) and digits[c] < digits[value[i+1]]
                     else digits[c] for i,c in enumerate(value))
        if roman(number).lower() != value:
            raise ValueError("Numéro romain invalide : " + name)
    if number < 1:
        raise ValueError("Numéro invalide : " + name)
    return number


def scan(root, collection):
    return {p.relative_to(root).as_posix(): number
            for p in sorted((root / "chapitres" / collection).glob("*.md"))
            if (number := number_of(p.name, collection)) is not None}


def load_registry(root):
    data = json.loads((root / REGISTRY).read_text(encoding="utf-8"))
    if data.get("version") != 1 or set(data.get("collections", {})) != set(COLLECTIONS):
        raise ValueError("Registre éditorial invalide")
    return data


def validate(root, data=None):
    data = data if data is not None else load_registry(root)
    request_ids = set()
    for collection in COLLECTIONS:
        state = data["collections"][collection]
        expected = dict(state["legacy"])
        occupied = set(expected.values())
        for request_id, allocation in state["allocations"].items():
            if request_id in request_ids:
                raise ValueError("Demande attribuée à plusieurs collections : " + request_id)
            request_ids.add(request_id)
            number, path = allocation["number"], allocation["path"]
            if number in occupied or path in expected:
                raise ValueError("Attribution en doublon : " + path)
            if Path(path).parent != Path("chapitres") / collection or number_of(Path(path).name, collection) != number:
                raise ValueError("Chemin d'attribution incohérent : " + path)
            request = root / INBOX / (request_id + ".json")
            if not request.is_file() or digest(request.read_bytes()) != allocation["request_sha256"]:
                raise ValueError("Demande publiée modifiée ou supprimée : " + request_id)
            occupied.add(number)
            expected[path] = number
        actual = scan(root, collection)
        if actual != expected:
            added = sorted(set(actual) - set(expected))
            missing = sorted(set(expected) - set(actual))
            raise ValueError(f"{collection} : numérotation non attribuée ou source manquante; "
                             f"ajouts={added}, absences={missing}. Utiliser editorial/inbox.")
    load_holds(root, request_ids)
    from comparative_history import validate as validate_history
    validate_history(root)
    from tragedy_work_identity import validate as validate_tragedy_identity
    validate_tragedy_identity(root)
    return data


def parse_request(path):
    if str(uuid.UUID(path.stem)) != path.stem:
        raise ValueError("Identifiant de demande non canonique : " + path.name)
    raw = path.read_bytes()
    item = json.loads(raw)
    if set(item) != {"version", "collection", "slug", "markdown"} or item["version"] != 1:
        raise ValueError("Schéma de demande invalide : " + path.name)
    if item["collection"] not in COLLECTIONS:
        raise ValueError("Collection inconnue")
    if not isinstance(item["slug"], str) or not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", item["slug"]):
        raise ValueError("Slug invalide")
    body = item["markdown"]
    if not isinstance(body, str) or not body.strip() or not any(t in body for t in ("{{numero}}", "{{volume}}")):
        raise ValueError("Le manuscrit doit utiliser {{numero}} ou {{volume}}, sans numéro réservé")
    if re.search(r"\{\{(?!(?:numero|volume)\}\})", body):
        raise ValueError("Variable de manuscrit inconnue")
    return item, digest(raw)


def load_holds(root, allocated_ids):
    """Explicit, hash-locked holds keep unresolved submissions intact in inbox.

    A hold never changes a published receipt or suppresses validation of its
    manuscript. Removing a hold restores the usual collision checks.
    """
    path = root / HOLDS
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if set(data) != {"version", "requests"} or data["version"] != 1 or not isinstance(data["requests"], dict):
        raise ValueError("Registre des attentes éditoriales invalide")
    for key, hold in data["requests"].items():
        if str(uuid.UUID(key)) != key or key in allocated_ids:
            raise ValueError("Attente interdite pour une demande déjà attribuée : " + key)
        if set(hold) != {"request_sha256", "reason"} or not isinstance(hold["reason"], str) or not hold["reason"].strip():
            raise ValueError("Motif d’attente éditoriale invalide : " + key)
        request = root / INBOX / (key + ".json")
        if not request.is_file():
            raise ValueError("Manuscrit en attente absent : " + key)
        _, payload_hash = parse_request(request)
        if payload_hash != hold["request_sha256"]:
            raise ValueError("Manuscrit en attente modifié : " + key)
    return data["requests"]


def apply(root):
    data = validate(root)
    receipts = {key: value for state in data["collections"].values()
                for key, value in state["allocations"].items()}
    holds = load_holds(root, receipts)
    planned = []
    # Prepare every request before writing anything; a malformed request cannot
    # leave a partially allocated batch in the worktree.
    for path in sorted((root / INBOX).glob("*.json")):
        quarantine = QUARANTINED_INVALID_REQUESTS.get(path.name)
        if quarantine:
            payload_hash = digest(path.read_bytes())
            if payload_hash != quarantine["sha256"]:
                raise ValueError("Manuscrit au nom UUID invalide modifié : " + path.name)
            print("Demande au nom UUID invalide conservée hors allocation : " + path.name + " — " + quarantine["reason"], file=sys.stderr)
            continue
        item, payload_hash = parse_request(path)
        if path.stem in receipts:
            continue
        if path.stem in holds:
            print("Attente éditoriale conservée : " + path.stem + " — " + holds[path.stem]["reason"], file=sys.stderr)
            continue
        collection = item["collection"]
        state = data["collections"][collection]
        numbers = [*scan(root, collection).values(),
                   *(a["number"] for a in state["allocations"].values())]
        number = max(numbers, default=0) + 1
        prefix, style, width = COLLECTIONS[collection]
        token = roman(number).lower() if style == "roman" else str(number).zfill(width)
        target = Path("chapitres") / collection / f"{prefix}{token}-{item['slug']}.md"
        # A new UUID cannot accidentally publish the same work twice.
        def same_slug(candidate):
            return (number_of(candidate.name, collection) is not None and
                    candidate.stem.removeprefix(prefix).split("-", 1)[1] == item["slug"])
        existing = [p for p in (root / "chapitres" / collection).glob("*.md") if same_slug(p)]
        if existing or any(p.parent == target.parent and same_slug(p) for p, _ in planned):
            raise ValueError("Étude déjà présente (slug identique) : " + item["slug"])
        if (root / target).exists():
            raise ValueError("Refus d'écraser " + str(target))
        body = item["markdown"].replace("{{numero}}", str(number))
        if "{{volume}}" in body:
            body = body.replace("{{volume}}", roman(number))
        encoded = body.encode("utf-8")
        state["allocations"][path.stem] = {
            "number": number, "path": target.as_posix(),
            "request_sha256": payload_hash, "initial_source_sha256": digest(encoded),
        }
        planned.append((target, encoded))
    from comparative_history import validate as validate_history
    validate_history(root, planned)
    from tragedy_work_identity import validate as validate_tragedy_identity
    validate_tragedy_identity(root, planned)
    for target, encoded in planned:
        (root / target).parent.mkdir(parents=True, exist_ok=True)
        with (root / target).open("xb") as stream:
            stream.write(encoded)
    if planned:
        (root / REGISTRY).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    validate(root, data)
    return [p.as_posix() for p, _ in planned]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    sub.add_parser("apply")
    enqueue = sub.add_parser("enqueue")
    enqueue.add_argument("--collection", choices=COLLECTIONS, required=True)
    enqueue.add_argument("--slug", required=True)
    enqueue.add_argument("--source", type=Path, required=True)
    enqueue.add_argument("--request-id", default=None)
    args = parser.parse_args()
    root = Path.cwd()
    if args.command == "check":
        validate(root)
        print("Numérotation : registre et sources cohérents dans les cinq collections")
    elif args.command == "apply":
        print(json.dumps({"allocated": apply(root)}, ensure_ascii=False))
    else:
        request_id = args.request_id or str(uuid.uuid4())
        if str(uuid.UUID(request_id)) != request_id:
            raise ValueError("UUID canonique requis")
        path = root / INBOX / (request_id + ".json")
        item = {"version": 1, "collection": args.collection, "slug": args.slug,
                "markdown": args.source.read_text(encoding="utf-8")}
        path.parent.mkdir(parents=True, exist_ok=True)
        encoded = (json.dumps(item, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        if path.exists():
            if path.read_bytes() != encoded:
                raise ValueError("UUID déjà utilisé pour un autre texte")
        else:
            with path.open("xb") as stream:
                stream.write(encoded)
            try:
                parse_request(path)
            except Exception:
                path.unlink()
                raise
        print(path.relative_to(root))


if __name__ == "__main__":
    main()
