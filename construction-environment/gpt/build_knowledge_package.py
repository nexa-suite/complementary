#!/usr/bin/env python3
"""Build the local-only Nexa GPT Knowledge package from current canon.

The upload directory deliberately contains only the exact 15 Markdown summaries
and five evidence ZIP archives accepted for this local GPT workflow.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BLUEPRINT = ROOT.parents[1] / "blueprint"
DEFAULT_REPORT = ROOT.parents[1] / "mobile-report"
COMP = ROOT.parents[0]

MARKDOWN_NAMES = [
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
]

ZIP_NAMES = [
    "15-NEXA-ACADEMIC-AND-FOUNDATIONAL-SOURCES.zip",
    "16-NEXA-C4-CANONICAL.zip",
    "17-NEXA-DDD-UML-AND-DOMAIN-STORIES-CANONICAL.zip",
    "18-NEXA-DATA-POSTGRESQL-ERD-CANONICAL.zip",
    "19-NEXA-MOBILE-CONSTRUCTION-SOURCES.zip",
]

BCS = [
    "BC-01-tenant-access-governance",
    "BC-02-customer-buyer-relationships",
    "BC-03-catalog-commercial-policy",
    "BC-04-sales-commitment",
    "BC-05-inventory-availability",
    "BC-06-fulfillment-delivery",
    "BC-07-credit-receivables",
    "BC-08-payments",
    "BC-09-business-documents",
    "BC-10-notifications",
    "BC-11-business-traceability",
]


def die(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def git_head(path: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
        ).strip()
    except subprocess.CalledProcessError as exc:
        die(f"cannot resolve Git HEAD for {path}: {exc}")


def ensure(path: Path) -> Path:
    if not path.exists():
        die(f"required source is missing: {path}")
    return path


def is_copyable(path: Path) -> bool:
    return not any(part == ".DS_Store" or part.startswith(".") for part in path.parts)


def copy_file(source: Path, destination: Path) -> None:
    ensure(source)
    if source.is_dir():
        die(f"expected file, found directory: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_tree(source: Path, destination: Path) -> None:
    ensure(source)
    if not source.is_dir():
        die(f"expected directory, found file: {source}")
    for path in sorted(source.rglob("*")):
        if not path.is_file() or not is_copyable(path.relative_to(source)):
            continue
        copy_file(path, destination / path.relative_to(source))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def provenance(title: str, generated_at: str, blueprint_commit: str, paths: str) -> str:
    return f"""# {title}

- generated-at: {generated_at}
- blueprint-source-commit: {blueprint_commit}
- blueprint-source-paths: {paths}
- source-status: CURRENT CANONICAL BLUEPRINT SUMMARY

"""


def knowledge_documents(generated_at: str, blueprint_commit: str, report_commit: str) -> dict[str, str]:
    return {
        MARKDOWN_NAMES[0]: provenance(
            "Nexa Knowledge Index", generated_at, blueprint_commit,
            "README.md; 01-shared; 03-mobile; 90-academic/mobile/course-1acc0238",
        ) + f"""This is a fast navigation layer, not an independent architecture source. Deep evidence is in ZIP 15–19.

## Authority

1. Explicit accepted Owner decision.
2. Current canonical Blueprint represented by this pack ({blueprint_commit}).
3. Verified modern implementation.
4. Current Design evidence.
5. Academic rubric for academic compliance only.
6. Foundational references/books.
7. Historical/legacy evidence.

If two knowledge files appear inconsistent, apply this authority map, consult provenance, and do not average answers. DDD or Scrum books never become Nexa Product authority.

## Pack map

- 01–04: governance, product and strategic domain.
- 05–09: tactical model, data, C4, reliability and security.
- 10–12: accepted Operations and Buyer construction baselines.
- 13–14: academic evidence and local construction gates.
- Deep evidence: `15-NEXA-ACADEMIC-AND-FOUNDATIONAL-SOURCES.zip`, `16-NEXA-C4-CANONICAL.zip`, `17-NEXA-DDD-UML-AND-DOMAIN-STORIES-CANONICAL.zip`, `18-NEXA-DATA-POSTGRESQL-ERD-CANONICAL.zip`, `19-NEXA-MOBILE-CONSTRUCTION-SOURCES.zip`.

