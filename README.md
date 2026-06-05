# Gaussian Computations Skill

A personal Codex-compatible skill for preparing, parsing, and diagnosing Gaussian 16 computational chemistry calculations.

It supports common Gaussian workflows including:

- geometry optimization, single-point energy, frequency, opt+freq, Raman, and TDDFT input preparation
- basis-set, ECP, relativistic, and CASSCF/CASCI guidance
- Gaussian `.log` / `.out` output parsing
- SCF, optimization, memory/disk, basis, Link, and syntax error diagnosis
- input sanity checks with `scripts/validate_gaussian_input.py`

## Installation

Copy this folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\gaussian-computations-skill "$env:USERPROFILE\.codex\skills\gaussian-computations"
```

Restart Codex after installation.

## Attribution

Adapted from [sylcliff/dft-skills-market](https://github.com/sylcliff/dft-skills-market), MIT License, for personal Codex skill usage.

Modifications include Codex skill frontmatter, a single-skill router, reorganized reference files, UI metadata, and a Windows-friendly Python input validator.
