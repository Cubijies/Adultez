# Protocolo de construcción del canon y corpus

**Proyecto:** investigación sobre posibles civilizaciones tecnológicas anteriores
**Versión:** 1.0
**Fecha:** 11 de agosto de 2026
**Estado:** operativo inicial; se revisará después del primer lote real de fuentes

## 1. Decisión de trabajo

Los archivos deben subirse como `.txt` siempre que sea posible. No es necesario pegarlos en el chat. Se procesarán localmente con `scripts/corpus_pipeline.py`, de modo que el inventario, la búsqueda y la selección de pasajes no consuman contexto conversacional innecesario.

Para libros muy grandes se aceptan selecciones. Una selección útil debe incluir identificación de la edición, ubicación interna y contexto suficiente. En textos como el *Mahābhārata* no hace falta entregar la obra completa si se proporcionan los libros, capítulos y versos relevantes con su aparato mínimo.

## 2. Principios no negociables

1. **Original inmutable.** Nunca se corrige, reemplaza ni sobrescribe silenciosamente un archivo recibido.
2. **Fuente y derivado separados.** Normalizaciones, fragmentos, resúmenes, traducciones y afirmaciones extraídas son derivados.
3. **Trazabilidad.** Toda afirmación debe poder volver al documento, edición y pasaje que la originó.
4. **Atribución antes de evaluación.** Primero se registra “el autor afirma X”; después, por separado, se evalúa X.
5. **Sin exclusión por heterodoxia.** Una fuente no queda fuera por ser alternativa, esotérica o minoritaria. Su función y calidad documental se describen explícitamente.
6. **Sin promoción por autoridad.** Una publicación académica no se convierte automáticamente en verdad; conserva ventajas de método, datos y revisión que deben auditarse.
7. **No mezclar ausencia con refutación.** `NO_ENCONTRADO`, `INSUFICIENTE`, `AMBIGUO`, `CONTRADICTORIO` y `REFUTADO` son estados distintos.
8. **No convertir mito en dato material sin puente.** Autenticidad textual, historicidad, cronología y corroboración arqueológica se evalúan por separado.
9. **No convertir una catástrofe en civilización.** La existencia de un impacto, erupción o inundación no demuestra qué sociedad pudo haber sufrido el evento.
10. **Canon versionado.** La admisión, función o prioridad de una fuente puede cambiar sin borrar su historial.

## 3. Estructura física

Los textos completos o protegidos no se incorporarán a Git. Se mantendrán en un área local ignorada:

```text
corpus_local/civilizaciones_anteriores/
├── 00_entrada/          # archivos tal como se reciben
├── 10_normalizados/     # copias UTF-8/LF; el contenido no se reescribe
├── 20_indices/          # manifiesto, chunks y mapas mecánicos
├── 30_selecciones/      # pasajes extraídos con línea/página
├── 40_extracciones/     # fichas de afirmaciones y relaciones
├── 50_auditorias/       # informes de integridad y cobertura
└── 90_cuarentena/       # archivos corruptos, duplicados dudosos o sin identidad
```

En Git se conservarán únicamente:

- protocolo y reglas;
- esquemas y plantillas;
- scripts reproducibles;
- catálogos bibliográficos y metadatos no extensos;
- resultados sintéticos que no reproduzcan libros enteros.

## 4. Formato de entrega

### 4.1. Archivos completos

Se prefiere un archivo por obra y edición:

```text
Apellido_Año_TituloCorto_Idioma.txt
```

No es obligatorio renombrarlo. El script asignará un identificador provisional.

### 4.2. Selecciones de obras grandes

Nombre recomendado:

```text
Apellido_Año_Titulo_seleccion_capitulos-o-paginas.txt
```

Cada selección debe indicar, cuando sea posible:

```text
=== CASSANDRA SOURCE METADATA ===
title: Título completo
creators: Autor; Editor
year: año de esta edición
edition: editorial, edición o reimpresión
translator: nombre, si corresponde
language: código o nombre del idioma
scope: selección
included_units: páginas/capítulos/versos incluidos
extraction_method: texto digital / OCR / transcripción manual
copy_source: biblioteca, URL o procedencia
omissions: páginas ilegibles, faltantes u otras omisiones
=== BEGIN SOURCE TEXT ===
```