The synchronized Mobile Report commit is {report_commit}; Blueprint remains authoritative.
""",
        MARKDOWN_NAMES[1]: provenance(
            "Authority, Governance and State Vocabulary", generated_at, blueprint_commit,
            "README.md; 01-shared/architecture; 01-shared/domain; 01-shared/security",
        ) + """Nexa is a B2B multi-tenant SaaS for importers and distributors with a strong cold-chain operations specialization. It is one C4 Software System, a Spring Boot modular monolith, and one shared authoritative PostgreSQL TARGET model.

Use status words precisely: **AS-IS** is verified current implementation evidence; **TARGET** is accepted construction direction; **FUTURE** is intentionally deferred; **OPEN** is an unresolved decision; **HISTORICAL** is provenance only. A technology decision is not implementation, technical verification, Product Acceptance, System Acceptance, or Production Readiness.

Tenant is the maximum business/data isolation boundary. Tenant is not Workspace. Missing scope fails closed. Human Identity, Workforce Membership, Buyer Relationship and Customer Account are separate concepts.

Keep → Refine → Rework is the default. Rewrite requires extraordinary evidence. Do not derive a Bounded Context from a client, module, package, schema, device or screen.
""",
        MARKDOWN_NAMES[2]: provenance(
            "Product Actors, Roles, Capabilities and Surfaces", generated_at, blueprint_commit,
            "02-product; 03-mobile/product; 01-shared/architecture/c4",
        ) + """Nexa serves tenant-scoped workforces and buyer relationships. Operations Mobile is an accepted TARGET workforce surface for access, warehouse, dispatch and delivery work. Buyer Mobile is an accepted TARGET buyer surface for delivery, handoff, receipt and discrepancy work. Platform, Portal and Website remain distinct client surfaces; none owns server business truth.

Product vocabulary is deliberate: Product is not SKU; Draft is not Purchase Request or Sales Order; Commercial Commitment is not Inventory Backing or Physical Allocation; Safety Stock is not a Reservation; Payment Reported is not Payment Confirmed; Driver Outcome is not Buyer Receipt; Notification is not Business Traceability or Security Audit.

Mobile clients request authoritative API decisions. Local intent or cache persistence does not establish business success.
""",
        MARKDOWN_NAMES[3]: provenance(
            "Domain Rules, Invariants and Ubiquitous Language", generated_at, blueprint_commit,
            "01-shared/domain; 01-shared/data/transaction-concurrency-matrix.md",
        ) + """Core Domain: Sales Commitment, Inventory Availability, and Fulfillment & Delivery. Strong invariants use the smallest correct persistence mechanism: revision/CAS for stale mutable state, conditional update or row lock for scarce resources, deterministic lock ordering, durable idempotency and explicit conflict outcomes.

Authoritative state and durable outbox rows are inserted in the same local transaction. The asynchronous publisher reads only committed outbox rows and publishes at-least-once; consumers tolerate duplicates where needed. Exactly-once transport is not claimed.

Business history remains immutable where required. Corrections and reversals create explicit evidence rather than silently rewriting issued documents, confirmed payments, inventory movements or traceability facts.
""",
        MARKDOWN_NAMES[4]: provenance(
            "Strategic DDD Context Map and Events", generated_at, blueprint_commit,
            "01-shared/domain/strategic-ddd; 01-shared/domain/processes; 01-shared/domain/bounded-contexts",
        ) + """The accepted Strategic DDD model has exactly 11 Bounded Contexts:

1. BC-01 Tenant & Access Governance
2. BC-02 Customer & Buyer Relationships
3. BC-03 Catalog & Commercial Policy
4. BC-04 Sales Commitment
5. BC-05 Inventory Availability
6. BC-06 Fulfillment & Delivery
7. BC-07 Credit & Receivables
8. BC-08 Payments
9. BC-09 Business Documents
10. BC-10 Notifications
11. BC-11 Business Traceability

Stable cross-context identities communicate ownership; they do not create cross-context relational ownership. Atomic same-context invariants use local contracts. Committed facts cross boundaries through explicit contracts and reliable outbox/inbox behavior. Deep evidence: `17-NEXA-DDD-UML-AND-DOMAIN-STORIES-CANONICAL.zip`.
""",
        MARKDOWN_NAMES[5]: provenance(
            "Tactical DDD Aggregates and Lifecycles", generated_at, blueprint_commit,
            "01-shared/domain/bounded-contexts/*/tactical-model.md; diagrams/domain-model.puml",
        ) + """Aggregate boundaries are current Blueprint decisions, not client models.

