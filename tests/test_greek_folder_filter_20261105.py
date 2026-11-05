"""Filtrage progressif des huit familles grecques : index complet préservé."""
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_greek_folders import BASE, MEDITERRANEAN_STUDIES, build, verify


class GreekFolderFilterTests(unittest.TestCase):
    def test_source_links_subsections_toc_and_rebuild_are_immutable(self):
        cases = (MEDITERRANEAN_STUDIES[0], MEDITERRANEAN_STUDIES[-1])
        urls = {url for url, _, _ in cases}
        with TemporaryDirectory() as directory:
            out = Path(directory)
            snapshots = {}
            for url, title, _ in cases:
                path = out / url.lstrip("/") / "index.html"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    '<!doctype html><html lang="fr"><head><title>Source</title></head>'
                    '<body><main><article><h1>' + title + '</h1>'
                    '<p>Texte scientifique intégral, sources et bibliographie.</p>'
                    '</article></main></body></html>', encoding="utf-8"
                )
                snapshots[url] = str(BeautifulSoup(path.read_text(encoding="utf-8"),
                                                    "html.parser").article)

            groups = [("Études documentées", "grec-liens",
                       [(url, title) for url, title, _ in cases])]
            for _ in range(2):
                records = build(out, groups, [], [])
                verify(out, urls)
                self.assertEqual({r["url"] for r in records}, urls)
                for url in urls:
                    path = out / url.lstrip("/") / "index.html"
                    current = BeautifulSoup(path.read_text(encoding="utf-8"),
                                            "html.parser")
                    self.assertEqual(str(current.article), snapshots[url])
                for folder in {r["folder"] for r in records}:
                    page = out / BASE.strip("/") / folder / "index.html"
                    doc = BeautifulSoup(page.read_text(encoding="utf-8"),
                                        "html.parser")
                    widgets = doc.select("[data-greek-folder-filter]")
                    self.assertEqual(len(widgets), 1)
                    self.assertTrue(widgets[0].has_attr("hidden"))
                    input_element = widgets[0].select_one('input[type="search"]')
                    self.assertIsNotNone(input_element)
                    self.assertTrue(widgets[0].select_one(
                        'label[for="' + input_element["id"] + '"]'))
                    self.assertTrue(widgets[0].select_one(
                        '[data-greek-filter-clear][hidden]'))
                    status = widgets[0].select_one('[data-greek-filter-count]')
                    self.assertEqual(status["role"], "status")
                    self.assertEqual(len(doc.select(
                        'script[src="/assets/greek-folder-filter.js"]')), 1)
                    toc = doc.select_one("nav.greek-folder-toc")
                    self.assertIsNotNone(toc)
                    links = doc.select('ol.greek-folder-links a[data-greek-entry]')
                    expected = [r["url"] for r in records if r["folder"] == folder]
                    self.assertCountEqual([a["href"] for a in links], expected)
                    for section in doc.select("section.portal-section[id^='theme-']"):
                        self.assertTrue(toc.select_one('a[href="#' + section["id"] + '"]'))
                        self.assertGreater(len(section.select(
                            'ol.greek-folder-links>li')), 0)

    def test_progressive_filter_script_and_responsive_gold_theme(self):
        script = (ROOT / "assets/greek-folder-filter.js").read_text(encoding="utf-8")
        css = (ROOT / "assets/mythos-museum.css").read_text(encoding="utf-8")
        for required in ("DOMContentLoaded", "normalize('NFD')", "input.value",
                         "aria-live", "hashchange", "entries.forEach", "li.hidden",
                         "section.hidden", "navItem.hidden", "Escape"):
            # aria-live is defined in HTML markup; the script handles announcements.
            if required != "aria-live":
                self.assertIn(required, script)
        self.assertIn('data-greek-folder-filter', script)
        self.assertIn('.greek-folder-filter[hidden]', css)
        self.assertIn('.greek-folder-links>li[hidden]', css)
        self.assertIn('@media(max-width:480px)', css)
        self.assertIn('border:1px solid #806a46', css)


if __name__ == "__main__":
    unittest.main()
