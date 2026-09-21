#!/usr/bin/env python3
"""Deterministic validator for the local Nexa GPT Knowledge upload package."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPLOAD = ROOT / "gpt/knowledge-upload"
CHECKSUMS = ROOT / "gpt/support/knowledge-sha256.txt"

MARKDOWN_NAMES = {
    "00-NEXA-KNOWLEDGE-INDEX.md",
    "01-NEXA-AUTHORITY-GOVERNANCE-AND-STATE-VOCABULARY.md",
    "02-NEXA-PRODUCT-ACTORS-ROLES-CAPABILITIES-AND-SURFACES.md",
    "03-NEXA-DOMAIN-RULES-INVARIANTS-AND-UBIQUITOUS-LANGUAGE.md",
    "04-NEXA-STRATEGIC-DDD-CONTEXT-MAP-AND-EVENTS.md",
    "05-NEXA-TACTICAL-DDD-AGGREGATES-AND-LIFECYCLES.md",
    "06-NEXA-DATA-POSTGRESQL-RLS-CONCURRENCY-AND-IDEMPOTENCY.md",
    "07-NEXA-C4-RUNTIME-DEPLOYMENT-AND-SYSTEM-BOUNDARIES.md",
    "08-NEXA-INTEGRATION-EVENTS-RELIABILITY-AND-OBSERVABILITY.md",
    "09-NEXA-SECURITY-MULTITENANCY-AUTHORIZATION-AND-MOBILE-SECURITY.md",
    "10-NEXA-OPERATIONS-MOBILE-ANDROID-CONSTRUCTION.md",
    "11-NEXA-BUYER-MOBILE-FLUTTER-CONSTRUCTION.md",
    "12-NEXA-MOBILE-ENGINEERING-MODULES-API-TESTING-AND-DOD.md",
    "13-NEXA-SCRUM-ACADEMIC-RUBRIC-BACKLOG-AND-EVIDENCE.md",
    "14-NEXA-CONSTRUCTION-ENVIRONMENT-QUALITY-GATES-OPEN-DECISIONS-AND-PROVENANCE.md",
}

ZIP_NAMES = {
    "15-NEXA-ACADEMIC-AND-FOUNDATIONAL-SOURCES.zip",
    "16-NEXA-C4-CANONICAL.zip",
    "17-NEXA-DDD-UML-AND-DOMAIN-STORIES-CANONICAL.zip",
    "18-NEXA-DATA-POSTGRESQL-ERD-CANONICAL.zip",
    "19-NEXA-MOBILE-CONSTRUCTION-SOURCES.zip",
}

BCS = [f"BC-{number:02d}" for number in range(1, 12)]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def members(path: Path, errors: list[str]) -> set[str]:
    native = subprocess.run(["unzip", "-t", str(path)], text=True, capture_output=True)
    if native.returncode != 0:
        fail(errors, f"native unzip integrity failure: {path.name}: {native.stderr.strip() or native.stdout.strip()}")
        return set()
    try:
        with zipfile.ZipFile(path) as archive:
            names = {entry.filename for entry in archive.infolist() if not entry.is_dir()}
    except zipfile.BadZipFile as exc:
        fail(errors, f"unreadable ZIP: {path.name}: {exc}")
        return set()
    if "MANIFEST.md" not in names:
        fail(errors, f"{path.name}: root MANIFEST.md is missing")
    if len(names) <= 1:
        fail(errors, f"{path.name}: archive is empty aside from its manifest")
    return names


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upload-dir", type=Path, default=UPLOAD)
    args = parser.parse_args()
    upload = args.upload_dir.resolve()
    errors: list[str] = []
    if not upload.is_dir():
        fail(errors, f"upload directory does not exist: {upload}")
        entries: list[Path] = []
    else:
        entries = sorted(upload.iterdir())
    files = [item for item in entries if item.is_file() and not item.is_symlink()]
    invalid = [item.name for item in entries if not item.is_file() or item.is_symlink() or item.name.startswith(".")]
    if invalid:
        fail(errors, "upload root contains forbidden entries: " + ", ".join(invalid))
    if len(files) != 20:
        fail(errors, f"expected exactly 20 root files, found {len(files)}")
    markdown = {item.name for item in files if item.suffix == ".md"}
    zips = {item.name for item in files if item.suffix == ".zip"}
    if len(markdown) != 15 or markdown != MARKDOWN_NAMES:
        fail(errors, "Markdown root set is not the exact required 15-file set")
    if len(zips) != 5 or zips != ZIP_NAMES:
        fail(errors, "ZIP root set is not the exact required 5-file set")
    unexpected = {item.name for item in files} - MARKDOWN_NAMES - ZIP_NAMES
    if unexpected:
        fail(errors, "unexpected upload root files: " + ", ".join(sorted(unexpected)))

    prohibited = {
        "framework open": "framework-selection question reopened",
        "kmp current target": "KMP stated as current target",
        "warehousebacking aggregate root": "WarehouseBacking classified as Aggregate Root",
        "pushsubscription aggregate root": "PushSubscription classified as Aggregate Root",
        "mobile bounded context": "Mobile classified as a Bounded Context",
        "safety stock = reservation": "Safety Stock equated to Reservation",
        "buyer receipt = driver outcome": "Buyer Receipt equated to Driver Outcome",
    }
    for name in MARKDOWN_NAMES & {item.name for item in files}:
        content = (upload / name).read_text(encoding="utf-8").lower()
        semantic_content = content.replace("exactly-once transport is not claimed", "")
        if "exactly-once" in semantic_content:
            fail(errors, f"{name}: unsupported exactly-once claim")
        for marker, reason in prohibited.items():
            if marker in content:
                fail(errors, f"{name}: {reason}")
        for required in ("generated-at:", "blueprint-source-commit:", "blueprint-source-paths:", "source-status:"):
            if required not in content:
                fail(errors, f"{name}: missing provenance field {required}")

    # Current knowledge must preserve explicit domain distinctions.  The
    # summaries intentionally use negated wording (for example, "is not"),
    # so reject only an un-negated assertion rather than matching vocabulary
    # mechanically.
    distinction_patterns = {
        "payment = receivable": r"payment\s*(?:=|is)\s*receivable",
        "reported payment = confirmed payment": r"payment\s+reported\s*(?:=|is)\s*payment\s+confirmed",
        "driver outcome = buyer receipt": r"driver\s+outcome\s*(?:=|is)\s*buyer\s+receipt",
        "safety stock = reservation": r"safety\s+stock\s*(?:=|is)\s*(?:a\s+)?reservation",
        "generic offline-first": r"generic\s+offline(?:[- ]first|\s+sync(?:hronization)?)",
        "permanent driver tracking": r"permanent\s+driver\s+(?:gps\s+)?tracking",
    }
    for name in MARKDOWN_NAMES & {item.name for item in files}:
        content = (upload / name).read_text(encoding="utf-8").lower()
        for label, pattern in distinction_patterns.items():
            for match in re.finditer(pattern, content):
                context = content[max(0, match.start() - 160):match.end() + 80]
                if not re.search(r"\b(?:not|never|no|!=)\b", context):
                    fail(errors, f"{name}: unsupported semantic claim {label}")

    accepted_construction_markers = {
        "10-NEXA-OPERATIONS-MOBILE-ANDROID-CONSTRUCTION.md": (
            "kotlin", "compose", "hilt", "navigation 3", "camerax",
            "ml kit", "bundled", "room", "datastore", "workmanager",
        ),
        "11-NEXA-BUYER-MOBILE-FLUTTER-CONSTRUCTION.md": (
            "flutter", "dart", "provider", "go_router", "android and ios",
        ),
    }
    for name, markers in accepted_construction_markers.items():
        path = upload / name
        if not path.is_file():
            fail(errors, f"missing current mobile construction summary: {name}")
            continue
        content = path.read_text(encoding="utf-8").lower()
        for marker in markers:
            if marker not in content:
                fail(errors, f"{name}: missing accepted construction marker {marker!r}")

    archives = {name: members(upload / name, errors) for name in ZIP_NAMES if (upload / name).exists()}
    academic = archives.get("15-NEXA-ACADEMIC-AND-FOUNDATIONAL-SOURCES.zip", set())
    if "academic-authority/mobile-applications-final-rubric-v4.md" not in academic:
        fail(errors, "academic archive lacks the authoritative V4 rubric Markdown source")
    if any(name.startswith("academic-projections/") for name in academic):
        fail(errors, "academic archive exposes Complementary projections as current")
    if not any(name.startswith("historical/academic-projections/") for name in academic):
        fail(errors, "academic archive lacks historical classification for Complementary projections")
    c4 = archives.get("16-NEXA-C4-CANONICAL.zip", set())
    if "source/structurizr/workspace.dsl" not in c4 or not any(name.endswith(".dsl") for name in c4):
        fail(errors, "C4 archive lacks canonical Structurizr DSL")
    ddd = archives.get("17-NEXA-DDD-UML-AND-DOMAIN-STORIES-CANONICAL.zip", set())
    for bc in BCS:
        if not any(name.startswith(f"tactical-ddd/bounded-contexts/{bc}-") and name.endswith("/diagrams/domain-model.puml") for name in ddd):
            fail(errors, f"DDD archive lacks current Domain UML source for {bc}")
    data = archives.get("18-NEXA-DATA-POSTGRESQL-ERD-CANONICAL.zip", set())
    if "source/master-and-shared/master-target-relational-model.sql" not in data:
        fail(errors, "Data archive lacks master TARGET relational SQL")
    for bc in BCS:
        if not any(name.startswith(f"source/per-bc/{bc}-") and name.endswith("/target-relational-model.sql") for name in data):
            fail(errors, f"Data archive lacks TARGET SQL for {bc}")
    mobile = archives.get("19-NEXA-MOBILE-CONSTRUCTION-SOURCES.zip", set())
    mobile_text_paths = {name for name in mobile if name.endswith(".md")}
    if "OFFICIAL-REFERENCES.md" not in mobile or not any("adr-0018" in name for name in mobile_text_paths) or not any("adr-0019" in name for name in mobile_text_paths):
        fail(errors, "Mobile archive lacks accepted Android/Flutter construction material")

    if errors:
        print("KNOWLEDGE PACKAGE: FAIL")
        print("\n".join(f"- {error}" for error in errors))
        raise SystemExit(1)

    checksum_lines = []
    for item in sorted(files, key=lambda value: value.name):
        checksum_lines.append(f"{sha256(item)}  ../knowledge-upload/{item.name}")
    CHECKSUMS.parent.mkdir(parents=True, exist_ok=True)
    CHECKSUMS.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    print("KNOWLEDGE PACKAGE: PASS")
    print("- root files: 20")
    print("- Markdown: 15")
    print("- ZIP: 5")
    print(f"- checksums: {CHECKSUMS}")


if __name__ == "__main__":
    main()
