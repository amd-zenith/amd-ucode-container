#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later
'''
Helper functions to extract uCode patches.
'''

from pathlib import Path
from .structures.file_section import FileSectionType
from .structures.ucode_section import UcodeSection
from .structures.amd_ucode_container import AmdUcodeContainer


def ucode_section_extract_file(section: UcodeSection, outfile: Path):
    with outfile.open('wb') as f:
        f.write(section.data)


def _section_out_file(section: UcodeSection, outdir: Path) -> Path:
    base = "patch"
    suffix = 1
    destination = outdir / f"{base}_{suffix}.bin"
    while destination.exists():
        destination = outdir / f"{base}_{suffix}.bin"
        suffix += 1
    return destination


def ucode_section_extract_folder(section: UcodeSection, outdir: Path):
    dest = _section_out_file(section, outdir)
    ucode_section_extract_file(section, dest)


def container_sections_extract(container: AmdUcodeContainer, outdir: Path):
    for section in container.sections:
        if section.section_type != FileSectionType.UCODE:
            continue
        ucode_section_extract_folder(section.payload, outdir)

def container_extract(container: Path, outdir: Path):
    with container.open("rb") as f:
        container_sections_extract(AmdUcodeContainer.from_bytes(f.read()), outdir)
