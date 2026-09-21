# Nexa skill bundle — HISTORICAL SNAPSHOT

Estado: `HISTORICAL SNAPSHOT` — fecha de captura `2026-08-27`.

Este directorio conserva el bundle portable de esa fecha. Su `MANIFEST.tsv` y
sus contenidos históricos no se reescriben para aparentar actualidad. El
baseline operativo actual está en
[`CURRENT-NEXA-AGENT-BASELINE.md`](./CURRENT-NEXA-AGENT-BASELINE.md).

El snapshot fue recopilado desde el entorno local de Codex con perfiles para:

- `blueprint`: Product, DDD, gobernanza, C4 y evidencia.
- `api`: Java 25, Spring Boot 4.1, REST/OpenAPI, JPA, PostgreSQL y Flyway.
- `platform` y `portal`: Angular 22, TypeScript estricto, Signals, RxJS,
  Angular Material y Playwright.
- `website` y `design-lab`: superficies web y Design System.
- `mobile`: snapshot anterior a la canonización de las tecnologías aceptadas.

La tecnología TARGET vigente es Operations Mobile = Android/Kotlin/Jetpack
Compose y Buyer Mobile = Flutter/Dart para Android+iOS, según Blueprint.

## Cómo usar el snapshot

Cada carpeta contiene una skill completa, incluyendo `references/`, `scripts/`,
`assets/` y `templates/` cuando existen. Para instalar el snapshot en otro
entorno Codex, copia las carpetas hijas a su directorio de skills:

```text
nexa-suite/complementary/skills/<skill-name>/  ->  <directorio-Codex>/skills/<skill-name>/
```

Consulta [`MANIFEST.tsv`](./MANIFEST.tsv) para el estado histórico. Contiene
**63 skills**: 27 base, 21 condicionales y 15 futuras.

## Reglas para el equipo

1. Leer primero las instrucciones del repositorio y el Blueprint cuando la
   tarea sea de arquitectura, dominio o documentación.
2. Mantener AS-IS separado de TARGET y no derivar Bounded Contexts desde
   nombres de carpetas o paquetes.
3. No inventar endpoints, entidades, dependencias ni decisiones de producto.
4. API conserva la autoridad de negocio, tenant, autorización y contratos; los
   clientes no duplican reglas de dominio.
5. Validar en el nivel correspondiente: tests/build, OpenAPI, runtime,
   navegador, accesibilidad o `validate-blueprint.sh`.
6. Este bundle no instala plugins ni dependencias externas.

## Proveniencia

`MANIFEST.tsv` identifica área, estado y propósito de cada skill. Los archivos
del snapshot se conservaron literalmente; no se modifican para hacerlos pasar
por un baseline actual. Skill != Product authority: toda decisión semántica
debe volver al Blueprint vigente.
