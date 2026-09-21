---
name: nexa-operations-mobile
description: Construct accepted Nexa Operations Mobile Android slices while preserving API and domain authority.
---

# Nexa Operations Mobile

Use for Nexa Operations Mobile construction only. Its accepted TARGET is native
Android/Kotlin/Jetpack Compose; read local Blueprint ADR-0018 and
`03-mobile/architecture/technical` before implementation.

Use Compose, ViewModels/UDF, Hilt, Navigation 3, CameraX/ML Kit with mandatory
manual fallback, Keystore, DataStore, justified Room staging/cache and
WorkManager safe retry. Feature and Gradle-module boundaries are client
construction concerns, not Bounded Contexts.

The API owns tenant scope, inventory, delivery and business lifecycle. Local
cache, draft and retry metadata are non-authoritative. Do not claim device,
provider, implementation or Product Acceptance evidence without its own proof.
