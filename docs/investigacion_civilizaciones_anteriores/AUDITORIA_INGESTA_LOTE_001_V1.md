# Auditoría de ingesta — LOTE-001-ADULTEZ

**Versión:** 1.0
**Fecha de recepción:** 12 de agosto de 2026
**Origen declarado:** <https://github.com/Cubijies/Adultez>
**Commit fijado:** `d021866609547f9f482bf84685c9ff7eba45d814`
**Estado:** G0 `GO`; G1 `GO`; G2 `HOLD`

## 1. Resultado ejecutivo

El repositorio remoto contenía 28 archivos TXT. Todos se descargaron desde el commit fijado, se cotejaron contra su Git blob SHA-1, se identificaron mediante SHA-256, se normalizaron sin modificar los originales y se verificaron nuevamente.

| Control | Resultado |
|---|---:|
| Archivos TXT recibidos | 28 |
| Documentos únicos por SHA-256 | 28 |
| Duplicados exactos | 0 |
| Tamaño total de originales | 16.301.862 bytes |
| Palabras aproximadas | 2.539.067 |
| Codificación detectada | 28 UTF-8 |
| Documentos con marcadores de página | 11 |
| Marcadores de página totales | 2.909 |
| Fragmentos locales recuperables | 1.467 |
| Verificación original/normalizado | 28/28 `PASS` |
| Fallos bloqueantes | 0 |

El contenedor de transporte quedó identificado localmente por SHA-256:

```text
b1161e38edbe28f457a38b2c6e30ea7db331ebf34f9354859a680458bf833b51
```

El usuario declaró que el *Mahābhārata* no está incluido debido a su tamaño. Su ausencia no bloquea G1.

## 2. Incidencias mecánicas

Estas incidencias no significan que la obra sea inválida; señalan controles pendientes:

| source_id | Incidencia | Acción G2 requerida |
|---|---|---|
| `DCA-000001` | `VERY_LONG_LINES`: 270 líneas superan 1.000 caracteres; máximo 4.749. La inspección del frontispicio muestra sustituciones OCR frecuentes. | Conservar para búsqueda tolerante, pero cotejar cualquier cita con una imagen o edición fiable. |
| `DCA-000013` | `CONTROL_CHARACTERS`: dos caracteres `U+0007` | Tratar como residuos del convertidor en una futura capa de limpieza; no alterar el original. |
| `DCA-000018` | `CONTROL_CHARACTERS`: un `U+0000`; `POSSIBLE_MOJIBAKE`: tres secuencias `Â` | Auditar los puntos concretos y anotar lectura normalizada sin corregir el original. |

No se detectaron archivos vacíos, errores de decodificación ni sustituciones de bytes.

## 3. Metadatos y completitud

Los nombres permiten proponer títulos, pero todavía no prueban edición, traducción ni completitud. Por eso los 28 registros permanecen con alcance `UNKNOWN` hasta la auditoría bibliográfica G2.

| Campo pendiente | Fuentes afectadas |
|---|---:|
| Autor/creador verificado | 28 |
| Edición verificable | 28 |
| Idioma registrado | 28 |
| Tipo documental | 28 |
| Alcance completo/parcial | 28 |
| Año | 24 |

Se registró la procedencia remota exacta de cada archivo mediante repositorio, commit y Git blob SHA-1. El catálogo con SHA-256 y métricas está en [`catalogos/LOTE_001_ADULTEZ_MANIFEST.jsonl`](catalogos/LOTE_001_ADULTEZ_MANIFEST.jsonl); su propio SHA-256 es `410c2f043c594045e0b6c5bec6b535c56cf732c2c0b8130d9213487cfbbe4d5a`.

## 4. Correspondencia provisional con la matriz

Esta correspondencia se basa solamente en nombres de archivo y referencias ya conocidas; debe confirmarse en G2.

