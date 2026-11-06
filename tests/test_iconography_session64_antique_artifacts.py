"""MYTHOS séance 64 : photographies antiques, sources et alternance."""
import json
from pathlib import Path
import unittest
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
CASES=[["philosophie-iliade.html","lecture-section-21","icono-iliade-mycene-porte-lionnes-s64-20261106","/media/2026/10/mythos-mycene-porte-lionnes-zde-2020.jpg","whc.unesco.org/en/list/941"],["philosophie-odyssee.html","lecture-section-21","icono-odyssee-menelas-helene-stamnos-s64-20261106","/media/2026/10/mythos-helene-menelas-stamnos-deepdene-met-41-162-20.jpg","metmuseum.org/art/collection/search/254187"],["philosophie-theogonie.html","lecture-section-14","icono-theogonie-derveni-commentaire-s64-20261106","/media/2026/10/mythos-derveni-papyrus-fragments-thessalonique-gts-tg.jpg","unesco.org/fr/memory-world/derveni-papyrus-oldest-book-europe"]]
class Iconography64(unittest.TestCase):
    def test_figures_are_unique_and_documented(self):
        for path, section, ident, src, source in CASES:
            with self.subTest(path=path):
                soup=BeautifulSoup((ROOT/path).read_text(encoding="utf-8"),"html.parser")
                fig=soup.find("figure",id=ident)
                self.assertIsNotNone(fig)
                # Les unités sont introduites par <h2>, non par des <section id="lecture-section-*">.
                self.assertEqual(fig.find_previous("h2").get("id"), section)
                img=fig.find("img")
                self.assertEqual(img.get("src"),src)
                self.assertTrue(img.get("alt","").strip())
                self.assertEqual(img.get("loading"),"lazy")
                self.assertGreater(int(img.get("width","0")),0)
                self.assertGreater(int(img.get("height","0")),0)
                self.assertEqual(len(soup.find_all("img",src=src)),1)
                self.assertTrue((ROOT/src.lstrip("/")).is_file())
                cap=fig.find("figcaption")
                self.assertIn("non générée par IA",cap.get_text(" ",strip=True))
                self.assertTrue(any(source in a["href"] for a in cap.find_all("a",href=True)))
                self.assertTrue(any("commons.wikimedia.org" in a["href"] for a in cap.find_all("a",href=True)))
                ids=[x["id"] for x in soup.find_all(id=True)]
                self.assertEqual(len(ids),len(set(ids)))
    def test_session64_and_historic_a4_minimum(self):
        d=json.loads((ROOT/"docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json").read_text(encoding="utf-8"))
        self.assertEqual(d["latest_session"],d["history"][-1])
        entries=[(i,x) for i,x in enumerate(d["history"]) if x.get("scope","").startswith("Séance 64 :")]
        self.assertEqual(len(entries),1)
        i,s=entries[0]
        self.assertEqual(d["history"][i-1]["kind"],"AUDIT ET CORRECTION")
        self.assertEqual(s["kind"],"ENRICHISSEMENT ICONOGRAPHIQUE")
        self.assertEqual(s["next_kind"],"AUDIT ET CORRECTION")
        if i+1<len(d["history"]):
            self.assertEqual(d["history"][i+1]["kind"],"AUDIT ET CORRECTION")
        p=json.loads((ROOT/"assets/philosophie/pagination-2026-11-04.json").read_text(encoding="utf-8"))
        for k in ("iliade","odyssee","theogonie"):
            self.assertGreaterEqual(p["studies"][k]["analyse-seule_pages"],10)
