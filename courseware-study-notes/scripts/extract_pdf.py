#!/usr/bin/env python3
"""Extract PDF text/layout facts and classify pages before visual reading."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import pymupdf as fitz
except ModuleNotFoundError:
    try:
        import fitz
    except ModuleNotFoundError:
        print("Missing PyMuPDF. Run: python -m pip install -r requirements.txt", file=sys.stderr)
        raise SystemExit(2)


def blocks(page: Any) -> list[dict[str, Any]]:
    output = []
    for item in page.get_text("blocks", sort=True):
        x0, y0, x1, y1, text, block_no, block_type = item[:7]
        if block_type == 0 and text.strip():
            output.append({"x0": round(x0, 2), "y0": round(y0, 2), "x1": round(x1, 2), "y1": round(y1, 2), "block_number": block_no, "text": text.strip()})
    return output


def title(page: Any) -> str | None:
    choices = []
    for block in page.get_text("dict", sort=True).get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            text = "".join(span.get("text", "") for span in line.get("spans", [])).strip()
            sizes = [span.get("size", 0) for span in line.get("spans", [])]
            if text and sizes:
                choices.append((max(sizes), line.get("bbox", [0, 0])[1], text))
    return max(choices, key=lambda value: (value[0], -value[1]))[2] if choices else None


def kind(text_length: int, images: int, drawings: int) -> str:
    visuals = images + drawings
    if visuals and text_length < 180:
        return "image-led"
    if visuals and text_length < 1200:
        return "mixed"
    return "text-led"


def page_data(page: Any, number: int) -> dict[str, Any]:
    text_blocks = blocks(page)
    text = "\n".join(block["text"] for block in text_blocks)
    image_count, drawing_count = len(page.get_images(full=True)), len(page.get_drawings())
    return {"page_number": number, "title_candidate": title(page), "text_blocks": text_blocks, "native_text": text, "native_text_characters": len(text), "image_count": image_count, "drawing_count": drawing_count, "classification": kind(len(text), image_count, drawing_count)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.input.suffix.lower() != ".pdf" or not args.input.is_file():
        parser.error("--input must name an existing .pdf file")
    document = fitz.open(args.input)
    try:
        data = {"source_file": str(args.input.resolve()), "page_count": document.page_count, "pages": [page_data(page, number) for number, page in enumerate(document, 1)]}
    finally:
        document.close()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
