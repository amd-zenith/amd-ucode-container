#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later
'''
A command line tool to print information about an AMD uCode container files.
'''

import argparse
from pathlib import Path
from typing import cast
from .banner import BANNER
from .structures.amd_ucode_container import AmdUcodeContainer
from .structures.equiv_cpu_section import EquivCpuSection
from .structures.file_section import FileSection, FileSectionType
from .structures.ucode_section import UcodeSection


def _describe_equiv_cpu_table(section: EquivCpuSection) -> None:
    print(f"    equivalency entries: {len(section.entries)}")
    for entry in section.entries:
        print(
            "      "
            f"installed_cpu={entry.installed_cpu:#010x} "
            f"equiv_cpu={entry.equiv_cpu:#06x} "
            f"mask={entry.fixed_errata_mask:#010x} "
            f"compare={entry.fixed_errata_compare:#010x}"
        )


def _describe_section(index: int, section: FileSection) -> None:
    print(f"  Section {index}: {section.section_type.name} (0x{section.section_type.value:04x})")
    print(f"    declared size: {section.section_size} bytes")

    if section.section_type == FileSectionType.EQUIV_CPU_TABLE:
        _describe_equiv_cpu_table(cast(EquivCpuSection, section.payload))


def ucode_container_info(file: Path):
    print(f"Info: Processing {file}...")
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

    print(f"\n{file}")
    print(f"  size: {len(raw)} bytes")
    print(f"  parsed sections: {len(container.sections)}")
    for idx, section in enumerate(container.sections, start=1):
        _describe_section(idx, section)


def main() -> None:
    print(BANNER)
    parser = argparse.ArgumentParser(description="Display information about an AMD uCode container files")
    parser.add_argument("files", nargs="+", type=Path, help="AMD uCode container files")
    args = parser.parse_args()
    for target in args.files:
        ucode_container_info(target)


if __name__ == "__main__":
    main()
