"""Dossiers universitaires postérieurs à 490 : inventaire complet sans numérotation nouvelle."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import origins_additional_index

class OriginsAdditionalIndexTests(unittest.TestCase):
    def test_all_attributed_studies_have_one_link_with_scientific_title(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "_site"
            records = {}
            for number, slug, title, generic in (
                (491, "source", "Les témoins historiques", False),
                (495, "royaute", "Les funérailles royales", True),
                (697, "palmyre", "La mémoire de Palmyre", True),
            ):
                url = f"/chapitres/origines-du-sacre/{number}-{slug}/"
                records[number] = {"url": url, "title": "Résumé scientifique"}
                source = root / (url.strip("/") + ".md")
                source.parent.mkdir(parents=True, exist_ok=True)
                heading = (f"# Chapitre {number} — {title}" if not generic else
                           f"# MYTHOS — Chapitre {number}\n\n## {title}")
                source.write_text(heading + "\n\n" + ("Recherche attestée. " * 130), encoding="utf-8")
                reader = output / url.strip("/") / "index.html"
                reader.parent.mkdir(parents=True, exist_ok=True)
                reader.write_text("<html><body><article>Texte complet</article></body></html>")
            html = origins_additional_index(records, root, output)
            page = BeautifulSoup(html, "html.parser")
            self.assertEqual(len(page.select(".origins-research-card")), 3)
            self.assertEqual(len(page.select(".origins-research-card")), 3)
            self.assertIn("La mémoire de Palmyre", page.get_text(" ", strip=True))
            self.assertNotIn("Résumé scientifique", page.get_text(" ", strip=True))
            self.assertEqual({a["href"] for a in page.select("a[href]")},
                             {r["url"] for r in records.values()})
            self.assertEqual(len(page.select("a[href]")), len(records))

    def test_bandeau_my_thos_suivi_du_titre_scientifique_chwaka(self):
        # Le bandeau initial ne doit pas faire passer le premier H2
        # « Résumé » pour le titre scientifique de la monographie.
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            url = "/chapitres/origines-du-sacre/756-chwaka-pemba/"
            source = root / (url.strip("/") + ".md")
            source.parent.mkdir(parents=True, exist_ok=True)
            original = ("# MYTHOS — Les Origines du sacré — Chapitre 756\\n"
                        "# Chwaka (Pemba) : quatre mosquées et la ville swahilie\\n\\n"
                        "## Résumé\\n\\n" + "Analyse scientifique. " * 155)
            source.write_text(original, encoding="utf-8")
            reader = root / "_site" / url.strip("/") / "index.html"
            reader.parent.mkdir(parents=True, exist_ok=True)
            reader.write_text("<article>Texte intégral inchangé</article>", encoding="utf-8")
            index = origins_additional_index(
                {756: {"url": url, "title": "Chapitre 756 — Résumé"}},
                root, root / "_site",
            )
            doc = BeautifulSoup(index, "html.parser")
            self.assertEqual(
                doc.select_one(".origins-research-card strong").get_text(" ", strip=True),
                "Chwaka (Pemba) : quatre mosquées et la ville swahilie",
            )
            self.assertEqual(source.read_text(encoding="utf-8"), original)

    def test_missing_reader_refuses_partial_or_unpublished_content(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            url = "/chapitres/origines-du-sacre/698-source/"
            source = root / (url.strip("/") + ".md")
            source.parent.mkdir(parents=True)
            source.write_text("# Chapitre 698 — Sujet\n" + "Texte. " * 500)
            with self.assertRaisesRegex(RuntimeError, "lecteur absent"):
                origins_additional_index({698: {"url": url, "title": "Sujet"}}, root, root/"_site")

    def test_earlier_48_documents_not_duplicated(self):
        self.assertEqual(origins_additional_index({490: {"url": "/chapitres/origines-du-sacre/490-source/"}}, ROOT, ROOT), "")

if __name__ == "__main__":
    unittest.main()