| Familia de la matriz | source_id candidatos | Contenido aparente |
|---|---|---|
| A07 | `DCA-000001` | Sitchin, *The 12th Planet / El duodécimo planeta*. |
| S03 | `DCA-000002`, `DCA-000008` | Khambhat/Cambay: artículo o selecciones breves. |
| A01 | `DCA-000003`, `DCA-000009` | Donnelly en inglés y español. |
| A09 | `DCA-000004`, `DCA-000011` | *Keeper/Guardian of Genesis* y *The Orion Mystery*. |
| T03 | `DCA-000005` | Verbrugghe y Wickersham, Beroso y Manetón. |
| A04 | `DCA-000006`, `DCA-000007`, `DCA-000019` | Hapgood: desplazamiento cortical y mapas antiguos. |
| A03 | `DCA-000010`, `DCA-000026` | Churchward en español e inglés. |
| S06/A10 | `DCA-000012`, `DCA-000021`, `DCA-000023`, `DCA-000024` | Geología de la Esfinge, Reader y Schoch/Bauval. |
| A08 | `DCA-000013`, `DCA-000016`, `DCA-000017` | Hancock: *America Before*, *Fingerprints* y *Magicians*. |
| S02 | `DCA-000014` | Kimura 2004 sobre Yonaguni; no parece ser el informe de 2001. |
| T02 | `DCA-000015` | Lambert y Millard, *Atra-Ḫasīs*. |
| T06 | `DCA-000018` | *Manu’s Code of Law*. |
| T10 | `DCA-000020` | Artículo sobre la edición de Taylor del manuscrito de Huarochirí; no equivale todavía al manuscrito completo. |
| T08 | `DCA-000022` | *Popol Vuh*, edición aún no identificada. |
| T05 | `DCA-000025`, `DCA-000028` | Lista real de Turín, versiones/estudios por identificar. |
| A12 | `DCA-000027` | Oppenheimer, *Eden in the East*. |

## 5. Alcance documental preliminar

La inspección selectiva de portada, inicio y final permite distinguir obras de documentos derivados sin cargar el texto integral:

- `DCA-000002` es una discusión y réplica publicada en 2003, no el artículo primario de Kathiroli et al. de 2002.
- `DCA-000006` y `DCA-000007` son componentes parciales de *Earth’s Shifting Crust*. El primero comienza alrededor de la página impresa 323 y llega a la bibliografía; el segundo comienza con el libro, declara que faltan páginas y termina a mitad de exposición. Deben relacionarse con un mismo `work_id`, sin confundirlos con duplicados.
- `DCA-000008` es una nota web breve de 2012 sobre Khambhat, no un informe técnico.
- `DCA-000009` es un documento compuesto: predomina el español hasta aproximadamente la línea 4.800 y después continúa en inglés. No constituye una traducción española íntegra y homogénea.
- `DCA-000011` no es el texto de *The Orion Mystery*: es un resumen derivado de Bookey con cuestionarios, y debe tratarse sólo como ayuda de navegación.
- `DCA-000013` es una muestra de *América antes* que termina en la página impresa 29.
- `DCA-000014` es el artículo completo aparente de Kimura de 2004 (pp. 947–953), no el informe de 2001.
- `DCA-000020` es la reseña de Frank Salomon de 1991 sobre la edición de Taylor; no contiene el manuscrito integral de Huarochirí.
- `DCA-000023` es una muestra de *Rewriting the History of the Great Sphinx* de Colin Reader (Archaeopress, 2026): incluye sumario e introducción, pero no los capítulos anunciados hasta la página 240.
- `DCA-000028` es una síntesis de cuatro páginas sobre el Canon Real de Turín, no una edición primaria.

Los demás registros aparentan cubrir obras o artículos completos, pero esta conclusión seguirá siendo provisional hasta comprobar su secuencia interna. En especial, la presencia de todas las páginas no garantiza calidad OCR suficiente para una cita literal.

### Duplicación bibliográfica no exacta

No hay duplicados de bytes, pero sí relaciones que deben conservarse:

- `DCA-000003` y `DCA-000009`: manifestaciones del mismo trabajo de Ignatius Donnelly; la segunda es compuesta y bilingüe.
- `DCA-000010` y `DCA-000026`: ediciones/traducciones del mismo trabajo de James Churchward.
- `DCA-000006` y `DCA-000007`: fragmentos complementarios de un mismo trabajo de Charles Hapgood.

## 6. Fragmentación y trazabilidad

Se crearon 1.467 fragmentos locales de hasta 12.000 caracteres, con dos líneas de solapamiento. Cada fragmento conserva:

- `source_id`;
- SHA-256 del original y de la copia normalizada;
- líneas y offsets de caracteres;
- páginas y encabezado cuando se detectan;
- SHA-256 del contenido del fragmento.

Se comprobó que los 1.467 fragmentos regresan correctamente a sus offsets y hashes. El índice contiene texto y permanece fuera de Git.

## 7. Decisión de puertas

### G0 — `GO`

El lote remoto quedó fijado por repositorio, commit y hash del contenedor. La ausencia declarada del *Mahābhārata* está documentada.

### G1 — `GO`

No existen fallos bloqueantes de integridad. Los originales y normalizados pasan la verificación de hashes.

### G2 — `HOLD`

Antes de admitir fuentes al corpus activo hay que confirmar edición, idioma, autoría y condición completa/parcial. También se deben resolver las tres incidencias mecánicas indicadas.

G3 (canon) y G4 (piloto de extracción) no han comenzado.