- BC-01: Tenant, HumanIdentity, WorkforceMembership, **workspace-scoped RoleDefinition**, CompanyOnboardingRequest.
- BC-02: CustomerAccount, BuyerRelationship.
- BC-03: Product, SKU, PriceList, CustomerTerms, Promotion.
- BC-04: RequestDraft, PurchaseRequest, CommercialCommitment, SalesOrder.
- BC-05: Warehouse, InventoryLot, InventoryPosition, InventoryReservation, PhysicalAllocation, WarehouseTransfer. WarehouseBacking is InventoryReservation-owned, not an Aggregate Root.
- BC-06: Fulfillment, Delivery, ProofOfDelivery, TemperatureEvidence.
- BC-07: CreditAccount, CreditReservation, Receivable, FinancialAdjustment.
- BC-08: Payment, PaymentReconciliationCase.
- BC-09: DocumentNumberSeries, BusinessDocument.
- BC-10: NotificationTemplate, Notification, NotificationPreference. PushSubscription is a technical/application delivery record, not an Aggregate Root.
- BC-11: BusinessTraceabilityRecord.

Lifecycle sources and generated UML are deep evidence in ZIP 17. Do not duplicate this model in Android or Flutter.
""",
        MARKDOWN_NAMES[6]: provenance(
            "Data, PostgreSQL, RLS, Concurrency and Idempotency", generated_at, blueprint_commit,
            "01-shared/data; 01-shared/domain/bounded-contexts/*/data",
        ) + """There is one authoritative PostgreSQL TARGET model: 95 current tables (90 owned by the 11 BCs and 5 shared technical tables). Web and Mobile do not own separate server databases. Mobile local persistence is not PostgreSQL authority.

Tenant/workspace predicates, database RLS classification and scoped candidate keys defend isolation; application correctness alone is insufficient. Same-scope root or bridge links use composite scoped foreign keys where practical. Parent-derived children document inherited scope rather than mechanically duplicating it.

Examples: membership_role joins WorkforceMembership and workspace-scoped RoleDefinition; DocumentNumberSeries is unique on `(tenant_id, workspace_id, document_type, series_code)`; current PushSubscription persists `provider_token_hash`, not raw provider tokens or `provider_endpoint_reference`.

The current tactical-to-SQL matrix names an actual guard for each mutable root. Do not add cosmetic version columns. Idempotency, revision guards, conditional updates and locks are selected by the invariant.
""",
        MARKDOWN_NAMES[7]: provenance(
            "C4 Runtime, Deployment and System Boundaries", generated_at, blueprint_commit,
            "01-shared/architecture/c4; 01-shared/architecture; 03-mobile/architecture",
        ) + """Nexa remains one C4 Software System. TARGET client containers include Operations Mobile and Buyer Mobile, each with one C4 container. Gradle modules and Flutter features are implementation boundaries, not Bounded Contexts or deployment units.

The canonical Structurizr DSL lives in Blueprint. The local rendering runtime lives separately at `complementary/structurizr` with Compose project `nexa-blueprint-architecture`; it reads the one canonical model and is not a second semantic source. It is not part of the Nexa runtime C4.

The C4 archive contains L1, L2, selective L3, seven Dynamic Views, deployment, styles and current SVG/PNG representations. AS-IS, TARGET and FUTURE remain visibly distinct.
""",
        MARKDOWN_NAMES[8]: provenance(
            "Integration Events, Reliability and Observability", generated_at, blueprint_commit,
            "01-shared/architecture; 01-shared/domain/processes; 01-shared/data",
        ) + """Committed facts can be propagated asynchronously only after authoritative transaction commit. The local transaction is: begin; business mutations; outbox insert; commit. Later, a publisher reads committed outbox data and publishes at-least-once. No Dynamic View may show commit followed by outbox persistence.

Consumers use idempotency/inbox or deduplication appropriate to their contract. External provider I/O is not held inside long database transactions unless explicitly justified. Transaction A persists/claims intent, then commits; external I/O follows; transaction B finalizes through fenced/idempotent logic.

