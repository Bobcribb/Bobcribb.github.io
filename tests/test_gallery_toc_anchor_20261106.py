"""Contrôle du sommaire de la galerie photoréaliste après ajouts concurrents."""
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / 'reconstitutions-photorealistes.html'


class GalleryTOCAnchorTests(unittest.TestCase):
    def test_all_gallery_section_links_target_existing_numbered_sections(self):
        text = GALLERY.read_text(encoding='utf-8')
        self.assertNotIn('{LECTURE_INDEX}', text)
        doc = BeautifulSoup(text, 'html.parser')
        ids = {node['id'] for node in doc.select('[id]')}
        targets = [a['href'][1:] for a in doc.select(
            'a[href^="#lecture-section-"]')]
        self.assertGreaterEqual(len(targets), 80)
        self.assertEqual(len(targets), len(set(targets)))
        for anchor in targets:
            with self.subTest(target=anchor):
                self.assertIn(anchor, ids)

    def test_metaponte_toc_and_actual_76_section_stay_connected(self):
        doc = BeautifulSoup(GALLERY.read_text(encoding='utf-8'), 'html.parser')
        section = doc.find(id='lecture-section-76')
        self.assertIsNotNone(section)
        matching = [link for link in doc.select('a[href="#lecture-section-76"]')
                    if 'Métaponte' in link.get_text(' ', strip=True)]
        self.assertEqual(len(matching), 1)


if __name__ == '__main__':
    unittest.main()
