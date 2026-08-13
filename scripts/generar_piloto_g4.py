#!/usr/bin/env python3
"""Genera y valida el piloto G4 de extracción de afirmaciones (Esfinge).

Piloto adversarial de dos fuentes:
  - DCA-000021 Schoch & Bauval, Origins of the Sphinx (2017)
  - DCA-000012 Gauri, Sinai & Bandyopadhyay, Geoarchaeology 10 (1995)

Límites: máx. 12 afirmaciones atómicas; sólo pasajes estrictamente necesarios;
referencia exacta a source_id, passage_id, páginas, líneas y hashes; cita separada
de afirmación, evidencia e interpretación; relaciones SUPPORTS/CONTRADICTS/
QUALIFIES/NO_DIRECT_RELATION; validación contra claim_record.schema.json.

Salida: JSONL de afirmaciones + resumen de validación (stdout).
"""
from __future__ import annotations
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_PATH = Path("docs/investigacion_civilizaciones_anteriores/esquemas/claim_record.schema.json")
OUT_PATH = Path("docs/investigacion_civilizaciones_anteriores/g4_piloto/AFIRMACIONES_PILOTO_G4.jsonl")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# source identity: original_sha256 (canonical)
SOURCE_SHA = {
    "DCA-000012": "e8031bd487a62c7ded96b1b0ccefac67c1a149b8693e8b9b3e8e56cd306df79a",
    "DCA-000021": "0054a66c67927ccc5f3b35e34d7af6483e3bf4f685f8e5985a5b8b8803b55ad4",
}

now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def qsha(text: str | None) -> str | None:
    return hashlib.sha256(text.encode("utf-8")).hexdigest() if text else None


def passage(sid: str, lstart: int, lend: int, pstart, pend, quotation: str | None):
    return {
        "passage_id": f"PAS-{sid}-L{lstart:07d}-L{lend:07d}",
        "source_id": sid,
        "source_sha256": SOURCE_SHA[sid],
        "hash_ref": "original",
        "line_start": lstart,
        "line_end": lend,
        "page_start": pstart,
        "page_end": pend,
        "quotation": quotation,
        "quotation_sha256": qsha(quotation),
    }


def rel(relation_type: str, target_id: str, semantic: str, note: str | None = None):
    # relation_type = valor válido del esquema; relation_semantic = taxonomía del piloto
    return {
        "relation_type": relation_type,
        "target_id": target_id,
        "relation_semantic": semantic,
        "note": note,
    }


