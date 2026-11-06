"""Réconcilier ODS 698/699 sans altérer les deux manuscrits attribués.

Le rapprochement porte sur le même corpus archéologique (Dalton et al., 2022) ;
les notices sont ajoutées au rendu HTML, hors des articles intégraux.
"""
from hashlib import sha256
from html import escape
import json
from pathlib import Path

from bs4 import BeautifulSoup

KEY = "ods-khaybar-698-699"
DOI = "https://doi.org/10.1177/09596836211060497"
PORTAL = "origines-du-sacre/index.html"
STUDIES = (
    {
        "number": 698,
        "uuid": "113452c2-9480-55b3-b64c-4b4979a9b592",
        "path": "chapitres/origines-du-sacre/698-khaybar-alula-avenues-funeraires-tombes-pendentifs-bronze.md",
        "title": "698 — Paysages mortuaires, tombes à pendentifs et mémoire territoriale",
        "focus": (
            "Étude des formes funéraires, de leur visibilité depuis les chemins, "
            "de la mémoire territoriale et des trois modèles proposés (repères, "
            "présence ancestrale, ritualisation du passage). Durkheim, Vernant, "
            "Detienne, Nietzsche (1874) et Hegel servent ici de cadres critiques, "
            "non de sources sur les croyances des bâtisseurs."
        ),
        "bibliography": (
            "Outre Dalton et al. (2022) : communiqué UWA (2022), "
            "Kennedy et al. (2023), Magee (2014), McCorriston (2011), "
            "Durkheim, Vernant, Detienne, Nietzsche et Hegel."
        ),
    },
    {
        "number": 699,
        "uuid": "1ab73d6e-5e9e-45c9-8ba1-2867a61c42fe",
        "path": "chapitres/origines-du-sacre/699-arabie-avenues-funeraires-oasis-khaybar-alula-mobilite-pastorale.md",
        "title": "699 — Systèmes de mobilité, oasis, eau et télédétection",
        "focus": (
            "Analyse des protocoles d'inventaire satellitaire et aérien, "
            "des segments d'avenues, des orientations et des relations aux "
            "points d'eau. Discussion des itinéraires, pâturages, modèles "
            "de déplacement, murs d'oasis et limites des hypothèses climatiques."
        ),
        "bibliography": (
            "Outre Dalton et al. (2022) : Kennedy et al. (2021), "
            "Thomas et al. (2025), Charloux et al. (2024), "
            "Bec Drelon et al. (2026), Petraglia et al. (2020), "
            "Douglas, Girard et les comparaisons péninsulaires."
        ),
    },
)

SHARED = (
    "Les chapitres 698 et 699 étudient le même ensemble Khaybar–al-ʿUlā, "
    "non deux découvertes indépendantes. Leur référence empirique centrale "
    "est Dalton et collaborateurs, The Holocene 32/3 (2022). Les chiffres "
    "d'inventaire, les typologies et les datations qui en sont issus ne "
    "constituent pas deux confirmations distinctes. Les monuments et leurs "
    "rapports spatiaux sont documentés ; la propriété lignagère, un culte "
    "des ancêtres ou un usage processionnel obligatoire restent des hypothèses."
)


def url_of(study):
    return "/" + Path(study["path"]).with_suffix("").as_posix() + "/"


def validate_sources(root, out):
    """Contrôler deux reçus, les sources immuables et l'absence de retenues."""
    root, out = Path(root), Path(out)
    registry = json.loads((root / "editorial/numbering.json").read_text(encoding="utf-8"))
    holds = json.loads((root / "editorial/holds.json").read_text(encoding="utf-8"))
    allocations = registry["collections"]["origines-du-sacre"]["allocations"]
    seen_urls = set()
    for study in STUDIES:
        uid = study["uuid"]
        receipt = allocations.get(uid)
        if not receipt or receipt["number"] != study["number"] or receipt["path"] != study["path"]:
            raise ValueError("Identité canonique ou reçu manquant : " + uid)
        if uid in holds.get("requests", {}):
            raise ValueError("Demande attribuée retenue à tort : " + uid)
        request = root / "editorial" / "inbox" / (uid + ".json")
        source = root / study["path"]
        page = out / url_of(study).strip("/") / "index.html"
        if not request.is_file() or not source.is_file() or not page.is_file():
            raise ValueError("Manuscrit ou lecteur historique absent : " + uid)
        if sha256(request.read_bytes()).hexdigest() != receipt["request_sha256"]:
            raise ValueError("Demande historique altérée : " + uid)
        source_bytes = source.read_bytes()
        if sha256(source_bytes).hexdigest() != receipt["initial_source_sha256"]:
            raise ValueError("Source historique altérée : " + study["path"])
        if len(source_bytes) < (28000 if study["number"] == 698 else 40000):
            raise ValueError("Étude abrégée : " + study["path"])
        source_text = source_bytes.decode("utf-8")
        if "10.1177/09596836211060497" not in source_text or "bibliograph" not in source_text.casefold():
            raise ValueError("Appareil scientifique absent : " + study["path"])
        if url_of(study) in seen_urls:
            raise ValueError("URL canonique dupliquée")
        seen_urls.add(url_of(study))
    if not (out / PORTAL).is_file():
        raise ValueError("Sommaire des Origines du sacré absent")
    return {study["path"]: sha256((root / study["path"]).read_bytes()).hexdigest()
            for study in STUDIES}


