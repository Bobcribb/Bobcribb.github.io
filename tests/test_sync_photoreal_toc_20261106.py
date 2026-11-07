"""Un seul sommaire de galerie : lien, légende et notice scientifique intacts."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from sync_photoreal_toc import GALLERY, TOC, sections_and_labels, synchronized_markup, synchronize


def sample():
    return (
        '<html lang="fr"><body><main><p id="scientific-source">Source primaire intacte.</p>'
        '<details class="mythos-reading-toc mythos-gallery-toc" data-reading-owned="true">'
        '<summary>Sommaire de lecture · 1 sections</summary>'
        '<ol><li><a href="#lecture-section-1">Ancien titre</a></li></ol></details>'
        '<article class="r3d-card panorama"><figure><figcaption><strong>'
        'Delphes — temple d’Apollon</strong></figcaption></figure>'
        '<div class="r3d-science"><h2 data-reading-section="true" '
        'id="lecture-section-1">Commentaire scientifique</h2>'
        '<p>Bibliographie et sources A.</p></div></article>'
        '<article class="r3d-card panorama"><figure><figcaption><strong>'
        'Délos — maison des Dauphins</strong></figcaption></figure>'
        '<div class="r3d-science"><h2 data-reading-section="true" '
        'id="lecture-section-2">Commentaire scientifique</h2>'
        '<p>Bibliographie et sources B.</p></div></article>'
        '</main></body></html>'
    )


class SyncPhotorealTOCTests(unittest.TestCase):
    def test_root_gallery_synchronized_to_all_scholarly_cards(self):
        source = GALLERY.read_text(encoding="utf-8")
        entries = sections_and_labels(source)
        self.assertGreaterEqual(len(entries), 82)
        self.assertEqual(len(entries), len(set(a for a, _ in entries)))
        self.assertEqual(source, synchronized_markup(source))
        self.assertIn("Sommaire de lecture · " + str(len(entries))
                      + " sections", source)

    def test_after_adding_new_card_corrects_only_generated_navigation(self):
        source = sample()
        fixed = synchronized_markup(source)
        self.assertNotEqual(source, fixed)
        self.assertEqual(len(sections_and_labels(fixed)), 2)
        self.assertIn('href="#lecture-section-2">Délos — maison des Dauphins'
                      ' — Commentaire scientifique</a>', fixed)
        self.assertIn('Sommaire de lecture · 2 sections', fixed)
        self.assertEqual(synchronized_markup(fixed), fixed)
        self.assertEqual(
            TOC.sub("", source), TOC.sub("", fixed),
            "Ne jamais réécrire les cartes, textes, dates, images ou sources"
        )

    def test_read_only_then_explicit_write(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "gallery.html"
            old = sample()
            path.write_text(old, encoding="utf-8")
            state = synchronize(path)
            self.assertTrue(state["changed"])
            self.assertFalse(state["saved"])
            self.assertEqual(path.read_text(), old)
            state = synchronize(path, write=True)
            self.assertTrue(state["saved"])
            self.assertEqual(synchronize(path)["changed"], False)
            self.assertIn("Source primaire intacte.", path.read_text())

    def test_refuse_duplicate_or_missing_historical_anchors(self):
        corrupted = sample().replace('id="lecture-section-2"', 'id="lecture-section-1"')
        with self.assertRaisesRegex(ValueError, "dupliquées"):
            sections_and_labels(corrupted)
        corrupted = sample().replace("Délos — maison des Dauphins", "")
        with self.assertRaisesRegex(ValueError, "Légende archéologique absente"):
            sections_and_labels(corrupted)
        with self.assertRaisesRegex(ValueError, "exactement un sommaire"):
            synchronized_markup(sample().replace('mythos-gallery-toc', 'mythos-legacy-toc'))


if __name__ == "__main__":
    unittest.main()
