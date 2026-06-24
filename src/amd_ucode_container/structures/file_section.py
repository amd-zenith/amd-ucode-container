#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

from enum import Enum
from dataclasses import dataclass
from typing import Union
from .equiv_cpu_section import EquivCpuSection
from .ucode_section import UcodeSection


class FileSectionType(Enum):
    """Enumeration of section types in AMD microcode containers."""
    EQUIV_CPU_TABLE = 0x0000
    UCODE = 0x0001


@dataclass
class FileSection:
    """A section in the AMD microcode container."""
    section_type: FileSectionType
    section_size: int
    payload: Union[EquivCpuSection, UcodeSection]

    @classmethod
    def from_bytes(cls, data: bytes) -> 'FileSection':
        """Create FileSection from bytes."""
        if len(data) < 8:
            raise ValueError(f"FileSection data must be at least 8 bytes, got {len(data)}")

        section_type = FileSectionType(int.from_bytes(data[0:4], 'little'))
        section_size = int.from_bytes(data[4:8], 'little')

        payload = data[8:]
        if len(payload) < section_size:
            raise ValueError(f"FileSection payload declares {section_size} bytes but only {len(payload)} bytes available")
        payload = payload[:section_size]

        if section_type == FileSectionType.EQUIV_CPU_TABLE:
            parsed = EquivCpuSection.from_bytes(payload)
        elif section_type == FileSectionType.UCODE:
            parsed = UcodeSection.from_bytes(payload)
        else:
            raise ValueError(f"Unsupported section type: {section_type}")

        return cls(
            section_type=section_type,
            section_size=section_size,
            payload=parsed,
        )