Client telemetry (crash, latency, retry, timeout, unknown-result, scanner/evidence failure) is distinct from Business Traceability and Security Audit. Use correlation identifiers across client, API, transaction, outbox and worker without logging secrets or unnecessary PII.
""",
        MARKDOWN_NAMES[9]: provenance(
            "Security, Multitenancy, Authorization and Mobile Security", generated_at, blueprint_commit,
            "01-shared/security; 01-shared/engineering/quality; 03-mobile/architecture",
        ) + """Security is defense in depth: authentication, authorization, object-level authorization, explicit Tenant/Workspace context, server-side predicates, PostgreSQL RLS and isolation tests. Workers reconstruct explicit SYSTEM scope and clean it afterward.

The mobile verification profile is aligned to OWASP MASVS without claiming certification: STORAGE, CRYPTO, AUTH, NETWORK, PLATFORM, CODE, PRIVACY and later RESILIENCE evidence are mapped to construction checks. Use platform crypto and protected storage boundaries; never home-grown crypto. Do not log raw access/refresh tokens, payment secrets, full sensitive payloads or unnecessary PII.

Camera, intents, external navigation and deep links require explicit platform handling. Security Audit stays separate from Business Traceability.
""",
        MARKDOWN_NAMES[10]: provenance(
            "Operations Mobile Android Construction", generated_at, blueprint_commit,
            "03-mobile/architecture; 03-mobile/product; 01-shared/engineering/quality; 01-shared/security",
        ) + """Accepted TARGET: Android, Kotlin 2.4.20, Jetpack Compose BOM 2026.09.00, AGP 9.4.x, Gradle 9.6.x, JDK 17, compile/target SDK 37 and min SDK 29. This does not alter API Java 25.

Use Hilt, Jetpack Navigation 3 stable 1.1.x, CameraX and ML Kit Barcode Scanning bundled model. Manual identification fallback is mandatory. DataStore holds small settings/context metadata; Room is a justified cache/staging store only; Keystore protects local key material; WorkManager supports safe persistent retry. No local store is business authority, generic offline synchronization, permanent driver GPS tracking or server-domain duplication.

One Operations C4 container may use a small feature/client-responsibility module direction: `:app`, `feature:access`, `feature:warehouse`, `feature:dispatch`, `feature:delivery`, and core network/database/security/design-system/testing. Presentation must not directly invoke HTTP implementations or Room DAOs.
""",
        MARKDOWN_NAMES[11]: provenance(
            "Buyer Mobile Flutter Construction", generated_at, blueprint_commit,
            "03-mobile/architecture; 03-mobile/product; 01-shared/engineering/quality; 01-shared/security",
        ) + """Accepted TARGET: Flutter 3.47.2, Dart 3.13.x, Android and iOS only. Android construction baseline: min API 24, compile API 37, target API 36; API 37 target compatibility is an acceptance hardening gate. iOS minimum is 15.

Use provider for dependency injection/state contract and go_router for navigation. Prefer Views/Widgets → ViewModels → Repositories → Services, immutable models, commands/actions and selective client use cases only where complexity/reuse warrants. Flutter client orchestration never becomes authority for sales orders, delivery, payments, inventory, credit or authorization.

Feature-first direction: `app/routing`, `app/dependency_injection`, `app/bootstrap`, `core/api`, `core/security`, `core/design_system`, `core/errors`, and delivery/handoff/receipt/discrepancy/access features. Do not add a backend Aggregate-shaped `domain/entities` layer. Swift Package Manager is the modern default for Flutter 3.44+ native dependencies; CocoaPods remains compatibility tooling.
""",
        MARKDOWN_NAMES[12]: provenance(
            "Mobile Engineering Modules, API, Testing and Definition of Done", generated_at, blueprint_commit,
            "03-mobile/architecture/technical; 01-shared/engineering/quality; 01-shared/design",
        ) + """Mobile API translation is: OpenAPI/server contract → remote DTO → remote data source/service → repository → client application model → UI model/UiState. Generated API classes and remote DTOs do not escape into presentation.

Commands handle Problem Details, Idempotency-Key, If-Match/expected revision, correlation identifiers, 401/403/404 scope-safe behavior, 409 conflict, 412 stale state, retryable versus terminal failures, network failure, timeout and unknown outcome. Authoritative server confirmation establishes business success.

