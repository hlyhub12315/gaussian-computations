# Gaussian Output Parsing

Use this reference to summarize `.log` or `.out` files. Prefer deterministic parsing with `Select-String`, `rg`, or a short script when files are large.

## Status

Search near the end:

- `Normal termination of Gaussian` means the job completed.
- `Error termination` means Gaussian stopped with an error.
- `Job cpu time` and `Elapsed time` give runtime.

Always report status first.

## Energies

Patterns:

- `SCF Done:` final and intermediate SCF energies in Hartree.
- Post-SCF methods may print method-specific final energies such as `E2 =`, `EUMP2 =`, or coupled-cluster summaries.
- `Zero-point correction=`
- `Thermal correction to Energy=`
- `Thermal correction to Enthalpy=`
- `Thermal correction to Gibbs Free Energy=`
- `Sum of electronic and zero-point Energies=`
- `Sum of electronic and thermal Free Energies=`

Use conversion when useful:

- 1 Hartree = 27.211386245988 eV
- 1 Hartree = 627.509474 kcal/mol
- 1 Hartree = 2625.499638 kJ/mol

## Geometry

For optimized coordinates:

1. Find the final `Standard orientation:` block. If absent, use `Input orientation:`.
2. Convert atomic numbers to element symbols.
3. Use coordinates in Angstrom from the block.
4. Count optimization steps from `Standard orientation:` or optimization summary blocks.

Optimization success patterns:

- `Optimization completed.`
- `-- Stationary point found.`

## Orbitals

Patterns:

- `Alpha  occ. eigenvalues --`
- `Alpha virt. eigenvalues --`
- `Beta  occ. eigenvalues --`
- `Beta virt. eigenvalues --`

HOMO is the last occupied eigenvalue. LUMO is the first virtual eigenvalue. Convert the HOMO-LUMO gap to eV when reporting.

## Frequencies

Patterns:

- `Frequencies --`
- `IR Intensities --`
- `Raman Activities --`

Negative frequencies are imaginary modes. Interpret:

- 0 imaginary frequencies: true minimum.
- 1 imaginary frequency: likely transition state if the mode matches the reaction coordinate.
- More than 1: not a converged minimum/TS for the intended structure.

Report ZPE and thermal corrections separately from electronic energy.

## TDDFT

Patterns:

- `Excited State`
- `Excitation energies and oscillator strengths`
- `f=` oscillator strength
- orbital contribution lines such as `70 -> 71`

Report:

- State number.
- Energy in eV.
- Wavelength in nm.
- Oscillator strength.
- Major orbital contributions when available.

## Population and Properties

Patterns:

- `Dipole moment`
- `Mulliken atomic charges:`
- `ESP charges:`
- `Summary of Natural Population Analysis:` if NBO is requested.
- `Charge =` and `Multiplicity =`
- `NBasis =`
- `NAlpha=` and `NBeta=`
- `Stoichiometry`

## Summary Template

```text
GAUSSIAN OUTPUT SUMMARY
=======================

Status:
- Normal termination:
- Runtime:

Method/System:
- Route:
- Charge/multiplicity:
- Basis functions:
- Electrons:

Energy:
- Final electronic energy:
- ZPE:
- Thermal Gibbs correction:
- Free energy:

Geometry:
- Optimization status:
- Final coordinates:

Frequency:
- Imaginary frequencies:
- Key frequencies / IR intensities:

Electronic structure:
- HOMO:
- LUMO:
- Gap:

TDDFT:
- State, eV, nm, oscillator strength, assignment:

Notes:
- Scientific checks or warnings:
```

Only include sections supported by the file.
