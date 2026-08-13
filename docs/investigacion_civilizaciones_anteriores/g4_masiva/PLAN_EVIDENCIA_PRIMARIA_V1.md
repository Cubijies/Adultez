# Plan de búsqueda de evidencia primaria — fase 1

**Versión:** 1.0
**Fecha:** 12 de agosto de 2026
**Objetivo:** localizar y auditar los datos primarios que falsarían o reforzarían cada línea de afirmación del registro consolidado (`REGISTRO_CONSOLIDADO_AFIRMACIONES_V1.jsonl`), según los "datos decisivos faltantes" de `EVALUACION_LOTE_V1.md`.

> Principios: la búsqueda no es bibliográfica exhaustiva; se busca solo lo que decide una afirmación. Cada hallazgo se registra con autor, título, año, DOI/URL, estado de verificación (D/M/S/N) y su relación con la afirmación.

## Prioridades (orden de falsabilidad / decisividad)

| # | Línea | Afirmación(s) | Dato decisivo que buscar | Búsqueda clave |
|---|---|---|---|---|
| P1 | **Esfinge — datación** | CLM-000001/007 | Datación absoluta de la talla original (exposición cosmogénica ²⁶Cl/¹⁰Be, U-Pb, etc.) | `cosmogenic dating Great Sphinx enclosure` |
| P2 | **Esfinge — geología** | CLM-000002/008/010 | Controles litológicos/porosidad: ¿la profundidad responde a litología o a tiempo? | `Gauri Sphinx weathering limestone porosity control` |
| P3 | **Mapas antiguos** | CLM-000027/032/033 | Análisis de proyección de Piri Reis/Oronteus Finaeus; historia del hielo antártico | `Piri Reis map projection analysis Antarctica` |
| P4 | **Younger Dryas impacto** | CLM-000026 | Estado actual de la controversia (datos, replicación) | `Younger Dryas impact hypothesis 2024 2025` |
| P5 | **Yonaguni** | CLM-000024 | Informe Kimura 2001; evaluación geológica (diaclasas) | `Yonaguni monument geology natural joints Kimura 2001` |
| P6 | **Khambhat** | (caso) | Expediente NIOT; contexto del dragado | `NIOT Gulf of Cambay sonar artifacts dating` |
| P7 | **Tablillas Naacal** | CLM-000021/029 | Procedencia/catálogo de las tablillas | `Naacal tablets provenance Churchward` |
| P8 | **Mahābhārata** | (tradición) | Edición BORI 3.186–189, pasajes sobre *astra* | `Mahabharata BORI 3.186 weapons` |
| P9 | **Sundaland** | CLM-000030/037 | Arqueología subacuática / datos genéticos | `Sundaland drowned landscape archaeology genetics` |
| P10 | **Anticitera / controles** | (control) | Datación y contexto | `Antikythera mechanism dating` |

## Entregables de cada búsqueda
1. Referencia primaria localizada (autor, título, año, DOI/URL, DOI de archivo).
2. Estado de verificación (D directa / M metadatos / S secundaria / N no realizada).
3. Relación con la afirmación: REFUERZA / FALSARÍA / NEUTRAL / INSUFICIENTE.
4. Cita textual clave si se accede al documento.
5. Dato faltante restante.

## Registro
Los resultados se registran en `g4_masiva/REGISTRO_EVIDENCIA_PRIMARIA.jsonl` y se resumen en `g4_masiva/INFORME_EVIDENCIA_PRIMARIA_V1.md` al cierre de la fase.
