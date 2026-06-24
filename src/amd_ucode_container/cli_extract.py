#!/usr/bin/env python
'''
A tool to extract AMD uCode container files.
'''

import argparse
from pathlib import Path
from typing import cast
from .banner import BANNER
from .extract import ucode_section_extract_folder
from .structures.amd_ucode_container import AmdUcodeContainer
from .structures.file_section import FileSection, FileSectionType
from .structures.ucode_section import UcodeSection


def ucode_container_extract(file: Path, outdir: Path) -> None:
    print(f"Extract: {file} -> {outdir}")
    if not file.exists():
        print(f"Error: {file} does not exist")
        return
    if not file.is_file():
        print(f"Error: {file} is not a regular file")
        return

    try:
        raw = file.read_bytes()
    except OSError as exc:
        print(f"Error: could not read {file}: {exc}")
        return

    try:
        container = AmdUcodeContainer.from_bytes(raw)
    except ValueError as exc:
        print(f"Error: {file}: {exc}")
        return

    outdir.mkdir(parents=True, exist_ok=True)
    extracted = 0
    for section in container.sections:
        if section.section_type != FileSectionType.UCODE:
            continue
        ucode_section_extract_folder(section.payload, outdir)
        extracted += 1

    if extracted == 0:
        print("  No UCODE sections found")
    else:
        print(f"  Extracted {extracted} patch(es)")


def main() -> None:
    print(BANNER)
    parser = argparse.ArgumentParser(description="Extract patches from AMD uCode container files.")
    parser.add_argument("files", nargs="+", type=Path, help="AMD uCode container files to extract")
    parser.add_argument("-o", "--output", type=Path, default=Path.cwd(), help="Directory to extract patches to")
    args = parser.parse_args()

    for target in args.files:
        ucode_container_extract(target, args.output)


if __name__ == "__main__":
    main()
