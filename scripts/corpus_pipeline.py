#!/usr/bin/env python3
"""Pipeline local y reproducible para el corpus de civilizaciones anteriores.

No usa dependencias externas ni envía texto a servicios remotos. Los originales se
leen en modo binario, se identifican por SHA-256 y nunca se escriben ni corrigen.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import math
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Iterable, Iterator

SCHEMA_VERSION = "1.0"
DEFAULT_ROOT = Path("corpus_local/civilizaciones_anteriores")
DIRS = {
    "inbox": "00_entrada",
    "normalized": "10_normalizados",
    "indexes": "20_indices",
    "selections": "30_selecciones",
    "extractions": "40_extracciones",
    "audits": "50_auditorias",
    "quarantine": "90_cuarentena",
}
MANIFEST_NAME = "manifest.jsonl"
REGISTRY_NAME = "source_registry.jsonl"
CHUNKS_NAME = "chunks.jsonl"
SOURCE_ID_RE = re.compile(r"^DCA-(\d{6})$")
TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)
HEADING_RE = re.compile(
    r"^\s*(?:"
    r"(?:chapter|cap[ií]tulo|book|libro|part|parte|section|secci[oó]n|"
    r"parvan|canto|tablet|tablilla|appendix|ap[eé]ndice)\b.*|"
    r"(?:[IVXLCDM]+|\d+)(?:[.)]|\s*[-—:]\s+).+"
    r")\s*$",
    re.IGNORECASE,
)
PAGE_RE = re.compile(
    r"^\s*(?:"
    r"\[\[\s*(?:page|p[aá]gina)\s*[:#]?\s*([^\]]+)\]\]|"
    r"[-=]{2,}\s*(?:page|p[aá]gina)\s+(.+?)\s*[-=]{2,}"
    r")\s*$",
    re.IGNORECASE,
)
MOJIBAKE_MARKERS = ("Ã", "Â", "â€", "ï»¿", "ðŸ", "�")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def json_dump_line(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True)


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json_dump_line(record) + "\n")
    temporary.replace(path)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"JSON inválido en {path}:{number}: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"Se esperaba un objeto JSON en {path}:{number}")
            records.append(value)
    return records


def paths(root: Path) -> dict[str, Path]:
    result = {key: root / value for key, value in DIRS.items()}
    result["manifest"] = result["indexes"] / MANIFEST_NAME
    result["registry"] = result["indexes"] / REGISTRY_NAME
    result["chunks"] = result["indexes"] / CHUNKS_NAME
    return result


def ensure_layout(root: Path) -> dict[str, Path]:
    result = paths(root)
    root.mkdir(parents=True, exist_ok=True)
    for key in DIRS:
        result[key].mkdir(parents=True, exist_ok=True)
    return result


def detect_and_decode(data: bytes) -> tuple[str, str, list[str]]:
    """Return text, encoding label and decoding warnings.

    UTF encodings are tried first. cp1252/latin-1 are explicit fallbacks so that a
    questionable decoding is visible instead of silently dropping characters.
    """
    warnings: list[str] = []
    if data.startswith(b"\xef\xbb\xbf"):
        return data.decode("utf-8-sig"), "utf-8-sig", warnings
    if data.startswith((b"\xff\xfe\x00\x00", b"\x00\x00\xfe\xff")):
        return data.decode("utf-32"), "utf-32", warnings
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return data.decode("utf-16"), "utf-16", warnings
    try:
        return data.decode("utf-8"), "utf-8", warnings
    except UnicodeDecodeError:
        pass
    try:
        text = data.decode("cp1252")
        warnings.append("DECODE_FALLBACK_CP1252")
        return text, "cp1252", warnings
    except UnicodeDecodeError:
        text = data.decode("latin-1")
        warnings.append("DECODE_FALLBACK_LATIN1")
        return text, "latin-1", warnings


def normalize_text(text: str) -> str:
    """Perform only reversible transport normalization: BOM and line endings."""
    if text.startswith("\ufeff"):
        text = text[1:]
    return text.replace("\r\n", "\n").replace("\r", "\n")


def split_lf_lines(text: str, keepends: bool = False) -> list[str]:
    """Split only on LF, leaving form feeds and other source characters intact."""
    if not text:
        return []
    pieces = text.split("\n")
    has_final_newline = pieces[-1] == ""
    if has_final_newline:
        pieces = pieces[:-1]
    if not keepends:
        return pieces
    result = [piece + "\n" for piece in pieces]
    if result and not has_final_newline:
        result[-1] = result[-1][:-1]
    return result


def page_label(line: str) -> str | None:
    match = PAGE_RE.match(line)
    if not match:
        return None
    return (match.group(1) or match.group(2) or "").strip()


def is_heading(line: str) -> bool:
    stripped = line.strip()
    if not stripped or len(stripped) > 160:
        return False
    if HEADING_RE.match(stripped):
        return True
    letters = [char for char in stripped if char.isalpha()]
    if 4 <= len(letters) and len(stripped) <= 100:
        upper_ratio = sum(char.isupper() for char in letters) / len(letters)
        return upper_ratio >= 0.90
    return False


def text_metrics(text: str) -> tuple[dict[str, Any], list[str]]:
    lines = split_lf_lines(text)
    words = TOKEN_RE.findall(text)
    pages = [label for line in lines if (label := page_label(line)) is not None]
    form_feed_pages = text.count("\f")
    headings = [
        {"line": index, "text": line.strip()}
        for index, line in enumerate(lines, 1)
        if is_heading(line)
    ]
    controls = sum(
        1 for char in text if unicodedata.category(char) == "Cc" and char not in "\n\t\f"
    )
    nonspace = sum(1 for char in text if not char.isspace())
    alpha = sum(1 for char in text if char.isalpha())
    long_lines = sum(1 for line in lines if len(line) > 1000)
    replacement_count = text.count("\ufffd")
    mojibake_count = sum(text.count(marker) for marker in MOJIBAKE_MARKERS)
    flags: list[str] = []
    if not text.strip():
        flags.append("EMPTY_TEXT")
    if replacement_count:
        flags.append("REPLACEMENT_CHARACTERS")
    if controls:
        flags.append("CONTROL_CHARACTERS")
    if long_lines:
        flags.append("VERY_LONG_LINES")
    if nonspace >= 500 and alpha / nonspace < 0.45:
        flags.append("LOW_ALPHA_RATIO")
    if mojibake_count:
        flags.append("POSSIBLE_MOJIBAKE")
    metrics = {
        "characters": len(text),
        "words": len(words),
        "lines": len(lines),
        "page_markers": len(pages) + form_feed_pages,
        "explicit_page_markers": len(pages),
        "form_feed_page_breaks": form_feed_pages,
        "page_labels_sample": pages[:10],
        "heading_candidates": len(headings),
        "headings_sample": headings[:30],
        "replacement_characters": replacement_count,
        "control_characters": controls,
        "very_long_lines": long_lines,
        "alpha_ratio_nonspace": round(alpha / nonspace, 4) if nonspace else 0.0,
    }
    return metrics, flags


def find_sidecar(path: Path) -> Path | None:
    candidates = [path.with_suffix(path.suffix + ".meta.json"), path.with_suffix(".meta.json")]
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def load_sidecar(path: Path) -> tuple[dict[str, Any], Path | None, list[str]]:
    sidecar = find_sidecar(path)
    if not sidecar:
        return {}, None, []
    try:
        value = json.loads(sidecar.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("la raíz debe ser un objeto")
        return value, sidecar, []
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return {}, sidecar, [f"SIDECAR_INVALID:{exc}"]


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def embedded_metadata(text: str) -> tuple[dict[str, Any], list[str]]:
    """Read an optional, preserved key/value header from the first 100 LF lines."""
    lines = split_lf_lines(text)[:100]
    start = next(
        (
            index
            for index, line in enumerate(lines)
            if line.strip().upper() == "=== CASSANDRA SOURCE METADATA ==="
        ),
        None,
    )
    if start is None:
        return {}, []
    end_markers = {
        "=== BEGIN SOURCE TEXT ===",
        "=== BEGIN TEXT ===",
        "=== INICIO DEL TEXTO ===",
    }
    raw: dict[str, str] = {}
    ended = False
    for line in lines[start + 1 :]:
        if line.strip().upper() in end_markers:
            ended = True
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        raw[fold_text(key).strip()] = value.strip()
    flags = [] if ended else ["EMBEDDED_METADATA_WITHOUT_END_MARKER"]

    def first(*keys: str) -> str | None:
        return next((raw[key] for key in keys if raw.get(key)), None)

    creators_value = first("creators", "authors", "autores", "author", "autor")
    creators = (
        [part.strip() for part in re.split(r"\s*;\s*", creators_value) if part.strip()]
        if creators_value
        else None
    )
    year_value = first("year", "ano")
    year: str | int | None = year_value
    if year_value and re.fullmatch(r"\d{4}", year_value):
        year = int(year_value)
    scope_value = first("scope", "alcance")
    scope_status = None
    if scope_value:
        scope_map = {
            "completa": "COMPLETA",
            "complete": "COMPLETA",
            "seleccion": "SELECCION_SIN_VERIFICAR",
            "selection": "SELECCION_SIN_VERIFICAR",
            "fragmento": "FRAGMENTARIA",
            "fragment": "FRAGMENTARIA",
        }
        scope_status = scope_map.get(fold_text(scope_value), scope_value)
    metadata: dict[str, Any] = {
        key: value
        for key, value in {
            "title": first("title", "titulo", "titulo completo"),
            "creators": creators,
            "year": year,
            "edition": first("edition", "edicion"),
            "publisher": first("publisher", "editorial"),
            "translator": first("translator", "traductor"),
            "language": first("language", "idioma"),
            "document_type": first("document_type", "tipo documental"),
        }.items()
        if value not in (None, "")
    }
    if scope_status or first("included_units", "paginas/capitulos/versos incluidos"):
        metadata["scope"] = {
            key: value
            for key, value in {
                "status": scope_status,
                "included_units": first(
                    "included_units", "paginas/capitulos/versos incluidos"
                ),
                "omissions": first("omissions", "omisiones"),
            }.items()
            if value not in (None, "")
        }
    method = first("extraction_method", "metodo")
    copy_source = first("copy_source", "procedencia")
    if method or copy_source:
        metadata["provenance"] = {
            key: value
            for key, value in {
                "extraction_method": method,
                "copy_source": copy_source,
            }.items()
            if value not in (None, "")
        }
    return metadata, flags


def infer_scope(filename: str) -> str:
    folded = fold_text(filename)
    if any(term in folded for term in ("seleccion", "extract", "excerpt", "fragment", "capitulo")):
        return "SELECCION_SIN_VERIFICAR"
    return "UNKNOWN"


def infer_bibliographic(path: Path) -> dict[str, Any]:
    title = re.sub(r"[_-]+", " ", path.stem).strip()
    year_match = re.search(r"(?<!\d)(1[5-9]\d{2}|20\d{2})(?!\d)", path.stem)
    return {
        "title": title or None,
        "creators": [],
        "year": int(year_match.group(1)) if year_match else None,
        "original_year": None,
        "edition": None,
        "publisher": None,
        "translator": None,
        "language": None,
        "identifiers": {},
    }


def normalize_creators(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


def metadata_from(path: Path, sidecar: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    inferred = infer_bibliographic(path)
    bibliographic_source = sidecar.get("bibliographic", {})
    if not isinstance(bibliographic_source, dict):
        bibliographic_source = {}
    title = sidecar.get("title", bibliographic_source.get("title", inferred["title"]))
    creators = sidecar.get(
        "creators",
        sidecar.get("authors", sidecar.get("author", bibliographic_source.get("creators", []))),
    )
    identifiers = sidecar.get("identifiers", bibliographic_source.get("identifiers", {}))
    if not isinstance(identifiers, dict):
        identifiers = {"other": str(identifiers)}
    bibliography = {
        "title": title,
        "creators": normalize_creators(creators),
        "year": sidecar.get("year", bibliographic_source.get("year", inferred["year"])),
        "original_year": sidecar.get(
            "original_year", bibliographic_source.get("original_year")
        ),
        "edition": sidecar.get("edition", bibliographic_source.get("edition")),
        "publisher": sidecar.get("publisher", bibliographic_source.get("publisher")),
        "translator": sidecar.get("translator", bibliographic_source.get("translator")),
        "language": sidecar.get("language", bibliographic_source.get("language")),
        "identifiers": identifiers,
    }
    scope_value = sidecar.get("scope", {})
    if isinstance(scope_value, str):
        scope = {"status": scope_value}
    elif isinstance(scope_value, dict):
        scope = dict(scope_value)
    else:
        scope = {}
    scope.setdefault("status", sidecar.get("completeness", infer_scope(path.name)))
    scope.setdefault("included_units", sidecar.get("included_units"))
    scope.setdefault("omissions", sidecar.get("omissions"))
    classification_value = sidecar.get("classification", {})
    classification = dict(classification_value) if isinstance(classification_value, dict) else {}
    classification.setdefault("domains", [])
    classification.setdefault("document_type", sidecar.get("document_type"))
    classification.setdefault("functions", [])
    classification.setdefault("theory_ids", [])
    classification.setdefault("corpus_status", "CANDIDATA")
    return bibliography, scope, classification


def metadata_missing(record: dict[str, Any]) -> list[str]:
    bibliography = record.get("bibliographic", {})
    scope = record.get("scope", {})
    classification = record.get("classification", {})
    missing: list[str] = []
    if not bibliography.get("title"):
        missing.append("title")
    if not bibliography.get("creators"):
        missing.append("creators")
    if bibliography.get("year") in (None, ""):
        missing.append("year")
    if not bibliography.get("edition"):
        missing.append("edition")
    if not bibliography.get("language"):
        missing.append("language")
    if not classification.get("document_type"):
        missing.append("document_type")
    if scope.get("status") in (None, "", "UNKNOWN"):
        missing.append("scope.status")
    provenance = record.get("provenance", {})
    if not provenance.get("copy_source"):
        missing.append("provenance.copy_source")
    return missing


def next_source_number(records: Iterable[dict[str, Any]]) -> int:
    maximum = 0
    for record in records:
        match = SOURCE_ID_RE.match(str(record.get("source_id", "")))
        if match:
            maximum = max(maximum, int(match.group(1)))
    return maximum + 1


def merge_preserved_fields(record: dict[str, Any], old: dict[str, Any] | None) -> None:
    """Keep explicitly human-managed fields if no sidecar replaced them."""
    if not old:
        return
    for field in ("human_review", "relationships", "notes"):
        if field in old and field not in record:
            record[field] = old[field]


def iter_text_files(inbox: Path) -> Iterator[Path]:
    for path in sorted(inbox.rglob("*")):
        if path.is_file() and path.suffix.lower() == ".txt":
            yield path


def command_init(args: argparse.Namespace) -> int:
    layout = ensure_layout(args.root)
    print(f"Estructura creada en: {args.root}")
    print(f"Suba o copie los TXT a: {layout['inbox']}")
    return 0


def command_inventory(args: argparse.Namespace) -> int:
    layout = ensure_layout(args.root)
    old_records = read_jsonl(layout["manifest"])
    registry = read_jsonl(layout["registry"])
    if not registry:
        # Migración automática si existe un manifiesto anterior a la introducción
        # del registro histórico.
        for record in old_records:
            digest = record.get("fixity", {}).get("original_sha256")
            if digest:
                registry.append(
                    {
                        "schema_version": SCHEMA_VERSION,
                        "source_id": record["source_id"],
                        "original_sha256": digest,
                        "first_seen": record.get("inventory_at"),
                        "last_seen": record.get("inventory_at"),
                        "last_record_version": record.get("record_version", 1),
                        "present_in_latest_inventory": True,
                        "current_paths": [item["path"] for item in record.get("files", [])],
                    }
                )
    old_by_hash = {
        record.get("fixity", {}).get("original_sha256"): record
        for record in old_records
        if record.get("fixity", {}).get("original_sha256")
    }
    old_by_path: dict[str, tuple[str, str]] = {}
    for record in old_records:
        digest = record.get("fixity", {}).get("original_sha256")
        for item in record.get("files", []):
            old_by_path[item["path"]] = (record["source_id"], digest)
    registry_by_hash = {record["original_sha256"]: record for record in registry}
    next_number = next_source_number([*old_records, *registry])
    inventory_time = now_iso()

    groups: dict[str, list[Path]] = collections.defaultdict(list)
    byte_cache: dict[str, bytes] = {}
    for path in iter_text_files(layout["inbox"]):
        data = path.read_bytes()
        digest = sha256_bytes(data)
        groups[digest].append(path)
        byte_cache.setdefault(digest, data)

    for entry in registry:
        entry["present_in_latest_inventory"] = False
        entry["current_paths"] = []

    records: list[dict[str, Any]] = []
    for digest, source_paths in sorted(groups.items(), key=lambda item: str(item[1][0])):
        old = old_by_hash.get(digest)
        registry_entry = registry_by_hash.get(digest)
        if registry_entry:
            source_id = registry_entry["source_id"]
        else:
            source_id = f"DCA-{next_number:06d}"
            next_number += 1
            registry_entry = {
                "schema_version": SCHEMA_VERSION,
                "source_id": source_id,
                "original_sha256": digest,
                "first_seen": inventory_time,
                "last_seen": inventory_time,
                "last_record_version": 0,
                "present_in_latest_inventory": True,
                "current_paths": [],
            }
            registry.append(registry_entry)
            registry_by_hash[digest] = registry_entry
        primary = source_paths[0]
        data = byte_cache[digest]
        text, encoding, decode_flags = detect_and_decode(data)
        normalized = normalize_text(text)
        metrics, text_flags = text_metrics(normalized)
        embedded, embedded_flags = embedded_metadata(normalized)
        sidecar, sidecar_path, sidecar_flags = load_sidecar(primary)
        supplied_metadata = deep_merge(embedded, sidecar)
        bibliography, scope, classification = metadata_from(primary, supplied_metadata)
        normalized_path = layout["normalized"] / f"{source_id}.txt"
        normalized_path.write_text(normalized, encoding="utf-8", newline="\n")
        normalized_bytes = normalized_path.read_bytes()
        relative_files = []
        immutability_flags: list[str] = []
        for path in source_paths:
            stat = path.stat()
            relative_path = path.relative_to(args.root).as_posix()
            previous = old_by_path.get(relative_path)
            if previous and previous[1] != digest:
                immutability_flags.append(f"PATH_CONTENT_CHANGED_FROM:{previous[0]}")
            relative_files.append(
                {
                    "path": relative_path,
                    "bytes": stat.st_size,
                    "modified_utc": dt.datetime.fromtimestamp(
                        stat.st_mtime, tz=dt.timezone.utc
                    ).replace(microsecond=0).isoformat(),
                }
            )
        provenance_value = supplied_metadata.get("provenance", {})
        provenance = dict(provenance_value) if isinstance(provenance_value, dict) else {}
        provenance.setdefault("copy_source", supplied_metadata.get("copy_source"))
        provenance.setdefault("provided_by", supplied_metadata.get("provided_by"))
        provenance.setdefault("extraction_method", supplied_metadata.get("extraction_method"))
        record_version = int(registry_entry.get("last_record_version", 0)) + 1
        record: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "record_version": record_version,
            "source_id": source_id,
            "inventory_at": inventory_time,
            "files": relative_files,
            "fixity": {
                "algorithm": "SHA-256",
                "original_sha256": digest,
                "normalized_sha256": sha256_bytes(normalized_bytes),
            },
            "normalized_path": normalized_path.relative_to(args.root).as_posix(),
            "text": {"encoding_detected": encoding, **metrics},
            "bibliographic": bibliography,
            "scope": scope,
            "classification": classification,
            "provenance": provenance,
            "work_id": supplied_metadata.get("work_id", old.get("work_id") if old else None),
            "parent_source_id": supplied_metadata.get(
                "parent_source_id", old.get("parent_source_id") if old else None
            ),
            "relationships": supplied_metadata.get(
                "relationships", old.get("relationships", []) if old else []
            ),
            "metadata_source": (
                sidecar_path.relative_to(args.root).as_posix()
                if sidecar_path
                else ("embedded_header" if embedded else "filename_inference")
            ),
            "audit_flags": sorted(
                set(
                    decode_flags
                    + text_flags
                    + embedded_flags
                    + sidecar_flags
                    + immutability_flags
                )
            ),
            "processing": {"status": "INVENTORIED_AND_NORMALIZED"},
        }
        if len(source_paths) > 1:
            record["audit_flags"].append("EXACT_DUPLICATE_PATHS")
        merge_preserved_fields(record, old)
        record["metadata_missing"] = metadata_missing(record)
        records.append(record)
        registry_entry.update(
            {
                "last_seen": inventory_time,
                "last_record_version": record_version,
                "present_in_latest_inventory": True,
                "current_paths": [item["path"] for item in relative_files],
            }
        )

    records.sort(key=lambda item: item["source_id"])
    registry.sort(key=lambda item: item["source_id"])
    if old_records:
        history_dir = layout["indexes"] / "history"
        timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
        write_jsonl(history_dir / f"manifest_{timestamp}.jsonl", old_records)
    write_jsonl(layout["manifest"], records)
    write_jsonl(layout["registry"], registry)
    print(f"Archivos TXT: {sum(len(value) for value in groups.values())}")
    print(f"Documentos únicos presentes: {len(records)}")
    print(f"Identificadores históricos: {len(registry)}")
    print(f"Manifiesto: {layout['manifest']}")
    print(f"Copias normalizadas: {layout['normalized']}")
    return 0


def source_lookup(records: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(record["source_id"]): record for record in records}


def line_offsets(lines: list[str]) -> list[int]:
    offsets: list[int] = []
    position = 0
    for line in lines:
        offsets.append(position)
        position += len(line)
    offsets.append(position)
    return offsets


def chunk_ranges(lines: list[str], max_chars: int, overlap_lines: int) -> Iterator[tuple[int, int]]:
    """Yield zero-based half-open line ranges, preferring paragraph boundaries."""
    if not lines:
        return
    start = 0
    total_lines = len(lines)
    while start < total_lines:
        size = 0
        end = start
        last_blank: int | None = None
        while end < total_lines:
            candidate = len(lines[end])
            if end > start and size + candidate > max_chars:
                break
            size += candidate
            end += 1
            if not lines[end - 1].strip() and size >= int(max_chars * 0.55):
                last_blank = end
        if end == total_lines:
            yield start, end
            break
        if last_blank is not None and last_blank > start:
            end = last_blank
        if end <= start:
            end = start + 1
        yield start, end
        next_start = max(start + 1, end - overlap_lines)
        start = next_start


def page_range(lines: list[str], start: int, end: int) -> tuple[str | None, str | None]:
    current: str | None = None
    found: list[str] = []
    form_feed_number = 0
    for index, line in enumerate(lines[:end]):
        explicit = page_label(line.rstrip("\n"))
        if explicit is not None:
            current = explicit
            if index >= start:
                found.append(current)
        feed_count = line.count("\f")
        for _ in range(feed_count):
            form_feed_number += 1
            current = f"FORMFEED-{form_feed_number}"
            if index >= start:
                found.append(current)
    first = found[0] if found else current
    last = found[-1] if found else current
    return first, last


def active_heading(lines: list[str], start: int) -> str | None:
    for index in range(start, -1, -1):
        line = lines[index].rstrip("\n") if index < len(lines) else ""
        if is_heading(line):
            return line.strip()
    return None


def command_chunk(args: argparse.Namespace) -> int:
    layout = ensure_layout(args.root)
    records = read_jsonl(layout["manifest"])
    if not records:
        print("No hay manifiesto. Ejecute primero: inventory", file=sys.stderr)
        return 2
    chunks: list[dict[str, Any]] = []
    for record in records:
        normalized = args.root / record["normalized_path"]
        if not normalized.exists():
            print(f"Falta copia normalizada: {normalized}", file=sys.stderr)
            return 2
        text = normalized.read_text(encoding="utf-8")
        lines = split_lf_lines(text, keepends=True)
        offsets = line_offsets(lines)
        for sequence, (start, end) in enumerate(
            chunk_ranges(lines, args.max_chars, args.overlap_lines), 1
        ):
            content = "".join(lines[start:end])
            page_start, page_end = page_range(lines, start, end)
            chunks.append(
                {
                    "schema_version": SCHEMA_VERSION,
                    "passage_id": (
                        f"PAS-{record['source_id']}-L{start + 1:07d}-L{end:07d}"
                    ),
                    "sequence": sequence,
                    "source_id": record["source_id"],
                    "source_sha256": record["fixity"]["original_sha256"],
                    "normalized_sha256": record["fixity"]["normalized_sha256"],
                    "line_start": start + 1,
                    "line_end": end,
                    "char_start": offsets[start],
                    "char_end": offsets[end],
                    "page_start": page_start,
                    "page_end": page_end,
                    "heading": active_heading(lines, start),
                    "content_sha256": sha256_bytes(content.encode("utf-8")),
                    "content": content,
                }
            )
    write_jsonl(layout["chunks"], chunks)
    print(f"Fragmentos: {len(chunks)}")
    print(f"Índice local: {layout['chunks']}")
    return 0


def fold_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def query_tokens(query: str) -> list[str]:
    return [token for token in TOKEN_RE.findall(fold_text(query)) if len(token) > 1]


def make_snippet(content: str, query: str, context_chars: int) -> str:
    folded = fold_text(content)
    folded_query = fold_text(query).strip()
    position = folded.find(folded_query) if folded_query else -1
    if position < 0:
        tokens = query_tokens(query)
        positions = [folded.find(token) for token in tokens if folded.find(token) >= 0]
        position = min(positions) if positions else 0
    start = max(0, position - context_chars)
    end = min(len(content), position + max(len(query), 1) + context_chars)
    snippet = content[start:end].strip().replace("\x0c", " ")
    if start:
        snippet = "…" + snippet
    if end < len(content):
        snippet += "…"
    return snippet


def command_search(args: argparse.Namespace) -> int:
    layout = ensure_layout(args.root)
    chunks = read_jsonl(layout["chunks"])
    if not chunks:
        print("No existe un índice de fragmentos. Ejecute primero: chunk", file=sys.stderr)
        return 2
    terms = query_tokens(args.query)
    if not terms:
        print("La consulta no contiene términos buscables.", file=sys.stderr)
        return 2
    tokenized: list[collections.Counter[str]] = []
    document_frequencies: collections.Counter[str] = collections.Counter()
    for chunk in chunks:
        counter = collections.Counter(query_tokens(chunk.get("content", "")))
        tokenized.append(counter)
        for term in set(terms):
            if counter[term]:
                document_frequencies[term] += 1
    total = len(chunks)
    scored: list[tuple[float, dict[str, Any]]] = []
    folded_phrase = fold_text(args.query)
    for chunk, counter in zip(chunks, tokenized):
        if not any(counter[term] for term in terms):
            continue
        length = max(1, sum(counter.values()))
        score = 0.0
        for term in terms:
            frequency = counter[term]
            if not frequency:
                continue
            inverse = math.log((total + 1) / (document_frequencies[term] + 0.5)) + 1.0
            score += inverse * (frequency / (frequency + 1.2 + 0.002 * length))
        if folded_phrase and folded_phrase in fold_text(chunk.get("content", "")):
            score += 3.0
        scored.append((score, chunk))
    scored.sort(key=lambda item: (-item[0], item[1]["passage_id"]))
    selected = scored[: args.top]
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    output = args.output or layout["selections"] / f"busqueda_{timestamp}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    report = [
        "# Resultado de búsqueda local",
        "",
        f"- Consulta: `{args.query}`",
        f"- Fragmentos evaluados: {total}",
        f"- Coincidencias mostradas: {len(selected)}",
        f"- Generado: {now_iso()}",
        "",
    ]
    for rank, (score, chunk) in enumerate(selected, 1):
        location = f"líneas {chunk['line_start']}–{chunk['line_end']}"
        if chunk.get("page_start"):
            location += f", páginas {chunk['page_start']}–{chunk.get('page_end') or chunk['page_start']}"
        report.extend(
            [
                f"## {rank}. {chunk['passage_id']} — puntuación {score:.3f}",
                "",
                f"- Fuente: `{chunk['source_id']}`",
                f"- Ubicación: {location}",
                f"- Encabezado: {chunk.get('heading') or 'no detectado'}",
                f"- Hash de pasaje: `{chunk['content_sha256']}`",
                "",
                make_snippet(chunk.get("content", ""), args.query, args.context_chars),
                "",
            ]
        )
    output.write_text("\n".join(report), encoding="utf-8", newline="\n")
    print(f"Coincidencias: {len(selected)}")
    print(f"Reporte: {output}")
    return 0


def parse_line_range(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+):(\d+)", value.strip())
    if not match:
        raise argparse.ArgumentTypeError("use INICIO:FIN, por ejemplo 120:220")
    start, end = map(int, match.groups())
    if start < 1 or end < start:
        raise argparse.ArgumentTypeError("el rango debe ser positivo y FIN >= INICIO")
    return start, end


def command_select(args: argparse.Namespace) -> int:
    layout = ensure_layout(args.root)
    records = source_lookup(read_jsonl(layout["manifest"]))
    record = records.get(args.source_id)
    if not record:
        print(f"source_id desconocido: {args.source_id}", file=sys.stderr)
        return 2
    path = args.root / record["normalized_path"]
    lines = split_lf_lines(path.read_text(encoding="utf-8"), keepends=True)
    start, end = args.lines
    if start > len(lines) or end > len(lines):
        print(f"Rango fuera del documento (1:{len(lines)}).", file=sys.stderr)
        return 2
    content = "".join(lines[start - 1 : end])
    page_start, page_end = page_range(lines, start - 1, end)
    output = args.output or layout["selections"] / f"{args.source_id}_L{start}-L{end}.txt"
    output.parent.mkdir(parents=True, exist_ok=True)
    header = "\n".join(
        [
            "=== CASSANDRA SELECTION METADATA ===",
            f"source_id: {args.source_id}",
            f"source_sha256: {record['fixity']['original_sha256']}",
            f"normalized_sha256: {record['fixity']['normalized_sha256']}",
            f"lines: {start}:{end}",
            f"pages: {page_start or 'UNKNOWN'}:{page_end or 'UNKNOWN'}",
            f"selection_sha256: {sha256_bytes(content.encode('utf-8'))}",
            f"generated_utc: {now_iso()}",
            "=== BEGIN EXACT NORMALIZED SELECTION ===",
            "",
        ]
    )
    output.write_text(header + content, encoding="utf-8", newline="\n")
    print(f"Selección: {output}")
    return 0


def audit_severity(flags: Iterable[str], missing: Iterable[str]) -> tuple[str, list[str]]:
    flags_list = list(flags)
    missing_list = list(missing)
    blocking_prefixes = ("EMPTY_TEXT", "SIDECAR_INVALID", "PATH_CONTENT_CHANGED_FROM")
    if any(flag.startswith(blocking_prefixes) for flag in flags_list):
        return "FAIL_BLOCKING", [*flags_list, *[f"MISSING:{item}" for item in missing_list]]
    if missing_list or flags_list:
        return "PASS_WITH_WARNINGS", [*flags_list, *[f"MISSING:{item}" for item in missing_list]]
    return "PASS", []


def markdown_cell(value: Any) -> str:
    return str(value if value not in (None, "") else "—").replace("|", "\\|").replace("\n", " ")


def command_audit(args: argparse.Namespace) -> int:
    layout = ensure_layout(args.root)
    records = read_jsonl(layout["manifest"])
    if not records:
        print("No hay manifiesto. Ejecute primero: inventory", file=sys.stderr)
        return 2
    statuses: collections.Counter[str] = collections.Counter()
    duplicate_paths = 0
    report = [
        "# Auditoría inicial del corpus",
        "",
        f"- Generado: {now_iso()}",
        f"- Documentos únicos: {len(records)}",
        f"- Archivos físicos: {sum(len(record.get('files', [])) for record in records)}",
        "",
        "## Resumen",
        "",
    ]
    details: list[tuple[dict[str, Any], str, list[str]]] = []
    for record in records:
        if len(record.get("files", [])) > 1:
            duplicate_paths += len(record["files"]) - 1
        status, reasons = audit_severity(
            record.get("audit_flags", []), record.get("metadata_missing", [])
        )
        statuses[status] += 1
        details.append((record, status, reasons))
    report.extend(
        [
            f"- PASS: {statuses['PASS']}",
            f"- PASS_WITH_WARNINGS: {statuses['PASS_WITH_WARNINGS']}",
            f"- FAIL_BLOCKING: {statuses['FAIL_BLOCKING']}",
            f"- Rutas duplicadas exactas: {duplicate_paths}",
            "",
            "## Detalle por fuente",
            "",
            "| source_id | Estado | Alcance | Título | Archivo(s) | Incidencias |",
            "|---|---|---|---|---:|---|",
        ]
    )
    for record, status, reasons in details:
        report.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(record["source_id"]),
                    markdown_cell(status),
                    markdown_cell(record.get("scope", {}).get("status")),
                    markdown_cell(record.get("bibliographic", {}).get("title")),
                    markdown_cell(len(record.get("files", []))),
                    markdown_cell(", ".join(reasons) or "—"),
                ]
            )
            + " |"
        )
    report.extend(
        [
            "",
            "## Criterio",
            "",
            "Esta auditoría cubre integridad mecánica y presencia de metadatos. No certifica todavía fidelidad bibliográfica, suficiencia contextual ni admisión al canon.",
            "",
        ]
    )
    output = args.output or layout["audits"] / "AUDITORIA_INICIAL.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(report), encoding="utf-8", newline="\n")
    print(f"Auditoría: {output}")
    print(dict(statuses))
    return 1 if statuses["FAIL_BLOCKING"] else 0


def command_verify(args: argparse.Namespace) -> int:
    layout = ensure_layout(args.root)
    records = read_jsonl(layout["manifest"])
    if not records:
        print("No hay manifiesto. Ejecute primero: inventory", file=sys.stderr)
        return 2
    failures: list[str] = []
    checked = 0
    for record in records:
        expected = record.get("fixity", {}).get("original_sha256")
        for file_info in record.get("files", []):
            path = args.root / file_info["path"]
            checked += 1
            if not path.exists():
                failures.append(f"MISSING {record['source_id']} {path}")
                continue
            actual = sha256_file(path)
            if actual != expected:
                failures.append(
                    f"HASH_MISMATCH {record['source_id']} {path} esperado={expected} actual={actual}"
                )
        normalized = args.root / record.get("normalized_path", "")
        expected_normalized = record.get("fixity", {}).get("normalized_sha256")
        if not normalized.exists():
            failures.append(f"NORMALIZED_MISSING {record['source_id']} {normalized}")
        elif sha256_file(normalized) != expected_normalized:
            failures.append(f"NORMALIZED_HASH_MISMATCH {record['source_id']} {normalized}")
    if failures:
        print("Verificación fallida:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PASS: {checked} originales y {len(records)} copias normalizadas verificados.")
    return 0


def command_pagemap(args: argparse.Namespace) -> int:
    """P1: mapea marcadores de página (PÁGINA/PAGE/form-feed) a rangos de línea."""
    layout = ensure_layout(args.root)
    records = source_lookup(read_jsonl(layout["manifest"]))
    record = records.get(args.source_id)
    if not record:
        print(f"source_id desconocido: {args.source_id}", file=sys.stderr)
        return 2
    normalized = args.root / record["normalized_path"]
    if not normalized.exists():
        print(f"Falta copia normalizada: {normalized}", file=sys.stderr)
        return 2
    lines = split_lf_lines(normalized.read_text(encoding="utf-8"))
    standalone_page_re = re.compile(r"^\s*(?:p[aá]gina|page)\s+(.+?)\s*$", re.IGNORECASE)

    def pagemap_page_label(line: str) -> str | None:
        explicit = page_label(line)
        if explicit is not None:
            return explicit
        match = standalone_page_re.match(line.rstrip("\n"))
        if match and len(match.group(1).strip()) <= 40:
            return match.group(1).strip()
        return None

    entries: list[dict[str, Any]] = []
    current_label: str | None = None
    current_start = 1
    form_feed_number = 0
    printed_candidates: list[str] = []

    def flush(end: int) -> None:
        nonlocal current_label, current_start, printed_candidates
        if current_label is not None:
            entries.append(
                {
                    "source_id": args.source_id,
                    "source_sha256": record["fixity"]["original_sha256"],
                    "hash_ref": "original",
                    "page_label": current_label,
                    "line_start": current_start,
                    "line_end": max(end - 1, current_start),
                    "page_number_candidates": printed_candidates,
                }
            )
        current_label = None
        printed_candidates = []

    for index, line in enumerate(lines, 1):
        explicit = pagemap_page_label(line)
        if explicit is not None:
            flush(index)
            current_label = explicit
            current_start = index
            continue
        feed_count = line.count("\f")
        if feed_count:
            flush(index)
            for _ in range(feed_count):
                form_feed_number += 1
            current_label = f"FORMFEED-{form_feed_number}"
            current_start = index
            continue
        if current_label is not None and not printed_candidates:
            stripped = line.strip()
            if re.fullmatch(r"\d{1,3}", stripped):
                printed_candidates.append(stripped)
    flush(len(lines) + 1)

    output = args.output or layout["indexes"] / f"pagemap_{args.source_id}.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(output, entries)
    print(f"Página(s) mapeadas: {len(entries)}")
    print(f"Página-map: {output}")
    return 0


def command_validate_claims(args: argparse.Namespace) -> int:
    """P7: valida un JSONL de afirmaciones contra claim_record.schema.json."""
    try:
        import jsonschema
    except ImportError:
        print(
            "No está disponible el módulo 'jsonschema'. "
            "Instálelo (p. ej. en un entorno virtual) para usar validate-claims.",
            file=sys.stderr,
        )
        return 2
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    records = read_jsonl(args.claims)
    validator = jsonschema.Draft202012Validator(schema)
    failures = 0
    for record in records:
        record.setdefault("schema_version", schema.get("properties", {}).get("schema_version", {}).get("const", "1.0"))
        errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
        if errors:
            failures += 1
            print(f"[FAIL] {record.get('claim_id', '?')}:")
            for error in errors:
                print("   ", "/".join(map(str, error.path)) or "<raíz>", "->", error.message)
        else:
            print(f"[OK]   {record.get('claim_id', '?')}")
    total = len(records)
    print(f"VALIDACIÓN: {total - failures}/{total} válidos.")
    return 0 if failures == 0 else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inventario, auditoría y recuperación local de fuentes TXT."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help=f"raíz local del corpus (predeterminado: {DEFAULT_ROOT})",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="crear la estructura local")
    init_parser.set_defaults(function=command_init)

    inventory_parser = subparsers.add_parser(
        "inventory", help="inventariar, hashear y normalizar los TXT"
    )
    inventory_parser.set_defaults(function=command_inventory)

    audit_parser = subparsers.add_parser("audit", help="generar auditoría inicial")
    audit_parser.add_argument("--output", type=Path, help="ruta Markdown de salida")
    audit_parser.set_defaults(function=command_audit)

    chunk_parser = subparsers.add_parser("chunk", help="crear fragmentos recuperables")
    chunk_parser.add_argument("--max-chars", type=int, default=12000)
    chunk_parser.add_argument("--overlap-lines", type=int, default=2)
    chunk_parser.set_defaults(function=command_chunk)

    search_parser = subparsers.add_parser("search", help="buscar en fragmentos locales")
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--top", type=int, default=20)
    search_parser.add_argument("--context-chars", type=int, default=500)
    search_parser.add_argument("--output", type=Path)
    search_parser.set_defaults(function=command_search)

    select_parser = subparsers.add_parser("select", help="extraer líneas exactas")
    select_parser.add_argument("--source-id", required=True)
    select_parser.add_argument("--lines", required=True, type=parse_line_range)
    select_parser.add_argument("--output", type=Path)
    select_parser.set_defaults(function=command_select)

    verify_parser = subparsers.add_parser("verify", help="verificar hashes")
    verify_parser.set_defaults(function=command_verify)

    pagemap_parser = subparsers.add_parser("pagemap", help="mapear marcadores de página a rangos de línea")
    pagemap_parser.add_argument("--source-id", required=True)
    pagemap_parser.add_argument("--output", type=Path)
    pagemap_parser.set_defaults(function=command_pagemap)

    validate_parser = subparsers.add_parser(
        "validate-claims", help="validar afirmaciones contra claim_record.schema.json"
    )
    validate_parser.add_argument("--schema", type=Path, required=True)
    validate_parser.add_argument("--claims", type=Path, required=True)
    validate_parser.set_defaults(function=command_validate_claims)
    return parser


def validate_arguments(args: argparse.Namespace) -> None:
    if hasattr(args, "max_chars") and args.max_chars < 500:
        raise ValueError("--max-chars debe ser al menos 500")
    if hasattr(args, "overlap_lines") and args.overlap_lines < 0:
        raise ValueError("--overlap-lines no puede ser negativo")
    if hasattr(args, "top") and args.top < 1:
        raise ValueError("--top debe ser positivo")
    if hasattr(args, "context_chars") and args.context_chars < 20:
        raise ValueError("--context-chars debe ser al menos 20")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        validate_arguments(args)
        return int(args.function(args))
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
