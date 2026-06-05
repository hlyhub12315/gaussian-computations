# Gaussian Error Diagnosis

Use this reference when a Gaussian `.log`/`.out` file failed or looks scientifically suspicious.

## Diagnosis Workflow

1. Check for `Normal termination`.
2. If absent, search for `Error termination`, `Fatal`, `Convergence failure`, `Link`, `l<number>.exe`, and the last 80-150 lines.
3. Identify whether the failure is input syntax, SCF, optimization, frequency, memory/disk, basis/ECP, or method incompatibility.
4. Suggest the least invasive fix first.
5. Provide exact route-section changes, not vague advice.

## SCF Convergence Failure

Evidence:

- `SCF Done` absent or not final.
- `Convergence failure`
- `SCF has not converged`
- Link 502 or similar SCF-related termination.

Fixes, from mild to stronger:

```text
SCF=(MaxCyc=512,Tight)
SCF=(DIIS,MaxCyc=512,Tight)
SCF=(QC,MaxCyc=512,Tight)
SCF=(XQC,MaxCyc=512,Tight)
SCF=(NoVarAcc,MaxCyc=512,Tight)
SCF=(VShift=500,MaxCyc=512,Tight)
SCF=Fermi
SCF=DM
```

For transition metals, open-shell systems, anions, and near-degenerate cases, `SCF=(XQC,Tight)` is often appropriate. Consider different spin states when chemically plausible.

## Optimization Not Converging

Evidence:

- `Maximum number of cycles exceeded`
- `Optimization stopped`
- No `Optimization completed`
- Oscillating gradients or displacements.

Fixes:

```text
Opt=(MaxCyc=200)
Opt=(CalcFC,MaxCyc=200)
Opt=(GDIIS,MaxCyc=200)
Opt=(EF,MaxCyc=200)
Opt=(NoTrustUpdate,MaxCyc=200)
Nosymm
```

For restarts:

```text
%oldchk=<old>.chk
%chk=<new>.chk
# <method>/<basis> Opt=Restart Geom=AllCheck Guess=Read
```

For poor starting geometries, recommend a lower-level preoptimization before production optimization.

## Input Syntax and Link 301-Style Errors

Evidence:

- `End of file in ZSymb`
- `EOF while reading`
- `Junk in input`
- `Unrecognized atomic symbol`
- Link 301 errors.

Checks:

- Link 0 commands (`%chk`, `%mem`, `%nprocshared`) are before the route section.
- Route section starts with `#`.
- A blank line follows the route section.
- A title section exists.
- A blank line follows the title.
- Charge/multiplicity line is exactly two integers, e.g. `0 1`.
- Coordinates are valid and followed by a final blank line.
- Basis name spelling is correct.

## Memory and Disk

Evidence:

- `Out-of-memory`
- `malloc failed`
- `Erroneous write`
- `No space left on device`
- Large RWF/scratch failures.

Fixes:

```text
%mem=32GB
%nprocshared=<cores>
%MaxDisk=100GB
```

Recommend setting `%mem` to no more than about 70-80% of available node RAM. For shared HPC nodes, follow local policy.

## Basis and ECP Problems

Evidence:

- `Basis set data is not on the checkpoint file`
- `Atomic number out of range for basis set`
- `Unrecognized basis set`
- Missing ECP cards with `GENECP`.

Fixes:

- Use a built-in basis name when possible: `6-31G(d)`, `6-311+G(d,p)`, `def2TZVP`, `LANL2DZ`, `SDD`.
- For mixed custom basis/ECP, use `GenECP` and include complete basis and ECP sections.
- For heavy elements, switch to `LANL2DZ`, `SDD`, `def2TZVP` with ECP, or a validated custom basis/ECP.

## Frequency Problems

If the job completed but imaginary frequencies are unexpected:

- Confirm the geometry optimization completed at the same or compatible level.
- Reoptimize with tighter settings:

```text
Opt=(Tight,CalcFC) Freq SCF=Tight Int=UltraFine
```

- Use `Nosymm` for numerical/symmetry artifacts.
- Inspect the displacement vectors of imaginary modes. Very small imaginary frequencies can be hindered rotations or numerical artifacts.

If frequency calculation fails:

```text
Freq=HPModes
SCF=Tight
Int=SuperFine
Nosymm
```

## TDDFT Problems

Common issues:

- Too few states: increase `NStates`.
- Charge-transfer states poor with B3LYP: switch to CAM-B3LYP or wB97XD.
- Root flipping during excited-state optimization: monitor state character, use state-specific checks, or reconsider workflow.
- Anions/Rydberg states missing diffuse functions: use `+`, `++`, or `aug-` basis.

## Response Template

```text
ERROR:
<brief label>

EVIDENCE:
<short relevant lines>

CAUSE:
<root cause>

SOLUTION:
<copy-paste-ready keyword or input fix>

NEXT CHECK:
<how to confirm the fix worked>
```