Every commit: unit/repository-use-case tests, static analysis, architecture fitness checks and lint. Pull request adds feature/component/Compose/widget/API contract checks. Sprint candidate adds emulator/simulator E2E, integrated API, interruption/retry/conflict and authorization cases. V1 acceptance adds physical Android/iOS evidence when applicable, scanner, network, accessibility, security, measured performance and system E2E. No coverage or performance number is invented.

Definition of Done requires applicable story/AC traceability, layer compliance, server authority, authorization, tests, accessibility, error/loading/empty/stale/conflict states, retry/idempotency, no secret/PII leakage, device fallback and current evidence. It is not Product Acceptance, System Acceptance or Production Readiness.
""",
        MARKDOWN_NAMES[13]: provenance(
            "Scrum, Academic Rubric, Backlog and Evidence", generated_at, blueprint_commit,
            "90-academic/mobile/course-1acc0238; 03-mobile; 02-product",
        ) + """The current mobile academic projection is evidence planning, not Product or architecture authority. The current rubric V4 controls academic compliance only. The academic record follows accepted targets: Operations uses Android/Kotlin/Compose; Buyer uses Flutter/Dart for Android+iOS. KMP is evaluated historical provenance. The SPIKE-002 framework-selection question is closed/superseded; device, provider, compatibility and physical-device evidence remain separate research/evidence concerns.

Scrum supports planning and empirical process. It does not redefine Nexa aggregate boundaries, database authority or client/server authority. Story/backlog evidence must distinguish planning, implementation, technical verification, Product Acceptance, System Acceptance and Production Readiness.

Deep evidence: `15-NEXA-ACADEMIC-AND-FOUNDATIONAL-SOURCES.zip` and `19-NEXA-MOBILE-CONSTRUCTION-SOURCES.zip`.
""",
        MARKDOWN_NAMES[14]: provenance(
            "Construction Environment, Quality Gates, Open Decisions and Provenance", generated_at, blueprint_commit,
            "01-shared/engineering; 03-mobile; 90-academic/mobile/course-1acc0238; complementary/construction-environment",
        ) + f"""This local construction environment is not version-controlled Blueprint canon. It records reproducible tools, validations and package provenance without secrets. The report projection commit is {report_commit}; its source commit records the exact Blueprint commit used to copy canonical artifacts and must be an ancestor of current Blueprint HEAD.

Accepted construction constraints include Android/Kotlin/Compose for Operations and Flutter/Dart for Buyer. Provider selection, telemetry provider selection, HTTP client library, local relational database library and secure-storage package selection remain intentionally deferred implementation decisions; they do not negate accepted mobile technology baselines.

Quality gates reject semantic drift: stale framework-selection claims, wrong Aggregate Root classifications, outbox-after-commit sequencing, missing high-value scoped integrity guards and unsupported concurrency claims. Local tooling readiness does not claim mobile implementation, Product Acceptance, System Acceptance, Production Readiness or release.
""",
    }


def archive_manifest(name: str, purpose: str, generated_at: str, blueprint_commit: str,
                     report_commit: str | None, stage: Path, statement: str) -> str:
    inventory = ["- `MANIFEST.md` — CURRENT CANONICAL PACKAGE METADATA"]
    for path in sorted(stage.rglob("*")):
        if path.is_file() and path.name != "MANIFEST.md":
            relative = path.relative_to(stage).as_posix()
            classification = "CURRENT CANONICAL" if not relative.startswith("historical/") else "HISTORICAL / PROVENANCE"
            inventory.append(f"- `{relative}` — {classification}")
    report_line = f"- mobile-report-commit: {report_commit}\n" if report_commit else ""
    return f"""# Archive Manifest

- archive-name: {name}
- purpose: {purpose}
- generated-at: {generated_at}
- blueprint-commit: {blueprint_commit}
{report_line}- source-of-truth: Explicit accepted Owner decisions, then current canonical Blueprint. This archive is evidence, not an independent source of truth.
- classification: CURRENT CANONICAL unless explicitly marked otherwise below.

## Authority statement

{statement}

## Complete internal file inventory

