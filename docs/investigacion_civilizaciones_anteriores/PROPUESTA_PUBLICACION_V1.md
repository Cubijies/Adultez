# Propuesta de publicación — PR a `main`

**Versión:** 1.0
**Fecha:** 12 de agosto de 2026
**Rama de trabajo:** `arena/019ff6a3-adultez`
**Destino:** `main` (repositorio `Cubijies/Adultez`)

> Este documento describe **qué** publicar y **cómo** hacerlo de forma segura. No se ejecuta el push/PR sin tu aprobación explícita.

## 1. Alcance: qué publicar

Solo los **artefactos genéricos de investigación** (protocolos, esquemas, plantillas, scripts, catálogos y resultados sintéticos). **No** se publican los 28 TXT originales ni los PDFs de evidencia (por derechos de las fuentes y tamaño).

| Grupo | Archivos | ¿Incluir en PR? |
|---|---|---|
| **Documentos de investigación** | `docs/investigacion_civilizaciones_anteriores/*.md` (15) | ✅ Sí |
| **Canon** | `docs/.../canon/LOTE_001_CANON_REGISTRY_V1.jsonl` | ✅ Sí |
| **Catálogo** | `docs/.../catalogos/LOTE_001_ADULTEZ_MANIFEST.jsonl` | ✅ Sí |
| **Esquemas** | `docs/.../esquemas/*.json`, `*.md` | ✅ Sí |
| **Plantillas** | `docs/.../plantillas/*.json` | ✅ Sí |
| **G4** (piloto, masiva, evidencia) | `docs/.../g4_piloto/*`, `g4_masiva/*` | ✅ Sí |
| **Scripts** | `scripts/*.py` | ✅ Sí |
| **Pruebas** | `tests/test_corpus_pipeline.py` | ✅ Sí |
| **README** | `README.md` | ✅ Sí |
| **Originales TXT** | `*.txt` (28) | ❌ No (ya en main; no se tocan) |
| **PDFs de evidencia** | `*.pdf` (5) | ❌ No versionar (derechos/tamaño) |
| **Área local** | `corpus_local/` | ❌ No (ignorada) |

## 2. Situación de Git (importante)

El entorno sufrió reinicios que fragmentaron el historial:
- `main` (= `origin/main`, commit `d7256fb`) contiene los 28 TXT **y** los PDFs que subiste.
- La rama de trabajo `arena/019ff6a3-adultez` (HEAD `6e83f1d`) contiene los docs/scripts/README, **sin** los PDFs (se mantienen en `corpus_local`, ignorado).
- Las dos ramas tienen **historias no relacionadas** (no hay `merge-base`), por lo que un `git merge` normal falla con *"refusing to merge unrelated histories"*.

**Implicación:** el PR a `main` no puede ser un merge normal. Las opciones seguras son:

### Opción A (recomendada): push directo de los archivos de investigación a `main`
- Copiar los archivos de `docs/`, `scripts/`, `tests/` y `README.md` a un árbol basado en `origin/main`.
- Commit directo en `main` (o en una rama nueva basada en `main`) **solo** con esos archivos.
- **No** borra ni modifica los TXT ni los PDFs ya presentes.
- Ventaja: simple y seguro. Desventaja: `main` acumula los PDFs (ya están ahí), que quedan como están.

### Opción B: PR desde una rama nueva basada en `main`
- Crear `main` local, subir los docs/scripts/README en una rama `publish/...` bifurcada de `main`, y abrir PR.
- Requiere reconciliar las historias no relacionadas con `--allow-unrelated-histories`.

### Recomendación
**Opción A** es la más segura: los artefactos de investigación se añaden a `main` sin tocar los originales. Si prefieres un PR formal, se usa la **Opción B**.

## 3. Pasos propuestos (Opción A)

1. Asegurar que el árbol de `origin/main` sea la base.
2. Copiar `README.md`, `docs/investigacion_civilizaciones_anteriores/` y `scripts/`, `tests/` (archivos de investigación) a ese árbol.
3. Commit con mensaje descriptivo.
4. Push a `main`.

## 4. Verificaciones post-publicación

- Los 28 TXT en `main` permanecen **byte a byte idénticos** (verificar `git diff`).
- Los PDFs subidos no se modifican.
- `docs/` contiene el índice maestro navegable.
- `tests/` pasa (4/4).

## 5. Decisión requerida

- [ ] **Aprobar Opción A** (añadir artefactos de investigación a `main`, commit directo).
- [ ] **Aprobar Opción B** (PR formal desde rama basada en `main`).
- [ ] **Solo documentar** (dejar este documento, sin tocar `main` todavía).
