# Adultez — Investigación: civilizaciones tecnológicas anteriores

Investigación privada y exploratoria sobre la posibilidad de civilizaciones tecnológicas iguales o más desarrolladas que la actual, potencialmente existentes cientos de miles de años atrás. Trabaja con perspectiva combinada de historiador, antropólogo, arqueólogo, investigador expedicionario y especialista en civilizaciones antiguas.

> **Aviso de método:** la admisión de una fuente al canon no implica aceptación de sus afirmaciones. El proyecto distingue en todo momento **hecho documentado / interpretación / hipótesis / especulación / contradicción / ausencia de datos**, y no reduce la investigación a «no puede demostrarse».

## Estructura

- `docs/investigacion_civilizaciones_anteriores/` — todos los documentos, registros, esquemas y scripts de la investigación.
- `scripts/` — pipeline reproducible (inventario, fragmentación, búsqueda, selección, validación).
- `tests/` — pruebas del pipeline.
- `corpus_local/` — **área local no versionada** (ignorada por Git): originales TXT, PDFs de evidencia, normalizados, índices y selecciones. Se conserva fuera de Git por tamaño, trazabilidad y derechos de las fuentes.

## Punto de entrada

| Documento | Contenido |
|---|---|
| `README.md` | Este archivo. |
| `docs/investigacion_civilizaciones_anteriores/INDICE_MAESTRO_V1.md` | Navegación de todos los entregables. |
| `docs/investigacion_civilizaciones_anteriores/RESUMEN_EJECUTIVO_V1.md` | Veredicto de una página. |
| `docs/investigacion_civilizaciones_anteriores/INFORME_REDACCION_V2.md` | Informe final integrando la evidencia primaria. |

## Cómo usar el pipeline

```bash
# Estructura local
python3 scripts/corpus_pipeline.py --root corpus_local/civilizaciones_anteriores init

# Inventario + normalización
python3 scripts/corpus_pipeline.py --root corpus_local/civilizaciones_anteriores inventory

# Fragmentos recuperables
python3 scripts/corpus_pipeline.py --root corpus_local/civilizaciones_anteriores chunk

# Búsqueda local
python3 scripts/corpus_pipeline.py --root corpus_local/civilizaciones_anteriores search --query "esfinge meteorización"

# Verificación de hashes
python3 scripts/corpus_pipeline.py --root corpus_local/civilizaciones_anteriores verify
```

Requiere Python 3.11+. Para `validate-claims` (validación de afirmaciones contra el esquema JSON) se necesita el módulo `jsonschema`.

## Estado del proyecto

- **Canon G3:** 28 fuentes con rol único (16 activas, 3 contraste, 5 tradicionales, 4 orientativas), etiquetas no excluyentes.
- **Registro de afirmaciones:** 37 afirmaciones consolidadas, validadas contra `esquemas/claim_record.schema.json` v2.0, con 15 relaciones entre hipótesis.
- **Evidencia primaria:** 33 hallazgos auditados.
- **Veredicto:** ninguna fuente demuestra una civilización tecnológica anterior; las líneas más ambiciosas se debilitaron con la evidencia; la Esfinge tiene una resolución publicada (Early Dynastic) que no exige civilización perdida.

## Nota sobre el contenido

Los 28 documentos originales en `.txt` y los PDFs de evidencia primaria se preservan en `corpus_local/` y **no se versionan en Git** (por tamaño, trazabilidad y derechos de las fuentes). El repositorio versiona únicamente protocolos, esquemas, plantillas, scripts reproducibles, catálogos bibliográficos y resultados sintéticos.
