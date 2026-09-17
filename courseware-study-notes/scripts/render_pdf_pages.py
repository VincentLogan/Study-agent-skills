#!/usr/bin/env python3
"""Render selected one-indexed PDF pages for targeted visual analysis."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import pymupdf as fitz
except ModuleNotFoundError:
    try:
        import fitz
    except ModuleNotFoundError:
        print("Missing PyMuPDF. Run: python -m pip install -r requirements.txt", file=sys.stderr)
        raise SystemExit(2)


def selected_pages(specification: str, maximum: int) -> list[int]:
    pages: set[int] = set()
    for component in specification.split(","):
        try:
            if "-" in component:
                first, last = (int(value.strip()) for value in component.split("-", 1))
                if first > last:
                    raise ValueError
                pages.update(range(first, last + 1))
            else:
                pages.add(int(component.strip()))
        except ValueError as error:
            raise argparse.ArgumentTypeError(f"invalid page selection: {component}") from error
    if not pages or min(pages) < 1 or max(pages) > maximum:
        raise argparse.ArgumentTypeError(f"pages must be within 1-{maximum}")
    return sorted(pages)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--pages", required=True, help="One-indexed pages, e.g. 3,7-9")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--dpi", default=180, type=int)
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error("--input must name an existing PDF")
    if not 72 <= args.dpi <= 400:
        parser.error("--dpi must be between 72 and 400")
    document = fitz.open(args.input)
    try:
        pages = selected_pages(args.pages, document.page_count)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        matrix = fitz.Matrix(args.dpi / 72, args.dpi / 72)
        for page_number in pages:
            document.load_page(page_number - 1).get_pixmap(matrix=matrix, alpha=False).save(args.output_dir / f"page-{page_number:04d}.png")
    finally:
        document.close()


if __name__ == "__main__":
    main()
