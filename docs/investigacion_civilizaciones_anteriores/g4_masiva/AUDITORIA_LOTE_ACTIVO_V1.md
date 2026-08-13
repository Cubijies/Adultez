# Auditoría de extracción masiva — Lote 1 (corpus activo)

**Versión:** 1.0
**Fecha:** 12 de agosto de 2026
**Esquema:** `claim_record.schema.json` **v2.0** (tras aplicar P1–P7)
**Archivo de afirmaciones:** `LOTE_ACTIVO_AFIRMACIONES_V1.jsonl`
**Total:** 18 afirmaciones atómicas · **Validación 18/18** contra el esquema v2.0 (vía `scripts/generar_extraccion_masiva.py` y comando `validate-claims`).

> Nota de calidad: la extracción se hizo sobre copias normalizadas con OCR en diversos grados. Las fuentes más degradadas (DCA-000001 Sitchin, DCA-000003/009 Donnelly) se marcan con `ocr_warning=true` y citan fragmentos breves. La admisión al corpus no implica aceptar las afirmaciones.

## 1. Tabla de afirmaciones por fuente

| claim_id | source_id | Tipo / Categoría | Afirmación (resumen) | OCR |
|---|---|---|---|---|
| CLM-000001 | DCA-000001 | INTERPRETIVE / Interpretativa | La Tierra fue visitada por astronautas de otro planeta (el 12.º) que crearon al hombre | sí |
| CLM-000002 | DCA-000001 | INTERPRETIVE / Interpretativa | Regresión cultural en Oriente Próximo ~11000 a.C. y aparición súbita del «hombre pensante» | sí |
| CLM-000003 | DCA-000003 | INTERPRETIVE / Interpretativa | Atlántida fue el verdadero mundo antediluviano, Jardín del Edén y cuna de la civilización | sí |
| CLM-000004 | DCA-000003 | INTERPRETIVE / Interpretativa | Egipto y el valle del Indo fueron colonias de la civilización atlante | sí |
| CLM-000005 | DCA-000004 | INTERPRETIVE / Interpretativa | La Esfinge, león con cabeza humana, vinculable a una fecha celeste muy anterior al Reino Antiguo | no |
| CLM-000006 | DCA-000006 | CAUSAL / Causal | Un desplazamiento de la corteza mata en gran número especies y gentes en un solo movimiento | no |
| CLM-000007 | DCA-000007 | EMPIRICAL / Observacional | «Nueva evidencia en la Antártida» apoya desplazamientos rápidos del polo/corteza | no |
| CLM-000008 | DCA-000009 | INTERPRETIVE / Interpretativa | Atlántida fue el mundo antediluviano y alcanzó grado avanzado (versión es) | no |
| CLM-000009 | DCA-000010 | INTERPRETIVE / Interpretativa | El continente de Mu es el lugar donde el hombre fue creado, hoy sumergido | no |
| CLM-000010 | DCA-000010 | EMPIRICAL / Observacional | Las placas Naacal contienen el registro de la civilización de Mu | no |
| CLM-000011 | DCA-000013 | INTERPRETIVE / Interpretativa | Se perdió una civilización avanzada a causa de una catástrofe | no |
| CLM-000012 | DCA-000014 | INTERPRETIVE / Interpretativa | Estructuras artificiales bajo el mar en Yonaguni indican una civilización megalítica antigua | no |
| CLM-000013 | DCA-000016 | EMPIRICAL / Observacional | Mapas antiguos (Oronteus Finaeus) muestran la Antártida antes de la última glaciación | no |
| CLM-000014 | DCA-000017 | CAUSAL / Causal | Un cometa golpeó hace ~11.600 años (Dryas reciente), asociado a la destrucción de una civilización | no |
| CLM-000015 | DCA-000019 | EMPIRICAL / Observacional | Los mapas de Piri Reis/Oronteus Finaeus derivan de cartografía de una civilización avanzada previa | no |
| CLM-000016 | DCA-000024 | CHRONOLOGICAL / Cronológica | La edad de la Esfinge es muy anterior a la egiptología convencional | no |
| CLM-000017 | DCA-000026 | EMPIRICAL / Observacional | Dos conjuntos de tablillas Naacal (2500+), escritas por los Naacal que salieron de Birmania >15.000 años | no |
| CLM-000018 | DCA-000027 | CAUSAL / Causal | Sundaland se inundó al final de la glaciación, dispersando poblaciones y mitos | no |

**Desglose categórico:** observacional 5, interpretativa 9, causal 3, cronológica 1.

## 2. Relaciones registradas (work_id entre manifestaciones)

| claim_id | Relación | target_id | Nota |
|---|---|---|---|
| CLM-000003 (DCA-000003) | SUPPORTS (CONTEXTUALIZA) | CLM-000008 (DCA-000009) | Misma obra de Donnelly, manifestaciones es/en |
| CLM-000008 (DCA-000009) | SUPPORTS | CLM-000003 | Ídem |
| CLM-000009 (DCA-000010) | SUPPORTS | CLM-000017 (DCA-000026) | Misma obra de Churchward, es/en |
| CLM-000017 (DCA-000026) | SUPPORTS | CLM-000009 | Ídem |
| CLM-000006 (DCA-000006) | SUPPORTS | CLM-000007 (DCA-000007) | Componentes del mismo *Earth's Shifting Crust* |
| CLM-000007 (DCA-000007) | SUPPORTS | CLM-000006 | Ídem |

## 3. Trazabilidad

- Cada pasaje lleva `source_id`, `passage_id`, `source_sha256` (+`hash_ref: original`), `line_start/end`, `page_start/end` (resueltos con `pagemap` P1), `quotation` y `quotation_sha256`.
- Las páginas se resolvieron automáticamente del página-map; donde no hay marcador (p. ej. portadas) `page_start` queda `null`.
- `matrix_id` y `theory_ids` enlazan a la matriz de fuentes (A01, A03, A04, A07, A08, A09, A12, S02, S06/A10, P10).
- Todos los `project_assessment.status` son `NO_EVALUADA`; `ocr_warning` señalado donde procede.

## 4. Cobertura del lote 1

Fuentes activas cubiertas (16/16, incluye el piloto DCA-000021 ya extraído):
DCA-000001, 000003, 000004, 000006, 000007, 000009, 000010, 000013, 000014, 000016, 000017, 000019, 000021 (piloto), 000024, 000026, 000027.

Pendiente de ampliación (no bloquea la trazabilidad): extraer más afirmaciones por fuente en lotes sucesivos (actualmente 1–2 por fuente), añadir relaciones entre hipótesis (p. ej. Esfinge ↔ Hapgood ↔ Hancock), y auditar con la edición/portada las afirmaciones marcadas `ocr_warning`.

## 5. Recomendación

**GO para continuar la extracción masiva en lotes sucesivos**, manteniendo: (a) validación obligatoria contra el esquema v2.0 en cada lote; (b) página/hash resueltos mecánicamente; (c) `NO_EVALUADA` hasta la fase de evaluación. Se recomienda priorizar: resolver los `ocr_warning`, añadir el segundo/tercer lote de afirmaciones por fuente, y luego construir el mapa de relaciones entre hipótesis (SUPPORTS/CONTRADICTS/QUALIFIES) antes de cualquier conclusión.
