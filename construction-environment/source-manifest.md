# Construction Source Manifest

| Source | Local path | Authority class | Use in this environment |
|---|---|---|---|
| Nexa Blueprint | `../../blueprint` | CURRENT CANONICAL | Semantic source for the package and custom skills |
| Mobile Report projection | `../../mobile-report` | DOWNSTREAM PROJECTION | Exact report provenance only; never promoted over Blueprint |
| Mobile Applications V4 rubric | `../academic/courses/mobile-1acc0238/rubrics/mobile-applications-final-rubric.md` and `source/mobile-applications-final-rubric.pdf` | ACADEMIC AUTHORITY | Academic compliance evidence only |
| Eric Evans DDD | `../library/02-domain-driven-design/domain-driven-design-eric-evans.pdf` | FOUNDATIONAL THEORY | Theory reference only |
| Structurizr runtime | `../structurizr/compose.yml` | LOCAL RENDERING TOOLING | Reads canonical Blueprint DSL; no second C4 source |

Authority order: explicit accepted Owner decision; current Blueprint; verified modern implementation; Design evidence; academic rubric for academic compliance only; foundational references; historical/legacy evidence. Books, course material and local tooling do not override accepted Nexa canon.