La cabecera forma parte del original y nunca se retira. Como alternativa preferida para metadatos extensos, se puede entregar un archivo lateral `nombre.txt.meta.json`. El lateral tiene precedencia si ambos existen.

### 4.3. Marcadores de página

Si el TXT procede de PDF u OCR, se recomienda conservar páginas así:

```text
[[PAGE: 123]]
```

No deben inventarse páginas cuando la edición digital no las tenga. En ese caso se citarán líneas estables de la copia normalizada y la división interna de la obra.

### 4.4. Tablas, notas e imágenes

- Las notas al pie o finales deben conservar su número.
- Las tablas pueden mantenerse como texto monoespaciado o Markdown.
- Una imagen importante debe acompañarse de su pie y página; puede subirse aparte.
- No se debe eliminar bibliografía, índice ni aparato de notas de un libro alternativo: a menudo contienen la ruta hacia sus fuentes primarias.

### 4.5. Codificación y compatibilidad

- Formato textual de ingestión: `.txt` sin compresión y sin DRM.
- Codificación preferida: UTF-8.
- También se detectan UTF-8 con BOM, UTF-16/32 con BOM, Windows-1252 e ISO-8859-1; los dos últimos generan advertencia.
- Se preservan signos diacríticos, caracteres cuneiformes, griego, sánscrito y transliteraciones Unicode.
- Los saltos CRLF/CR se convierten a LF únicamente en la copia normalizada.
- Un binario renombrado como `.txt`, un archivo vacío o un texto ilegible no se fuerza: pasa a revisión/cuarentena.
- PDF, EPUB e imágenes pueden acompañar al TXT para conservar paginación o figuras, pero el índice automatizado v1 se construye desde TXT.

## 5. Metadatos mínimos

### Obligatorios antes de admitir una fuente al corpus principal

```text
source_id
Título
Autor, editor o institución
Año
Idioma
Tipo de fuente
Alcance: completa / selección / fragmento / desconocido
Edición o descripción suficiente para distinguirla
Archivo y hash SHA-256
Procedencia de la copia
```

### Deseables

```text
Editorial
ISBN / DOI / identificador de catálogo
Traductor
Fecha de la edición original
Páginas totales y páginas recibidas
Método de extracción
Estado del OCR
Derechos o condición de acceso
Notas de integridad
```

Un archivo sin metadatos no se desecha: entra como `METADATA_PENDING` o en cuarentena hasta identificarlo.

## 6. Identificadores

- **Obra intelectual que agrupa ediciones/traducciones:** `WCA-000001`
- **Fuente/documento/manifestación recibida:** `DCA-000001`
- **Fragmento recuperable:** `PAS-DCA-000001-L0000120-L0000220`
- **Afirmación:** `CLM-000001`
- **Relación:** `REL-000001`
- **Auditoría:** `AUD-000001`
- **Versión de registro:** número entero creciente

El identificador no depende del nombre del archivo. Un hash idéntico permite detectar duplicados aunque cambie el nombre.

## 7. Clasificación multidimensional

No se usará una única etiqueta que mezcle contenido, autoridad y certeza.

### 7.1. Dominio

```text
MET  metodología y epistemología
TEC  tecnofirmas y detección
ARQ  arqueología y capacidades prehistóricas
GEO  geología, estratigrafía y preservación
SUB  paisajes sumergidos
CAT  catástrofes y resets
TXT  textos y tradiciones antiguas
ALT  autores y modelos alternativos/esotéricos
SIT  sitios disputados
OOP  OOPArts y objetos anómalos
HIS  historia de las ideas y recepción
```

### 7.2. Tipo documental

```text
ARTICULO_PARES
REVISION
INFORME_TECNICO
DATOS_PRIMARIOS
INFORME_EXCAVACION
EDICION_CRITICA
TEXTO_ANTIGUO
MONOGRAFIA_ACADEMICA
HIPOTESIS_ALTERNATIVA
ARCHIVO_TESTIMONIAL
DIVULGACION
RETRACTACION_CRITICA
```