{chr(10).join(inventory) if inventory else '- (archive content generated after manifest creation)'}
"""


def make_zip(output: Path, stage: Path) -> None:
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(stage.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(stage).as_posix())


def prepare_academic(stage: Path, blueprint: Path, generated_at: str, blueprint_commit: str,
                     report_commit: str) -> None:
    rubric = COMP / "academic/courses/mobile-1acc0238/rubrics"
    copy_file(rubric / "mobile-applications-final-rubric.md", stage / "academic-authority/mobile-applications-final-rubric-v4.md")
    copy_file(rubric / "source/mobile-applications-final-rubric.pdf", stage / "academic-authority/mobile-applications-final-rubric-v4.pdf")
    copy_file(rubric / "final-project-rubric.md", stage / "academic-authority/final-project-rubric.md")
    # Complementary projections are preserved as historical evidence.  Current
    # academic semantics come from Blueprint /90-academic and must not be
    # presented as a second current canon inside the knowledge archive.
    copy_tree(COMP / "academic/courses/mobile-1acc0238/projections", stage / "historical/academic-projections")
    copy_file(COMP / "library/02-domain-driven-design/domain-driven-design-eric-evans.pdf",
              stage / "foundational-theory/domain-driven-design-eric-evans.pdf")
    write_text(stage / "official-method-reference/OFFICIAL-SCRUM-GUIDE-2020-REFERENCE.md", """# Official Scrum Guide 2020 Reference

- organization: Scrum Guides
- official URL: https://scrumguides.org/scrum-guide.html
- status: OFFICIAL METHOD REFERENCE

