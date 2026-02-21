#!/usr/bin/env python

from dataclasses import dataclass
from typing import List
from .file_section import FileSection


@dataclass
class AmdUcodeContainer:
    """Complete AMD microcode container structure."""
    magic: str
    sections: List[FileSection]

    @classmethod
    def from_bytes(cls, data: bytes) -> 'AmdUcodeContainer':
        """Create AmdUcodeContainer from bytes."""
        if len(data) < 4:
            raise ValueError("Data too short for AMD microcode container")

        magic = data[0:4].decode('ascii')
        if magic != "DMA\x00":
            raise ValueError(f"Invalid magic: expected 'DMA\\x00', got {repr(magic)}")

        sections = []
        offset = 4

        while offset < len(data):
            section = FileSection.from_bytes(data[offset::])
            sections.append(section)
            offset += 8 + section.section_size

        return cls(magic=magic, sections=sections)
    