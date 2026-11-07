"""Vérifier la conservation et la visibilité des compléments Énéide du 7 novembre 2026."""
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "philosophie-eneide.html"
CORPUS = ROOT / "corpus/philosophie/eneide"
SAMPLES = {
    "00-introduction.md": "La fondation romaine comme récit de plusieurs temps historiques",
    "01-chant-i.md": "Le proème et la question du jugement porté sur les dieux",
    "02-chant-ii.md": "Lecture rapprochée : Priam, Pyrrhus et les droits du suppliant",
    "03-chant-iii.md": "Polydore : quand le sol révèle le crime",
    "04-chant-iv.md": "Microlecture philologique : « coniugium » et « culpa »",
    "05-chant-v.md": "Les jeux d’Anchise : l’honneur comme distribution contestable",
    "06-chant-vi.md": "Les impératifs d’Anchise",
    "07-chant-vii.md": "« Acheronta movebo »",
    "08-chant-viii.md": "L’ekphrasis et la fabrication d’une mémoire politique",
    "09-chant-ix.md": "« Dine hunc ardorem »",
    "10-chant-x.md": "Lausus, miroir de la pietas du vainqueur",
    "11-chant-xi.md": "La trêve des morts : un minimum commun entre ennemis",
    "12-chant-xii.md": "Une supplication exactement formulée",
    "13-pietas-destin.md": "La pietas entre fidélité familiale et responsabilité publique",
    "14-empire-memoire.md": "L’augustéisme de l’épopée",
    "15-philosophies-comparaisons.md": "Hegel, téléologie et résistance des existences singulières",
    "16-poetique-conclusion.md": "Récits enchâssés, récits de survivants et autorité de la voix",
    "17-reperes-et-sources.md": "Appareil critique complémentaire",
}

