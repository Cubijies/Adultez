# Auditoría del piloto G4 — Esfinge: Schoch/Bauval vs. Gauri et al.

**Versión:** 1.0
**Fecha:** 12 de agosto de 2026
**Alcance:** extracción adversarial limitada a 12 afirmaciones atómicas (límite cumplido).
**Fuentes:**
- `DCA-000021` — R. M. Schoch y R. Bauval, *Origins of the Sphinx* (2017). original_sha256 `0054a66c…3d9`
- `DCA-000012` — K. L. Gauri, J. J. Sinai, J. K. Bandyopadhyay, “Geologic Weathering and Its Implications on the Age of the Sphinx”, *Geoarchaeology* 10 (1995), 119–133. original_sha256 `e8031bd4…9a`
- Archivo de afirmaciones: `AFIRMACIONES_PILOTO_G4.jsonl` (12 registros).
- Validación: **12/12 válidos** contra `esquemas/claim_record.schema.json`.
- **No se formula aquí conclusión global sobre la Esfinge.** Toda evaluación de `project_assessment` es `NO_EVALUADA`.

> Nota metodológica: los `relations[]` del esquema usan valores `APOYA / CONTRADICE / CUESTIONA / DEPENDE_DE / CONTEXTUALIZA / REPLICA / CITA / REFUTA / DUPLICA / TRADUCE`. La taxonomía pedida por el usuario (SUPPORTS / CONTRADICTS / QUALIFIES / NO_DIRECT_RELATION) se conserva en el campo adicional `relation_semantic` de cada relación (permitido por `additionalProperties: true`). Equivalencias: SUPPORTS→APOYA/DEPENDE_DE; CONTRADICTS→CONTRADICE; QUALIFIES→CUESTIONA/CONTEXTUALIZA; NO_DIRECT_RELATION→CONTEXTUALIZA.

## 1. Tabla de afirmaciones

| ID | Fuente | Tipo | Categoría | Afirmación (resumen) | Pasaje (pág.) | Incertidumbre | Falsación potencial |
|---|---|---|---|---|---|---|---|
| CLM-000001 | DCA-000021 | CHRONOLOGICAL | Cronológica | Core body datado ~10,000 a.C. por profundidad de meteorización subsuperficial (sísmica) | L1639–1675 (pp. 68–69) | Calibración lineal vs. no lineal; asociación muestra–construcción | Si la profundidad responde a litología/diagénesis y no al tiempo |
| CLM-000002 | DCA-000021 | CAUSAL | Causal | Dos modos de meteorización: eólica (angular) vs. por precipitación (rolling); la Esfinge conserva precipitación | L5216–5244 (pp. 214–215) | Discriminación de procesos por morfología | Si la forma 'rolling' se produce por sales en clima árido |
| CLM-000003 | DCA-000021 | INTERPRETIVE | Interpretativa | La cabeza es un recarve dinástico de un monumento mucho más antiguo | L4544–4557 (p. 178) | Estilo/atribución del recarve | Si la cabeza original era de proporciones similares |
| CLM-000004 | DCA-000021 | CHRONOLOGICAL | Cronológica | Proto-Sphinx previo al final de la última glaciación (~9700 a.C.), contemporáneo de Göbekli Tepe | L1670–1674 (p. 69) | Depende de CLM-000001 | Si CLM-000001 se refuta o la sincronía no se sostiene |
| CLM-000005 | DCA-000021 | EMPIRICAL | Observacional | Críticas (roca más dura al oeste; perfiles = estratos buzantes) son incorrectas | L1678–1690 (p. 69) | Datos sísmicos primarios no auditaron | Si se demuestra heterogeneidad litológica/buzamiento |
| CLM-000006 | DCA-000021 | INTERPRETIVE | Interpretativa | La atribución a Cuarta Dinastía es circunstancial (solo 'contexto') | L4520–4539 (p. 177) | Criterio de datación por contexto | Si el contexto arqueológico de Khafra es demostrativo |
| CLM-000007 | DCA-000012 | CHRONOLOGICAL | Cronológica | No hay edad absoluta; la Esfinge sigue siendo faraónica (~4500 años) | L100–104 (p. 3); L519–531 (p. 14) | Ausencia de datación absoluta robusta | Si se logra datación absoluta fiable de la talla |
| CLM-000008 | DCA-000012 | CAUSAL | Causal | Perfil redondeado por cristalización salina en clima árido (gradación litológica) | L20–25 (p. 1); L286–295 (p. 7) | Tasas de meteorización salina | Si la forma 'rolling' exige lluvia y no sales |
| CLM-000009 | DCA-000012 | EMPIRICAL | Observacional | Los canales del recinto son karst pre-Plioceno por agua subterránea, no lluvia | L23–25 (p. 1); L378–386 (p. 9) | Cartografía/petrografía de las cavidades | Si las cavidades son de erosión subaérea por escorrentía |
| CLM-000010 | DCA-000012 | INTERPRETIVE | Interpretativa | Los términos 'precipitation-/wind-induced' son defectuosos; dependen de propiedades de la roca | L324–333 (p. 8) | Validez de la clasificación de Schoch | Si el agente controla la morfología de forma discriminante |
| CLM-000011 | DCA-000012 | METHODOLOGICAL | Cronológica | El grado de meteorización no puede relacionarse cuantitativamente con el tiempo (tasa desconocida, enterramiento) | L422–426 (p. 11); L475–477 (p. 13) | Calibración de tasas | Si se calibra una tasa robusta y controlada |
| CLM-000012 | DCA-000012 | EMPIRICAL | Observacional | Sísmica: 1,2 m (posterior) vs. 1,8–2,5 m (resto); posible excavación en dos etapas, pero no da edad | L492–505 (p. 13); L526–529 (p. 14) | Datos sísmicos crudos; crítica de Harrell 1994 | Si la profundidad de meteorización se correlaciona calibradamente con el tiempo |

