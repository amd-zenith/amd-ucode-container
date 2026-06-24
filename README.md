# AMD Microcode Container Parser

[![Build](https://github.com/amd-zenith/amd-ucode-container/actions/workflows/build.yml/badge.svg)](https://github.com/amd-zenith/amd-ucode-container/actions/workflows/build.yml)
[![CodeQL](https://github.com/amd-zenith/amd-ucode-container/actions/workflows/codeql.yml/badge.svg)](https://github.com/amd-zenith/amd-ucode-container/actions/workflows/codeql.yml)
[![PyPI version](https://img.shields.io/pypi/v/amd-ucode-container.svg)](https://pypi.org/project/amd-ucode-container/)
[![Python versions](https://img.shields.io/pypi/pyversions/amd-ucode-container.svg)](https://pypi.org/project/amd-ucode-container/)
[![Snyk package health](https://img.shields.io/badge/Snyk-package%20health-4C4A73?logo=snyk&logoColor=white)](https://snyk.io/advisor/python/amd-ucode-container)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/amd-zenith/amd-ucode-container/badge)](https://scorecard.dev/viewer/?uri=github.com/amd-zenith/amd-ucode-container)

A Python library for parsing and interpreting AMD microcode container files used in the Linux kernel.

This library provides functionality to read, parse, and interpret AMD microcode container files. These files contain microcode updates for AMD processors and are used by the Linux kernel's microcode loading mechanism.

The format is based on the AMD Linux Kernel MicroCode container format, documented in the Linux kernel source at `arch/x86/kernel/cpu/microcode/amd.c`.

## Installation

```bash
pip install amd-ucode-container
```

## Command line tools

Installing the package provides two command line executables:

### `amd_ucode_container_info`

Parses one or more AMD microcode container files and prints a human-readable
summary of their contents, including each section's type and size and, for
equivalence tables, the per-CPU equivalence entries.

```bash
amd_ucode_container_info <file> [<file> ...]
```

### `amd_ucode_container_extract`

Extracts the individual microcode patches contained in one or more AMD
microcode container files, writing each patch to an output directory.

```bash
amd_ucode_container_extract <file> [<file> ...] [-o OUTPUT]
```

| Option           | Description                                                                  |
| ---------------- | ---------------------------------------------------------------------------- |
| `-o`, `--output` | Directory to extract patches to (defaults to the current working directory). |

