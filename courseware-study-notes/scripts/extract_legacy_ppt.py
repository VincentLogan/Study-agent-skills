#!/usr/bin/env python3
"""Create a course-map JSON directly from a binary .ppt file."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from convert_legacy_ppt import convert_legacy_ppt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--cache-dir", required=True, type=Path, help="Directory for reusable converted PPTX files.")
    parser.add_argument("--mode", choices=("index", "full"), default="index")
    parser.add_argument("--force", action="store_true", help="Reconvert even when a matching cached PPTX exists.")
    args = parser.parse_args()
    if args.input.suffix.lower() != ".ppt" or not args.input.is_file():
        parser.error("--input must name an existing .ppt file")

    try:
        converted, cache_hit = convert_legacy_ppt(args.input, args.cache_dir, args.force)
    except (ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        raise SystemExit(str(error)) from error

    extractor = Path(__file__).with_name("extract_pptx.py")
    subprocess.run(
        [sys.executable, str(extractor), "--input", str(converted), "--output", str(args.output), "--mode", args.mode],
        check=True,
    )
    data = json.loads(args.output.read_text(encoding="utf-8"))
    data["source_file"] = str(args.input.resolve())
    data["source_format"] = "ppt"
    data["converted_pptx"] = str(converted.resolve())
    data["conversion_cache_hit"] = cache_hit
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
