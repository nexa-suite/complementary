---
name: nexa-implementation-slice
description: Build one Nexa implementation slice without widening accepted Product or Domain scope.
---

# Nexa implementation slice

Use when an accepted Nexa slice is ready to implement. Locate its canonical
Blueprint Product, tactical, data and API-contract sources before touching an
application repository.

Build the smallest vertical slice that preserves tenant scope, authorization,
idempotency, concurrency and error outcomes. Keep presentation, application,
domain and infrastructure responsibilities explicit. Do not use client cache,
events or a new service to bypass an atomic invariant.

Validate the narrowest relevant tests first. Record gaps as AS-IS/TARGET or
OPEN evidence; never claim Product Acceptance from compilation or a green unit
test.