**Desglose categórico (taxonomía del usuario):** observacional 3 (CLM-000005/009/012), cronológica 4 (CLM-000001/004/007/011), causal 2 (CLM-000002/008), interpretativa 3 (CLM-000003/006/010).
**Separatividad:** cada registro separa `attributed_claim` (afirmación del autor) / `invoked_evidence` (evidencia aportada) / `controlled_paraphrase`+`project_assessment` (interpretación del proyecto, marcada NO_EVALUADA). Las citas (`quotation`) están en `passages[]` con `quotation_sha256`.

## 2. Mapa de relaciones

Matriz entre pares relevantes de afirmaciones (taxonomía del piloto):

| De | A | Relación | Nota |
|---|---|---|---|
| CLM-000001 (Schoch: ~10,000 a.C.) | CLM-000007 | **CONTRADICTS** | Edad antigua vs. faraónica |
| CLM-000001 | CLM-000012 | **CONTRADICTS** | Sísmica como datación vs. 'sísmica sola no da edad' |
| CLM-000004 (proto-Sphinx pleistocénico) | CLM-000007 | **CONTRADICTS** | Edad pleistocénica vs. faraónica |
| CLM-000004 | CLM-000001 | **SUPPORTS** | Depende de la datación del core body |
| CLM-000002 (dos modos) | CLM-000010 | **CONTRADICTS** | Validez de los dos modos de meteorización |
| CLM-000002 | CLM-000008 | **CONTRADICTS** | Rival causal del perfil redondeado (precipitación vs. sales) |
| CLM-000002 | CLM-000009 | **CONTRADICTS** | Canales como lluvia vs. karst pre-Plioceno |
| CLM-000003 (recarve) | CLM-000007 | **CONTRADICTS** | Reutilización pre-faraónica vs. creación faraónica |
| CLM-000006 (contexto circunstancial) | CLM-000007 | **CONTRADICTS** | Debilita la base faraónica que Gauri mantiene |
| CLM-000011 (meteorización no es reloj) | CLM-000001 | **CONTRADICTS** | Limita la base metodológica de la datación |
| CLM-000011 | CLM-000004 | **NO_DIRECT_RELATION** | Impacto indirecto |
| CLM-000012 | CLM-000001 | **CONTRADICTS** | Reinterpreta la sísmica |
| CLM-000012 | CLM-000005 | **NO_DIRECT_RELATION** | Lados opuestos de la misma evidencia sísmica |
| CLM-000005 | CLM-000012 | **NO_DIRECT_RELATION** | Contra-objeción de Schoch vs. límite señalado por Gauri |

