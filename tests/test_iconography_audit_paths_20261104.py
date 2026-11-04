"""Régression de l'audit MYTHOS : chemins locaux, ancres et légendes.
Les documents publiés sont lus sans modifier leurs textes ni leurs numéros.
"""
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit
import posixpath
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PRIMARY_PAGES = (
    "index.html",
    "origines-du-sacre/index.html",
    "mythologie-grecque/index.html",
    "philosophie-iliade.html",
    "philosophie-odyssee.html",
    "philosophie-theogonie.html",
    "livre-iliade-scenes/index.html",
    "livre-odyssee/index.html",
    "livre-hesiode/index.html",
    "reconstitutions-photorealistes.html",
    "glossaire/index.html",
    "bestiaire/index.html",
)
SITE_PAGES = (
    "sites/dodone.html",
    "sites/nemee.html",
    "sites/corinthe.html",
    "sites/bassae.html",
    "sites/egine-aphaia.html",
    "sites/brauron.html",
    "sites/sounion.html",
    "sites/messene.html",
    "sites/delphes.html",
)


def local_file(source_page: str, href: str):
    """Résoudre un lien relatif, racine ou absolu local sans sa query string."""
    parsed = urlsplit(href)
    if parsed.scheme not in ("", "https", "http"):
        return None, None
    if parsed.netloc and parsed.netloc not in ("bobmythos.fr", "www.bobmythos.fr"):
        return None, None
    if not parsed.path and parsed.fragment:
        return ROOT / source_page, unquote(parsed.fragment)
    if not parsed.path:
        return None, None
    base = "/" + str(Path(source_page).parent).replace(".", "").strip("/")
    if parsed.path.startswith("/"):
        resolved = parsed.path
    else:
        resolved = posixpath.join(base, parsed.path)
    resolved = posixpath.normpath(unquote(resolved))
    if resolved == "/":
        resolved = "/index.html"
    elif resolved.endswith("/"):
        resolved += "index.html"
    target = ROOT / resolved.lstrip("/")
    if not target.is_file() and not target.suffix:
        target = target / "index.html"
    return target, unquote(parsed.fragment)


class IconographyAuditPathTests(unittest.TestCase):
    def test_twelve_reader_pages_have_valid_local_paths_and_fragments(self):
        for path in PRIMARY_PAGES:
            with self.subTest(page=path):
                doc = BeautifulSoup((ROOT / path).read_text(encoding="utf-8"), "html.parser")
                ids = [tag["id"] for tag in doc.find_all(id=True)]
                duplicated = [id_ for id_, n in Counter(ids).items() if n > 1]
                self.assertFalse(duplicated, (path, duplicated))
                for img in doc.find_all("img"):
                    self.assertTrue(img.has_attr("alt"), (path, str(img)[:160]))
                for tag in doc.select("a[href], img[src], script[src], link[href]"):
                    attr = "src" if tag.name in ("img", "script") else "href"
                    href = tag[attr]
                    target, fragment = local_file(path, href)
                    if target is None:
                        continue
                    self.assertTrue(target.is_file(), (path, tag.name, href, str(target)))
                    # Les renvois externes vers d'autres pages sont contrôlés
                    # séparément, pour ne pas imposer de traitement non nécessaire
                    # à l'intégralité des dizaines de milliers de liens du site.
                    if tag.name == "a" and href.startswith("#") and fragment:
                        self.assertIn(fragment, ids, (path, href))

    def test_iliad_and_heracles_cross_page_fragments_reach_named_passages(self):
        """Contrôler les signets inter-pages, pas seulement les ancres # locales."""
        references = {
            "iliade/index.html": ("/glossaire/#kleos",),
            "heracles/index.html": (
                "/bestiaire/#nemean",
                "/bestiaire/#hydre",
                "/bestiaire/#cerbere",
                "/religion/#heros-cultuels",
            ),
        }
        for source, addresses in references.items():
            source_doc = BeautifulSoup(
                (ROOT / source).read_text(encoding="utf-8"), "html.parser"
            )
            for address in addresses:
                with self.subTest(source=source, href=address):
                    self.assertIsNotNone(
                        source_doc.find("a", href=address),
                        "Renvoi historique absent : " + source + " → " + address,
                    )
                    target, fragment = local_file(source, address)
                    self.assertIsNotNone(fragment, address)
                    self.assertTrue(target.is_file(), str(target))
                    target_doc = BeautifulSoup(
                        target.read_text(encoding="utf-8"), "html.parser"
                    )
                    self.assertIsNotNone(
                        target_doc.find(id=fragment),
                        "Cible du signet absente : " + address,
                    )


    def test_nine_archaeology_pages_link_to_existing_gallery_anchors(self):
        gallery = BeautifulSoup(
            (ROOT / "reconstitutions-photorealistes.html").read_text(encoding="utf-8"),
            "html.parser",
        )
        targets = {tag["id"] for tag in gallery.find_all(id=True)}
        seen = 0
        for path in SITE_PAGES:
            page = BeautifulSoup((ROOT / path).read_text(encoding="utf-8"), "html.parser")
            for anchor in page.find_all("a", href=True):
                parsed = urlsplit(anchor["href"])
                if parsed.path != "/reconstitutions-photorealistes.html" or not parsed.fragment:
                    continue
                seen += 1
                self.assertIn(unquote(parsed.fragment), targets, (path, anchor["href"]))
        self.assertGreaterEqual(seen, 40)


if __name__ == "__main__":
    unittest.main()
