# Nexa skill bundle

Catálogo portable de las skills que uso para trabajar en Nexa. El bundle fue
recopilado el **2026-08-27** desde el entorno local de Codex y está alineado
con el workspace actual:

- `blueprint`: Product, DDD, gobernanza, C4 y evidencia.
- `api`: Java 25, Spring Boot 4.1, REST/OpenAPI, JPA, PostgreSQL y Flyway.
- `platform` y `portal`: Angular 22, TypeScript estricto, Signals, RxJS,
  Angular Material y Playwright.
- `website`: sitio estático público.
- `design-lab`: Design System Angular y validación visual/accesible.
- `mobile`: runway documental; todavía no tiene tecnología nativa seleccionada.

## Cómo usarlo

Cada carpeta contiene una skill completa, incluyendo sus `references/`,
`scripts/`, `assets/` y `templates/` cuando existen. Para instalar el bundle en
otro entorno Codex, copia las carpetas hijas de este directorio al directorio
de skills del usuario:

```text
nexa-suite/skills/<skill-name>/  ->  <directorio-Codex>/skills/<skill-name>/
```

La carpeta `superpowers` se invoca como `using-superpowers` en el flujo de
trabajo. Consulta [`MANIFEST.tsv`](./MANIFEST.tsv) para saber qué skills son
  base, condicionales o futuras. Actualmente contiene **63 skills**: 27 base,
  21 condicionales y 15 futuras.

## Clasificación

| Estado | Significado |
|---|---|
| `base` | Se recomienda tenerla disponible para el trabajo cotidiano de Nexa. |
| `conditional` | Se usa únicamente cuando la tarea activa requiere esa capacidad. |
| `future` | Corresponde al runway mobile/KMP/SwiftUI o a una tecnología aún no seleccionada. |

## Reglas para el equipo

1. Leer primero las instrucciones del repositorio y el Blueprint cuando la
   tarea sea de arquitectura, dominio o documentación.
2. Mantener AS-IS separado de TARGET y no derivar Bounded Contexts desde
   nombres de carpetas o paquetes.
3. No inventar endpoints, entidades, dependencias ni decisiones de producto.
4. API conserva la autoridad de negocio, tenant, autorización y contratos;
   los clientes no duplican reglas de dominio.
5. Validar en el nivel correspondiente: tests/build, OpenAPI, runtime,
   navegador, accesibilidad o `validate-blueprint.sh`.
6. Este bundle no instala plugins ni dependencias externas. Figma, Notion,
   GitHub, Sentry y proveedores de despliegue requieren además su conector o
   CLI autorizado en cada entorno.

## Exclusiones deliberadas

No se incluyeron skills de trading, música, CRM, tareas personales ni otras
capacidades sin relación con Nexa. Tampoco se incluyeron `aspnet-core` como
skill base —ASP.NET pertenece a la referencia legacy— ni los builders de
Spring/Kotlin específicos para un backend que hoy es Java 25. Las skills de
Kotlin aparecen solo como `future` porque Mobile aún es documentación y
runway, no una implementación nativa.

## Proveniencia e integridad

`MANIFEST.tsv` identifica el área, estado y propósito de cada skill. Los
archivos se copiaron literalmente desde el entorno local; no se modificó su
contenido. El bundle vive en el nivel raíz de `nexa-suite`, que es un
contenedor y no un repositorio Git, por lo que no altera ninguno de los siete
repositorios independientes.

También se generó `nexa-skills-bundle-2026-08-27.tar.gz` en la raíz para
compartir el bundle completo como un solo archivo.