def panel(study=None):
    """Notice contextuelle pour un lecteur, ou concordance pour le portail."""
    common = (
        '<p>' + escape(SHARED) + ' <a href="' + DOI +
        '">Étude archéologique commune (DOI 10.1177/09596836211060497)</a>.</p>'
    )
    entries = "".join(
        '<li><a href="' + escape(url_of(s), quote=True) + '">' +
        escape(s["title"]) + '</a><small>' + escape(s["focus"]) +
        '</small></li>'
        for s in STUDIES if study is None or s["number"] != study["number"]
    )
    if study is None:
        heading = "Khaybar et al-ʿUlā — concordance scientifique des chapitres 698 et 699"
        context = (
            "<p>Deux monographies intégrales et deux numéros canoniques conservés : "
            "le 698 analyse la monumentalisation de la mort et la mémoire territoriale ; "
            "le 699 étudie les traces de circulation, les données SIG, les oasis "
            "et les mobilités pastorales. Lire ensemble, sans double comptage "
            "des observations de Dalton et collaborateurs.</p>"
        )
        tag = "section"
    else:
        heading = "Concordance éditoriale — chapitres 698 et 699"
        context = (
            "<p><strong>Objet propre du chapitre " + str(study["number"]) + " :</strong> " +
            escape(study["focus"]) + "</p><p><strong>Bibliographie spécifique :</strong> " +
            escape(study["bibliography"]) + "</p>"
        )
        tag = "aside"
    return (
        '<' + tag + ' class="mythos-concordance" data-mythos-concordance="' +
        KEY + '" aria-label="' + escape(heading, quote=True) + '">' +
        '<h2>' + escape(heading) + '</h2>' + context + common +
        '<ul>' + entries + '</ul></' + tag + '>'
    )


def install(root, out):
    """Insérer des notices réciproques et une entrée dans le sommaire.

    Les articles et les sources Markdown restent byte-identiques. La passe
    est idempotente pour les reconstructions et ne modifie aucun registre.
    """
    root, out = Path(root), Path(out)
    snapshots = validate_sources(root, out)
    for study in STUDIES:
        url = url_of(study)
        path = out / url.strip("/") / "index.html"
        doc = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        main = doc.select_one("main")
        article = main.select_one("article.content") if main else None
        if article is None:
            raise ValueError("Lecteur universitaire absent : " + url)
        original_article = str(article)
        for old in main.select('aside[data-mythos-concordance="' + KEY + '"]'):
            old.decompose()
        main.append(BeautifulSoup(panel(study), "html.parser").aside)
        if str(article) != original_article:
            raise ValueError("Texte universitaire modifié : " + url)
        path.write_text(str(doc), encoding="utf-8")
    index = out / PORTAL
    doc = BeautifulSoup(index.read_text(encoding="utf-8"), "html.parser")
    main = doc.select_one("main article.content") or doc.select_one("main")
    if main is None:
        raise ValueError("Sommaire des Origines sans conteneur")
    for old in main.select('section[data-mythos-concordance="' + KEY + '"]'):
        old.decompose()
    main.append(BeautifulSoup(panel(), "html.parser").section)
    index.write_text(str(doc), encoding="utf-8")
    for name, expected in snapshots.items():
        if sha256((root / name).read_bytes()).hexdigest() != expected:
            raise ValueError("Manuscrit original modifié pendant la concordance : " + name)
    return {"readers": 2, "portal": 1, "canonical_numbers": [698, 699]}