CLAIMS = [
    # ============ DCA-000021  Schoch & Bauval, Origins of the Sphinx ============
    {
        "claim_id": "CLM-000001",
        "attributed_claim": "A partir de la profundidad de la meteorización subsuperficial del suelo de la Esfinge, el núcleo original (core body) fue tallado mucho antes del Reino Antiguo: los datos sísmicos son compatibles con una fecha inicial de circa 10,000 a.C. (o algo antes), es decir, miles de años antes de la atribución estándar de circa 2500 a.C.",
        "controlled_paraphrase": "Afirmación cronológica atribuida a Schoch; no es conclusión del proyecto.",
        "claimant": "Schoch, Robert M.; Bauval, Robert",
        "source_id": "DCA-000021",
        "passages": [
            passage("DCA-000021", 1639, 1675, "68", "69",
                "Using the depth of subsurface weathering, we can calculate when the original floor of the Sphinx Enclosure was exposed, and thus date the original carving of the core body ... the seismic data are compatible with an initial date of circa 10,000 BCE (or even a bit earlier) for the core body of the Sphinx."),
        ],
        "claim_type": "CHRONOLOGICAL",
        "category": "CRONOLOGICA",
        "object": "Gran Esfinge de Guiza (core body)",
        "asserted_date": "circa 10,000 BCE (core body)",
        "mechanism": "datación por profundidad de meteorización subsuperficial (sísmica)",
        "invoked_evidence": "Perfiles sísmicos (Dobecki & Schoch 1992) de profundidad de meteorización del suelo del recinto de la Esfinge.",
        "stance": "FAVORABLE",
        "theory_ids": ["S06", "A10"],
        "project_assessment": {
            "status": "NO_EVALUADA",
            "reasoning": "Registro de la afirmación del autor con su evidencia invocada; se requiere evaluar los datos sísmicos primarios, la calibración lineal/no lineal y la asociación muestra-construcción.",
            "missing_to_test": "Datos sísmicos crudos (Dobecki & Schoch 1992), litología exacta, modelos de tasa de meteorización subsuperficial y controles independientes.",
            "confidence": "NOT_APPLICABLE",
            "falsification_potential": "Si la profundidad de meteorización responde a litología/diagénesis y no al tiempo de exposición, la datación pierde sustento; o si un método independiente (p. ej. exposición cosmogénica) arrojara edad dinástica.",
        },
        "relations": [
            rel("CONTRADICE", "CLM-000007", "CONTRADICTS", "Fecha antigua vs. 'edad faraónica'."),
            rel("CONTRADICE", "CLM-000012", "CONTRADICTS", "Sísmica como evidencia de edad vs. 'la sísmica sola no da edad'."),
        ],
        "extraction_status": "DRAFT",
        "extractor": "arena-piloto-g4",
        "reviewer": None,
        "created_utc": now,
    },
    {
        "claim_id": "CLM-000002",
        "attributed_claim": "Existen dos modos de meteorización/erosión en la meseta de Guiza: la eólica por arena (perfil angular) y la inducida por precipitación (perfil ondulado y 'rolling'); la Esfinge conserva meteorización por precipitación que requiere exposición prolongada a lluvia, incompatible con el Sáhara híper-árido actual.",
        "controlled_paraphrase": "Afirmación causal/observacional atribuida a Schoch; describe su clasificación de los dos modos de meteorización.",
        "claimant": "Schoch, Robert M.; Bauval, Robert",
        "source_id": "DCA-000021",
        "passages": [
            passage("DCA-000021", 5216, 5244, "214", "215",
                "Wind-driven sand abrades and scours the stone surfaces ... will generally produce an angular profile ... Such precipitation-induced weathering and erosion typically creates a rolling and undulating surface profile ... the Sphinx shows evidence of wind weathering as well ... These wind-induced features are evident."),
        ],
        "claim_type": "CAUSAL",
        "category": "CAUSAL",
        "object": "Meteorización/erosión de la Esfinge y la meseta de Guiza",
        "asserted_date": None,
        "mechanism": "distinción entre meteorización eólica (viento+arena) y por precipitación (lluvia/escorrentía)",
        "invoked_evidence": "Observación de perfiles 'angular' vs 'rolling/ondulado' en monumentos y paredes del recinto.",
        "stance": "FAVORABLE",
        "theory_ids": ["S06", "A10"],
        "project_assessment": {
            "status": "NO_EVALUADA",
            "reasoning": "Clasificación del autor sobre los dos modos; se discute en la literatura (Gauri et al. 1995) si estos términos son válidos.",
            "missing_to_test": "Mapeo litológico 3D, cuantificación de perfiles, controles de campo y comparación ciega con canteras fechadas.",
            "confidence": "NOT_APPLICABLE",
            "falsification_potential": "Si la forma 'rolling' puede producirse por meteorización salina en clima árido (hipótesis de Gauri), la atribución a precipitación antigua se debilita.",
        },
        "relations": [
            rel("CUESTIONA", "CLM-000010", "CONTRADICTS", "Schoch sostiene la distinción; Gauri la considera 'fundamentalmente defectuosa'."),
        ],
        "extraction_status": "DRAFT",
        "extractor": "arena-piloto-g4",
        "reviewer": None,
        "created_utc": now,
    },
    {
        "claim_id": "CLM-000003",
        "attributed_claim": "La cabeza actual de la Esfinge es una recarve dinástico (recarving) de una cabeza original más grande; su tamaño desproporcionado indica que los egipcios del Reino Antiguo reutilizaron, restauraron y re-trabajaron un monumento mucho más antiguo (originalmente quizá un león recumbente), y que la cabeza no demuestra que la Esfinge fuera tallada por primera vez en época dinástica.",
        "controlled_paraphrase": "Afirmación interpretativa atribuida a Schoch sobre el recarve y la reutilización del monumento.",
        "claimant": "Schoch, Robert M.",
        "source_id": "DCA-000021",
        "passages": [
            passage("DCA-000021", 4544, 4557, "178", "178",
                "There is strong, and in my assessment compelling, evidence that the Old Kingdom Egyptians did not create the statue de novo, but reused, restored, and reworked a preexisting, and much older, monument ... the head does not demonstrate that it was the dynastic-period Egyptians who first carved the original structure."),
        ],
        "claim_type": "INTERPRETIVE",
        "category": "INTERPRETATIVA",
        "object": "Cabeza y núcleo original de la Gran Esfinge",
        "asserted_date": None,
        "mechanism": "reutilización/recarve dinástico de un monumento preexistente",
        "invoked_evidence": "Anomalía de tamaño proporcional de la cabeza; comparaciones con monumentos reutilizados.",
        "stance": "FAVORABLE",
        "theory_ids": ["S06", "A10"],
        "project_assessment": {
            "status": "NO_EVALUADA",
            "reasoning": "Interpretación del autor sobre el recarve; no se evalúa aquí.",
            "missing_to_test": "Estudios de cantería, análisis de la cabeza original, comparaciones de estilo y evidencia de re-trabajo.",
            "confidence": "NOT_APPLICABLE",
            "falsification_potential": "Si se demostrara que la cabeza original era ya de proporciones similares o que no hubo reutilización, la inferencia se debilita.",
        },
        "relations": [
            rel("CUESTIONA", "CLM-000007", "CONTRADICTS", "Reutilización pre-faraónica vs. creación faraónica (Kephren)."),
        ],
        "extraction_status": "DRAFT",
        "extractor": "arena-piloto-g4",
        "reviewer": None,
        "created_utc": now,
    },
    {
        "claim_id": "CLM-000004",
        "attributed_claim": "El proto-Sphinx ya existía antes del final de la última glaciación (antes de 9700 a.C.) y fue contemporáneo de otras estructuras tempranas como las porciones más antiguas de Göbekli Tepe (circa 10,000 a.C.).",
        "controlled_paraphrase": "Afirmación cronológica atribuida a Schoch; vincula la Esfinge con el límite del Holoceno.",
        "claimant": "Schoch, Robert M.",
        "source_id": "DCA-000021",
        "passages": [
            passage("DCA-000021", 1670, 1674, "69", "69",
                "I suspect that the proto-Sphinx was in existence prior to the end of the last ice age (that is, prior to 9700 BCE) and was contemporaneous with other structures, such as the oldest portions of Göbekli Tepe in southeastern Turkey."),
        ],
        "claim_type": "CHRONOLOGICAL",
        "category": "CRONOLOGICA",
        "object": "Proto-Sphinx",
        "asserted_date": "antes de 9700 BCE; contemporáneo de Göbekli Tepe",
        "mechanism": "inferencia cronológica a partir de la datación sísmica del core body",
        "invoked_evidence": "Datos sísmicos del recinto (Schoch 2012; Dobecki & Schoch 1992).",
        "stance": "FAVORABLE",
        "theory_ids": ["S06", "A10"],
        "project_assessment": {
            "status": "NO_EVALUADA",
            "reasoning": "Afirmación del autor; depende de CLM-000001.",
            "missing_to_test": "Datación independiente y estratigrafía; evaluación de la sincronía con Göbekli Tepe.",
            "confidence": "NOT_APPLICABLE",
            "falsification_potential": "Si CLM-000001 se refuta o si la correlación con Göbekli Tepe no se sostiene, esta afirmación se debilita.",
        },
        "relations": [
            rel("DEPENDE_DE", "CLM-000001", "SUPPORTS", "Deriva de la datación del core body."),
            rel("CUESTIONA", "CLM-000007", "CONTRADICTS", "Edad pleistocénica vs. edad faraónica."),
        ],
        "extraction_status": "DRAFT",
        "extractor": "arena-piloto-g4",
        "reviewer": None,
        "created_utc": now,
    },
    {
        "claim_id": "CLM-000005",
        "attributed_claim": "Las objeciones críticas de que (a) la roca del extremo oeste del recinto es más dura y resistente, o (b) los perfiles sísmicos sólo mapean estratos buzantes al sureste y no una capa de meteorización, son incorrectas según Dobecki & Schoch (1992).",
        "controlled_paraphrase": "Réplica empírica/observacional atribuida a Schoch contra críticos; se registra la afirmación, no su veracidad.",
        "claimant": "Schoch, Robert M.",
        "source_id": "DCA-000021",
        "passages": [
            passage("DCA-000021", 1678, 1690, "69", "69",
                "Some of my critics have asserted that the rock under the floor of the Sphinx Enclosure is harder ... Other critics have asserted that the seismic profiles are simply mapping southeastern-dipping strata ... both of these assertions are incorrect. ... Dobecki and I addressed this directly in our original 1992 paper."),
        ],
        "claim_type": "EMPIRICAL",
        "category": "OBSERVACIONAL",
        "object": "Interpretación de los perfiles sísmicos del recinto",
        "asserted_date": None,
        "mechanism": None,
        "invoked_evidence": "Dobecki & Schoch (1992), velocidades sísmicas de la línea S3 y otras líneas.",
        "stance": "FAVORABLE",
        "theory_ids": ["S06", "A10"],
        "project_assessment": {
            "status": "NO_EVALUADA",
            "reasoning": "Contra-objeción del autor; requiere los datos sísmicos primarios y la evaluación independiente (p. ej. Harrell 1994).",
            "missing_to_test": "Datos sísmicos crudos, litología de testigos y réplica independiente.",
            "confidence": "NOT_APPLICABLE",
            "falsification_potential": "Si se demuestra heterogeneidad litológica o buzamiento que explique la diferencia de profundidad, la interpretación como meteorización temporal se debilita.",
        },
        "relations": [
            rel("CUESTIONA", "CLM-000012", "NO_DIRECT_RELATION", "Ambas discuten la sísmica; la contra-objeción de Schoch y el límite señalado por Gauri se relacionan de forma indirecta."),
        ],
        "extraction_status": "DRAFT",
        "extractor": "arena-piloto-g4",
        "reviewer": None,
        "created_utc": now,
    },
    {
        "claim_id": "CLM-000006",
        "attributed_claim": "La atribución de la Gran Esfinge a la Cuarta Dinastía (Khafre/Kephren o Khufu) se basa sólo en 'contexto' (yacer dentro de la necrópolis del Reino Antiguo) y es circunstancial, no demostrativa.",
        "controlled_paraphrase": "Afirmación interpretativa/metodológica de Schoch sobre la lógica de datación por contexto.",
        "claimant": "Schoch, Robert M.",
        "source_id": "DCA-000021",
        "passages": [
            passage("DCA-000021", 4520, 4539, "177", "177",
                "the dating of the Great Sphinx to the Fourth Dynasty ... is entirely circumstantial ... their field relies heavily on 'context' ... I find this line of thinking rather weak, to put it mildly."),
        ],
        "claim_type": "INTERPRETIVE",
        "category": "INTERPRETATIVA",
        "object": "Criterio arqueológico de datación de la Esfinge",
        "asserted_date": None,
        "mechanism": None,
        "invoked_evidence": "Lógica de 'contexto' usada por la egiptología; analogía de la Hagia Sophia.",
        "stance": "FAVORABLE",
        "theory_ids": ["S06", "A10"],
        "project_assessment": {
            "status": "NO_EVALUADA",
            "reasoning": "Crítica metodológica del autor; se registra como interpretación.",
            "missing_to_test": "Evidencia contextual arqueológica completa del complejo de Khafra.",
            "confidence": "NOT_APPLICABLE",
            "falsification_potential": "Si el contexto arqueológico (templos, estelas, estatuas) fuera demostrativo de construcción por Khafra, la crítica pierde fuerza.",
        },
        "relations": [
            rel("CUESTIONA", "CLM-000007", "CONTRADICTS", "Debilita la base 'faraónica'; Gauri mantiene la edad faraónica."),
        ],
        "extraction_status": "DRAFT",
        "extractor": "arena-piloto-g4",
        "reviewer": None,
        "created_utc": now,
    },
    # ============ DCA-000012  Gauri, Sinai & Bandyopadhyay (1995) ============
    {
        "claim_id": "CLM-000007",
        "attributed_claim": "No puede asignarse una edad absoluta a la Esfinge a partir de la evidencia geológica existente; mientras no haya más evidencia, la Esfinge debe seguir considerándose de origen faraónico (tallada por Kephren, hace ~4500 años).",
        "controlled_paraphrase": "Afirmación cronológica de Gauri et al.; postura opuesta a Schoch.",
        "claimant": "Gauri, K. Lal; Sinai, John J.; Bandyopadhyay, Jayanta K.",
        "source_id": "DCA-000012",
        "passages": [
            passage("DCA-000012", 100, 104, "3", "3",
                "In our view they have erred in their interpretation of these features. We believe that an absolute age cannot be assigned to the Sphinx on the basis of existing geologic evidence."),
            passage("DCA-000012", 519, 531, "14", "14",
                "We have shown that they have misinterpreted the geomorphologic features ... their only remaining argument, based on seismic data, does not provide a clue to the age of the Sphinx by itself. Therefore, the Sphinx should continue to be regarded as of pharaonic age until further evidence is forthcoming."),
        ],
        "claim_type": "CHRONOLOGICAL",
        "category": "CRONOLOGICA",
        "object": "Gran Esfinge de Guiza",
        "asserted_date": "~4500 años (faraónica); sin edad absoluta demostrada",
        "mechanism": None,
        "invoked_evidence": "Crítica de las interpretaciones geomorfológicas de Schoch & West; contexto faraónico.",
        "stance": "CRITICA",
        "theory_ids": ["S06", "A10"],
        "project_assessment": {
            "status": "NO_EVALUADA",
            "reasoning": "Postura de Gauri et al.; se registra como contra-afirmación sin concluir.",
            "missing_to_test": "Método de datación absoluta fiable asociado a la construcción; datos de campo independientes.",
            "confidence": "NOT_APPLICABLE",
            "falsification_potential": "Si se consiguiera una datación absoluta robusta de la talla original (no de muestras sueltas), se podría decidir.",
        },
        "relations": [
            rel("CONTRADICE", "CLM-000001", "CONTRADICTS", "Edad faraónica vs. circa 10,000 a.C."),
            rel("CONTRADICE", "CLM-000004", "CONTRADICTS", "Edad faraónica vs. proto-Sphinx pleistocénico."),
            rel("CUESTIONA", "CLM-000006", "CONTRADICTS", "Gauri mantiene la atribución faraónica que Schoch critica."),
        ],
        "extraction_status": "DRAFT",
        "extractor": "arena-piloto-g4",
        "reviewer": None,
        "created_utc": now,
    },
    {
        "claim_id": "CLM-000008",
        "attributed_claim": "El perfil redondeado de la Esfinge puede producirse por la meteorización actual en ambiente árido mediante la cristalización de sales (halita/yeso) en los poros, dada la gradación gradual de litología, sin necesidad de un clima húmedo pre-Sáhara ni de miles de años.",
        "controlled_paraphrase": "Afirmación causal de Gauri et al.; explica el perfil redondeado por meteorización salina presente.",
        "claimant": "Gauri, K. Lal; Sinai, John J.; Bandyopadhyay, Jayanta K.",
        "source_id": "DCA-000012",
        "passages": [
            passage("DCA-000012", 20, 25, "1", "1",
                "In this article we show how weathering in an arid environment can produce the rounded profile given the gradual change in lithology of the alternating hard and soft limestone strata."),
            passage("DCA-000012", 286, 295, "7", "7",
                "The structural joints in the rock have also significantly contributed to weathering ... the internal pressure due to salt crystallization has produced what may be called spheroidal weathering ... rounded surfaces have formed both in the lateral as well as in vertical direction."),
        ],
        "claim_type": "CAUSAL",
        "category": "CAUSAL",
        "object": "Perfil redondeado ('rolling') de la Esfinge",
        "asserted_date": None,
        "mechanism": "cristalización de sales en poros + gradación litológica + meteorización esferoidal",
        "invoked_evidence": "Estudios de porosidad y durabilidad (Chowdhury et al. 1990; Gauri 1984, 1990; Yerrapragada et al. 1993).",
        "stance": "FAVORABLE",
        "theory_ids": ["S06", "A10"],
        "project_assessment": {
            "status": "NO_EVALUADA",
            "reasoning": "Mecanismo propuesto por Gauri et al.; rival causal de la explicación por precipitación de Schoch.",
            "missing_to_test": "Tasas de meteorización salina, modelado, y comparación con canteras de edad conocida.",
            "confidence": "NOT_APPLICABLE",
            "falsification_potential": "Si se demostrara que la forma 'rolling' sólo puede originarse por lluvia y no por sales, la explicación salina se debilita.",
        },
        "relations": [
            rel("CUESTIONA", "CLM-000002", "CONTRADICTS", "Rival causal del perfil redondeado (sales vs. precipitación)."),
        ],
        "extraction_status": "DRAFT",
        "extractor": "arena-piloto-g4",
        "reviewer": None,
        "created_utc": now,
    },
    {
        "claim_id": "CLM-000009",
        "attributed_claim": "Los canales profundos en las paredes del recinto de la Esfinge son cavidades cársticas pre-Plioceno formadas por agua subterránea en la antigüedad geológica y expuestas por la excavación del foso, no por erosión de lluvia tras la excavación.",
        "controlled_paraphrase": "Afirmación empírica/observacional de Gauri et al.; reinterpreta los canales como karst pre-Plioceno.",
        "claimant": "Gauri, K. Lal; Sinai, John J.; Bandyopadhyay, Jayanta K.",
        "source_id": "DCA-000012",
        "passages": [
            passage("DCA-000012", 23, 25, "1", "1",
                "We show further that the channels are actually the pre-Pliocene karst features formed by underground water and exposed due to the excavation of the Sphinx ditch."),
            passage("DCA-000012", 378, 386, "9", "9",
                "these cavities are of pre-Pliocene age, having formed by the underground water and are not a result of erosion since the Sphinx had been excavated and the ditch formed."),
        ],
        "claim_type": "EMPIRICAL",
        "category": "OBSERVACIONAL",
        "object": "Canales/cavidades del recinto de la Esfinge",
        "asserted_date": "pre-Plioceno (cavidades)",
        "mechanism": "disolución kárstica por circulación de agua subterránea pre-Plioceno",
        "invoked_evidence": "Estructuras kársticas, revestimientos de yeso ('diffusion fronts'), contextos en necrópolis.",
        "stance": "FAVORABLE",
        "theory_ids": ["S06", "A10"],
        "project_assessment": {
            "status": "NO_EVALUADA",
            "reasoning": "Interpretación geomorfológica de Gauri et al.; rival de la atribución a lluvia de Schoch.",
            "missing_to_test": "Cartografía 3D de las cavidades, petrografía y análisis de los revestimientos de yeso.",
            "confidence": "NOT_APPLICABLE",
            "falsification_potential": "Si las cavidades mostraran morfología exclusivamente de erosión subaérea por escorrentía, la hipótesis kárstica pre-Plioceno se debilitaría.",
        },
        "relations": [
            rel("CUESTIONA", "CLM-000002", "CONTRADICTS", "Los canales no serían evidencia de lluvia antigua según Gauri."),
        ],
        "extraction_status": "DRAFT",
        "extractor": "arena-piloto-g4",
        "reviewer": None,
        "created_utc": now,
    },
    {
        "claim_id": "CLM-000010",
        "attributed_claim": "Los términos de Schoch 'precipitation-induced' y 'wind-induced weathering' son fundamentalmente defectuosos, porque la meteorización depende de las propiedades intrínsecas de la roca (distribución de tamaños de poro y contenido de sales), no de la erosión por viento o lluvia; ninguna de estas características puede dar una edad absoluta a la Esfinge.",
        "controlled_paraphrase": "Afirmación interpretativa/metodológica de Gauri et al.; crítica conceptual de la clasificación de Schoch.",
        "claimant": "Gauri, K. Lal; Sinai, John J.; Bandyopadhyay, Jayanta K.",
        "source_id": "DCA-000012",
        "passages": [
            passage("DCA-000012", 324, 333, "8", "8",
                "Whatever the precise mechanisms behind 'precipitation-induced' and 'wind-induced' weathering may be, these terms seem to be fundamentally flawed. Weathering, as commonly understood, depends upon the intrinsic properties of rock ... we will discuss ... show that none of these features can be used to give an absolute age to the Sphinx."),
        ],
        "claim_type": "INTERPRETIVE",
        "category": "INTERPRETATIVA",
        "object": "Terminología y validez de los modos de meteorización de Schoch",
        "asserted_date": None,
        "mechanism": None,
        "invoked_evidence": "Propiedades de la roca (porosidad, sales) y estudios de porosidad.",
        "stance": "CRITICA",
        "theory_ids": ["S06", "A10"],
        "project_assessment": {
            "status": "NO_EVALUADA",
            "reasoning": "Crítica conceptual de Gauri et al.; se registra sin concluir.",
            "missing_to_test": "Cuantificación de perfiles y atribución de procesos de meteorización/erosión por agentes.",
            "confidence": "NOT_APPLICABLE",
            "falsification_potential": "Si se demostrara que el agente (viento vs. lluvia) controla la morfología de modo discriminante, la crítica perdería fuerza.",
        },
        "relations": [
            rel("CONTRADICE", "CLM-000002", "CONTRADICTS", "Validez de los dos modos de meteorización."),
        ],
        "extraction_status": "DRAFT",
        "extractor": "arena-piloto-g4",
        "reviewer": None,
        "created_utc": now,
    },
    {
        "claim_id": "CLM-000011",
        "attributed_claim": "El grado de retroceso de los estratos y el grado de meteorización de las calizas de la Esfinge no pueden relacionarse cuantitativamente con el tiempo transcurrido desde la exposición: la tasa de retroceso es desconocida y variable, y el tiempo real de exposición es desconocido por los prolongados enterramientos bajo arena.",
        "controlled_paraphrase": "Afirmación metodológica de Gauri et al.; limita el uso de la meteorización como reloj.",
        "claimant": "Gauri, K. Lal; Sinai, John J.; Bandyopadhyay, Jayanta K.",
        "source_id": "DCA-000012",
        "passages": [
            passage("DCA-000012", 422, 426, "11", "11",
                "At any rate, the degree of recession of this slope does not offer any clue to the time involved because the rate of recession is unknown and changes in that rate may have occurred over time."),
            passage("DCA-000012", 475, 477, "13", "13",
                "Thus the degree of weathering of the limestones at the Sphinx cannot be related quantitatively with the extent of the time passed since exposure to the environment."),
        ],
        "claim_type": "METHODOLOGICAL",
        "category": "CRONOLOGICA",
        "object": "Uso de la meteorización como indicador de tiempo",
        "asserted_date": None,
        "mechanism": None,
        "invoked_evidence": "Ejemplo del bloque de la zanja expuesto una estación (Fig. 8) y restauraciones.",
        "stance": "CRITICA",
        "theory_ids": ["S06", "A10"],
        "project_assessment": {
            "status": "NO_EVALUADA",
            "reasoning": "Limitación metodológica señalada por Gauri et al.; cuestiona el reloj de meteorización de Schoch.",
            "missing_to_test": "Calibración de tasas de meteorización y control del historial de enterramiento/exposición.",
            "confidence": "NOT_APPLICABLE",
            "falsification_potential": "Si se calibrara una tasa de meteorización robusta y controlada, la relación tiempo-grado de meteorización podría restablecerse.",
        },
        "relations": [
            rel("CUESTIONA", "CLM-000001", "CONTRADICTS", "Limita la base metodológica de la datación por meteorización."),
            rel("CUESTIONA", "CLM-000004", "NO_DIRECT_RELATION", "Impacta indirectamente la cronología pleistocénica."),
        ],
        "extraction_status": "DRAFT",
        "extractor": "arena-piloto-g4",
        "reviewer": None,
        "created_utc": now,
    },
    {
        "claim_id": "CLM-000012",
        "attributed_claim": "Los datos sísmicos (variabilidad de la profundidad de meteorización: 1,2 m en la parte posterior, 1,8–2,5 m en el resto) podrían apoyar una excavación en dos etapas de la Esfinge, pero por sí solos no pueden dar la edad de la Esfinge.",
        "controlled_paraphrase": "Afirmación metodológica/empírica de Gauri et al.; concede un posible argumento de dos etapas pero niega que fije la edad.",
        "claimant": "Gauri, K. Lal; Sinai, John J.; Bandyopadhyay, Jayanta K.",
        "source_id": "DCA-000012",
        "passages": [
            passage("DCA-000012", 492, 505, "13", "13",
                "A seismic survey of the subsurface within the Sphinx Enclosure ... reveals that the depth of 'weathering' in the posterior portion of the Sphinx is only 1.2 m and it increases abruptly to 1.8-2.5 m ... could be a significant argument in favor of two-stage excavation of the Sphinx. But this feature alone cannot be used to give an age to the Sphinx."),
            passage("DCA-000012", 526, 529, "14", "14",
                "Their only remaining argument, based on seismic data, does not provide a clue to the age of the Sphinx by itself."),
        ],
        "claim_type": "EMPIRICAL",
        "category": "OBSERVACIONAL",
        "object": "Perfil sísmico subsuperficial del recinto de la Esfinge",
        "asserted_date": None,
        "mechanism": None,
        "invoked_evidence": "Encuesta sísmica de Dobecki (1992) y Dobecki & Schoch (1992); crítica de Harrell (1994).",
        "stance": "CRITICA",
        "theory_ids": ["S06", "A10"],
        "project_assessment": {
            "status": "NO_EVALUADA",
            "reasoning": "Reinterpretación de los datos sísmicos por Gauri et al.; niega que fijen la edad.",
            "missing_to_test": "Datos sísmicos crudos y validación independiente de la variable profundidad.",
            "confidence": "NOT_APPLICABLE",
            "falsification_potential": "Si la profundidad de meteorización se correlacionara de forma calibrada con el tiempo de exposición, la sísmica podría datar la construcción.",
        },
        "relations": [
            rel("CONTRADICE", "CLM-000001", "CONTRADICTS", "Sísmica no dataría por sí sola (contra Schoch)."),
            rel("CONTEXTUALIZA", "CLM-000005", "NO_DIRECT_RELATION", "Ambas discuten la interpretación sísmica desde lados opuestos."),
        ],
        "extraction_status": "DRAFT",
        "extractor": "arena-piloto-g4",
        "reviewer": None,
        "created_utc": now,
    },
]


def main() -> int:
    with OUT_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        for c in CLAIMS:
            record = dict(c)
            record.setdefault("schema_version", "2.0")
            record.setdefault("matrix_id", "S06/A10")
            for p in record.get("passages", []):
                p.setdefault("hash_ref", "original")
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    # Validar contra el esquema
    import jsonschema
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    records = [json.loads(line) for line in OUT_PATH.open(encoding="utf-8")]
    print(f"Afirmaciones generadas: {len(records)} (objetivo <= 12)")
    errors = 0
    for r in records:
        errs = sorted(validator.iter_errors(r), key=lambda e: list(e.path))
        if errs:
            errors += 1
            print(f"[FAIL] {r['claim_id']}:")
            for e in errs:
                print("   ", "/".join(map(str, e.path)), "->", e.message)
        else:
            print(f"[OK]   {r['claim_id']} ({r['source_id']}) {r['claim_type']}")
    if errors:
        print(f"VALIDACIÓN: {len(records)-errors}/{len(records)} válidos, {errors} errores.")
        return 1
    print(f"VALIDACIÓN: {len(records)}/{len(records)} válidos contra {SCHEMA_PATH.name}.")
    print(f"Archivo: {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
