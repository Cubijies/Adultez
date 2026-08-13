# Auditoría de ingesta — PDFs LOTE-002 (evidencia primaria)

**Versión:** 1.0
**Fecha:** 12 de agosto de 2026
**Procedencia:** subidos por el usuario al repo (rama `main` de `Cubijies/Adultez`); recuperados a `corpus_local/civilizaciones_anteriores/00_entrada_pdf/` (área ignorada por Git, según el protocolo: los originales no se versionan).
**Método:** extracción de texto con `pypdf` (venv local); preservación del PDF íntegro como complemento no textual.

## 1. Documentos recibidos (4 PDFs)

| Archivo | Páginas | SHA-256 | Correspondencia con el corpus |
|---|---|---|---|
| `Surface_luminescence_dating.pdf` | 17 | `62f7be11…2da8` | **NUEVO** — verifica en nivel D la SLD de Guiza |
| `Review_of_the_media_reports_and_research.pdf` | 12 | `fe4b8643…0dce` | **NUEVO** — revisión 2025 de la controversia Khambhat |
| `KimuraOcean04.pdf` | 7 | `4e0a3092…76ed` | Equivale al TXT `DCA-000014` (Kimura 2004) |
| `A_new_archaeological_find_in_the_Gulf_of.pdf` | 2 | `3cd85f3e…c5de` | Equivale al TXT `DCA-000002` (Discusión/Réplica JGSI 2003) |

## 2. Resultado de la revisión

**A. SLD de Guiza (Liritzis & Vafiadou 2015, *Journal of Cultural Heritage* 16):**
- Datación por luminiscencia superficial (SLD) de **Sphinx Temple** y **Valley Temple**.
- Edades: Sphinx Temple `2220±220`, `1190±340`, `2740±640`, `3100±540 a.C.`; Valley Temple `3060±470` y `1050±540 a.C.`.
- Coherentes con la **IV Dinastía (ca. 2613–2494 a.C.)**.
- **Cita clave:** "none of the dates for the Sphinx Temple or for Giza as a whole corroborates a prehistoric age".
- **Efecto:** **REFUERZA** la edad dinástica de los templos y contradice una edad prehistórica; pero fechó los **templos**, no el recinto/core body tallado.

**B. Revisión Khambhat (Ramakrishna Rao 2025):**
- Documenta la cronología 2000→2024 de la controversia NIOT.
- Confirma: sonar 2000 (paleocanal >9 km, 20–40 m), muestras con datación a ~9500 YBP, artefactos (abalorio de chert, cuchillo, cerámica, huesos).
- Críticas persistentes (Mahadevan, Parpola, Justin Morris 2024): datación por una sola pieza de madera, contexto de dragado, falta de excavación in-situ.
- Tras 23 años **no hay conclusión firme**; NIOT sostiene que los objetos son in situ.
- **Efecto:** **NEUTRAL** — anomalía legítima, no ciudad establecida.

**C. Kimura 2004 (Yonaguni):** equivalencia verificada con `DCA-000014`. **Corrección importante:** la datación ¹⁰Be de 4.000–3.000 años corresponde a la torre costera **Sanninu-dai**, no a la pirámide submarina (YUP, ~10.000 a.C. según Kimura). El hogar de Sanninu-dai dio ¹⁰Be/14C de 1.600 BP.

**D. Discusión/Réplica JGSI 2003:** equivalencia verificada con `DCA-000002`. Confirma el abalorio de chert (~6000 a.C.) y el nivel del mar -40 m en -9500 BP.

## 3. Decisión

- Los 4 PDFs quedan **preservados** en `corpus_local` (no versionados, por derechos y tamaño).
- El texto extraído queda en `30_selecciones_pdf/` (también ignorado).
- Los **hallazgos** se registran en `g4_masiva/REGISTRO_EVIDENCIA_PRIMARIA.jsonl` (nivel D) y en el informe de evidencia.
- **No se altera el canon** (roles/documental); la SLD de Guiza y la revisión Khambhat **reducen aún más el peso probatorio** de las afirmaciones de civilización avanzada en esos dos casos.

## 4. Pendientes (sin cambio)
- Datación cosmogénica del recinto/core body de la Esfinge (no publicada).
- Informe Kimura 2001 íntegro (no localizado).
- Expediente NIOT completo (no accesible).
- Artículo primario Kathiroli et al. 2002 (JGSI 60:4) de pago (la discusión 2003 lo resume).
