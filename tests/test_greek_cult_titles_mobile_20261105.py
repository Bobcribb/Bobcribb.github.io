"""Two intact encyclopedia studies: precise cult classification and accessible TOCs.

Never create or renumber manuscripts; thematic links are generated from sources.
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_greek_folders import classify

CASES = (
    (398, 'artemis-soteira-megare-trezene-pellene-salut-cites',
     'Mégare, Trézène et Pellène — Artémis Sôteira et salut civique', 24),
    (424, 'dionysos-aisymnetes-patras-eurypyle-triklaria-fete-rites',
     'Patras — Dionysos Aisymnètès, Artémis Triklaria et Eurypyle', 52),
)


class GreekCultNavigationTests(unittest.TestCase):
    def test_published_monographs_keep_cote_sections_sources_and_precise_home(self):
        for number, slug, section, minimum_sections in CASES:
            with self.subTest(chapter=number):
                path = ROOT / 'chapitres/encyclopedie' / f'chapitre-{number}-{slug}.md'
                self.assertTrue(path.is_file())
                text = path.read_text(encoding='utf-8')
                self.assertTrue(text.startswith(f'# Chapitre {number} '))
                self.assertGreaterEqual(len(text), 10000)
                self.assertGreaterEqual(len(re.findall(r'^## \d+\. ', text, re.M)),
                                        minimum_sections)
                self.assertIn('Pausanias', text)
                self.assertRegex(text.lower(), r'bibliograph')
                url = f'/chapitres/encyclopedie/chapitre-{number}-{slug}/'
                self.assertEqual(
                    classify(url, 'Zeus Homère Artémis cités au passage',
                             'Chapitre universitaire'),
                    ('cultes-sanctuaires', section))
                self.assertNotEqual(classify(url, '', 'Chapitre universitaire')[1],
                                    'Nouvelles études à classer')

    def test_other_dionysos_and_artemis_titles_are_not_reclassified_en_masse(self):
        for subject in ('dionysos-fete-thebes', 'artemis-olympienne'):
            actual = classify('/chapitres/encyclopedie/chapitre-9999-' + subject + '/',
                              'titre générique', 'Chapitre universitaire')
            self.assertEqual(actual[0], 'divinites')

    def test_long_edition_toc_remains_responsive_keyboard_and_touch_accessible(self):
        css = (ROOT / 'assets/mythos-discovery.css').read_text(encoding='utf-8')
        self.assertIn('.mythos-reading-toc>summary{display:flex;align-items:center;justify-content:center;min-height:44px', css)
        self.assertIn('.mythos-reading-toc li>a{display:flex;align-items:center;min-height:44px', css)
        self.assertIn('.mythos-reading-toc[open]>ol{max-height:min(60vh,630px);overflow-y:auto', css)
        self.assertIn('.mythos-reading-toc li>a:focus-visible', css)
        self.assertIn('@media(max-width:700px)', css)
        self.assertIn('max-height:55vh', css)
        # A native <details>/<summary> retains keyboard and assistive-tech support.
        html = (ROOT / 'chapitres/encyclopedie/chapitre-424-dionysos-aisymnetes-patras-eurypyle-triklaria-fete-rites/index.html').read_text(encoding='utf-8')
        self.assertIn('class="mythos-reading-toc"', html)
        self.assertIn('Sommaire de lecture · 52 sections', html)
        self.assertIn('href="#chapitre-52"', html)


if __name__ == '__main__':
    unittest.main()
