# Current Nexa agent baseline

Verified: `2026-09-20`. This is public operational metadata, not Product or
Architecture authority. All Nexa skills must defer canonical semantics to
`nexa-suite/blueprint`.

## Official Android construction skills

Selected from the Android CLI skill source (`android skills add`):

- `android-cli`
- `testing-setup`
- `camerax`
- `navigation-3`
- `edge-to-edge`
- `android-intent-security`
- `r8-analyzer`
- `android-profiler`
- `adaptive`

Classification: official selected construction skills. The Android CLI is the
installation authority; exact installed versions are host evidence, not a
Product decision.

## Official Flutter/Dart construction skill

- `dart-flutter@dart-flutter`, origin `flutter/agent-plugins`, marketplace
  version `1.0.5`.

Classification: official current plugin for Buyer Mobile construction.

## Nexa custom skills

Current custom skill names:

- `nexa-canonical-guardrails`
- `nexa-implementation-slice`
- `nexa-architecture-conformance`
- `nexa-operations-mobile`
- `nexa-buyer-mobile`
- `nexa-quality-evidence-gates`

Origin: `complementary/construction-environment/skills/custom/<name>`.
Classification: current Nexa custom skills; local source and generated links
remain local-only. Install them into the agent skills directory with the
documented setup helper rather than committing host-specific paths.

## Authority rule

Skill != Product authority. Agents must distinguish AS-IS, TARGET, evidence,
Product Acceptance, System Acceptance and Production Readiness, and must read
the current Blueprint decision before making a semantic claim.
