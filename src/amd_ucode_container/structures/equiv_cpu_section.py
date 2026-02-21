#!/usr/bin/env python

from dataclasses import dataclass
from typing import List, ClassVar


@dataclass
class EquivCpuEntry:
    """Entry in the CPU equivalency table."""
    SIZE: ClassVar[int] = 16

    installed_cpu: int
    fixed_errata_mask: int
    fixed_errata_compare: int
    equiv_cpu: int
    res: int

    @classmethod
    def from_bytes(cls, data: bytes) -> 'EquivCpuEntry':
        """Create EquivCpuEntry from 16 bytes of data."""
        if len(data) != EquivCpuEntry.SIZE:
            raise ValueError(f"EquivCpuEntry data must be {EquivCpuEntry.SIZE} bytes, got {len(data)}")

        return cls(
            installed_cpu=int.from_bytes(data[0:4], 'little'),
            fixed_errata_mask=int.from_bytes(data[4:8], 'little'),
            fixed_errata_compare=int.from_bytes(data[8:12], 'little'),
            equiv_cpu=int.from_bytes(data[12:14], 'little'),
            res=int.from_bytes(data[14:16], 'little')
        )


@dataclass
class EquivCpuSection:
    '''CPU equivalency section.'''
    entries: List[EquivCpuEntry]

    @classmethod
    def from_bytes(cls, data: bytes) -> 'EquivCpuSection':
        '''Create EquivCpuSection from bytes.'''
        entry_count = len(data) // EquivCpuEntry.SIZE
        entries: List[EquivCpuEntry] = []
        offset = 0
        for _ in range(entry_count):
            chunk = data[offset:offset + EquivCpuEntry.SIZE]
            entries.append(EquivCpuEntry.from_bytes(chunk))
            offset += EquivCpuEntry.SIZE

        if offset != len(data):
            raise Exception(f"Data size is {len(data)} wich seems to not be a multiple of EquivCpuEntry size ({EquivCpuEntry.SIZE})")

        return cls(entries=entries)
