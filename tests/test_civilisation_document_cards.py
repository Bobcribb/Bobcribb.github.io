"""Cartes de l'accueil : provenance complète, liens, images et refus des lacunes."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from improve_reading import (CIVILISATION_DOCUMENTS, civilisation_document_cards,
                             install_civilisation_reciprocal_navigation)


class CivilisationDocumentCardsTests(unittest.TestCase):
    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.out = Path(self._tmp.name)
        registered = json.loads((ROOT / "scripts/editorial_media.json").read_text(encoding="utf-8"))
        self.registry = {entry["id"]: entry for entry in registered["media"]}
        for portal, _, _, media_id in CIVILISATION_DOCUMENTS:
            obj = self.registry[media_id]
            for rel in (portal.lstrip("/") + "index.html",
                        obj["path"], obj["provenance_page"]):
                target = self.out / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                if rel.endswith("index.html"):
                    target.write_text('<html><body><main><article class="content">'
                                      '<h1>Étude universitaire attestée</h1>'
                                      '<p id="texte-source">Texte scientifique conservé, sources et bibliographie.</p>'
                                      '</article></main></body></html>', encoding="utf-8")
                else:
                    target.write_bytes(b"Fixture MYTHOS")

    def test_all_three_archaeological_cards_keep_provenance_and_navigation(self):
        markup = civilisation_document_cards(self.out, ROOT)
        doc = BeautifulSoup(markup, "html.parser")
        cards = doc.select(".mythos-civilisation-card")
        self.assertEqual(len(cards), 3)
        self.assertEqual(len({c["data-document-id"] for c in cards}), 3)
        self.assertEqual(len(doc.select("details.mythos-civilisation-credit")), 3)
        for (url, title, _, media_id), card in zip(CIVILISATION_DOCUMENTS, cards):
            source = self.registry[media_id]
            self.assertEqual(card.select_one("a.mythos-civilisation-link")["href"], url)
            self.assertEqual(card["id"], "mythos-document-" + media_id)
            self.assertEqual(card.select_one(".mythos-civilisation-study a")["href"],
                             "/" + source["provenance_page"])
            self.assertIn(title, card.get_text(" ", strip=True))
            self.assertEqual(card.select_one("img")["src"], "/" + source["path"])
            self.assertEqual(card.select_one("img")["alt"], source["alt"])
            self.assertEqual(
                card.select_one('details a[href^="/"]')["href"],
                "/" + source["provenance_page"])
            self.assertTrue(card.select_one("details a[href^='https://']"))
            self.assertIn("Source et crédits", card.get_text(" ", strip=True))

    def test_studies_get_reciprocal_links_without_altering_scholarly_prose(self):
        updated = install_civilisation_reciprocal_navigation(self.out, ROOT)
        self.assertEqual(len(updated), 3)
        for library, label, _, media_id in CIVILISATION_DOCUMENTS:
            study = self.out / self.registry[media_id]["provenance_page"]
            page = BeautifulSoup(study.read_text(encoding="utf-8"), "html.parser")
            self.assertEqual(page.select_one("#texte-source").get_text(strip=True),
                             "Texte scientifique conservé, sources et bibliographie.")
            nav = page.select_one('[data-mythos-document-reciprocal="true"]')
            self.assertIsNotNone(nav)
            self.assertEqual(nav.select_one('a[href^="/#"]')["href"],
                             "/#mythos-document-" + media_id)
            self.assertTrue(nav.select_one('a[href="' + library + '"]'))
            self.assertIn(label, nav.get_text(" ", strip=True))
        self.assertEqual(install_civilisation_reciprocal_navigation(self.out, ROOT), [])
        for _, _, _, media_id in CIVILISATION_DOCUMENTS:
            page = BeautifulSoup((self.out / self.registry[media_id]["provenance_page"]).read_text(encoding="utf-8"), "html.parser")
            self.assertEqual(len(page.select('[data-mythos-document-reciprocal]')), 1)

    def test_reciprocal_links_refuse_missing_study(self):
        missing = self.registry[CIVILISATION_DOCUMENTS[0][3]]["provenance_page"]
        (self.out / missing).unlink()
        with self.assertRaisesRegex(RuntimeError, "Étude documentaire absente"):
            install_civilisation_reciprocal_navigation(self.out, ROOT)

    def test_missing_image_blocks_build_instead_of_inventing_fallback(self):
        source = self.registry[CIVILISATION_DOCUMENTS[1][3]]
        (self.out / source["path"]).unlink()
        with self.assertRaisesRegex(RuntimeError, "Image archéologique absente"):
            civilisation_document_cards(self.out, ROOT)

    def test_missing_source_page_blocks_build(self):
        source = self.registry[CIVILISATION_DOCUMENTS[2][3]]
        (self.out / source["provenance_page"]).unlink()
        with self.assertRaisesRegex(RuntimeError, "Dossier de provenance absent"):
            civilisation_document_cards(self.out, ROOT)


if __name__ == "__main__":
    unittest.main()
