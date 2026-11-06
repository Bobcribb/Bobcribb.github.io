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
        # Dix-huit nouveaux lecteurs HTML : un par source, sans perte de bibliographie.
        for i, name in enumerate(NAMES):
            target = self.out / SOURCE_DIR / name.replace(".md", ".html")
            self.assertTrue(target.is_file(), name)
            reader = BeautifulSoup(target.read_text(encoding="utf-8"), "html.parser")
            self.assertEqual(reader.select_one("html").get("lang"), "fr")
            self.assertIn("Texte universitaire intégral", reader.select_one("article").get("aria-label"))
            self.assertIn(f"Source universitaire {i:02}", reader.select_one("article h1").get_text())
            self.assertIn("Analyse des sources primaires", reader.select_one("article").get_text(" "))
            self.assertIn("/corpus/philosophie/eneide/" + name,
                          [a.get("href") for a in reader.select(".eneide-reader-nav a")])
            if i == 17:
                self.assertIn("Bibliographie et références primaires", reader.select_one("article").get_text(" "))
        self.assertEqual(
            study.select_one(".mythos-eneide-source-grid li a").get("href"),
            "/corpus/philosophie/eneide/00-introduction.html"
        )

    def test_idempotent_links(self):
        install(self.root, self.out)
        one = (self.out / STUDY).read_bytes()
        second = (self.out / NARRATIVE).read_bytes()
        install(self.root, self.out)
        self.assertEqual(one, (self.out / STUDY).read_bytes())
        self.assertEqual(second, (self.out / NARRATIVE).read_bytes())
        self.assertIn(
            "/corpus/philosophie/eneide/01-chant-i.html",
            (self.out / SOURCE_DIR / "00-introduction.html").read_text(encoding="utf-8"),
        )

    def test_public_museum_banner_keeps_h1_outside_article(self):
        """Le récit réel place son h1 dans la bannière et débute par un h2."""
        path = self.out / NARRATIVE
        page = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        article = page.select_one("main article.content")
        title = article.find("h1").extract()
        header = page.new_tag("header")
        header.append(title)
        page.body.insert(0, header)
        heading = page.new_tag("h2")
        heading.string = "1. Le poème et le pouvoir d'Auguste"
        article.insert(0, heading)
        path.write_text(str(page), encoding="utf-8")
        self.assertEqual(install(self.root, self.out), 18)
        rendered = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        aside = rendered.select_one('main article.content aside[data-mythos-eneide-sources="narrative"]')
        self.assertIsNotNone(aside)
        self.assertEqual(aside.find_next_sibling().name, "h2")
        self.assertEqual(len(rendered.select("header h1")), 1)
        self.assertEqual(len(rendered.select('aside[data-mythos-eneide-sources="narrative"]')), 1)
        # Le rendu doit être stable lors des reconstructions horaires.
        first = path.read_bytes()
        self.assertEqual(install(self.root, self.out), 18)
        self.assertEqual(path.read_bytes(), first)

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