### 7.3. Función en la investigación

```text
FORMULA_HIPOTESIS
APORTA_EVIDENCIA
APORTA_CONTEXTO
APORTA_METODO
APOYA
CUESTIONA
REFUTA
RESPONDE_CRITICA
TRANSMITE_TRADICION
DOCUMENTA_RECEPCION
```

Una fuente puede tener varias funciones.

### 7.4. Posición frente a una afirmación

```text
FAVORABLE
CRITICA
NEUTRA
MIXTA
NO_APLICA
```

### 7.5. Estado de acceso

```text
COMPLETA
SELECCION_SUFICIENTE
SELECCION_INSUFICIENTE
FRAGMENTARIA
SOLO_RESUMEN
SOLO_METADATOS
NO_LOCALIZADA
```

## 8. Canon y corpus: definición operativa

### 8.1. Corpus total

Todo documento identificado y conservado, incluso si es débil, falso, retractado o contradictorio. Su inclusión significa “forma parte de la investigación”, no “es verdadero”.

### 8.2. Corpus activo

Fuentes con texto suficiente y metadatos mínimos que ya pueden usarse en extracción o contraste.

### 8.3. Canon nuclear

Fuentes a las que el proyecto deberá regresar constantemente porque cumplen al menos una función indispensable:

- formulan de primera mano una hipótesis central;
- publican la evidencia primaria de un caso;
- constituyen la edición crítica de un texto antiguo;
- presentan la crítica técnica principal;
- definen el método de detección o de evaluación.

### 8.4. Canon de contraste

Fuentes indispensables para comprobar explicaciones alternativas, falsos positivos, problemas de procedencia o críticas a una teoría nuclear.

### 8.5. Corpus auxiliar

Obras de contexto, recepción, divulgación, entrevistas y repeticiones que ayudan a rastrear la historia de una afirmación, pero no deben sustituir su fuente original.

### 8.6. Cuarentena

Archivos sin identidad suficiente, corruptos, presuntamente adulterados, de procedencia desconocida o que no permiten distinguir cita de comentario. Permanecen disponibles, pero no alimentan conclusiones hasta resolver el problema.

## 9. Admisión al canon

La decisión se tomará después de inventariar el material. Cada candidatura responderá:

1. ¿Es la fuente más próxima disponible a la afirmación o al dato?
2. ¿Puede identificarse la edición y ubicarse el pasaje?
3. ¿Es necesaria para una familia teórica del mapa?
4. ¿Aporta algo que no pueda sustituirse por una fuente mejor?
5. ¿Su texto está completo o la selección cubre la cuestión pertinente?
6. ¿Tiene una contraparte crítica o un control adecuado cuando lo necesita?
7. ¿Podemos citarla sin atribuirle algo que no dice?

Estados:

```text
CANDIDATA
CANON_NUCLEAR
CANON_CONTRASTE
CORPUS_ACTIVO
CORPUS_AUXILIAR
CUARENTENA
RETIRADA_DEL_CANON
```

Una fuente retractada puede seguir en el corpus como historia de una afirmación, aunque quede fuera del canon probatorio.

## 10. Duplicados, ediciones, traducciones y selecciones

1. Dos archivos con el mismo SHA-256 son un duplicado exacto: comparten `source_id` y se conservan todas las rutas recibidas.
2. Dos OCR de la misma edición con bytes diferentes conservan identificadores distintos hasta cotejarlos. Se elige una copia de referencia, pero no se borra la otra.
3. Cada edición, revisión o traducción con cambios sustantivos recibe `source_id` propio y puede compartir un `work_id`.
4. Una traducción nunca sustituye silenciosamente al original; se relaciona mediante `TRANSLATION_OF`.
5. Una selección recibida es un documento parcial por derecho propio. Si también existe el texto completo del cual se obtuvo, usa `parent_source_id` y `EXCERPT_OF`; si no existe localmente, conserva la referencia bibliográfica de la obra madre.
6. Versiones abreviadas, ediciones populares y reimpresiones se cotejan antes de tratarlas como equivalentes.
7. El algoritmo v1 automatiza duplicados exactos. Duplicados aproximados, OCR alternativos y ediciones encubiertas quedan para auditoría bibliográfica/humana.
8. Relaciones permitidas entre fuentes: `SAME_WORK`, `SAME_EDITION`, `DUPLICATE_OF`, `EXCERPT_OF`, `TRANSLATION_OF`, `SUPERSEDES`, `CITES`.

