#!/usr/bin/env python3
"""Convert a legacy .ppt to a .pptx copy with LibreOffice."""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    if args.input.suffix.lower() != ".ppt" or not args.input.is_file():
        parser.error("--input must name an existing .ppt file")
    executable = shutil.which("libreoffice") or shutil.which("soffice")
    if not executable:
        parser.error("LibreOffice is required to convert .ppt files but was not found")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [executable, "--headless", "--convert-to", "pptx", "--outdir", str(args.output_dir), str(args.input)],
        check=True,
    )
    output = args.output_dir / f"{args.input.stem}.pptx"
    if not output.is_file():
        raise SystemExit(f"conversion finished without expected output: {output}")
    print(output)


if __name__ == "__main__":
    main()
