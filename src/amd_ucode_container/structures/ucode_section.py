#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

from dataclasses import dataclass
from typing import ClassVar, List


@dataclass
class UcodeSection:
    '''uCode section.'''
    data: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> 'UcodeSection':
        return cls(data)
