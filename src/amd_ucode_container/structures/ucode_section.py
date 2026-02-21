#!/usr/bin/env python

from dataclasses import dataclass
from typing import ClassVar, List


@dataclass
class UcodeSection:
    '''uCode section.'''
    data: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> 'UcodeSection':
        return cls(data)
