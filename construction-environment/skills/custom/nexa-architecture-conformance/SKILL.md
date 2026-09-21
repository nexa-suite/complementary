---
name: nexa-architecture-conformance
description: Check a Nexa change against current Blueprint C4, DDD, SQL and ownership boundaries.
---

# Nexa architecture conformance

Use for a bounded conformance review of a proposed or completed Nexa change.
Start from local Blueprint sources: `01-shared/architecture/c4`,
`01-shared/domain/bounded-contexts`, `01-shared/data`, and the relevant ADR.

Check only the affected invariant: owning context, aggregate boundary, scoped
relational integrity, transaction/outbox ordering, concurrency guard, API
boundary and generated-artifact provenance. Keep shared PostgreSQL logical
ownership distinct from physical schemas and do not add cross-BC FKs merely to
enforce scope.

Report verified evidence, caveats and genuine open decisions. Do not redesign
the accepted architecture during a conformance check.