No local official Scrum Guide PDF was substituted into this archive. Consult the official source if the current guide is required. Scrum guidance does not override accepted Nexa Product or Architecture canon.
""")
    write_text(stage / "MANIFEST.md", archive_manifest(
        ZIP_NAMES[0], "Primary academic constraints and foundational theory.", generated_at,
        blueprint_commit, report_commit, stage,
        "The V4 mobile rubric is ACADEMIC AUTHORITY. Eric Evans is FOUNDATIONAL THEORY. The official Scrum reference is OFFICIAL METHOD REFERENCE. Academic projections are HISTORICAL/ACADEMIC planning evidence. academic rubric controls academic compliance only; DDD/Scrum books do not override accepted Nexa Product/Architecture canon.",
    ))


def prepare_c4(stage: Path, blueprint: Path, generated_at: str, blueprint_commit: str) -> None:
    c4 = blueprint / "01-shared/architecture/c4"
    copy_tree(c4 / "structurizr", stage / "source/structurizr")
    copy_tree(c4 / "exports", stage / "generated/exports")
    for name in ("README.md", "component-rubric-coverage.md"):
        copy_file(c4 / name, stage / "source" / name)
    copy_file(blueprint / "01-shared/architecture/README.md", stage / "provenance/architecture-readme.md")
    readme = (c4 / "structurizr/README.md").read_text(encoding="utf-8")
    view_keys = [line.strip()[2:] for line in readme.splitlines() if line.strip().startswith("- `Nexa-")]
    write_text(stage / "provenance/view-keys.md", "# Current C4 View Keys\n\n" + "\n".join(f"- `{key.rstrip('`')}`" for key in view_keys))
    write_text(stage / "MANIFEST.md", archive_manifest(
        ZIP_NAMES[1], "Current canonical C4 DSL, generated views and provenance.", generated_at,
        blueprint_commit, None, stage,
        "Source paths are `source/structurizr` and `source`. Generated SVG/PNG are under `generated/exports`. View keys are recorded in `provenance/view-keys.md`. AS-IS, TARGET and FUTURE labels in the current source remain authoritative; no obsolete C4 model is presented as canonical.",
    ))


def prepare_ddd(stage: Path, blueprint: Path, generated_at: str, blueprint_commit: str) -> None:
    domain = blueprint / "01-shared/domain"
    for relative in ("strategic-ddd", "ubiquitous-language", "ownership", "interaction-contracts"):
        candidate = domain / relative
        if candidate.exists():
            copy_tree(candidate, stage / "strategic-ddd" / relative)
    copy_file(domain / "README.md", stage / "strategic-ddd/README.md")
    copy_tree(domain / "bounded-contexts", stage / "tactical-ddd/bounded-contexts")
    copy_tree(domain / "state-machines", stage / "generated-representations/state-machines")
    copy_tree(domain / "processes", stage / "generated-representations/processes")
    eventstorming = domain / "eventstorming"
    if eventstorming.exists():
        copy_tree(eventstorming, stage / "discovery/eventstorming")
    else:
        copy_file(domain / "processes/eventstorming.md", stage / "discovery/current-eventstorming.md")
    write_text(stage / "MANIFEST.md", archive_manifest(
        ZIP_NAMES[2], "Current Strategic/Tactical DDD, UML, lifecycle and Domain Story evidence.", generated_at,
        blueprint_commit, None, stage,
        "`strategic-ddd` contains accepted strategic material; `tactical-ddd` contains all 11 current BC sources including Domain UML; `generated-representations` contains current renders. Discovery material is separated and never overrides current aggregate boundaries.",
    ))


def prepare_data(stage: Path, blueprint: Path, generated_at: str, blueprint_commit: str) -> None:
    data = blueprint / "01-shared/data"
    copy_tree(data, stage / "source/master-and-shared")
    bc_root = blueprint / "01-shared/domain/bounded-contexts"
    for bc in BCS:
        data_dir = bc_root / bc / "data"
        copy_tree(data_dir, stage / "source/per-bc" / bc)
    copy_file(data / "master-database-diagram.puml", stage / "generated/master-erd/master-database-diagram.puml")
    copy_file(data / "master-database-diagram.svg", stage / "generated/master-erd/master-database-diagram.svg")
    copy_file(data / "master-database-diagram.png", stage / "generated/master-erd/master-database-diagram.png")
    for bc in BCS:
        data_dir = bc_root / bc / "data"
        for suffix in ("puml", "svg", "png"):
            copy_file(data_dir / f"database-diagram.{suffix}", stage / "generated/per-bc" / bc / f"database-diagram.{suffix}")
    write_text(stage / "MANIFEST.md", archive_manifest(
        ZIP_NAMES[3], "One authoritative PostgreSQL TARGET model, ERDs and data architecture evidence.", generated_at,
        blueprint_commit, None, stage,
        "There is one authoritative PostgreSQL TARGET model: 95 current tables (90 BC-owned plus 5 shared technical). Web/Mobile do not own separate server databases. Mobile local persistence is not PostgreSQL authority. Cross-BC stable IDs do not imply relational ownership. `source` contains master/shared and all 11 per-BC SQL models; `generated` contains master and per-BC ERD representations.",
    ))


def official_references(generated_at: str) -> str:
    refs = [
        ("Android Developers", "https://developer.android.com/"),
        ("Kotlin", "https://kotlinlang.org/docs/home.html"),
        ("Jetpack Compose", "https://developer.android.com/develop/ui/compose"),
        ("Hilt", "https://developer.android.com/training/dependency-injection/hilt-android"),
        ("Navigation 3", "https://developer.android.com/guide/navigation/navigation-3"),
        ("CameraX", "https://developer.android.com/media/camera/camerax"),
        ("ML Kit Barcode Scanning", "https://developers.google.com/ml-kit/vision/barcode-scanning/android"),
        ("Room", "https://developer.android.com/training/data-storage/room"),
        ("DataStore", "https://developer.android.com/topic/libraries/architecture/datastore"),
        ("WorkManager", "https://developer.android.com/topic/libraries/architecture/workmanager"),
        ("Flutter", "https://docs.flutter.dev/"),
        ("Dart", "https://dart.dev/guides"),
        ("provider", "https://pub.dev/packages/provider"),
        ("go_router", "https://pub.dev/packages/go_router"),
        ("OWASP MASVS", "https://mas.owasp.org/MASVS/"),
        ("OpenAPI Specification", "https://spec.openapis.org/oas/latest.html"),
        ("Scrum Guide", "https://scrumguides.org/scrum-guide.html"),
    ]
    return "# Official References\n\n- consulted-for-package: " + generated_at + "\n- scope: Primary-source construction references; Nexa canonical decisions remain above external references.\n\n" + "\n".join(f"- [{name}]({url})" for name, url in refs) + "\n"


def prepare_mobile(stage: Path, blueprint: Path, generated_at: str, blueprint_commit: str) -> None:
    copy_tree(blueprint / "03-mobile", stage / "canonical/mobile")
    copy_file(blueprint / "01-shared/architecture/technology-baseline.md",
              stage / "canonical/architecture/technology-baseline.md")
    for adr in (
        "adr-0018-operations-mobile-native-android.md",
        "adr-0019-buyer-mobile-flutter.md",
        "adr-0020-mobile-client-layering.md",
        "adr-0021-mobile-local-persistence-boundary.md",
    ):
        copy_file(blueprint / "01-shared/architecture/decisions/adr" / adr,
                  stage / "canonical/architecture/decisions/adr" / adr)
    for relative in (
        "01-shared/engineering/quality",
        "01-shared/security",
        "01-shared/design/design-system/web-evidence",
        "90-academic/mobile/course-1acc0238",
    ):
        source = blueprint / relative
        if source.exists():
            copy_tree(source, stage / "canonical" / relative)
    copy_file(ROOT / "skills/manifest.md", stage / "construction-environment/skills-manifest.md")
    copy_file(ROOT / "toolchain-manifest.md", stage / "construction-environment/toolchain-manifest.md")
    write_text(stage / "OFFICIAL-REFERENCES.md", official_references(generated_at))
    write_text(stage / "MANIFEST.md", archive_manifest(
        ZIP_NAMES[4], "Accepted Mobile construction sources and concise official references.", generated_at,
        blueprint_commit, None, stage,
        "Canonical/current mobile sources cover accepted Android/Kotlin/Compose Operations and Flutter/Dart Android+iOS Buyer baselines, application layering, module boundaries, DI/navigation, API boundary, environments, local persistence, security, test/DoD/fitness evidence and Design System engineering contract. Official references provide dated primary-source links; they do not override Nexa canon.",
    ))


def build_archives(upload: Path, blueprint: Path, generated_at: str, blueprint_commit: str,
                   report_commit: str) -> None:
    builders = [prepare_academic, prepare_c4, prepare_ddd, prepare_data, prepare_mobile]
    with tempfile.TemporaryDirectory(prefix="nexa-gpt-stage-", dir=ROOT / "gpt") as tmp:
        temp = Path(tmp)
        for name, builder in zip(ZIP_NAMES, builders):
            stage = temp / Path(name).stem
            stage.mkdir(parents=True)
            if builder is prepare_academic:
                builder(stage, blueprint, generated_at, blueprint_commit, report_commit)
            else:
                builder(stage, blueprint, generated_at, blueprint_commit)
            make_zip(upload / name, stage)


def write_support_files(generated_at: str, blueprint_commit: str, report_commit: str) -> None:
    support = ROOT / "gpt/support"
    write_text(support / "knowledge-manifest.md", f"""# Nexa GPT Knowledge Package Manifest