El registro histórico `source_registry.jsonl` nunca reutiliza un identificador, aunque el archivo deje de estar presente. Cada inventario anterior se archiva localmente antes de generar el siguiente.

## 11. Flujo de elaboración

### Fase 0 — Recepción

- conservar nombre y bytes originales;
- registrar fecha y procedencia;
- calcular SHA-256;
- no interpretar aún.

### Fase 1 — Inventario mecánico

- detectar codificación;
- contar bytes, caracteres, palabras y líneas;
- detectar marcadores de página y posibles encabezados;
- buscar duplicados exactos;
- unir el archivo con sus metadatos laterales.

### Fase 2 — Auditoría de integridad

- verificar que el archivo abre;
- detectar caracteres de reemplazo, texto vacío, OCR roto y líneas anómalas;
- comprobar si se declara completo o parcial;
- identificar páginas/capítulos faltantes cuando sea posible.

### Fase 3 — Normalización reversible

- crear copia UTF-8 con saltos LF;
- retirar únicamente BOM y normalizar saltos de línea;
- no modernizar ortografía ni corregir OCR dentro de la fuente;
- registrar el hash de original y normalizado.

### Fase 4 — Segmentación

Orden preferido:

1. parte/libro/tablilla;
2. capítulo/sección;
3. página;
4. párrafo;
5. ventana mecánica si no existe estructura.

Todo fragmento conserva `source_id`, encabezado, líneas inicial/final, páginas detectadas y hash.

### Fase 5 — Mapeo temático

Cada fuente y pasaje puede relacionarse con:

- identificadores de la matriz (`H01`, `P01`, `T01`, `A01`, `S01`, `O01`, etc.);
- dominio;
- teoría o caso;
- personas, lugares, objetos, fechas y eventos;
- otras fuentes citadas;
- afirmaciones que apoya, cuestiona o contextualiza.

El mapeo automático solo produce candidatos. La asignación canónica requiere revisión.

### Fase 6 — Extracción de afirmaciones

Cada ficha deberá separar:

```text
AFIRMACION_ATRIBUIDA    qué sostiene la fuente
PASAJE                  cita o ubicación que lo demuestra
PARAFRASIS_CONTROLADA   formulación breve sin ampliar el sentido
TIPO_DE_AFIRMACION      textual / empírica / cronológica / causal / interpretativa
OBJETO                  sitio, evento, texto o fenómeno
FECHA_AFIRMADA          si existe
MECANISMO               si existe
EVIDENCIA_INVOCADA      qué usa el autor
POSICION                 favorable / crítica / mixta
EVALUACION_DEL_PROYECTO análisis separado
VACIO                    qué falta para comprobarla
```

### Fase 7 — Cotejo

No se compararán libros enteros como bloques. Se compararán afirmaciones atómicas:

```text
CLM-000123
├── formulada por DCA-000010
├── cita evidencia de DCA-000042
├── apoyada por DCA-000077
├── cuestionada por DCA-000081
├── depende de traducción DCA-000115
└── estado provisional: CONTRADICTORIA
```

### Fase 8 — Canonización

- revisar cobertura de todas las familias;
- evitar un canon compuesto solo por proponentes o solo por críticos;
- asignar función, no prestigio genérico;
- documentar por qué entra cada fuente;
- versionar los cambios.

## 12. Reglas de extracción