Observaciones:
- El **núcleo de la controversia** es un triángulo: cronología (CLM-000001/000004/000007), mecanismo de la forma 'rolling' (CLM-000002/000008/000010) y significado de la sísmica (CLM-000001/000005/000012).
- Las relaciones dominantes son **CONTRADICTS** (contrapuestas directas), lo que refleja el objetivo adversarial del piloto.
- No hay relaciones **QUALIFIES** puras entre los pares elegidos; el matiz aparece en CLM-000012 (concede dos etapas pero niega la datación).

## 3. Problemas de trazabilidad encontrados

1. **Doble hash de fuente:** el esquema pide `source_sha256`, pero el pipeline distingue `original_sha256` y `normalized_sha256`. Se usó el original (canonical); debe decidirse y documentarse cuál usar (posible campo `hash_ref`).
2. **`passage_id` sin página:** el patrón del esquema (`PAS-DCA-…-L…-L…`) no incorpora páginas, aunque las páginas se guardan en `page_start/page_end`. Si se quiere localizar por página, conviene ampliar el patrón o añadir un campo `page_ref`.
3. **Convención de página en DCA-000012:** los marcadores son `PÁGINA n` (nº de página del escaneo 1–15), no la paginación impresa (119–133) que aparece en el pie. Es necesario mapear página de escaneo ↔ página impresa para citar formalmente.
4. **Marcadores de página inconsistentes en DCA-000021:** algunas páginas no tienen marcador explícito; la asignación a `page_start/page_end` requirió interpolación entre marcadores.
5. **Taxonomía de relaciones bilingüe:** el esquema exige enum en español mientras la tarea pide SUPPORTS/CONTRADICTS/QUALIFIES/NO_DIRECT_RELATION. Se resolvió con el campo extra `relation_semantic`; conviene oficializarlo en el esquema.
6. **`category` (observacional/cronológica/causal/interpretativa) como campo extra:** no está en el esquema; se añadió vía `additionalProperties`. Si se quiere obligatorio, debe incorporarse al esquema.
7. **Sin mapeo a `work_id`/teoría por pasaje:** los pasajes no enlazan a la matriz (S06/A10 se fija solo a nivel de afirmación). Añadir `matrix_id` opcional mejoraría el rastreo a `MATRIZ_FUENTES_V1.md`.

## 4. Cambios propuestos al esquema o pipeline

| # | Objeto | Cambio propuesto |
|---|---|---|
| P1 | pipeline | Añadir un comando o flag que exporte un mapa página-escaneo↔página-impresa y lo incorpore al manifest (resuelve problema 3). |
| P2 | schema | Añadir `hash_ref: "original"|"normalized"` en `passages[]` para fijar el hash usado (problema 1). |
| P3 | schema | Ampliar patrón `passage_id` o añadir `page_ref` para incluir la página (problema 2). |
| P4 | schema | Añadir enumerado canónico de relaciones en la taxonomía del proyecto (SUPPORTS/CONTRADICTS/QUALIFIES/NO_DIRECT_RELATION) como campo `relation_semantic` obligatorio, además del enum técnico (problema 5). |
| P5 | schema | Incorporar `category` (OBSERVACIONAL/CRONOLOGICA/CAUSAL/INTERPRETATIVA) como enumerado en `claim_type` o campo obligatorio (problema 6). |
| P6 | schema/plantilla | Añadir `matrix_id` opcional en el registro para enlazar afirmaciones a la matriz de fuentes (problema 7). |
| P7 | pipeline | Validación automática de los registros contra el esquema dentro del flujo (reutilizar la lógica del validador jsonschema) para evitar errores como el `schema_version` faltante. |

## 5. Recomendación para escalar G4

**Recomendación: HOLD para la extracción masiva.**

Justificación:
- El piloto **demostró** que la extracción adversarial y la relación de afirmaciones contrapuestas es viable y que los registros **validan contra el esquema (12/12)**.
- Pero antes de escalar conviene resolver los problemas de trazabilidad 1–3 y 5–6 y aplicar los cambios de esquema P1–P7, en particular:
  - fijar el hash de referencia y el mapeo de páginas;
  - oficializar `relation_semantic` y `category` en el esquema (evita campos ad-hoc por registro);
  - automatizar la validación en el pipeline.
- Con el esquema estabilizado, un próximo piloto ampliado (por ejemplo 3–5 fuentes del corpus activo/contraste) serviría de revalidación antes de la extracción masiva.

**No se autoriza la extracción masiva en esta etapa** (pendiente de aprobación del piloto y de los cambios propuestos).
