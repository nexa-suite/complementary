# Nexa Skills Manifest

- recorded-at: 2026-09-20
- source model: official/vendor skills remain vendor-owned; Nexa custom skills have one local source and user-level symlinks.

## Android official skills

Installed under `~/.codex/skills/` through Android CLI:

- `android-cli`
- `testing-setup`
- `camerax`
- `navigation-3`
- `edge-to-edge`
- `android-intent-security`
- `r8-analyzer`
- `android-profiler`
- `adaptive`

## Flutter/Dart official plugin

- marketplace: `dart-flutter`
- plugin: `dart-flutter@dart-flutter`
- version: `1.0.5`
- local marketplace path: `~/.codex/.tmp/marketplaces/dart-flutter`
- confirmed capabilities: Flutter architecture, widget and integration testing, responsive layout, declarative routing, localization, JSON serialization; Dart unit testing, static analysis, package-conflict resolution and coverage.

## Nexa custom skills

| Skill | Canonical local source | User-level availability |
|---|---|---|
| `nexa-canonical-guardrails` | `custom/nexa-canonical-guardrails/SKILL.md` | `~/.agents/skills/nexa-canonical-guardrails` symlink |
| `nexa-implementation-slice` | `custom/nexa-implementation-slice/SKILL.md` | `~/.agents/skills/nexa-implementation-slice` symlink |
| `nexa-architecture-conformance` | `custom/nexa-architecture-conformance/SKILL.md` | `~/.agents/skills/nexa-architecture-conformance` symlink |
| `nexa-operations-mobile` | `custom/nexa-operations-mobile/SKILL.md` | `~/.agents/skills/nexa-operations-mobile` symlink |
| `nexa-buyer-mobile` | `custom/nexa-buyer-mobile/SKILL.md` | `~/.agents/skills/nexa-buyer-mobile` symlink |
| `nexa-quality-evidence-gates` | `custom/nexa-quality-evidence-gates/SKILL.md` | `~/.agents/skills/nexa-quality-evidence-gates` symlink |

Each custom skill passed the Codex skill-creator `quick_validate.py` structural
check available in the local Codex installation. Routing sanity expectations:
warehouse barcode identification → `nexa-operations-mobile` plus
CameraX/testing; Buyer receipt → `nexa-buyer-mobile`; API versus Blueprint →
`nexa-architecture-conformance`; Product Accepted claim →
`nexa-quality-evidence-gates`.
