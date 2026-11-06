"""Contrôle non destructif des 18 manuscrits de l'Énéide et des liens croisés."""
import sys
import tempfile
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from eneide_source_access import install, NAMES, SOURCE_DIR, STUDY, NARRATIVE


class EneideSourcesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "repository"
        self.out = Path(self.tmp.name) / "_site"
        (self.root / SOURCE_DIR).mkdir(parents=True)
        (self.out / STUDY).parent.mkdir(parents=True, exist_ok=True)
        (self.out / NARRATIVE).parent.mkdir(parents=True, exist_ok=True)
        body = []
        for i, name in enumerate(NAMES):
            title = f"Source universitaire {i:02}"
            body.append(f'<section><h2 id="eneide-{i:02}">{title}</h2><p>Texte original.</p></section>')
            text = "# " + title + "\n\n" + ("Analyse des sources primaires et du texte. " * 260)
            if i == 17:
                text += "\n\nBibliographie et références primaires : Virgile, Énéide.\n"
            (self.root / SOURCE_DIR / name).write_text(text, encoding="utf-8")
        (self.out / STUDY).write_text(
            '<!doctype html><html lang="fr"><head><title>Énéide</title></head>'
            '<body class="mythos-design"><main class="philo-work">'
            '<h1>Étude intégrale</h1><nav class="philo-toc">Sommaire</nav>'
            + "".join(body)
            + '<nav class="reader-bottom"><a href="/">Accueil</a></nav>'
            '</main></body></html>', encoding="utf-8"
        )
        (self.out / NARRATIVE).write_text(
            '<!doctype html><html lang="fr"><head><title>Énée</title></head>'
            '<body class="mythos-design"><main><article class="content">'
            '<h1>Le récit d’Énée et de Didon</h1><p>Texte entier du récit.</p>'
            '</article></main></body></html>', encoding="utf-8"
        )

    def test_copy_exact_sources_and_bidirectional_navigation(self):
        self.assertEqual(install(self.root, self.out), 18)
        for name in NAMES:
            self.assertEqual(
                (self.root / SOURCE_DIR / name).read_bytes(),
                (self.out / SOURCE_DIR / name).read_bytes(),
            )
        study = BeautifulSoup((self.out / STUDY).read_text(encoding="utf-8"), "html.parser")
        narrative = BeautifulSoup((self.out / NARRATIVE).read_text(encoding="utf-8"), "html.parser")
        self.assertEqual(len(study.select(".mythos-eneide-source-grid li a")), 18)
        self.assertEqual(len(study.select('[data-mythos-eneide-sources="study"]')), 1)
        self.assertEqual(len(study.select('[data-mythos-eneide-sources="shelf"]')), 1)
        self.assertEqual(len(narrative.select('[data-mythos-eneide-sources="narrative"]')), 1)
        self.assertEqual(len(study.select("section > h2[id^=eneide-]")), 18)
        self.assertIn("Texte entier du récit.", narrative.get_text(" "))

    def test_idempotent_links(self):
        install(self.root, self.out)
        one = (self.out / STUDY).read_bytes()
        second = (self.out / NARRATIVE).read_bytes()
        install(self.root, self.out)
        self.assertEqual(one, (self.out / STUDY).read_bytes())
        self.assertEqual(second, (self.out / NARRATIVE).read_bytes())

    def test_refuse_missing_original_without_writing(self):
        (self.root / SOURCE_DIR / NAMES[5]).unlink()
        before = (self.out / STUDY).read_bytes()
        with self.assertRaisesRegex(RuntimeError, "Source Énéide absente"):
            install(self.root, self.out)
        self.assertEqual(before, (self.out / STUDY).read_bytes())

    def test_refuse_html_mismatch_without_writing(self):
        original = (self.out / STUDY).read_text(encoding="utf-8")
        (self.out / STUDY).write_text(
            original.replace('id="eneide-03"', 'id="erreur-03"'), encoding="utf-8"
        )
        before = (self.out / STUDY).read_bytes()
        with self.assertRaisesRegex(RuntimeError, "source et lecteur HTML divergents"):
            install(self.root, self.out)
        self.assertEqual(before, (self.out / STUDY).read_bytes())


if __name__ == "__main__":
    unittest.main()
