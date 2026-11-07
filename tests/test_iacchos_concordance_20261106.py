"""Issue #58 : conserver les deux manuscrits et distinguer leurs interprétations."""
from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_native import annotate_iacchos_search
from editorial_concordances import PAIRS, IACCHOS_CONCORDANCE_ROWS, iacchos_scientific_table


class IacchosConcordanceTests(unittest.TestCase):
    def allocations(self):
        registry = json.loads((ROOT / "editorial/numbering.json").read_text(encoding="utf-8"))
        spec = PAIRS["iacchos"]
        items = []
        for collection, uuid, number, title, context in spec["members"]:
            receipt = registry["collections"][collection]["allocations"][uuid]
            self.assertEqual(receipt["number"], number)
            self.assertEqual(collection, "comparatif")
            request = ROOT / "editorial/inbox" / (uuid + ".json")
            self.assertEqual(sha256(request.read_bytes()).hexdigest(),
                             receipt["request_sha256"])
            self.assertTrue((ROOT / receipt["path"]).is_file())
            items.append((uuid, number, ROOT / receipt["path"],
                          "/" + Path(receipt["path"]).with_suffix("").as_posix() + "/"))
        return items

    def test_original_full_texts_receipts_and_bibliographies(self):
        pairs = self.allocations()
        self.assertEqual({n for _, n, _, _ in pairs}, {269, 273})
        self.assertEqual(len({url for _, _, _, url in pairs}), 2)
        expected_min = {269: 62000, 273: 77000}
        for uuid, number, source, url in pairs:
            with self.subTest(volume=number):
                body = source.read_text(encoding="utf-8")
                self.assertGreater(len(body), expected_min[number])
                self.assertIn("bibliograph", body.casefold())
                self.assertIn("Iacch", body)
                self.assertIn("405", body)
                self.assertIn(str(number), body.splitlines()[0])
                self.assertIn("Grenouilles", body)
        # La notice n'est pas une attribution numérotée supplémentaire.
        self.assertEqual(len(IACCHOS_CONCORDANCE_ROWS), 8)
        self.assertEqual(PAIRS["iacchos"]["portal"], "mythologie-comparee/index.html")

    def test_search_distinguishes_both_urls_without_duplication(self):
        first, second = self.allocations()
        entries = [{"title": "Volume " + str(number), "url": url, "excerpt": ""}
                   for _, number, _, url in (first, second)]
        entries.append({"title": "Autre étude", "url": "/chapitres/comparatif/autre/", "excerpt": "Original"})
        self.assertIs(annotate_iacchos_search(entries), entries)
        self.assertEqual(len(entries), 3)
        self.assertIn("purification politique", entries[0]["excerpt"])
        self.assertIn("politique de l'écoute", entries[1]["excerpt"])
        self.assertIn("273", entries[0]["excerpt"])
        self.assertIn("269", entries[1]["excerpt"])
        self.assertEqual(entries[2]["excerpt"], "Original")
        self.assertTrue(all(len(item["excerpt"]) <= 190 for item in entries))

    def test_portal_sitemap_and_existing_search_index_contain_both_urls(self):
        targets = {url for _, _, _, url in self.allocations()}
        portal = (ROOT / "mythologie-comparee/index.html").read_text(encoding="utf-8")
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        indexed = json.loads((ROOT / "search.json").read_text(encoding="utf-8"))
        for url in targets:
            with self.subTest(url=url):
                self.assertIn('href="' + url + '"', portal)
                self.assertIn("https://bobmythos.fr" + url, sitemap)
                self.assertEqual(sum(entry.get("url") == url for entry in indexed), 1)

    def test_scholarly_table_and_detailed_document_are_not_new_manuscripts(self):
        html = BeautifulSoup(iacchos_scientific_table(), "html.parser")
        self.assertEqual(len(html.select("tbody tr")), 8)
        self.assertEqual(len(html.select("thead th")), 3)
        self.assertIn("Concordance des vers", html.get_text(" ", strip=True))
        self.assertIn("Contexte 407–405", html.get_text(" ", strip=True))
        text = (ROOT / "docs/CONCORDANCE_IACCHOS_GRENOUILLES_269_273.md").read_text(encoding="utf-8")
        self.assertIn("politique de l'écoute", text)
        self.assertIn("purification politique", text)
        self.assertIn("Diagoras", text)
        self.assertIn("Thucydide", text)
        self.assertIn("Phédon", text)
        self.assertIn("troisième monographie", text)
        self.assertNotIn("nouvel UUID est créé", text)


    def test_policy_prevents_unjustified_third_study(self):
        """Toute nouvelle étude sur ce passage exige un apport scientifique démontré."""
        policy = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Recouvrement des *Grenouilles* (issue #58)", policy)
        self.assertIn("Avant toute troisième livraison", policy)
        self.assertIn("sources ou variantes nouvelles", policy)
        concordance = (ROOT / "docs/CONCORDANCE_IACCHOS_GRENOUILLES_269_273.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("troisième monographie", concordance)
        self.assertIn("une revue éditoriale", concordance)


if __name__ == "__main__":
    unittest.main()
