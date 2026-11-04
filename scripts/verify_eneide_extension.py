#!/usr/bin/env python3
"""Verify the evolving scholarly Eneid against the immutable PR #4 corpus."""
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
from pypdf import PdfReader
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "corpus/philosophie/eneide"
BASELINE = json.loads((ROOT / "assets/philosophie/eneide-original-hashes.json").read_text(encoding="utf-8"))
REPORT = json.loads((ROOT / "assets/philosophie/eneide-pagination.json").read_text(encoding="utf-8"))
PDF = ROOT / "assets/philosophie/pdf/eneide-etude-a4.pdf"
PAGE = ROOT / "philosophie-eneide.html"
IMAGES = ROOT / "assets/philosophie/eneide-art-sources.json"

def digest(blob):
    return hashlib.sha256(blob).hexdigest()

def main():
    originals = BASELINE["original_source_sha256"]
    assert len(originals) == 18, "Changed original corpus reference"
    for name, original_sha in originals.items():
        src = SOURCE / name
        assert src.is_file(), f"Original source absent: {src}"
        actual_sha = digest(src.read_bytes())
        assert actual_sha == original_sha, f"Original study modified: {src}"
        assert REPORT["sources_sha256"][name] == actual_sha, "Outdated source evidence"
    all_sources = sorted(SOURCE.glob("*.md"))
    assert len(all_sources) >= len(originals) + 6, "Missing scholarly extensions"
    for src in all_sources:
        assert REPORT["sources_sha256"][src.name] == digest(src.read_bytes()), f"Stale report for {src.name}"
    assert REPORT["target_analysis_pages"] == 300
    assert REPORT["actual_analysis_pages"] > BASELINE["actual_analysis_pages"], "No measurable progress"
    assert REPORT["analysis_words"] > BASELINE["analysis_words"] + 15000
    assert REPORT["status"] == ("complete" if REPORT["actual_analysis_pages"] >= 300 else "partial")
    assert REPORT["duplicate_analysis_paragraphs"] == 0
    assert REPORT["format"] == "A4" and not REPORT["forced_analysis_page_breaks"]
    assert "illustrations" in REPORT["analysis_excludes"]
    assert PDF.is_file() and digest(PDF.read_bytes()) == REPORT["pdf_sha256"], "Incorrect PDF sha256"
    reader = PdfReader(PDF)
    assert len(reader.pages) == REPORT["actual_total_pdf_pages"]
    assert len(reader.pages) > REPORT["actual_analysis_pages"]
    for i, p in enumerate(reader.pages, 1):
        w, h = float(p.mediabox.width), float(p.mediabox.height)
        assert abs(w - 595.276) < 1 and abs(h - 841.89) < 1, f"Non-A4 page {i}"
        txt = p.extract_text() or ""
        assert len(txt.strip()) >= 10, f"Blank PDF page {i}"
    assert "Sommaire" in (reader.pages[1].extract_text() or ""), "PDF TOC missing"
    html = BeautifulSoup(PAGE.read_text(encoding="utf-8"), "html.parser")
    assert html.find("meta", attrs={"name": "viewport"}), "No smartphone viewport"
    ids = [tag["id"] for tag in html.select("[id]")]
    assert len(ids) == len(set(ids)), "Duplicate anchors"
    entries = html.select(".philo-toc a[href^='#']")
    assert len(entries) == len(all_sources), "Incomplete HTML contents"
    for link in entries:
        assert link["href"][1:] in ids, "Broken internal contents link"
    source_art = json.loads(IMAGES.read_text(encoding="utf-8"))
    assert len(source_art) >= 4, "Iconography is incomplete"
    known_image_paths = set()
    for image in source_art:
        rel = image["path"]
        assert rel.startswith("assets/philosophie/eneide/"), "Unsafe illustration path"
        f = ROOT / rel
        assert f.is_file() and f.stat().st_size >= 8000, f"Missing image: {rel}"
        assert digest(f.read_bytes()) == image["sha256"], "Source art changed"
        assert image["rights"] == "Public Domain — Met Open Access / CC0", "Unknown image rights"
        known_image_paths.add(rel)
    html_imgs = html.select(".philo-chapter img")
    assert len(html_imgs) >= 4, "Illustrations not visible in HTML"
    for tag in html_imgs:
        assert tag.get("alt") and tag["src"] in known_image_paths, "Broken or uncaptioned art"
    script = (ROOT / "scripts/render_eneide.py").read_text(encoding="utf-8")
    assert "@media(max-width:680px)" in script, "Phone CSS missing"
    assert "max-width:100%" in script, "Non-responsive images"
    print(json.dumps({
        "result": "PASS",
        "original_sources_preserved": len(originals),
        "study_markdown_files": len(all_sources),
        "analysis_words": REPORT["analysis_words"],
        "actual_analysis_pages": REPORT["actual_analysis_pages"],
        "pdf_pages_total": len(reader.pages),
        "status": REPORT["status"],
        "pages_remaining": max(0, 300 - REPORT["actual_analysis_pages"]),
        "museum_images": len(source_art),
        "html_contents_links": len(entries),
        "pdf_sha256_verified": True,
        "responsive_styles_present": True,
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
