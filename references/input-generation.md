# Gaussian Input Generation

Use this reference when creating Gaussian 16 `.com` or `.gjf` files for geometry optimization, single-point energy, frequency, opt+freq, Raman, or TDDFT calculations.

## Required Sections

```text
%chk=<name>.chk
%mem=<memory>
%nprocshared=<cores>
# <method>/<basis> <route keywords>

<title>

<charge> <multiplicity>
<coordinates>

```

Always preserve the final blank line after coordinates. For checkpoint restarts, use `Geom=AllCheck` or `Geom=Check Guess=Read` only when the input really should read from an existing checkpoint.

## Defaults

- Neutral organic optimization: `B3LYP/6-31G(d) Opt=Tight SCF=Tight Int=UltraFine EmpiricalDispersion=GD3BJ`
- Publication upgrade for organic single points: `B3LYP/6-311+G(d,p)` or a user-specified higher level.
- Anions: prefer `wB97XD/6-311+G(d,p)` or another diffuse basis.
- Transition-metal systems: prefer `PBE0/def2TZVP`, `SCF=(XQC,Tight)`, and spin-state caution.
- Heavy elements beyond Kr: prefer def2/ECP, SDD, LANL2DZ, or an all-electron relativistic method when needed.
- Minnesota functionals (`M06`, `M06-2X`, `M06-L`, `M11`) need `Int=SuperFine`.

## Route Templates

### Geometry Optimization

```text
# <functional>/<basis> Opt=Tight SCF=Tight Int=UltraFine EmpiricalDispersion=GD3BJ
```

Use `SCF=(XQC,Tight)` for open-shell, transition-metal, or difficult SCF systems. Add `SCRF=(SMD,Solvent=<solvent>)` when solvation is requested.

### Single-Point Energy

```text
# <functional>/<basis> SCF=Tight Int=UltraFine EmpiricalDispersion=GD3BJ Pop=Mulliken
```

Do not include `Opt` keywords in pure single-point jobs. Add `Density=Current` only when the user asks for density-derived properties for the current state.

### Frequency

```text
# <functional>/<basis> Freq SCF=Tight Int=UltraFine EmpiricalDispersion=GD3BJ
```

Use `Freq=Raman` for Raman activities. Use the same electronic-structure level as the optimized geometry unless the user explicitly requests a different level.

Common scale factors:

| Level | Scale |
|---|---:|
| B3LYP/6-31G(d) | 0.9614 |
| B3LYP/6-311+G(d,p) | 0.9679 |
| B3LYP/def2TZVP | 0.985 |
| PBE0/def2TZVP | 0.955 |
| wB97XD/6-311+G(d,p) | 0.957 |
| M06-2X/6-311+G(d,p) | 0.946 |

### Combined Opt+Freq

```text
# <functional>/<basis> Opt=Tight Freq SCF=Tight Int=UltraFine EmpiricalDispersion=GD3BJ
```

Use this when the user wants stationary-point confirmation in the same job.

### TDDFT

```text
# <functional>/<basis> TD=(NStates=<n>,Root=<r>) SCF=Tight Int=UltraFine EmpiricalDispersion=GD3BJ
```

- Default `NStates=6`; recommend 10-20 for spectra.
- Use `TD=(NStates=<n>,Root=<r>,Triplets)` for triplet excitations.
- Use `TD=(NStates=<n>,Root=<r>,Singlets,Triplets)` when both are requested.
- Add `Density=Current` for excited-state density, charges, and dipole on the selected root.
- For charge-transfer states, recommend CAM-B3LYP, wB97XD, LC-BLYP, or M06-2X rather than B3LYP.
- For solution vertical excitations, consider non-equilibrium solvation syntax such as `SCRF=(SMD,Solvent=<solvent>,State=1)` when appropriate.

## Charge and Multiplicity

Validate electron parity:

- `system_electrons = sum(atomic_numbers) - charge`
- Even electron count: multiplicity 1, 3, 5, ...
- Odd electron count: multiplicity 2, 4, 6, ...

For multiplicity greater than 1, mention that unrestricted Kohn-Sham or unrestricted HF will normally be used. For transition metals, recommend comparing plausible spin states.

## Solvation

Use SMD by default:

```text
SCRF=(SMD,Solvent=Water)
```

Preserve the user's solvent name, but normalize obvious capitalization. Do not invent a solvent if the user did not ask for solvation.

## Output Format

Return a complete file, not fragments. Include:

```text
Suggested filename: <name>-<task>.com

<complete input>

Method summary:
- Functional/basis:
- Job type:
- Charge/multiplicity:
- Solvent:
- Notes:

Run:
g16 <name>-<task>.com > <name>-<task>.log
```