1. Una afirmación por ficha siempre que sea posible.
2. Conservar modales: “podría”, “sugiere” y “demuestra” no son equivalentes.
3. No reemplazar “antiguo” por una fecha si la fuente no la da.
4. Distinguir fecha del objeto, del estrato, de la muestra y de la construcción.
5. Distinguir material hallado *in situ* de material dragado, comprado o sin procedencia.
6. No atribuir al autor una conclusión que aparece solo en el prólogo, editor o comentarista.
7. En traducciones, registrar traductor y, cuando sea decisivo, término original.
8. En textos antiguos, separar fecha del acontecimiento narrado, fecha de composición y fecha del manuscrito conservado.
9. En literatura alternativa, conservar notas, figuras y bibliografía; no extraer solo frases llamativas.
10. En críticas, registrar exactamente qué proposición se critica: una objeción parcial no refuta necesariamente todo el modelo.
11. Toda corrección de OCR se hace en una capa de anotación y conserva lectura original/corregida.
12. Si el contexto cambia el significado, ampliar la selección; nunca reducirla para forzar una coincidencia.

## 13. Obras grandes y selecciones

Una selección puede considerarse **suficiente** cuando contiene:

- portada o ficha de la edición;
- índice relevante;
- capítulo/sección completos cuando el argumento depende de su desarrollo;
- páginas anterior y posterior si el pasaje aislado es ambiguo;
- todas las notas y figuras citadas por la selección;
- bibliografía utilizada en ese capítulo;
- declaración explícita de lo que fue omitido.

### Regla especial para el *Mahābhārata*

Cada pasaje deberá incluir:

```text
parvan
capítulo y versos
edición sánscrita o repositorio textual
traductor y edición
texto original o transliteración, si está disponible
mínimo contexto anterior/posterior
nota sobre variantes de la edición crítica
origen de la cita moderna que lo interpreta tecnológicamente
```

No se incorporará como prueba una “cita nuclear” viral sin ubicación verificable.

## 14. Auditorías

### AUD-0 — Integridad de archivo

- hash reproducible;
- archivo legible;
- original no modificado;
- duplicados identificados.

### AUD-1 — Identidad bibliográfica

- título, autor, año, edición, idioma y alcance;
- correspondencia entre archivo y metadatos.

### AUD-2 — Calidad textual

- OCR y codificación;
- páginas o secciones faltantes;
- notas, tablas y figuras necesarias;
- marcador `COMPLETA`, `SELECCION_SUFICIENTE` o inferior justificado.

### AUD-3 — Trazabilidad de fragmentos

- cada pasaje vuelve a líneas/páginas del original;
- los límites no alteran el sentido;
- hash del fragmento.

### AUD-4 — Fidelidad de extracción

- afirmación atribuida fiel;
- cita suficiente;
- paráfrasis sin adiciones;
- evaluación separada.

### AUD-5 — Mapeo y contradicción

- relación correcta con teorías/casos;
- fuentes favorables y críticas identificadas;
- contradicciones explícitas y no fusionadas.

### AUD-6 — Admisión canónica

- función indispensable demostrada;
- cobertura equilibrada;
- decisión y fecha registradas;
- ausencia de una fuente mejor explicada.

Resultados posibles:

```text
PASS
PASS_WITH_WARNINGS
FAIL_CORRECTABLE
FAIL_BLOCKING
NOT_APPLICABLE
```

### Responsabilidad de la auditoría

| Control | Automático | Humano |
|---|---:|---:|
| Hash, tamaño, codificación, líneas y duplicado exacto | Sí | Revisa incidencias |
| Página/encabezado/chunk candidato | Sí | Confirma estructura real |
| Identidad de obra, edición y traducción | Propone | Decide |
| Integridad y suficiencia de una selección | Señala vacíos detectables | Decide |
| Fidelidad de cita y paráfrasis | Comprueba ubicación/hash | Decide significado/contexto |
| Relación temática y contradicción | Propone candidatos | Confirma |
| Admisión al canon y función probatoria | No | Decide y documenta |

## 15. Control de errores y no invención

- Ningún campo desconocido se completa por intuición: se usa `null` o `UNKNOWN`.
- Los metadatos inferidos del nombre se marcan `inferred`, nunca `verified`.
- El resumen automático no se considera cita.
- La búsqueda por palabras no demuestra relación conceptual; solo propone pasajes.
- Una fecha mencionada en una nota moderna no se atribuye automáticamente al texto antiguo.
- Las fuentes secundarias no rellenan silenciosamente lagunas de una fuente primaria.
- Si dos ediciones discrepan, ambas lecturas se conservan.

