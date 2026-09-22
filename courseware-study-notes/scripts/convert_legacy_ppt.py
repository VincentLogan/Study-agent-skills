#!/usr/bin/env python3
"""Convert a binary .ppt to a cached .pptx copy through LibreOffice."""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


def source_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def libreoffice() -> str:
    executable = shutil.which("libreoffice") or shutil.which("soffice")
    if not executable:
        raise RuntimeError("LibreOffice is required for binary .ppt files. Install LibreOffice, then retry.")
    return executable


def convert_legacy_ppt(input_file: Path, cache_dir: Path, force: bool = False) -> tuple[Path, bool]:
    """Return (converted_pptx, cache_hit) without modifying the source file."""
    if input_file.suffix.lower() != ".ppt" or not input_file.is_file():
        raise ValueError("input must name an existing .ppt file")

    fingerprint = source_digest(input_file)[:16]
    cache_dir.mkdir(parents=True, exist_ok=True)
    output = cache_dir / f"{input_file.stem}.{fingerprint}.pptx"
    if output.is_file() and zipfile.is_zipfile(output) and not force:
        return output, True

    executable = libreoffice()
    with tempfile.TemporaryDirectory(prefix="courseware-ppt-stage-", dir=cache_dir) as stage_name:
        with tempfile.TemporaryDirectory(prefix="courseware-lo-profile-") as profile_name:
            stage = Path(stage_name)
            profile = Path(profile_name)
            command = [
                executable,
                "--headless",
                "--nologo",
                "--nodefault",
                "--nolockcheck",
                "--nofirststartwizard",
                "--norestore",
                f"-env:UserInstallation={profile.as_uri()}",
                "--convert-to",
                "pptx:Impress MS PowerPoint 2007 XML",
                "--outdir",
                str(stage),
                str(input_file.resolve()),
            ]
            result = subprocess.run(command, text=True, capture_output=True, timeout=180)
            if result.returncode:
                details = (result.stderr or result.stdout).strip()
                raise RuntimeError(f"LibreOffice failed to convert {input_file.name}: {details or 'no diagnostic output'}")

        staged = stage / f"{input_file.stem}.pptx"
        if not staged.is_file() or not zipfile.is_zipfile(staged):
            raise RuntimeError(f"LibreOffice finished without a valid PPTX output for {input_file.name}")
        if output.is_file() and not force and zipfile.is_zipfile(output):
            return output, True
        staged.replace(output)
    return output, False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--cache-dir", "--output-dir", dest="cache_dir", required=True, type=Path, help="Directory for reusable converted PPTX files.")
    parser.add_argument("--force", action="store_true", help="Ignore a matching cached conversion and convert again.")
    args = parser.parse_args()
    try:
        output, cache_hit = convert_legacy_ppt(args.input, args.cache_dir, args.force)
    except (ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        raise SystemExit(str(error)) from error
    print(f"{output}\t{'cache-hit' if cache_hit else 'converted'}")


if __name__ == "__main__":
    main()
