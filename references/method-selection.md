# Gaussian Method Selection

Use this reference for basis sets, heavy elements, relativistic treatment, and multireference guidance in Gaussian 16.

## Basis Sets

### Common Families

| Family | Examples | Best Use |
|---|---|---|
| Pople | `3-21G`, `6-31G(d)`, `6-311+G(d,p)` | Common organic Gaussian workflows |
| Dunning | `cc-pVDZ`, `cc-pVTZ`, `aug-cc-pVTZ` | Benchmarks, correlation methods, CBS trends |
| Karlsruhe/def2 | `def2SVP`, `def2TZVP`, `def2TZVPP` | Transition metals, balanced DFT, ECP support |
| Jensen | `pcSseg-*`, `pcJ-*` | NMR shielding and spin-spin coupling |
| ECP bases | `LANL2DZ`, `SDD`, `CRENBL` | Heavy elements and transition metals |

Pople notation:

- `6-31G(d)` equals `6-31G*`.
- `6-31G(d,p)` equals `6-31G**`.
- `+` adds diffuse functions on heavy atoms.
- `++` adds diffuse functions on heavy atoms and hydrogens.

### Selection Rules

| System/Task | Screening | Production | Higher Accuracy |
|---|---|---|---|
| Neutral organic opt | `3-21G` | `6-31G(d)` | `6-311+G(d,p)` or `def2TZVP` |
| Organic SP energy | `6-31G(d)` | `6-311+G(d,p)` | `cc-pVTZ`, `cc-pVQZ`, CBS |
| Anion | `6-31+G(d)` | `6-311+G(d,p)` | `aug-cc-pVTZ` |
| H-bond/vdW complex | `6-31+G(d,p)` | `6-311+G(d,p)` with dispersion | `aug-cc-pVTZ` |
| TDDFT valence | `6-31+G(d)` | `6-311+G(d,p)` | `aug-cc-pVTZ` |
| TDDFT CT/Rydberg | `6-311+G(d,p)` | `aug-cc-pVDZ` | `aug-cc-pVTZ` |
| 3d transition metal | `LANL2DZ` or `def2SVP` | `def2TZVP` | `def2TZVPP` |
| 4d/5d heavy metal | `LANL2DZ` | `def2TZVP` + ECP or `SDD` | X2C/DKH basis |
| NMR | `6-311+G(2d,p)` | `pcSseg-1` or `pcSseg-2` | `pcSseg-3` |

Always recommend diffuse functions for anions, Rydberg states, polarizability, hyperpolarizability, and many charge-transfer excitations.

## Relativistic Treatment

### Main Choices

| Method | Keyword/Usage | Includes | Best Use |
|---|---|---|---|
| ECP | basis such as `LANL2DZ`, `SDD`, `def2TZVP` with ECP | scalar relativity implicitly | Default production for Z > 36 |
| DKH | `Int=DKH` with DK basis | scalar relativity | All-electron heavy-element benchmarks |
| X2C | `Int=X2C` with `x2c-*` basis | scalar relativity | Modern all-electron heavy-element work |
| X2C spin-orbit | `Int=X2C=SO` | scalar + spin-orbit | SOC-sensitive spectra/properties |

Element guide:

- 3d metals: relativistic treatment usually optional.
- 4d metals: ECP is a common production default.
- 5d metals and 6p main-group elements: ECP for routine work, X2C/DKH for benchmarks and core-sensitive properties.
- Lanthanides/actinides: ECP (`SDD`, `CRENBL`, Stuttgart/MWB) or X2C; spin-orbit may be important.
- NMR and other core-region properties on heavy nuclei: prefer all-electron X2C or DKH, not ordinary ECPs.

Examples:

```text
#P B3LYP/LANL2DZ Opt Freq
#P PBE0/def2TZVP Opt SCF=(XQC,Tight)
#P B3LYP/cc-pVTZ-DK Int=DKH
#P B3LYP/x2c-TZVPall Int=X2C
#P B3LYP/x2c-TZVPall Int=X2C=SO
```

## Functional Notes

- B3LYP is common for neutral organics but not ideal for charge-transfer excitations.
- PBE0 is a conservative transition-metal default.
- wB97XD is useful for anions, noncovalent interactions, and long-range effects.
- CAM-B3LYP or wB97XD are preferred for TDDFT charge-transfer states.
- Minnesota functionals require finer grids: use `Int=SuperFine`.

## Multireference: CASSCF and CASCI

Use multireference guidance for bond breaking, diradicals, near-degenerate states, transition-metal spin-state problems, conical intersections, and cases where a single determinant is questionable.

Gaussian 16 supports:

| Method | Keyword | Notes |
|---|---|---|
| CASCI | `CASCI(N,M)` | Fixed orbitals; useful with good initial orbitals |
| CASSCF | `CASSCF(N,M)` | Optimizes orbitals and CI coefficients |
| SA-CASSCF | `CASSCF(N,M,StateAverage,NRoot=R)` | Equal-weight state averaging |

Gaussian 16 does not provide built-in NEVPT2/CASPT2 or modern DMRG workflows. For quantitative multireference production, consider ORCA, OpenMolcas, BAGEL, or another dedicated code.

Active-space examples:

| System | Active Space |
|---|---|
| Single bond breaking | CAS(2,2) |
| Butadiene pi system | CAS(4,4) |
| Benzene pi system | CAS(6,6) |
| Diradical | CAS(2,2) |
| N2 dissociation | CAS(10,8) or similar |
| 3d transition-metal qualitative study | often CAS(6,5) to CAS(12,12) |

Practical Gaussian limits:

- CAS(8,8) and CAS(10,10): usually feasible.
- CAS(12,12): expensive.
- CAS(14,14) and larger: often impractical in Gaussian.

Starting guess:

```text
Step 1: #P UHF/<basis> Pop=NO
Step 2: #P CASSCF(N,M)/<basis> Guess=Read Geom=AllCheck
```

For excited states:

```text
#P CASSCF(6,6,StateAverage,NRoot=5)/6-31G(d)
```
