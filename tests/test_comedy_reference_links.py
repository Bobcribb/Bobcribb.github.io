"""Régression du lien documentaire corrigé dans la comédie 91 de MYTHOS."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STEM = "volume-091-nikochares-galateia-polypheme-dithyrambe-philonides-cumin-nereides"
TARGET = "/comedies-grecques-aristophane-menandre/"


class ComedyReferenceLinkTests(unittest.TestCase):
    def test_target_exists_and_both_versions_use_it(self):
        self.assertTrue((ROOT / TARGET.lstrip("/") / "index.html").is_file())
        for filename in (
            ROOT / "chapitres/comedies" / (STEM + ".md"),
            ROOT / "chapitres/comedies" / STEM / "index.html",
        ):
            with self.subTest(path=str(filename)):
                text = filename.read_text(encoding="utf-8")
                self.assertIn(TARGET, text)
                self.assertNotIn("/comedies-grecques/", text)


    def test_volume_101_documentary_links_resolve_to_public_html(self):
        """The comedies' manuscript .md files are not published as HTML links."""
        stem = "volume-101-philyllios-eunikos-anteia-attribution-hetaire-baiser-chytra-pollux"
        sources = (
            ROOT / "chapitres/comedies" / (stem + ".md"),
            ROOT / "chapitres/comedies" / stem / "index.html",
        )
        targets = (
            "/chapitres/comedies/volume-100-philyllios-aigeus-poisson-ancetre-analphiton-thesee-reconnaissance/",
            "/chapitres/comedies/volume-099-philonikos-poete-comique-victoire-leneennes-inscription-ig2325-memoire/",
        )
        for target in targets:
            self.assertTrue((ROOT / target.lstrip("/") / "index.html").is_file())
        for source in sources:
            with self.subTest(path=str(source)):
                body = source.read_text(encoding="utf-8")
                for target in targets:
                    self.assertIn(target, body)
                    self.assertNotIn(target[:-1] + ".md", body)



    def test_volumes_102_and_103_use_existing_comedy_overview(self):
        """Keep the two public comedies links valid in both Markdown and rendered HTML."""
        self.assertTrue((ROOT / TARGET.lstrip("/") / "index.html").is_file())
        stems = (
            "volume-102-philyllios-atalante-titre-souda-attribution-douteuse-chasse-course-mythes",
            "volume-103-philyllios-auge-telephos-banquet-pannychis-pain-chanson-paratragedie",
        )
        for stem in stems:
            for filename in (
                ROOT / "chapitres/comedies" / (stem + ".md"),
                ROOT / "chapitres/comedies" / stem / "index.html",
            ):
                with self.subTest(filename=str(filename)):
                    text = filename.read_text(encoding="utf-8")
                    self.assertIn(TARGET, text)
                    self.assertNotIn("/comedies-grecques/", text)



if __name__ == "__main__":
    unittest.main()