class EneideDeepeningTest(unittest.TestCase):
    def test_sources_et_lecteur_contiennent_chaque_ajout(self):
        doc = BeautifulSoup(STUDY.read_text(encoding="utf-8"), "html.parser")
        self.assertEqual(18, len(doc.select("section.philo-chapter")))
        txt = doc.get_text(" ", strip=True)
        for name, signature in SAMPLES.items():
            raw = (CORPUS / name).read_text(encoding="utf-8")
            self.assertIn(signature, raw)
            self.assertIn(signature, txt)
        self.assertIn("Le PDF de 84 pages", txt)
        for target, phrase in {
            "04-chant-iv.md": "Mariage contesté et dramaturgie des signes",
            "12-chant-xii.md": "Le baudrier tragique : objet, trophée",
            "14-empire-memoire.md": "Trois systèmes de reconnaissance",
            "17-reperes-et-sources.md": "Dossier critique vérifié — mariage de Didon",
        }.items():
            self.assertIn(phrase, (CORPUS / target).read_text(encoding="utf-8"))
            self.assertIn(phrase, txt)
        self.assertIn("ne comprennent pas encore ces nouveaux développements", txt)

    def test_intertexts_rites_and_gendered_mourning_in_sources_and_reader(self):
        """Vérifier les nouveaux dossiers et l'absence de doublons d'ancres."""
        import re
        doc = BeautifulSoup(STUDY.read_text(encoding="utf-8"), "html.parser")
        chapters = doc.select("section.philo-chapter")
        targets = {
            5: ("05-chant-v.md", [
                "Nisus, Salius et Euryale : la fidélité peut-elle justifier la fraude ?",
                "Du tournoi funéraire à la guerre",
            ]),
            7: ("07-chant-vii.md", [
                "Les portes de Janus : institution, refus royal",
                "Lavinia, Amata et le coût politique",
            ]),
            9: ("09-chant-ix.md", [
                "De la course du chant V à l'expédition nocturne",
                "La mère d’Euryale et la protestation",
            ]),
            11: ("11-chant-xi.md", [
                "Diane, Opis et l'honneur différé",
                "Camille, Nisus et les morts prématurées",
            ]),
            14: ("14-empire-memoire.md", [
                "Fidélité, fraude et récit public",
            ]),
            17: ("17-reperes-et-sources.md", [
                "Dossier philologique vérifié — concours, Janus",
            ]),
        }
        for idx, (file, headings) in targets.items():
            source = (CORPUS / file).read_text(encoding="utf-8")
            chapter = chapters[idx].get_text(" ", strip=True)
            for heading in headings:
                self.assertIn(heading, source, file)
                self.assertIn(heading, chapter, file)
                self.assertEqual(source.count("## " + heading), 1, file)
            ids = [h["id"] for h in chapters[idx].select("h3[id]")]
            self.assertEqual(len(ids), len(set(ids)), file)
        sources = (CORPUS / "17-reperes-et-sources.md").read_text(encoding="utf-8")
        for marker in (
            "10.54563/eugesta.1117",
            "10.11647/OBP.0158",
            "Eurialo e Niso: fides e perfidia",
            "Vie parallele: a proposito di Camilla e Niso",
        ):
            self.assertIn(marker, sources)
        self.assertIn("ne comprennent pas encore ces nouveaux développements",
                      doc.get_text(" ", strip=True))

    def test_comparative_epirus_arcadia_sources_reader_and_anchors(self):
        """Lectures universitaires des chants III et VIII : cohérence des sources et du lecteur."""
        import re
        from html import unescape
        doc = BeautifulSoup(STUDY.read_text(encoding="utf-8"), "html.parser")
        checks = {
            3: ("03-chant-iii.md", [
                "« Antiquam exquirite matrem » : l'oracle, la Crète",
                "Céléno et les tables mangées",
                "Andromaque et la « parva Troia »",
            ]),
            8: ("08-chant-viii.md", [
                "Du Tibre à Pallantée",
                "Hercule et Cacus : mémoire religieuse",
                "Le Palatin d'Évandre",
                "Étreintes, regards et savoir",
                "L'ekphrasis d'Actium",
            ]),
            14: ("14-empire-memoire.md", [
                "Troie reproduite, Rome annoncée",
            ]),
            17: ("17-reperes-et-sources.md", [
                "Dossier critique — chant III, mémoire d'Andromaque",
            ]),
        }
        chapters = doc.select("section.philo-chapter")
        self.assertEqual(len(chapters), 18)
        for idx, (name, signatures) in checks.items():
            raw = (CORPUS / name).read_text(encoding="utf-8")
            section = chapters[idx]
            render = section.get_text(" ", strip=True)
            render_paragraphs = [" ".join(p.get_text().split()) for p in section.select("p")]
            for label in signatures:
                self.assertEqual(raw.count("## " + label), 1, name + " : " + label)
                self.assertIn(label, render, name + " : " + label)
            for paragraph in raw.split("\n\n"):
                paragraph = paragraph.strip()
                if not paragraph or paragraph.startswith("#") or paragraph.startswith("Références"):
                    continue
                if paragraph.startswith("**") or paragraph.startswith("- "):
                    continue
                # Les liens Markdown sont matérialisés en ancres, leur texte reste inchangé.
                plain = re.sub(r"\[([^\]]+)\]\(https?://[^)]+\)", r"\1", paragraph)
                plain = plain.replace("*", "").replace("\n", " ")
                plain = unescape(plain)
                self.assertIn(" ".join(plain.split()), render_paragraphs,
                              name + " : paragraphe source absent du lecteur")
        refs = (CORPUS / "17-reperes-et-sources.md").read_text(encoding="utf-8")
        for doi in (
            "10.2307/25011052", "10.1017/S0009838824000260",
            "10.1017/S0017383506000271", "10.1525/ca.2014.33.2.281",
            "10.1163/1568525X-BJA10123",
        ):
            self.assertIn(doi, refs)
        all_ids = [e["id"] for e in doc.select("[id]")]
        self.assertEqual(len(all_ids), len(set(all_ids)))

    def test_references_et_titles_sont_uniques(self):
        doc = BeautifulSoup(STUDY.read_text(encoding="utf-8"), "html.parser")
        ids = [node["id"] for node in doc.select("[id]")]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("10.1017/S000983881600077X",
                      (CORPUS / "17-reperes-et-sources.md").read_text(encoding="utf-8"))
        self.assertIn("vitaque cum gemitu fugit indignata sub umbras",
                      (CORPUS / "12-chant-xii.md").read_text(encoding="utf-8"))


    def test_all_eighteen_sources_match_the_html_chapter_map(self):
        """Ne jamais perdre une section ni casser les ancres lors d'un enrichissement."""
        import re
        doc = BeautifulSoup(STUDY.read_text(encoding="utf-8"), "html.parser")
        names = [
            "00-introduction.md", "01-chant-i.md", "02-chant-ii.md",
            "03-chant-iii.md", "04-chant-iv.md", "05-chant-v.md",
            "06-chant-vi.md", "07-chant-vii.md", "08-chant-viii.md",
            "09-chant-ix.md", "10-chant-x.md", "11-chant-xi.md",
            "12-chant-xii.md", "13-pietas-destin.md",
            "14-empire-memoire.md", "15-philosophies-comparaisons.md",
            "16-poetique-conclusion.md", "17-reperes-et-sources.md",
        ]
        chapters = doc.select("section.philo-chapter")
        self.assertEqual(len(chapters), len(names))
        for i, name in enumerate(names):
            text = (CORPUS / name).read_text(encoding="utf-8")
            title = re.search(r"^# (.+)$", text, flags=re.M).group(1)
            headings = re.findall(r"^## (.+)$", text, flags=re.M)
            chapter = chapters[i]
            heading = chapter.select_one(f'h2[id="eneide-{i:02}"]')
            self.assertIsNotNone(heading, name)
            self.assertEqual(heading.get_text(" ", strip=True), title, name)
            anchors = chapter.select("h3[id]")
            self.assertEqual(len(anchors), len(headings), name)
            for j, expected in enumerate(headings):
                subheading = chapter.select_one(f'h3[id="eneide-{i:02}-{j:02}"]')
                self.assertIsNotNone(subheading, name + ": " + expected)
                self.assertEqual(subheading.get_text(" ", strip=True), expected)
        shelf = doc.select("#eneide-manuscrits-originaux")
        self.assertLessEqual(len(shelf), 1)
        if shelf:
            self.assertEqual(
                len(shelf[0].select(".mythos-eneide-source-grid li a")), 18
            )

    def test_eneide_hector_didon_treve_20261107(self):
        """Contrôler les 3 études nouvelles et le catalogue critique."""
        from bs4 import BeautifulSoup
        doc = BeautifulSoup(STUDY.read_text(encoding="utf-8"), "html.parser")
        chapters = doc.select("section.philo-chapter")
        self.assertEqual(len(chapters), 18)
        titles = {
            2: ("02-chant-ii.md", "Hector et les Pénates : sauver le culte lorsque les murailles tombent (II, 268–297)"),
            4: ("04-chant-iv.md", "Une reine privée de sommeil : délibérer au bord de l'impossible (IV, 522–583)"),
            11: ("11-chant-xi.md", "Le droit des morts : négociation, hospitalité ancienne et limite de la victoire (XI, 100–138)"),
            17: ("17-reperes-et-sources.md", "Complément critique : Hector, la nuit de Didon et la trêve des morts (7 novembre 2026)"),
        }
        for index, (filename, heading) in titles.items():
            raw = (CORPUS / filename).read_text(encoding="utf-8")
            self.assertEqual(raw.count("## " + heading), 1)
            self.assertEqual(
                [h.get_text(" ", strip=True) for h in chapters[index].select("h3[id]")].count(heading), 1
            )
        for filename, marker in {
            "02-chant-ii.md": "sacra suosque tibi commendat Troia penates",
            "04-chant-iv.md": "ingeminant curae",
            "11-chant-xi.md": "nullum cum victis certamen et aethere cassis",
            "17-reperes-et-sources.md": "10.1017/9781108680226.003",
        }.items():
            self.assertIn(marker, (CORPUS / filename).read_text(encoding="utf-8"))
            self.assertIn(marker, doc.get_text(" ", strip=True))
        ids = [item["id"] for item in doc.select("[id]")]
        self.assertEqual(len(ids), len(set(ids)))

if __name__ == "__main__":
    unittest.main()
