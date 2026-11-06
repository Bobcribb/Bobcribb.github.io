"""Accès vérifié à l'édition historique complète ODS I–XXVII, sans troncature."""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from origins_integral_reader import RELATIVE, URL, RETURN, link_integral_edition


class OdsIntegralEditionTests(unittest.TestCase):
    def prepare(self, directory):
        root, out = directory / "root", directory / "site"
        original, rendered = root / RELATIVE, out / RELATIVE
        original.parent.mkdir(parents=True, exist_ok=True)
        rendered.parent.mkdir(parents=True, exist_ok=True)
        scholarly = "Sources primaires ; bibliographie ; étude de textes. " * 12500
        markup = ('<!doctype html><html lang="fr"><body><header><h1>Tomes I–XXVII</h1>'
                  '</header><main><article><h2>Étude intégrale</h2><p>'
                  + scholarly + '</p></article></main></body></html>')
        original.write_text(markup, encoding="utf-8")
        rendered.write_text(markup, encoding="utf-8")
        return root, out, markup

    def test_aucun_volume_invente_si_absent(self):
        with TemporaryDirectory() as temp:
            base = Path(temp)
            self.assertEqual(link_integral_edition("<section>Archives</section>",
                                                   base / "site", base / "root"),
                             "<section>Archives</section>")

    def test_lien_retour_et_integrite_deux_passages(self):
        with TemporaryDirectory() as temp:
            root, out, markup = self.prepare(Path(temp))
            source = root / RELATIVE
            page = out / RELATIVE
            source_text = BeautifulSoup(markup, "html.parser").main.get_text(" ", strip=True)
            for _ in range(2):
                fragment = link_integral_edition("<section>Archives</section>", out, root)
                self.assertEqual(fragment.count('id="origines-edition-historique-integrale"'), 1)
                doc = BeautifulSoup(fragment, "html.parser")
                cards = doc.select(".origins-integral-link[href]")
                self.assertEqual(len(cards), 1)
                self.assertEqual(cards[0]["href"], URL)
                rendered = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
                self.assertEqual(rendered.main.get_text(" ", strip=True), source_text)
                nav = rendered.select("nav[data-mythos-integral-return]")
                self.assertEqual(len(nav), 1)
                self.assertEqual(nav[0].a["href"], RETURN)
                self.assertEqual(source.read_text(encoding="utf-8"), markup)

    def test_un_lecteur_manquant_interdit_lien_trompeur(self):
        with TemporaryDirectory() as temp:
            root, out, markup = self.prepare(Path(temp))
            (out / RELATIVE).unlink()
            with self.assertRaisesRegex(RuntimeError, "manquant"):
                link_integral_edition("", out, root)

    def test_un_lecteur_tronque_est_refuse(self):
        with TemporaryDirectory() as temp:
            root, out, markup = self.prepare(Path(temp))
            (out / RELATIVE).write_text("<main>résumé</main>", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "courte"):
                link_integral_edition("", out, root)


if __name__ == "__main__":
    unittest.main()
