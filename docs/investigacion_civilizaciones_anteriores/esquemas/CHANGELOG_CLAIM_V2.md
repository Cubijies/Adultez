# Cambios al esquema de afirmaciones — v1.0 → v2.0

**Fecha:** 12 de agosto de 2026
**Motivo:** aplicar los cambios propuestos P2–P6 del piloto G4 antes de la extracción masiva.

| Propuesta | Cambio aplicado |
|---|---|
| P2 | `passages[].hash_ref` (`original`/`normalized`) para fijar a qué hash apunta `source_sha256`. |
| P3 | `passage_id` acepta un segmento opcional de página (`PAS-DCA-…-P…-L…-L…` o solo líneas); nuevo campo `page_ref`. |
| P4 | `relations[].relation_semantic` obligatorio con enum SUPPORTS/CONTRADICTS/QUALIFIES/NO_DIRECT_RELATION. |
| P5 | Nuevo campo `category` obligatorio (OBSERVACIONAL/CRONOLOGICA/CAUSAL/INTERPRETATIVA/METODOLOGICA/TEXTUAL). |
| P6 | Nuevo campo opcional `matrix_id` para enlazar a `MATRIZ_FUENTES_V1.md`. |

Además:
- `project_assessment.falsification_potential` queda disponible (ya se usaba en el piloto).
- `schema_version` cambia de `"1.0"` a `"2.0"`.

**Pipeline (P1 y P7):**
- `corpus_pipeline.py pagemap --source-id DCA-xxxxxx` → mapea marcadores de página (PÁGINA/PAGE/form-feed) a rangos de línea y detecta números de página impresos (P1).
- `corpus_pipeline.py validate-claims --schema … --claims …` → valida un JSONL de afirmaciones contra el esquema (P7).

**Validación:** el piloto G4 y el lote 1 de extracción masiva validan 12/12 y 18/18 respectivamente contra el esquema v2.0.
