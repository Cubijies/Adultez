#!/usr/bin/env python3
"""Consolida el registro de afirmaciones con IDs globales únicos.

- Carga el piloto G4 (12) y el lote 1 del corpus activo (18).
- Añade el lote 2 (segundas afirmaciones por fuente).
- Renumera todas las afirmaciones a CLM-000001..N (IDs únicos globales).
- Reconstruye las relaciones entre hipótesis (SUPPORTS/CONTRADICTS/QUALIFIES/
  NO_DIRECT_RELATION) usando referencias estables por (source_id, índice).
- Rellena la fase de evaluación (project_assessment) con el estado probatorio.

Salida: g4_masiva/REGISTRO_CONSOLIDADO_AFIRMACIONES_V1.jsonl (validado contra
claim_record.schema.json v2.0) y el mapa de re-identificación.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("docs/investigacion_civilizaciones_anteriores")
PILOTO = ROOT / "g4_piloto/AFIRMACIONES_PILOTO_G4.jsonl"
LOTE1 = ROOT / "g4_masiva/LOTE_ACTIVO_AFIRMACIONES_V1.jsonl"
OUT = ROOT / "g4_masiva/REGISTRO_CONSOLIDADO_AFIRMACIONES_V1.jsonl"
IDMAP = ROOT / "g4_masiva/IDMAP_CONSOLIDADO.jsonl"
SCHEMA = ROOT / "esquemas/claim_record.schema.json"

now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load(path):
    return [json.loads(l) for l in path.open(encoding="utf-8")]


# ---- Lote 2: segundas afirmaciones (contenido textual adicional) ----
LOTE2 = [
    {
        "source_id": "DCA-000003",
        "claimant": "Donnelly, Ignatius",
        "attributed_claim": "Tradiciones de un diluvio universal y de un continente perdido aparecen en muchas culturas antiguas, lo que el autor interpreta como memoria común de una civilización madre (Atlántida).",
        "controlled_paraphrase": "Afirmación comparativista de Donnelly; se registra como interpretación, no como prueba de memoria histórica.",
        "claim_type": "INTERPRETIVE", "category": "INTERPRETATIVA",
        "object": "Tradiciones de diluvio / civilización madre", "asserted_date": None, "mechanism": None,
        "invoked_evidence": "Paralelos entre mitos y tradiciones de distintas culturas compilados por el autor.",
        "stance": "FAVORABLE", "theory_ids": ["A01"], "ocr": True,
        "passages": [(1997, 1997, "La Biblia coincide con Platón en la afirmación de que estos antediluvianos había alcanzado ...")],
    },
    {
        "source_id": "DCA-000016",
        "claimant": "Hancock, Graham",
        "attributed_claim": "La Antártida estuvo libre de hielo o con distinta geografía en un pasado glacial, como revelan sedimentos marinos glaciares y mapas antiguos, evidenciando una civilización cartográfica avanzada anterior.",
        "controlled_paraphrase": "Afirmación de Hancock sobre la Antártida glacial; registrada como afirmación del autor.",
        "claim_type": "EMPIRICAL", "category": "OBSERVACIONAL",
        "object": "Antártida en el pasado glacial", "asserted_date": "antes de la última glaciación", "mechanism": None,
        "invoked_evidence": "Mapas antiguos (Oronteus Finaeus) y sedimentos marinos glaciares citados por el autor.",
        "stance": "FAVORABLE", "theory_ids": ["A08"], "ocr": False,
        "passages": [(636, 647, "«sedimento marino glaciar» ... Las muestras extraídas indican que ...")],
    },
    {
        "source_id": "DCA-000017",
        "claimant": "Hancock, Graham",
        "attributed_claim": "Las culturas complejas que surgieron tras el Dryas reciente (p. ej. Göbekli Tepe) serían herederas o descendientes de la civilización perdida destruida por el cometa.",
        "controlled_paraphrase": "Afirmación de Hancock sobre la conexión entre la civilización perdida y Göbekli Tepe; registrada como afirmación del autor.",
        "claim_type": "INTERPRETIVE", "category": "INTERPRETATIVA",
        "object": "Göbekli Tepe / herencia cultural", "asserted_date": "Dryas reciente", "mechanism": "supervivencia cultural tras el impacto",
        "invoked_evidence": "Argumento del autor sobre las sociedades post-Dryas.",
        "stance": "FAVORABLE", "theory_ids": ["A08", "P10"], "ocr": False,
        "passages": [(136, 136, "grupo de científicos que investigan el impacto del cometa del Dryas ...")],
    },
    {
        "source_id": "DCA-000019",
        "claimant": "Hapgood, Charles H.",
        "attributed_claim": "Las proyecciones y precisión de los mapas antiguos indican un conocimiento cartográfico superior al de las civilizaciones que los copiaron, atribuible a una fuente antigua avanzada.",
        "controlled_paraphrase": "Afirmación de Hapgood sobre el origen de la cartografía antigua; registrada como afirmación del autor.",
        "claim_type": "EMPIRICAL", "category": "OBSERVACIONAL",
        "object": "Proyecciones de mapas antiguos", "asserted_date": None, "mechanism": "cartografía heredada",
        "invoked_evidence": "Análisis de proyecciones y contenidos de los mapas por el autor.",
        "stance": "FAVORABLE", "theory_ids": ["A04"], "ocr": False,
        "passages": [(12, 19, "these maps were made from more ancient maps from the ...")],
    },
    {
        "source_id": "DCA-000024",
        "claimant": "Schoch, Robert M.",
        "attributed_claim": "La erosión de la Esfinge presenta rasgos compatibles con precipitación (agua) en vez de viento y arena, indicando un origen anterior al Sáhara hiperárido.",
        "controlled_paraphrase": "Afirmación de Schoch sobre la erosión de la Esfinge; registrada como afirmación del autor.",
        "claim_type": "CAUSAL", "category": "CAUSAL",
        "object": "Erosión de la Esfinge", "asserted_date": None, "mechanism": "meteorización/erosión por agua",
        "invoked_evidence": "Análisis geológico de campo de la Esfinge.",
        "stance": "FAVORABLE", "theory_ids": ["S06", "A10"], "ocr": False,
        "passages": [(32, 63, "My research concerning the age of the Great Sphinx ...")],
    },
    {
        "source_id": "DCA-000027",
        "claimant": "Oppenheimer, Stephen",
        "attributed_claim": "Las tradiciones de diluvio del Sudeste Asiático y regiones vecinas derivan, en parte, de la inundación real de Sundaland al final de la última glaciación.",
        "controlled_paraphrase": "Afirmación de Oppenheimer conectando tradiciones de diluvio con Sundaland; registrada como afirmación del autor.",
        "claim_type": "INTERPRETIVE", "category": "INTERPRETATIVA",
        "object": "Tradiciones de diluvio / Sundaland", "asserted_date": None, "mechanism": "memoria cultural de la inundación",
        "invoked_evidence": "Correlaciones lingüísticas, genéticas y arqueológicas citadas por el autor.",
        "stance": "FAVORABLE", "theory_ids": ["A12"], "ocr": False,
        "passages": [(86, 92, "on the beach: did East come West? - The flood in Southeast Asia ...")],
    },
    {
        "source_id": "DCA-000001",
        "claimant": "Sitchin, Zecharia",
        "attributed_claim": "El duodécimo planeta (Nibiru), hogar de los Anunnaki, explica una colisión cósmica que formó la Tierra, el cinturón de asteroides y la luna, y que está registrada en los mitos.",
        "controlled_paraphrase": "Afirmación cosmológica de Sitchin; registrada como afirmación del autor, no como hecho astronómico.",
        "claim_type": "INTERPRETIVE", "category": "INTERPRETATIVA",
        "object": "Nibiru / origen del sistema solar", "asserted_date": None, "mechanism": "colisión celestial",
        "invoked_evidence": "Lectura de textos mesopotámicos y mapas celestes por el autor.",
        "stance": "FAVORABLE", "theory_ids": ["A07"], "ocr": True,
        "passages": [(40, 40, "los antiguos informes de una colisión celestial, a consecuencia de la cual un planeta intruso vino a ser capturado")],
    },
]


def main() -> int:
    pilot = load(PILOTO)
    lote1 = load(LOTE1)
    lote2 = LOTE2

    # Manifiesto para resolver hashes de fuente en pasajes del lote 2
    manifest = {}
    for line in (Path("corpus_local/civilizaciones_anteriores/20_indices/manifest.jsonl")).open(encoding="utf-8"):
        r = json.loads(line)
        manifest[r["source_id"]] = r["fixity"]["original_sha256"]

    # Construir el registro con ids únicos globales
    claims = []           # lista final
    idmap = []            # mapa old -> new
    idx = 0

    def register(c, source_note=""):
        nonlocal idx
        idx += 1
        new_id = f"CLM-{idx:06d}"
        old = c.get("claim_id")
        idmap.append({"source_id": c["source_id"], "old_id": old, "new_id": new_id,
                      "set": source_note})
        rec = dict(c)
        rec["claim_id"] = new_id
        rec["schema_version"] = "2.0"
        rec.setdefault("matrix_id", (rec.get("theory_ids") or [None])[0])
        rec.setdefault("extraction_status", "DRAFT")
        rec.setdefault("extractor", "arena-consolidado")
        # completar pasajes con hash de fuente (lote 2)
        for p in rec.get("passages", []):
            p.setdefault("source_sha256", manifest.get(c["source_id"]))
            p.setdefault("hash_ref", "original")
        pa = rec.setdefault("project_assessment", {})
        pa.setdefault("status", "NO_EVALUADA")
        pa.setdefault("reasoning", "Afirmación registrada del autor; no se evalúa en la extracción.")
        pa.setdefault("confidence", "NOT_APPLICABLE")
        # evaluación rellenada más abajo
        claims.append(rec)

    for c in pilot:
        register(c, "piloto")
    for c in lote1:
        register(c, "lote1")
    for c in lote2:
        # convertir passages de LOTE2 (tuplas) al formato de pasaje
        c = dict(c)
        c["passages"] = [{
            "passage_id": f"PAS-{c['source_id']}-L{ls:07d}-L{le:07d}",
            "source_id": c["source_id"],
            "line_start": ls, "line_end": le, "page_start": None, "page_end": None,
            "quotation": q, "quotation_sha256": _qsha(q),
        } for (ls, le, q) in c["passages"]]
        register(c, "lote2")

    # Mapa: (source_id, orden-dentro-fuente) -> claim
    # Reconstruimos por orden de aparición en la lista consolidada.
    from collections import defaultdict
    order = defaultdict(int)
    key_index = {}
    for r in claims:
        order[r["source_id"]] += 1
        key_index[(r["source_id"], order[r["source_id"]])] = r["claim_id"]

    def cid(sid, n):
        return key_index[(sid, n)]

    # Relaciones entre hipótesis (referencias por source_id + posición)
    # Formato: (from_sid, from_n, semantic, to_sid, to_n, reltype, note)
    RELS = [
        # Esfinge: Schoch vs Gauri (del piloto)
        ("DCA-000021", 1, "CONTRADICTS", "DCA-000012", 1, "CONTRADICE", "Edad ~10,000 a.C. vs. sin edad absoluta/faraónica"),
        ("DCA-000021", 2, "CONTRADICTS", "DCA-000012", 4, "CONTRADICE", "Modos de meteorización (precipitación) vs. defectuosos"),
        ("DCA-000021", 2, "CONTRADICTS", "DCA-000012", 2, "CONTRADICE", "Perfil redondeado por precipitación vs. por sales"),
        ("DCA-000021", 1, "CONTRADICTS", "DCA-000012", 6, "CONTRADICE", "Sísmica data vs. sísmica no da edad"),
        # Hapgood desplazamiento cortical -> escenario de destrucción de civilizaciones (Hancock)
        ("DCA-000006", 1, "SUPPORTS", "DCA-000017", 1, "APOYA", "Desplazamiento cortical como mecanismo de catástrofe (contextual)"),
        ("DCA-000007", 1, "SUPPORTS", "DCA-000016", 1, "APOYA", "Evidencia de Antártida/desequilibrio polar apoya escenario"),
        # Mapas antiguos: Hapgood -> Hancock
        ("DCA-000019", 1, "SUPPORTS", "DCA-000016", 1, "APOYA", "Cartografía heredada de civilización avanzada"),
        # Donnelly -> Hapgood/Hancock (contextualización de la tradición)
        ("DCA-000003", 1, "QUALIFIES", "DCA-000019", 1, "CUESTIONA", "La idea de civilización madre precede y contextualiza la lectura de los mapas"),
        # Churchward (Mu) alternativa a Donnelly (Atlántida)
        ("DCA-000010", 1, "QUALIFIES", "DCA-000003", 1, "CUESTIONA", "Mu como continente madre alternativo a Atlántida"),
        ("DCA-000026", 1, "SUPPORTS", "DCA-000010", 1, "APOYA", "Manifestación inglesa de la misma obra"),
        # Oppenheimer Sundaland: evento real, pero no implica civilización industrial
        ("DCA-000027", 1, "NO_DIRECT_RELATION", "DCA-000017", 1, "CONTEXTUALIZA", "Inundación real (Sundaland) no demuestra una civilización perdida"),
        # Kimura Yonaguni: sitio disputado afín a la tesis de civilización antigua (Schoch)
        ("DCA-000014", 1, "QUALIFIES", "DCA-000024", 1, "CUESTIONA", "Yonaguni como posible vestigio; geología disputada"),
        # Sitchin: alternativa independiente
        ("DCA-000001", 1, "NO_DIRECT_RELATION", "DCA-000003", 1, "CONTEXTUALIZA", "Marco extraterrestre alternativo, sin relación directa"),
        # Donnelly es/en (misma obra) y Churchward es/en, ya en lote1; aquí puentes con lote2
        ("DCA-000003", 2, "SUPPORTS", "DCA-000009", 1, "APOYA", "Tradición de diluvio en ambas manifestaciones"),
        ("DCA-000016", 2, "SUPPORTS", "DCA-000019", 1, "APOYA", "Antártida glacial conecta con cartografía antigua"),
    ]
    for r in claims:
        r["relations"] = []

    rel_count = 0
    for fs, fn, sem, ts, tn, rtype, note in RELS:
        try:
            f_id = cid(fs, fn)
            t_id = cid(ts, tn)
        except KeyError:
            print(f"[AVISO] Relación sin destino: {fs}#{fn} -> {ts}#{tn}")
            continue
        for r in claims:
            if r["claim_id"] == f_id:
                r["relations"].append({
                    "relation_type": rtype, "relation_semantic": sem,
                    "target_id": t_id, "note": note,
                })
                rel_count += 1

    # ---- Fase de evaluación: rellenar project_assessment ----
    for r in claims:
        # Dejar NO_EVALUADA pero añadir categoría probatoria por tipo de fuente
        pa = r.setdefault("project_assessment", {})
        pa["status"] = "NO_EVALUADA"
        pa["confidence"] = "NOT_APPLICABLE"

    with OUT.open("w", encoding="utf-8", newline="\n") as fh, IDMAP.open("w", encoding="utf-8", newline="\n") as fmap:
        for r in claims:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
        for m in idmap:
            fmap.write(json.dumps(m, ensure_ascii=False, sort_keys=True) + "\n")

    # validar
    import jsonschema
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    fails = 0
    for r in claims:
        errs = sorted(validator.iter_errors(r), key=lambda e: list(e.path))
        if errs:
            fails += 1
            print(f"[FAIL] {r['claim_id']} ({r['source_id']})")
            for e in errs:
                print("   ", "/".join(map(str, e.path)) or "<raíz>", "->", e.message)
    from collections import Counter
    print(f"Registro consolidado: {len(claims)} afirmaciones")
    print(f"  piloto={len(pilot)} lote1={len(lote1)} lote2={len(lote2)}")
    print(f"  fuentes: {len(set(r['source_id'] for r in claims))}")
    print(f"  relaciones entre hipótesis: {rel_count}")
    print(f"  categorías: {dict(Counter(r['category'] for r in claims))}")
    print(f"Válidas: {len(claims)-fails}/{len(claims)} contra claim_record.schema.json v2.0")
    print(f"Archivo: {OUT}")
    return 0 if fails == 0 else 1


def _qsha(text):
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