- generated-at: {generated_at}
- blueprint-source-commit: {blueprint_commit}
- mobile-report-commit: {report_commit}
- upload policy: exactly 15 Markdown files and 5 ZIP archives; no other root files.
- source-of-truth: accepted Owner decisions then current Blueprint.

Use `../validate_knowledge_package.py` for deterministic structure and archive verification. Checksums are kept outside `knowledge-upload`.
""")
    write_text(ROOT / "gpt/archives/README-local.md", """# Local archive location

The five ZIP evidence archives are intentionally the five approved Knowledge uploads in `../knowledge-upload/`. They are not duplicated here, so there is one local copy of each generated archive.
""")


def clear_upload(upload: Path) -> None:
    upload.mkdir(parents=True, exist_ok=True)
    for child in upload.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blueprint-dir", type=Path, default=DEFAULT_BLUEPRINT)
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    blueprint = ensure(args.blueprint_dir.resolve())
    report = ensure(args.report_dir.resolve())
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    blueprint_commit = git_head(blueprint)
    report_commit = git_head(report)
    upload = ROOT / "gpt/knowledge-upload"
    clear_upload(upload)
    docs = knowledge_documents(generated_at, blueprint_commit, report_commit)
    if set(docs) != set(MARKDOWN_NAMES):
        die("Markdown generator name set is not exact")
    for name in MARKDOWN_NAMES:
        write_text(upload / name, docs[name])
    write_support_files(generated_at, blueprint_commit, report_commit)
    build_archives(upload, blueprint, generated_at, blueprint_commit, report_commit)
    print(json.dumps({
        "upload": str(upload),
        "blueprint_commit": blueprint_commit,
        "report_commit": report_commit,
        "markdown": len(MARKDOWN_NAMES),
        "zip": len(ZIP_NAMES),
    }, indent=2))


if __name__ == "__main__":
    main()
