# Nexa Construction Environment

Reusable, safe construction tooling for Nexa. This directory supports
Blueprint and application repositories; it is not Product, Domain or
Architecture authority.

Expected sibling layout:

```text
nexa-suite/
├── blueprint/
├── complementary/
├── mobile-report/        # optional downstream evidence
└── api/                  # optional local runtime
```

Run the secret-free readiness doctor:

```bash
./doctor.sh
```

Build the local GPT package from current sibling repositories:

```bash
python3 gpt/build_knowledge_package.py \
  --blueprint-dir ../../blueprint \
  --report-dir ../../mobile-report
python3 gpt/validate_knowledge_package.py
```

The generated upload directory is local-only: exactly 15 Markdown indexes and
five evidence ZIP archives. Checksums stay outside that directory. Generated
reports, caches, host toolchains and personal runtime state are ignored.

`toolchains/flutter-3.47.2/` may exist as an optional local checkout; it is not
required source and is never committed. Set `NEXA_FLUTTER_DIR` to use another
local checkout, or let `doctor.sh` detect host Flutter.

Canonical C4 DSL remains in Blueprint. Structurizr tooling lives in
`../structurizr/`, consumes the Blueprint workspace and is not a Nexa runtime
C4 Container.