## 16. Economía de tokens

1. Los textos completos permanecen en archivos locales.
2. Python realiza inventario, hashes, segmentación y búsqueda.
3. Al chat solo llegan:
   - metadatos resumidos;
   - lista de pasajes candidatos;
   - fragmentos estrictamente necesarios;
   - contradicciones que requieren razonamiento.
4. El tamaño normal de revisión será un capítulo o entre 5 y 20 pasajes relacionados, no un libro entero.
5. Los resultados se escriben en archivos antes de generar una síntesis conversacional.

## 17. Comandos de trabajo

```bash
# Crear la estructura local
python scripts/corpus_pipeline.py init

# Inventariar lo subido
python scripts/corpus_pipeline.py inventory

# Auditar integridad y metadatos
python scripts/corpus_pipeline.py audit

# Crear fragmentos locales recuperables
python scripts/corpus_pipeline.py chunk

# Buscar candidatos sin enviar el libro al chat
python scripts/corpus_pipeline.py search --query "erosión precipitación Esfinge" --top 20

# Extraer un rango exacto para revisión
python scripts/corpus_pipeline.py select --source-id DCA-000001 --lines 120:220

# Verificar que los originales no cambiaron
python scripts/corpus_pipeline.py verify
```

## 18. Primera auditoría después de la carga

Al recibir los TXT se ejecutará primero una auditoría sin análisis de contenido. El reporte deberá responder:

- cuántos archivos y obras hay;
- cuáles son completos, selecciones o desconocidos;
- qué duplicados existen;
- qué codificaciones/OCR presentan problemas;
- qué fuentes carecen de edición;
- qué entradas de la matriz cubre cada documento;
- qué bibliografía imprescindible continúa realmente ausente.

Solo después se propondrá el **canon v1**. De esta manera el canon dependerá del corpus real y no de lo que suponemos tener.

## 19. Entregables y puertas de aprobación

### Formatos

| Entregable | Formato principal | Contenido textual extenso |
|---|---|---:|
| Registro histórico de identificadores | JSONL | No |
| Manifiesto vigente de fuentes | JSONL validable con esquema | No |
| Auditoría inicial y auditorías por fase | Markdown + JSONL si se automatiza | No |
| Índice de fragmentos | JSONL local | Sí; no se incorpora a Git |
| Selección para revisión | TXT/Markdown con líneas y hashes | Solo el contexto necesario |
| Fichas de afirmaciones | JSONL validable con esquema | Citas puntuales |
| Matriz canon/corpus/contraste | Markdown o CSV + decisiones | No |
| Informe de contradicciones y vacíos | Markdown | Citas puntuales |
| Síntesis final | Markdown | Solo evidencia necesaria |

### Puertas

1. **G0 — Recepción cerrada del lote.** Se confirma qué archivos pertenecen al lote; no implica que estén completos.
2. **G1 — Inventario aceptado.** Se revisan duplicados, corrupciones y cambios de bytes. Un `FAIL_BLOCKING` impide avanzar con esa fuente, no con todo el corpus.
3. **G2 — Metadatos y alcance aceptados.** Se aprueban obra, edición, idioma y condición completa/parcial; las fuentes irresolubles pasan a cuarentena.
4. **G3 — Canon v1 aprobado.** Se presenta la propuesta de canon nuclear, contraste y auxiliar con justificación por fuente. No se canoniza automáticamente al subir.
5. **G4 — Piloto de extracción aprobado.** Se extraen de 5 a 20 afirmaciones de familias diferentes y se revisan fidelidad, granularidad y costo en tokens.
6. **G5 — Extracción principal autorizada.** Solo después del piloto se procesa el resto por expedientes priorizados.
7. **G6 — Cierre de expediente.** Se aprueban contradicciones, incertidumbres, faltantes decisivos y estado provisional; el expediente sigue siendo versionable.

En cada puerta la decisión se registra como `GO`, `RETURN_FOR_CORRECTION` o `HOLD`. El usuario conserva la aprobación final de G3, G4 y G6.
