#!/usr/bin/env python3
"""Validate Gaussian input files for common structural mistakes."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ATOMIC_NUMBERS = {
    "H": 1,
    "He": 2,
    "Li": 3,
    "Be": 4,
    "B": 5,
    "C": 6,
    "N": 7,
    "O": 8,
    "F": 9,
    "Ne": 10,
    "Na": 11,
    "Mg": 12,
    "Al": 13,
    "Si": 14,
    "P": 15,
    "S": 16,
    "Cl": 17,
    "Ar": 18,
    "K": 19,
    "Ca": 20,
    "Sc": 21,
    "Ti": 22,
    "V": 23,
    "Cr": 24,
    "Mn": 25,
    "Fe": 26,
    "Co": 27,
    "Ni": 28,
    "Cu": 29,
    "Zn": 30,
    "Ga": 31,
    "Ge": 32,
    "As": 33,
    "Se": 34,
    "Br": 35,
    "Kr": 36,
    "Rb": 37,
    "Sr": 38,
    "Y": 39,
    "Zr": 40,
    "Nb": 41,
    "Mo": 42,
    "Tc": 43,
    "Ru": 44,
    "Rh": 45,
    "Pd": 46,
    "Ag": 47,
    "Cd": 48,
    "In": 49,
    "Sn": 50,
    "Sb": 51,
    "Te": 52,
    "I": 53,
    "Xe": 54,
    "Cs": 55,
    "Ba": 56,
    "La": 57,
    "Ce": 58,
    "Pr": 59,
    "Nd": 60,
    "Pm": 61,
    "Sm": 62,
    "Eu": 63,
    "Gd": 64,
    "Tb": 65,
    "Dy": 66,
    "Ho": 67,
    "Er": 68,
    "Tm": 69,
    "Yb": 70,
    "Lu": 71,
    "Hf": 72,
    "Ta": 73,
    "W": 74,
    "Re": 75,
    "Os": 76,
    "Ir": 77,
    "Pt": 78,
    "Au": 79,
    "Hg": 80,
    "Tl": 81,
    "Pb": 82,
    "Bi": 83,
    "Po": 84,
    "At": 85,
    "Rn": 86,
    "Fr": 87,
    "Ra": 88,
    "Ac": 89,
    "Th": 90,
    "Pa": 91,
    "U": 92,
    "Np": 93,
    "Pu": 94,
    "Am": 95,
    "Cm": 96,
}


def canonical_symbol(raw: str) -> str | None:
    match = re.match(r"^([A-Za-z]{1,2})", raw.strip())
    if not match:
        return None
    token = match.group(1)
    return token[0].upper() + token[1:].lower()


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_gaussian_input.py <file.com|file.gjf>")
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"ERROR: file not found: {path}")
        return 2

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    errors: list[str] = []
    warnings: list[str] = []

    route_indices = [i for i, line in enumerate(lines) if line.lstrip().startswith("#")]
    if not route_indices:
        errors.append("No route section found. Gaussian route section must start with '#'.")
        route_index = -1
        route = ""
    else:
        route_index = route_indices[0]
        route = lines[route_index].strip()

    if not any(line.lower().startswith("%mem") for line in lines):
        warnings.append("No %mem line found.")
    if not any(line.lower().startswith("%chk") for line in lines):
        warnings.append("No %chk line found.")
    if not any(line.lower().startswith("%nprocshared") for line in lines):
        warnings.append("No %nprocshared line found; Gaussian may use one core.")

    charge_mult_index = None
    charge = multiplicity = None
    charge_mult_re = re.compile(r"^\s*(-?\d+)\s+(\d+)\s*$")
    for i, line in enumerate(lines[route_index + 1 :], start=route_index + 1):
        match = charge_mult_re.match(line)
        if match:
            charge_mult_index = i
            charge = int(match.group(1))
            multiplicity = int(match.group(2))
            break

    if charge_mult_index is None or charge is None or multiplicity is None:
        errors.append("No charge/multiplicity line found, e.g. '0 1'.")
        coordinate_lines: list[str] = []
    else:
        if multiplicity < 1:
            errors.append("Multiplicity must be >= 1.")
        coordinate_lines = []
        for line in lines[charge_mult_index + 1 :]:
            if not line.strip():
                break
            if line.lstrip().startswith("--"):
                break
            coordinate_lines.append(line)

    electron_count = 0
    unknown_elements: list[str] = []
    for line in coordinate_lines:
        parts = line.split()
        if not parts:
            continue
        symbol = canonical_symbol(parts[0])
        if symbol is None or symbol not in ATOMIC_NUMBERS:
            unknown_elements.append(parts[0])
            continue
        electron_count += ATOMIC_NUMBERS[symbol]

    if coordinate_lines and charge is not None and multiplicity is not None:
        system_electrons = electron_count - charge
        if unknown_elements:
            warnings.append(
                "Unknown element symbols; electron parity was computed without them: "
                + ", ".join(sorted(set(unknown_elements)))
            )
        if system_electrons > 0 and (system_electrons % 2) != ((multiplicity - 1) % 2):
            expected = "odd multiplicity (1,3,5,...)" if system_electrons % 2 == 0 else "even multiplicity (2,4,6,...)"
            errors.append(
                f"Charge/multiplicity parity mismatch: {system_electrons} electrons require {expected}, got {multiplicity}."
            )

    lower_route = route.lower()
    if "m06" in lower_route or "m11" in lower_route:
        if "superfine" not in lower_route:
            warnings.append("Minnesota functional detected; consider Int=SuperFine.")
    if "td" in lower_route and "b3lyp" in lower_route:
        warnings.append("TDDFT with B3LYP can underestimate charge-transfer states; consider CAM-B3LYP or wB97XD if CT is relevant.")
    if ("freq" in lower_route) and ("scf=tight" not in lower_route and "scf=(" not in lower_route):
        warnings.append("Frequency job lacks explicit tight SCF convergence.")

    print(f"Gaussian input validation: {path}")
    if route:
        print(f"Route: {route}")
    if charge is not None and multiplicity is not None:
        print(f"Charge/multiplicity: {charge} {multiplicity}")
    if coordinate_lines:
        print(f"Coordinate lines: {len(coordinate_lines)}")
        print(f"Known-electron count before charge: {electron_count}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"RESULT: FAILED ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1
    print(f"RESULT: PASSED ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
