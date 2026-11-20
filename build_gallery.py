#!/usr/bin/env python3
"""Build Gallery 4 in place, using the same static layout as Gallery 3."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
ASSETS = ("styles/gallery.css", "scripts/gallery-data.js", "scripts/gallery.js")


def write_if_changed(path: Path, content: str) -> None:
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8")


def build() -> dict:
    image_root = ROOT / "images"
    if not image_root.is_dir():
        raise RuntimeError(f"Missing source directory: {image_root}")
    items = []
    for image_path in sorted(image_root.rglob("*"), key=lambda p: p.as_posix().casefold()):
        if not image_path.is_file() or image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        with Image.open(image_path) as image:
            width, height = image.size
        item = {
            "category": image_path.parent.relative_to(image_root).as_posix(),
            "src": image_path.relative_to(ROOT).as_posix(),
            "hasDescription": image_path.with_suffix(".md").is_file(),
            "title": image_path.stem,
            "width": width,
            "height": height,
        }
        items.append(item)
    data = "window.__GALLERY_IMAGES__ = " + json.dumps(items, ensure_ascii=False, indent=2) + ";\n"
    write_if_changed(ROOT / "scripts/gallery-data.js", data)
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for asset in ASSETS:
        digest = hashlib.sha256((ROOT / asset).read_bytes()).hexdigest()[:12]
        pattern = rf'((?:src|href)=")({re.escape(asset)})(?:\?[^"\']*)?(")'
        html = re.sub(pattern, lambda match: f'{match[1]}{match[2]}?v={digest}{match[3]}', html)
    write_if_changed(ROOT / "index.html", html)
    report = {"total_categorized": len(items), "category_counts": dict(Counter(item["category"] for item in items)), "with_descriptions": sum(item["hasDescription"] for item in items)}
    write_if_changed(ROOT / "catalog_report.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2))
