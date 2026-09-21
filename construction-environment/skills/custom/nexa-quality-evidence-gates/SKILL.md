---
name: nexa-quality-evidence-gates
description: Apply Nexa validation and evidence gates without converting planned work into acceptance claims.
---

# Nexa quality evidence gates

Use before reporting a Nexa slice, architecture artifact or Mobile milestone as
ready. Read local Blueprint `01-shared/engineering/quality`,
`01-shared/security`, `04-delivery` and the directly relevant product source.

Run deterministic validation first, then targeted implementation evidence.
Separate static/documentation PASS, test PASS, device evidence, deployment,
solution validation, Product Acceptance and production readiness. Preserve
negative evidence and open provider/device gates; do not fabricate screenshots,
URLs, credentials, physical-device results or approval.

For canonical assets, verify source provenance and generated-byte identity.
For Mobile, require tenant/context failure handling, idempotency/conflict states,
local non-authority and sensitive-data protection before calling a slice done.
