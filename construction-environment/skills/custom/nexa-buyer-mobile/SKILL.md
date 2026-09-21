---
name: nexa-buyer-mobile
description: Construct accepted Nexa Buyer Mobile Flutter slices while preserving API and domain authority.
---

# Nexa Buyer Mobile

Use for Nexa Buyer Mobile construction only. Its accepted TARGET is
Flutter/Dart for Android+iOS; read local Blueprint ADR-0019 and
`03-mobile/architecture/technical` before implementation.

Use feature-first `app/core/features` organization, Views/Widgets, ViewModels,
`provider`, `go_router`, immutable Commands and repositories/services. Do not
create a generic client `domain/entities` duplicate of Nexa aggregates. Modern
Swift Package Manager is the default iOS path; CocoaPods is compatibility only.

Follow the mobile API anti-corruption path and surface Problem Details,
idempotency, conflicts and unknown results explicitly. Local state is never
server authority and technology selection does not prove implementation or
Product Acceptance.
