# Índice maestro — Investigación: civilizaciones tecnológicas anteriores

**Proyecto:** Cubijies/Adultez (rama `arena/019ff6a3-adultez`)
**Versión del índice:** 1.0 · **Fecha:** 12 de agosto de 2026
**Función:** navegar todos los documentos, registros y scripts producidos. Los originales (28 TXT y PDFs) se preservan en `corpus_local/` (ignorado por Git), no versionados.

---

## 1. Marco y protocolo
| Documento | Contenido |
|---|---|
| `PROTOCOLO_CANON_CORPUS_V1.md` | Principios, estructura física del corpus, formato de entrega, reglas de incorporación. |
| `MATRIZ_FUENTES_V1.md` | Matriz maestra de hipótesis, tradiciones, sitios, OOPArts y su estado probatorio. |
| `FUENTES_PENDIENTES_IMPRESCINDIBLES_V1.md` | Lista práctica de literatura pendiente y criterio de prioridad. |

## 2. Canon y lote 001
| Documento | Contenido |
|---|---|
| `AUDITORIA_INGESTA_LOTE_001_V1.md` | Auditoría de ingesta de los 28 TXT (G0/G1 GO, G2 HOLD). |
| `G2_METADATOS_LOTE_001_V1.md` | Metadatos bibliográficos de los 28 documentos (propuesta). |
| `PROPUESTA_CANON_G3_V1.md` | Propuesta de canon: corpus activo/contraste/tradicional/alternativo/parcial/orientativo. |
| `canon/LOTE_001_CANON_REGISTRY_V1.jsonl` | Registro de canon: 28 roles únicos + etiquetas no excluyentes. |
| `catalogos/LOTE_001_ADULTEZ_MANIFEST.jsonl` | Catálogo histórico (hashes, métricas). SHA-256 `410c2f04…4d5a`. |
| `scripts/check_canon_registry.py` | Verificador de invariantes del canon (28 roles, provisionales, incidencias). |

## 3. Esquemas y plantillas
| Documento | Contenido |
|---|---|
| `esquemas/claim_record.schema.json` | Esquema de afirmación **v2.0** (hash_ref, category, relation_semantic, matrix_id). |
| `esquemas/CHANGELOG_CLAIM_V2.md` | Cambios P2–P6 aplicados al esquema (v1.0→v2.0). |
| `esquemas/source_record.schema.json` | Esquema de registro de fuente. |
| `plantillas/FUENTE.meta.example.json` | Plantilla de metadatos de fuente. |
| `plantillas/AFIRMACION.example.json` | Plantilla de afirmación. |

## 4. Extracción y evaluación (G4)
| Documento | Contenido |
|---|---|
| `g4_piloto/AFIRMACIONES_PILOTO_G4.jsonl` | 12 afirmaciones del piloto adversarial (Esfinge: Schoch vs. Gauri). |
| `g4_piloto/AUDITORIA_PILOTO_G4_V1.md` | Auditoría del piloto (tabla, relaciones, trazabilidad, recomendación). |
| `g4_masiva/LOTE_ACTIVO_AFIRMACIONES_V1.jsonl` | Lote 1 de extracción masiva (18 afirmaciones, corpus activo). |
| `g4_masiva/REGISTRO_CONSOLIDADO_AFIRMACIONES_V1.jsonl` | **Registro consolidado de 37 afirmaciones** con IDs globales y 15 relaciones. |
| `g4_masiva/IDMAP_CONSOLIDADO.jsonl` | Mapa de re-identificación de claim_id. |
| `g4_masiva/EVALUACION_LOTE_V1.md` | Evaluación probatoria por tema (estado, falsación). |
| `g4_masiva/AUDITORIA_LOTE_ACTIVO_V1.md` | Auditoría del lote 1. |

## 5. Evidencia primaria (Fases 1–5 + filología)
| Documento | Contenido |
|---|---|
| `g4_masiva/PLAN_EVIDENCIA_PRIMARIA_V1.md` | Prioridades de búsqueda y criterio de falsabilidad. |
| `g4_masiva/REGISTRO_EVIDENCIA_PRIMARIA.jsonl` | **33 hallazgos** de evidencia primaria (Esfinge, mapas, YD, Yonaguni, Khambhat, Naacal, Mahābhārata, Sundaland, Anticitera). |
| `g4_masiva/INFORME_EVIDENCIA_PRIMARIA_V1.md` | Informe consolidado de evidencia primaria + impacto sobre el canon. |
| `g4_masiva/NOTA_FILOLOGICA_MAHABHARATA_V1.md` | **Cotejo filológico resuelto:** arma de Aśvatthāman = Agneya-astra (fuego), no nuclear; corrección de 3.186–189. |
| `AUDITORIA_INGESTA_PDF_LOTE_002_V1.md` | Ingesta de 4 PDFs de evidencia (SLD Guiza, Khambhat, Kimura, JGSI). |

## 6. Informes finales
| Documento | Contenido |
|---|---|
| `INFORME_REDACCION_V1.md` | Informe inicial (pre-evidencia). |
| `INFORME_REDACCION_V2.md` | **Informe final** integrando la evidencia primaria. |
| `INDICE_MAESTRO_V1.md` | Este índice. |

## 7. Scripts
| Script | Función |
|---|---|
| `scripts/corpus_pipeline.py` | Inventario, chunk, search, select, audit, verify, **pagemap** (P1), **validate-claims** (P7). |
| `scripts/generar_piloto_g4.py` | Genera y valida el piloto G4. |
| `scripts/generar_extraccion_masiva.py` | Genera el lote 1 de extracción. |
| `scripts/generar_registro_consolidado.py` | Consolida piloto+lotes en el registro único (37 afirmaciones). |
| `scripts/check_canon_registry.py` | Verifica invariantes del canon. |

## 8. Área local (no versionada, `corpus_local/`)
- `00_entrada/` — 28 TXT originales.
- `00_entrada_pdf/` — 4 PDFs de evidencia primaria.
- `00_entrada_mb/` — Mahābhārata (Vol. VII PDF, Dronabhisheka/Vaivahika txt).
- `10_normalizados/` — copias normalizadas (28).
- `20_indices/` — manifiesto, chunks, page-maps.
- `30_selecciones/`, `30_selecciones_pdf/`, `30_selecciones_mb/` — selecciones y texto extraído.
- `50_auditorias/` — auditorías.
