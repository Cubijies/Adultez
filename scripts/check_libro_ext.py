#!/usr/bin/env python3
"""Verifica objetivamente la extensión de las piezas del libro contra el canon editorial.

Uso: python3 scripts/check_libro_ext.py
"""
from __future__ import annotations
import sys
from pathlib import Path

LIBRO = Path("docs/investigacion_civilizaciones_anteriores/libro")

# Umbrales [min, objetivo_min, objetivo_max, max] del canon editorial §10.5
UMBRALES = {
    "01_Prologo.md": (2800, 2800, 3500, 4000),
    "02_Introduccion.md": (2500, 2500, 3500, 4000),
    "03_Cap1_La_pregunta_prohibida.md": (5500, 5500, 7000, 8000),
    "04_Cap2_El_estandar_de_la_evidencia.md": (5500, 5500, 7000, 8000),
    "05_Cap3_Las_huellas_reales_de_la_prehistoria_profunda.md": (5500, 5500, 7000, 8000),
    "06_Cap4_La_Esfinge_y_su_enigma.md": (7500, 7500, 9000, 10500),
    "07_Cap5_Los_mapas_que_mostraban_la_Antartida.md": (7500, 7500, 9000, 10500),
    "08_Cap6_Atlantida_y_Mu.md": (7500, 7500, 9000, 10500),
    "09_Cap7_Cuando_el_cielo_cayo.md": (7500, 7500, 9000, 10500),
    "10_Cap8_Las_ciudades_sumergidas.md": (7500, 7500, 9000, 10500),
    "11_Cap9_Los_dioses_los_astros_y_las_maquinas.md": (7500, 7500, 9000, 10500),
    "12_Cap10_El_arma_que_no_fue.md": (7500, 7500, 9000, 10500),
    "13_Cap11_Lo_que_sabemos_y_lo_que_no.md": (6000, 6000, 7500, 8500),
    "14_Cap12_Como_se_sabria.md": (6000, 6000, 7500, 8500),
    "15_Epilogo.md": (2800, 2800, 3500, 4000),
}


def count_words(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").split())


def main() -> int:
    total = 0
    revisar = 0
    print(f"{'Pieza':<55} {'Actual':>7} {'Mín':>5} {'Obj':>6} {'Máx':>5}  Estado")
    print("-" * 100)
    for fname, (lo, olo, ohi, hi) in UMBRALES.items():
        path = LIBRO / fname
        if not path.exists():
            print(f"{fname:<55} {'--':>7}  FALTA ARCHIVO")
            revisar += 1
            continue
        n = count_words(path)
        total += n
        if n < lo:
            estado = "REVISAR (bajo mínimo)"
            revisar += 1
        elif lo <= n < olo:
            estado = "REVISAR (bajo objetivo)"
            revisar += 1
        elif n > hi:
            estado = "REVISAR (sobre máximo)"
            revisar += 1
        else:
            estado = "OK"
        print(f"{fname:<55} {n:>7} {lo:>5} {olo:>3}-{ohi:<3} {hi:>5}  {estado}")

    print("-" * 100)
    print(f"TOTAL piezas presentes: {sum(1 for f in UMBRALES if (LIBRO/f).exists())}")
    print(f"TOTAL palabras (piezas presentes): {total}")
    print(f"META DEL CUERPO (canon): ~105.000-115.000 palabras")
    print(f"Piezas en REVISAR: {revisar}")
    if revisar:
        print("RESULTADO: EXISTEN PIEZAS QUE NO CUMPLEN LA EXTENSIÓN")
        return 1
    print("RESULTADO: TODAS LAS PIEZAS CUMPLEN LA EXTENSIÓN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
