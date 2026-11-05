import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from editorial_queue import COLLECTIONS, HOLDS, INBOX, REGISTRY, QUARANTINED_INVALID_REQUESTS, apply, digest, scan, validate


def git(root, *args, check=True):
    return subprocess.run(["git", "-C", str(root), *args], check=check,
                          text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def initialize(root):
    for collection in COLLECTIONS:
        (root / "chapitres" / collection).mkdir(parents=True)
    existing = root / "chapitres/origines-du-sacre/583-premiere-etude.md"
    existing.write_text("# Chapitre 583\n\nTexte universitaire intact.\n")
    (root / REGISTRY).parent.mkdir(parents=True)
    data = {"version":1, "collections":{c:{"legacy":scan(root,c),"allocations":{}} for c in COLLECTIONS}}
    (root / REGISTRY).write_text(json.dumps(data))
    return existing


def request(root, slug, collection="origines-du-sacre", request_id=None, body=None):
    request_id = request_id or str(uuid.uuid4())
    path = root / INBOX / (request_id + ".json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"version":1,"collection":collection,"slug":slug,
                               "markdown":body or "# Chapitre {{numero}}\n\nÉtude intégrale, référence antique 583.1.\n"}))
    return path


class AllocationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.existing = initialize(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_two_requests_unique_replay_and_manuscript_preservation(self):
        before = self.existing.read_bytes()
        request(self.root,"premier")
        request(self.root,"second")
        paths = apply(self.root)
        self.assertEqual({scan(self.root,"origines-du-sacre")[p] for p in paths},{584,585})
        for path in paths:
            self.assertIn("référence antique 583.1.", (self.root/path).read_text())
        self.assertEqual(apply(self.root),[])
        self.assertEqual(self.existing.read_bytes(),before)

    def test_collection_counters_are_independent_and_formats_are_preserved(self):
        request(self.root,"premier","comedies")
        request(self.root,"second","tragedies",body="# Volume {{volume}}\n\nAnalyse.")
        request(self.root,"troisieme","comparatif",body="# Volume {{volume}}\n\nAnalyse.")
        request(self.root,"quatrieme","encyclopedie")
        paths = apply(self.root)
        self.assertIn("chapitres/comedies/volume-001-premier.md",paths)
        self.assertIn("chapitres/tragedies/volume-i-second.md",paths)
        self.assertIn("chapitres/comparatif/volume-i-troisieme.md",paths)
        self.assertIn("chapitres/encyclopedie/chapitre-1-quatrieme.md",paths)

    def test_mutated_request_rejected(self):
        path = request(self.root,"etude")
        apply(self.root)
        path.write_text(path.read_text()+"\n")
        with self.assertRaisesRegex(ValueError,"modifiée"):
            apply(self.root)

    def test_unallocated_duplicate_and_unregistered_new_number_rejected(self):
        for name in ("583-autre.md","584-autre.md"):
            path = self.existing.with_name(name)
            path.write_text("# Autre texte")
            with self.assertRaisesRegex(ValueError,"non attribuée"):
                validate(self.root)
            path.unlink()

    def test_bad_batch_writes_nothing_and_keeps_requests(self):
        request(self.root,"valide",request_id="00000000-0000-0000-0000-000000000001")
        request(self.root,"invalide",request_id="ffffffff-ffff-ffff-ffff-ffffffffffff",body="# Numéro fixé 584")
        before = (self.root/REGISTRY).read_bytes()
        with self.assertRaises(ValueError):
            apply(self.root)
        self.assertEqual((self.root/REGISTRY).read_bytes(),before)
        self.assertEqual(len(list((self.root/INBOX).glob("*.json"))),2)
        self.assertEqual(len(scan(self.root,"origines-du-sacre")),1)

    def test_duplicate_slug_rejected(self):
        request(self.root,"meme-sujet")
        apply(self.root)
        request(self.root,"meme-sujet")
        with self.assertRaisesRegex(ValueError,"déjà présente"):
            apply(self.root)

    def hold(self, *requests):
        (self.root / HOLDS).write_text(json.dumps({"version": 1, "requests": {
            p.stem: {"request_sha256": digest(p.read_bytes()), "reason": "Collision à réconcilier"}
            for p in requests}}))

    def test_explicit_holds_preserve_both_conflicts_without_blocking_valid_work(self):
        body = "# Volume {{volume}}\n\n## MC-033 — Dieux absents\n\nTexte intégral et bibliographie.\n"
        a = request(self.root, "absence-a", "comparatif", body=body)
        b = request(self.root, "absence-b", "comparatif", body=body)
        originals = {p: p.read_bytes() for p in (a, b)}
        self.hold(a, b)
        valid = request(self.root, "etude-valide")
        self.assertEqual(apply(self.root), ["chapitres/origines-du-sacre/584-etude-valide.md"])
        self.assertEqual(scan(self.root, "comparatif"), {})
        receipts = json.loads((self.root / REGISTRY).read_text())["collections"]
        self.assertEqual(receipts["comparatif"]["allocations"], {})
        self.assertIn(valid.stem, receipts["origines-du-sacre"]["allocations"])
        self.assertEqual({p: p.read_bytes() for p in (a,b)}, originals)
        self.assertEqual(apply(self.root), [])
        # Releasing unresolved requests must restore the strict collision guard.
        before = (self.root / REGISTRY).read_bytes()
        (self.root / HOLDS).unlink()
        with self.assertRaisesRegex(ValueError, "MC-033"):
            apply(self.root)
        self.assertEqual((self.root / REGISTRY).read_bytes(), before)
        self.assertEqual(scan(self.root, "comparatif"), {})

    def test_one_held_mc042_allows_first_allocation_without_identity_collision(self):
        """Historical MC identity is distinct from the canonical number.

        When two different manuscripts claim MC-042, a hash-locked hold on the
        second must not suppress the first or permit a second MC-042 volume.
        Neither original inbox manuscript may be rewritten by the allocator.
        """
        first = request(
            self.root, "mc-042-measurement", "comparatif",
            body="# Volume {{volume}} ({{numero}})\n"
                 "## MC-042 — Mesurer le sacré\n\n"
                 "Étude A : étalons, poids et justice.\n",
        )
        second = request(
            self.root, "mc-042-scribes", "comparatif",
            body="# Volume {{volume}} ({{numero}})\n"
                 "## MC-042 — Qui écrit pour les dieux ?\n\n"
                 "Étude B : Nisaba, Nabû, Thot et Seshat.\n",
        )
        originals = {p: p.read_bytes() for p in (first, second)}
        self.hold(second)

        self.assertEqual(apply(self.root), [
            "chapitres/comparatif/volume-i-mc-042-measurement.md"
        ])
        state = json.loads((self.root / REGISTRY).read_text())["collections"]["comparatif"]
        self.assertEqual(state["allocations"][first.stem]["number"], 1)
        self.assertNotIn(second.stem, state["allocations"])
        self.assertEqual({p: p.read_bytes() for p in (first, second)}, originals)
        self.assertEqual(apply(self.root), [])

        # An unreconciled hold must never be lifted as a shortcut to publish.
        (self.root / HOLDS).unlink()
        before = (self.root / REGISTRY).read_bytes()
        with self.assertRaisesRegex(ValueError, "MC-042"):
            apply(self.root)
        self.assertEqual((self.root / REGISTRY).read_bytes(), before)
        self.assertEqual({p: p.read_bytes() for p in (first, second)}, originals)

    def test_hold_rejects_manuscript_mutation_before_any_allocation(self):
        held = request(self.root, "attente")
        self.hold(held)
        request(self.root, "autre")
        before = (self.root / REGISTRY).read_bytes()
        held.write_text(held.read_text() + "\n")
        with self.assertRaisesRegex(ValueError, "attente modifié"):
            apply(self.root)
        self.assertEqual((self.root / REGISTRY).read_bytes(), before)

    def test_hold_cannot_hide_a_published_receipt(self):
        published = request(self.root, "etude")
        apply(self.root)
        self.hold(published)
        with self.assertRaisesRegex(ValueError, "déjà attribuée"):
            validate(self.root)


    def test_non_uuid_mc069_request_is_hash_locked_and_kept_without_blocking_queue(self):
        """A malformed historical submission must survive without blocking unrelated studies."""
        source = Path(__file__).resolve().parents[1] / INBOX / "20261105-mc-069-souffle-vent-vie-philologie.json"
        original = source.read_bytes()
        self.assertEqual(digest(original), QUARANTINED_INVALID_REQUESTS[source.name]["sha256"])
        self.assertEqual(json.loads(original)["collection"], "comparatif")
        self.assertEqual(len(json.loads(original)["markdown"]), 91145)
        held = self.root / INBOX / source.name
        held.parent.mkdir(parents=True, exist_ok=True)
        held.write_bytes(original)
        request(self.root, "valide-apres-quarantaine")
        self.assertEqual(apply(self.root), ["chapitres/origines-du-sacre/584-valide-apres-quarantaine.md"])
        self.assertEqual(held.read_bytes(), original)
        self.assertEqual(apply(self.root), [])
        held.write_bytes(original + b"\\n")
        with self.assertRaisesRegex(ValueError, "modifié"):
            apply(self.root)


class GitRaceTests(unittest.TestCase):
    def test_ci_script_retries_real_race_then_replays_without_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            origin, a, b = tmp/"origin.git", tmp/"a", tmp/"b"
            git(tmp,"init","--bare",str(origin))
            git(tmp,"clone",str(origin),str(a))
            git(a,"checkout","-b","main")
            initialize(a)
            scripts = Path(__file__).resolve().parents[1]/"scripts"
            (a/"scripts").mkdir()
            for name in ("editorial_queue.py","publish_site.py","comparative_history.py"):
                shutil.copy2(scripts/name, a/"scripts"/name)
            # Lightweight fixtures isolate actual Git retry behaviour from the
            # full site build, which is exercised separately on the real corpus.
            (a/"scripts/build_native.py").write_text("from pathlib import Path\nPath('_site').mkdir(exist_ok=True)\nPath('_site/index.html').write_text('test')\n")
            (a/"scripts/validate_publication.py").write_text("from pathlib import Path\nfrom editorial_queue import validate\nvalidate(Path('.'))\n")
            (a/".gitignore").write_text("_site/\n__pycache__/\n")
            request(a,"texte-a",request_id="00000000-0000-0000-0000-000000000001")
            for name,value in (("user.name","Test"),("user.email","test@example.invalid")):
                git(a,"config",name,value)
            git(a,"add",".");git(a,"commit","-m","Queued request A")
            git(a,"push","-u","origin","main")
            git(tmp,"clone","--branch","main",str(origin),str(b))
            for name,value in (("user.name","Test"),("user.email","test@example.invalid")):
                git(b,"config",name,value)
            request(b,"texte-b",request_id="00000000-0000-0000-0000-000000000002")
            git(b,"add",".");git(b,"commit","-m","Concurrent request B")
            hook=a/".git/hooks/pre-push"
            # A's first push is made stale after its local allocation/build.
            hook.write_text("#!/bin/sh\nrm -- \"$0\"\nunset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE\ngit -C '"+str(b)+"' push origin HEAD:main\n")
            hook.chmod(0o755)
            env={**os.environ,"GITHUB_ACTIONS":"true"}
            result=subprocess.run([sys.executable,"scripts/publish_site.py"],cwd=a,env=env,text=True,capture_output=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertIn("Nouvelles demandes conservées",result.stdout)
            state=json.loads(git(origin,"show","main:"+REGISTRY.as_posix()).stdout)["collections"]["origines-du-sacre"]
            self.assertEqual(sorted([*state["legacy"].values(),*(x["number"] for x in state["allocations"].values())]),[583,584])
            first_receipts=state["allocations"]
            self.assertEqual(len(first_receipts),1)
            replay=subprocess.run([sys.executable,"scripts/publish_site.py"],cwd=a,env=env,text=True,capture_output=True)
            self.assertEqual(replay.returncode,0,replay.stdout+replay.stderr)
            state=json.loads(git(origin,"show","main:"+REGISTRY.as_posix()).stdout)["collections"]["origines-du-sacre"]
            self.assertEqual(sorted([*state["legacy"].values(),*(x["number"] for x in state["allocations"].values())]),[583,584,585])
            self.assertTrue(all(state["allocations"][key]==value for key,value in first_receipts.items()))
            first_head=git(origin,"rev-parse","main").stdout
            replay=subprocess.run([sys.executable,"scripts/publish_site.py"],cwd=a,env=env,text=True,capture_output=True)
            self.assertEqual(replay.returncode,0,replay.stdout+replay.stderr)
            self.assertEqual(git(origin,"rev-parse","main").stdout,first_head)

    def test_rejected_push_reloads_main_and_assigns_next_number(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            origin, a, b = tmp/"origin.git", tmp/"a", tmp/"b"
            git(tmp,"init","--bare",str(origin))
            git(tmp,"clone",str(origin),str(a))
            git(a,"checkout","-b","main")
            initialize(a)
            for name,value in (("user.name","Test"),("user.email","test@example.invalid")):
                git(a,"config",name,value)
            git(a,"add","."); git(a,"commit","-m","Baseline")
            git(a,"push","-u","origin","main")
            git(tmp,"clone","--branch","main",str(origin),str(b))
            for name,value in (("user.name","Test"),("user.email","test@example.invalid")):
                git(b,"config",name,value)
            request(a,"texte-a")
            queued_b=request(b,"texte-b")
            payload_b=queued_b.read_bytes(); id_b=queued_b.name
            self.assertIn("584-texte-a",apply(a)[0])
            self.assertIn("584-texte-b",apply(b)[0])
            for checkout in (a,b):
                git(checkout,"add",".");git(checkout,"commit","-m","Allocation")
            git(a,"push","origin","HEAD:main")
            self.assertNotEqual(git(b,"push","origin","HEAD:main",check=False).returncode,0)
            git(b,"fetch","origin","main");git(b,"reset","--hard","origin/main")
            (b/INBOX/id_b).write_bytes(payload_b)
            self.assertIn("585-texte-b",apply(b)[0])
            git(b,"add",".");git(b,"commit","-m","Allocation recalculated")
            git(b,"push","origin","HEAD:main")
            validate(b)
            self.assertTrue((b/"chapitres/origines-du-sacre/584-texte-a.md").is_file())
            self.assertTrue((b/"chapitres/origines-du-sacre/585-texte-b.md").is_file())


if __name__ == "__main__":
    unittest.main()
