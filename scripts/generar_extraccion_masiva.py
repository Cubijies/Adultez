#!/usr/bin/env python3
"""Primer lote de extracción masiva de afirmaciones — corpus activo (schema v2.0).

Cubre las fuentes del corpus activo del LOTE-001 (DCA-000021 ya está en el
piloto G4). Cada afirmación se referencia con source_id, passage_id, líneas,
página (via página-map) y hashes. La página se resuelve automáticamente desde
`20_indices/pagemap_{sid}.jsonl`; el hash de fuente, desde el manifiesto.

Advertencia de calidad: varias fuentes presentan OCR degradado; las citas son
fragmentos breves y se marca `ocr_warning=True` donde la lectura es incierta.

Uso: python3 scripts/generar_extraccion_masiva.py [--root RAIZ]
"""
from __future__ import annotations
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("corpus_local/civilizaciones_anteriores")
OUT = Path("docs/investigacion_civilizaciones_anteriores/g4_masiva/LOTE_ACTIVO_AFIRMACIONES_V1.jsonl")
SCHEMA = Path("docs/investigacion_civilizaciones_anteriores/esquemas/claim_record.schema.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_manifest():
    return {r["source_id"]: r for r in (json.loads(l) for l in (ROOT / "20_indices/manifest.jsonl").open(encoding="utf-8"))}


def load_pagemap(sid):
    path = ROOT / "20_indices" / f"pagemap_{sid}.jsonl"
    if not path.exists():
        return []
    return [json.loads(l) for l in path.open(encoding="utf-8")]


def page_for_line(pagemap, line):
    for entry in pagemap:
        if entry["line_start"] <= line <= entry["line_end"]:
            label = entry["page_label"]
            if label.startswith("FORMFEED-"):
                return "p." + label.split("-")[-1]
            cand = entry.get("page_number_candidates") or []
            extra = f"/p.{cand[0]}" if cand else ""
            return f"p.{label}{extra}"
    return None


def qsha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# (source_id, claimant_abbr, attributed_claim, paraphrase, claim_type, category,
#  object, asserted_date, mechanism, evidence, stance, theory, ocr, passages)
# passages: list of (line_start, line_end, quotation)
CLAIMS = [
    # --- DCA-000001 Sitchin (OCR muy degradado) ---
    ("DCA-000001", "Sitchin, Zecharia",
     "La Tierra fue visitada en el pasado por astronautas de otro planeta (el duodécimo planeta del sistema solar), que crearon al hombre mediante métodos avanzados.",
     "Tesis central de Sitchin: visitas extraterrestres y creación humana; registrada como afirmación del autor, no como hecho.",
     "INTERPRETIVE", "INTERPRETATIVA", "Origen de la civilización / creación del hombre",
     None, "intervención de seres de otro planeta (Anunnaki)",
     "Lectura de textos, dibujos y objetos de Oriente Próximo según el autor.",
     "FAVORABLE", "A07", True,
     [(40, 40, "cierta civilización de otro planeta, más avanzada que la nuestra, fuera capaz de hacer aterrizar a sus astronautas en la Tierra")]),
    ("DCA-000001", "Sitchin, Zecharia",
     "En Oriente Próximo se observa una regresión cultural y casi desaparición de la población hacia ~11000 a.C., seguida de la aparición súbita de un 'hombre pensante' con alto nivel cultural, sin preparación gradual previa.",
     "Interpretación de Sitchin del registro arqueológico de Shanidar; señalada como inferencia suya.",
     "INTERPRETIVE", "INTERPRETATIVA", "Discontinuidad cultural en Oriente Próximo",
     "circa 11000 a.C.", "intervención externa (dioses) en la cultura humana",
     "Evidencia arqueológica (cueva de Shanidar) y estudios citados.",
     "FAVORABLE", "A07", True,
     [(65, 65, "el Hombre pensante volvió a aparecer con un nuevo vigor y con un inexplicablemente alto nivel cultural")]),

    # --- DCA-000003 Donnelly (en) ---
    ("DCA-000003", "Donnelly, Ignatius",
     "Atlántida fue el verdadero mundo antediluviano, el Jardín del Edén y la cuna de la civilización, desde la que se difundieron las artes, la agricultura y el conocimiento a todo el mundo.",
     "Proposición central de Donnelly sobre Atlántida como civilización madre; registrada como afirmación del autor.",
     "INTERPRETIVE", "INTERPRETATIVA", "Atlántida",
     "periodo antediluviano", None,
     "Correspondencias culturales y textos antiguos compilados por el autor.",
     "FAVORABLE", "A01", True,
     [(329, 329, "That it was the true Antediluvian world; the Garden of Eden")]),
    ("DCA-000003", "Donnelly, Ignatius",
     "Las civilizaciones de Egipto y del valle del Indo fueron colonias de una civilización más antigua, la de la Atlántida.",
     "Afirmación de difusión de Donnelly; registrada como afirmación del autor.",
     "INTERPRETIVE", "INTERPRETATIVA", "Difusión cultural desde Atlántida",
     None, None,
     "Paralelos culturales y lingüísticos según el autor.",
     "FAVORABLE", "A01", True,
     [(300, 300, "THE ANTEDILUVIAN WORLD")]),

    # --- DCA-000004 Bauval & Hancock (Guardian del Génesis) ---
    ("DCA-000004", "Bauval, Robert; Hancock, Graham",
     "La Gran Esfinge, un colosal león con cabeza humana, tiene una orientación y relación con los monumentos de Guiza que permiten vincularla con una fecha celeste muy anterior al Reino Antiguo.",
     "Presentación de la Esfinge como león recumbente y su posible correlación celeste; registrada como afirmación de los autores.",
     "INTERPRETIVE", "INTERPRETATIVA", "Gran Esfinge de Guiza",
     None, "correlación celeste/orientación astronómica",
     "Descripción del monumento y su contexto.",
     "FAVORABLE", "A09", False,
     [(130, 146, "Una estatua gigantesca, con cuerpo de león y cabeza humana ... Es la Gran Esfinge.")]),

    # --- DCA-000006 Hapgood (Earth's Shifting Crust, componente) ---
    ("DCA-000006", "Hapgood, Charles H.",
     "Un desplazamiento de la corteza terrestre puede trasladar continentes a latitudes muy distintas, provocando la muerte en grandes cantidades de especies y personas durante un solo movimiento de la corteza.",
     "Afirmación de Hapgood sobre desplazamiento cortical como mecanismo de catástrofes; registrada como afirmación del autor.",
     "CAUSAL", "CAUSAL", "Desplazamiento cortical",
     None, "desplazamiento de la corteza terrestre",
     "Análisis geológico y paleoclimático del autor.",
     "FAVORABLE", "A04", False,
     [(16, 30, "two opposite quarters of the earth's surface would be moving equatorward while two others were moving poleward ... during a single movement of the crust")]),

    # --- DCA-000007 Hapgood (Earth's Shifting Crust, componente) ---
    ("DCA-000007", "Hapgood, Charles H.",
     "Existe evidencia en la Antártida ('The New Evidence from Antarctica') que apoya la teoría de desplazamientos rápidos del polo/corteza, con épocas cálidas en la Antártida.",
     "Afirmación de Hapgood sobre la evidencia antártica del desplazamiento cortical; registrada como afirmación del autor.",
     "EMPIRICAL", "OBSERVACIONAL", "Antártida / desplazamiento cortical",
     None, "desplazamiento rápido de la corteza",
     "Evidencia geológica y paleoclimática citada por el autor.",
     "FAVORABLE", "A04", False,
     [(60, 60, "The New Evidence from Antarctica")]),

    # --- DCA-000009 Donnelly (es) ---
    ("DCA-000009", "Donnelly, Ignatius",
     "Atlántida fue el verdadero mundo antediluviano y el Jardín del Edén, y su civilización alcanzó un grado avanzado antes de su destrucción.",
     "Tesis de Donnelly en su versión española; registrada como afirmación del autor.",
     "INTERPRETIVE", "INTERPRETATIVA", "Atlántida",
     None, None,
     "Compilación de textos antiguos y tradiciones.",
     "FAVORABLE", "A01", False,
     [(147, 147, "it was the true Antediluvian world; the Garden of Eden; the Gardens of the Hesperides")]),

    # --- DCA-000010 Churchward (es, Mu) ---
    ("DCA-000010", "Churchward, James",
     "El continente de Mu es el lugar donde el hombre fue creado y su civilización originaria, hoy desaparecido bajo el océano.",
     "Afirmación de Churchward sobre Mu como cuna de la humanidad; registrada como afirmación del autor.",
     "INTERPRETIVE", "INTERPRETATIVA", "Continente de Mu",
     None, None,
     "Supuestas tablillas Naacal y tradiciones según el autor.",
     "FAVORABLE", "A03", False,
     [(711, 711, "El continente de Mu es el lugar en que el hombre ...")]),
    ("DCA-000010", "Churchward, James",
     "Las placas Naacal, escritas por una hermandad de sacerdotes, contienen el registro de la civilización perdida de Mu.",
     "Afirmación de Churchward sobre el origen de las placas Naacal; registrada como afirmación del autor.",
     "EMPIRICAL", "OBSERVACIONAL", "Placas Naacal",
     None, None,
     "Las supuestas placas Naacal y su lectura según el autor.",
     "FAVORABLE", "A03", False,
     [(734, 734, "PLACAS DE NAACAL")]),

    # --- DCA-000013 Hancock (América antes, muestra) ---
    ("DCA-000013", "Hancock, Graham",
     "Se perdió una civilización avanzada a causa de una catástrofe (inundación/hielo), cuya memoria se habría conservado en monumentos y tradiciones.",
     "Tesis de Hancock según el texto de muestra; registrada como afirmación del autor.",
     "INTERPRETIVE", "INTERPRETATIVA", "Civilización avanzada perdida",
     None, "catástrofe (inundación/hielo)",
     "Argumento general del autor en la muestra.",
     "FAVORABLE", "A08", False,
     [(27, 27, "¿Se perdió una civilización avanzada debido al ca...")]),

    # --- DCA-000014 Kimura (2004) ---
    ("DCA-000014", "Kimura, Masaaki",
     "Existen estructuras artificiales de piedra bajo el mar frente a las islas Ryukyu (Yonaguni), una estructura mixta a modo de castillo y templo, que indican una civilización megalítica antigua.",
     "Afirmación de Kimura de que las estructuras submarinas de Yonaguni son artificiales; registrada como afirmación del autor.",
     "INTERPRETIVE", "INTERPRETATIVA", "Estructuras submarinas de Yonaguni",
     None, None,
     "Inspecciones submarinas y distribución de estructuras según el autor.",
     "FAVORABLE", "S02", False,
     [(53, 111, "mixed structure, part castle and part temple ... ancient, megalithic civilization in the Ryukyu ... believe it man-made")]),

    # --- DCA-000016 Hancock (Fingerprints) ---
    ("DCA-000016", "Hancock, Graham",
     "Mapas antiguos, como el de Oronteus Finaeus, muestran la Antártida con rasgos geográficos (glaciares, costa) anteriores a la última glaciación, como evidencia de una cartografía heredada de una civilización avanzada.",
     "Afirmación de Hancock sobre los mapas antiguos; registrada como afirmación del autor.",
     "EMPIRICAL", "OBSERVACIONAL", "Mapas antiguos de la Antártida",
     "antes de la última glaciación", None,
     "Análisis del mapa de Oronteus Finaeus y sedimentos.",
     "FAVORABLE", "A08", False,
     [(636, 647, "sedimento marino glaciar ... Las muestras extraídas indican que ...")]),

    # --- DCA-000017 Hancock (Magicians) ---
    ("DCA-000017", "Hancock, Graham",
     "Un gigantesco cometa entró en el sistema solar y una segunda serie de impactos tuvo lugar hace unos 11.600 años (Dryas reciente), asociada a la destrucción de una civilización.",
     "Afirmación de Hancock sobre el impacto cometario del Younger Dryas; registrada como afirmación del autor.",
     "CAUSAL", "CAUSAL", "Impacto del cometa / Dryas reciente",
     "hace ~11.600 años", "impacto cometario (Younger Dryas)",
     "Grupo de científicos que investigan el impacto del cometa del Dryas.",
     "FAVORABLE", "A08/P10", False,
     [(16, 22, "gigantesco cometa que había entrado en el sistema solar ... Una segunda serie de impactos tuvieron lugar hace 11.600 años")]),

    # --- DCA-000019 Hapgood (Maps) ---
    ("DCA-000019", "Hapgood, Charles H.",
     "Mapas antiguos (Piri Reis, Oronteus Finaeus, Hadji Ahmed) muestran la Antártida y Hapgood concluyó que fueron hechos a partir de mapas aun más antiguos, derivados de una civilización avanzada anterior a la última era glacial.",
     "Afirmación de Hapgood sobre el origen de los mapas antiguos; registrada como afirmación del autor.",
     "EMPIRICAL", "OBSERVACIONAL", "Mapas antiguos / Antártida",
     "anterior a la última era glacial", "cartografía heredada",
     "Análisis de los mapas y sus proyecciones.",
     "FAVORABLE", "A04", False,
     [(12, 19, "the Piri Reis Map that shows Antarctica ... these maps were made from more ancient maps")]),

    # --- DCA-000024 Schoch (Voices of the Rocks) ---
    ("DCA-000024", "Schoch, Robert M.",
     "La investigación sobre la edad de la Gran Esfinge indica que su problema de edad es mucho mayor de lo que sostiene la egiptología convencional.",
     "Tesis de Schoch sobre la edad de la Esfinge; registrada como afirmación del autor.",
     "CHRONOLOGICAL", "CRONOLOGICA", "Gran Esfinge de Guiza",
     "anterior al Reino Antiguo", "erosión por agua / meteorización",
     "Trabajo de campo geológico en la Esfinge.",
     "FAVORABLE", "S06/A10", False,
     [(32, 63, "My research concerning the age of the Great Sphinx ... interested in the problem of the age of the Sphinx")]),

    # --- DCA-000026 Churchward (en, Mu) ---
    ("DCA-000026", "Churchward, James",
     "Existen dos conjuntos de tablillas antiguas (las tablillas Naacal) —una colección de más de 2500 tablillas de piedra— escritas por los Naacal, que salieron de Birmania hace más de 15.000 años.",
     "Afirmación de Churchward sobre las tablillas Naacal y su antigüedad; registrada como afirmación del autor.",
     "EMPIRICAL", "OBSERVACIONAL", "Tablillas Naacal",
     "hace más de 15.000 años", None,
     "Traducciones de dos conjuntos de tablillas antiguas.",
     "FAVORABLE", "A03", False,
     [(144, 161, "translations of two sets of ancient tablets. Naacal tablets ... over 2500 ... the Naacals left Burma more than 15,000 years ago")]),

    # --- DCA-000027 Oppenheimer (Eden in the East) ---
    ("DCA-000027", "Oppenheimer, Stephen",
     "Sundaland, un continente hoy sumergido en el Sudeste Asiático, fue inundado por una serie de inundaciones al final de la última glaciación, dispersando poblaciones y mitos.",
     "Afirmación de Oppenheimer sobre la inundación de Sundaland y sus consecuencias; registrada como afirmación del autor.",
     "CAUSAL", "CAUSAL", "Sundaland (continente sumergido)",
     "final de la última glaciación", "inundación por subida del nivel del mar",
     "Evidencia del registro de inundaciones (Older/Younger Dryas, Mar Negro).",
     "FAVORABLE", "A12", False,
     [(27, 40, "flood at the end of the last ice age ... The Drowned Continent")]),
]

# Contra-pares de contraste enlazados (relaciones entre afirmaciones del lote activo)
# Se añade una relación SUPPORTS dentro de cada par que comparte work_id de la misma obra,
# y un puente hacia el piloto G4 para los pares Esfinge (ya cubiertos).
WORK_PAIRS = {("DCA-000003", "DCA-000009"), ("DCA-000010", "DCA-000026"), ("DCA-000006", "DCA-000007")}


def main() -> int:
    manifest = load_manifest()
    pagemaps = {sid: load_pagemap(sid) for sid in manifest}
    records = []
    for i, c in enumerate(CLAIMS, 1):
        sid, claimant, claim, para, ctype, cat, obj, date, mech, evid, stance, theory, ocr, passages = c
        rec = {
            "schema_version": "2.0",
            "claim_id": f"CLM-{i:06d}",
            "attributed_claim": claim,
            "controlled_paraphrase": para,
            "claimant": claimant,
            "source_id": sid,
            "matrix_id": theory,
            "passages": [],
            "claim_type": ctype,
            "category": cat,
            "object": obj,
            "asserted_date": date,
            "mechanism": mech,
            "invoked_evidence": evid,
            "stance": stance,
            "theory_ids": [theory] if theory else [],
            "project_assessment": {
                "status": "NO_EVALUADA",
                "reasoning": "Afirmación registrada del autor; no se evalúa en la extracción.",
                "missing_to_test": "Fuente/edición completa, datos primarios y contexto.",
                "confidence": "NOT_APPLICABLE",
                "ocr_warning": ocr,
            },
            "relations": [],
            "extraction_status": "DRAFT",
            "extractor": "arena-extraccion-masiva-v1",
            "reviewer": None,
            "created_utc": now,
        }
        first = None
        for (ls, le, quote) in passages:
            page = page_for_line(pagemaps[sid], ls)
            rec["passages"].append({
                "passage_id": f"PAS-{sid}-L{ls:07d}-L{le:07d}",
                "source_id": sid,
                "source_sha256": manifest[sid]["fixity"]["original_sha256"],
                "hash_ref": "original",
                "line_start": ls,
                "line_end": le,
                "page_start": page,
                "page_end": page,
                "quotation": quote,
                "quotation_sha256": qsha(quote),
            })
            first = f"PAS-{sid}-L{ls:07d}-L{le:07d}"
        records.append(rec)

    # Enlazar relaciones de work_id entre manifestaciones de la misma obra
    # (los claim_id se asignan por orden de la lista; reconstruimos mapa fuente->claim)
    from collections import defaultdict
    by_src = defaultdict(list)
    for r in records:
        by_src[r["source_id"]].append(r["claim_id"])
    for r in records:
        r["relations"] = []
        for other in WORK_PAIRS:
            a, b = other
            if a == r["source_id"]:
                tgt = by_src.get(b, [None])[0]
                if tgt:
                    r["relations"].append({
                        "relation_type": "CONTEXTUALIZA", "relation_semantic": "SUPPORTS",
                        "target_id": tgt, "note": f"misma obra (manifestación {b})"})
            elif b == r["source_id"]:
                tgt = by_src.get(a, [None])[0]
                if tgt:
                    r["relations"].append({
                        "relation_type": "CONTEXTUALIZA", "relation_semantic": "SUPPORTS",
                        "target_id": tgt, "note": f"misma obra (manifestación {a})"})

    with OUT.open("w", encoding="utf-8", newline="\n") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")

    # validar
    import jsonschema
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    fails = 0
    for r in records:
        errs = sorted(validator.iter_errors(r), key=lambda e: list(e.path))
        if errs:
            fails += 1
            print(f"[FAIL] {r['claim_id']} ({r['source_id']})")
            for e in errs:
                print("   ", "/".join(map(str, e.path)) or "<raíz>", "->", e.message)
    print(f"Afirmaciones: {len(records)}")
    print(f"Válidas: {len(records)-fails}/{len(records)} contra claim_record.schema.json v2.0")
    print(f"Archivo: {OUT}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
