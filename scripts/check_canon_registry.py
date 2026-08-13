#!/usr/bin/env python3
"""Verifica los invariantes del registro de canon del LOTE-001.

Requisitos del canon G3:
1. Cada documento tiene EXACTAMENTE un canon_role principal.
2. Las condiciones (PARTIAL, DERIVATIVE, OCR_WARNING, etc.) son etiquetas NO excluyentes.
3. La suma de canon_role principales es exactamente 28.
4. DCA-000022 y DCA-000025 llevan PROVISIONAL_PENDING_METADATA.
5. Las incidencias de DCA-000001, DCA-000013 y DCA-000018 permanecen marcadas (abiertas).
6. La admisión al corpus no implica aceptación de las afirmaciones (documental).

Uso: python3 scripts/check_canon_registry.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

REGISTRY = Path("docs/investigacion_civilizaciones_anteriores/canon/LOTE_001_CANON_REGISTRY_V1.jsonl")
EXPECTED_IDS = {f"DCA-{i:06d}" for i in range(1, 29)}


def main() -> int:
    rows = [json.loads(line) for line in REGISTRY.open(encoding="utf-8")]
    errors: list[str] = []

    if len(rows) != 28:
        errors.append(f"Total registros = {len(rows)}, debe ser 28.")

    by_id = {r["source_id"]: r for r in rows}
    if set(by_id) != EXPECTED_IDS:
        missing = sorted(EXPECTED_IDS - set(by_id))
        extra = sorted(set(by_id) - EXPECTED_IDS)
        errors.append(f"source_ids faltantes: {missing}; extra: {extra}")

    # 1) y 3) un canon_role principal por documento; suma = 28
    roles = []
    for sid, r in by_id.items():
        role = r.get("canon_role")
        if not isinstance(role, str) or not role:
            errors.append(f"{sid}: sin canon_role principal.")
        roles.append(role)
    from collections import Counter
    print("Distribución de canon_role principales:")
    for role, n in sorted(Counter(roles).items()):
        print(f"  {role}: {n}")
    print(f"SUMA = {len(roles)} (objetivo 28)")

    # 2) etiquetas no excluyentes
    tags_ok = all(isinstance(r.get("tags", []), list) for r in by_id.values())
    if not tags_ok:
        errors.append("Algún registro no tiene tags como lista.")
    else:
        alltags = set().union(*(r["tags"] for r in by_id.values()))
        print("Etiquetas (no excluyentes) usadas:", sorted(alltags))

    # 4) provisionales
    for sid in ("DCA-000022", "DCA-000025"):
        tags = by_id[sid].get("tags", [])
        if "PROVISIONAL_PENDING_METADATA" not in tags:
            errors.append(f"{sid}: debe llevar etiqueta PROVISIONAL_PENDING_METADATA.")

    # 5) incidencias abiertas
    expected_open = {
        "DCA-000001": "OCR_WARNING",
        "DCA-000013": "CONTROL_CHARS",
        "DCA-000018": "CONTROL_CHARS",
    }
    for sid, tag in expected_open.items():
        tags = by_id[sid].get("tags", [])
        if tag not in tags:
            errors.append(f"{sid}: debe conservar la etiqueta {tag} (incidencia abierta).")

    print("")
    if errors:
        print("ERRORES:", file=sys.stderr)
        for e in errors:
            print("  - " + e, file=sys.stderr)
        return 1
    print("OK: invariantes del canon cumplidos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
