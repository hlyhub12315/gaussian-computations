---
name: gaussian-computations
description: Prepare, review, parse, and troubleshoot Gaussian 16 quantum-chemistry calculations. Use when working with Gaussian/GaussView files or tasks involving .com, .gjf, .log, .out, .chk, .fchk, geometry optimization, single-point energy, opt+freq, harmonic frequency, IR/Raman, TDDFT/UV-Vis/excited states, basis-set choice, heavy-element/ECP/relativistic treatment, CASSCF/CASCI active spaces, SCF or optimization failures, Link errors, or extraction of energies, coordinates, orbitals, thermochemistry, and spectra from Gaussian outputs.
---

# Gaussian Computations

Use this skill for Gaussian 16 computational chemistry workflows. It is adapted from the Gaussian package in `sylcliff/dft-skills-market` and reshaped into a Codex-discoverable skill.

## Task Router

- Generate `.com`/`.gjf` input for geometry optimization, single-point energy, frequency, opt+freq, Raman, or TDDFT: read `references/input-generation.md`.
- Recommend functionals, basis sets, ECPs, relativistic treatments, or CASSCF/CASCI active spaces: read `references/method-selection.md`.
- Parse `.log`/`.out` results for status, energies, final coordinates, orbitals, thermochemistry, frequencies, dipole moments, charges, or TDDFT states: read `references/output-parse.md`.
- Diagnose failed Gaussian jobs, SCF failures, geometry convergence problems, memory/disk errors, Link errors, basis/input syntax problems, or suspicious imaginary frequencies: read `references/error-diagnosis.md`.
- Validate an input file before advising a run: use `scripts/validate_gaussian_input.py <file.com>`.

## Working Rules

1. Confirm the requested calculation type before writing route keywords. If the user asks for `opt+freq`, generate one combined `Opt Freq` job unless they ask for separate steps.
2. Preserve user-specified method, basis, charge, multiplicity, solvent, memory, processor count, and coordinates. If a required value is missing, choose a conservative default and state it.
3. Validate charge/multiplicity parity when coordinates are available. For odd electron counts, multiplicity must be even; for even electron counts, multiplicity must be odd.
4. For publication-oriented DFT inputs, include tight SCF, an appropriate integration grid, and dispersion when chemically appropriate. Do not add expensive or unsupported keywords casually.
5. For anions, Rydberg states, charge-transfer states, and weakly bound complexes, consider diffuse basis functions. For elements beyond Kr, consider ECPs or scalar relativistic methods.
6. For TDDFT, warn when B3LYP is used for charge-transfer states and recommend range-separated hybrids such as CAM-B3LYP or wB97XD.
7. For frequency jobs, remind the user that true minima have zero imaginary frequencies and transition states should normally have exactly one.
8. When diagnosing errors, quote only the relevant short log lines, identify the likely root cause, and provide a copy-paste-ready route-section fix.
9. Do not claim a calculation is publication-ready without noting the key assumptions: functional, basis, dispersion, solvation, relativistic/ECP treatment, spin state, and frequency verification.

## Output Conventions

For generated inputs, return:

- Filename suggestion, usually `<name>-opt.com`, `<name>-sp.com`, `<name>-freq.com`, `<name>-opfreq.com`, or `<name>-tddft.com`.
- Complete Gaussian input block.
- Short method summary.
- Run command: `g16 <file.com> > <file.log>`.
- Checks to perform after completion.

For parsed or diagnosed outputs, return:

- Status first: normal termination, error termination, or incomplete.
- Key evidence from the file.
- Extracted quantities with units.
- Next action if the run is failed or scientifically ambiguous.
