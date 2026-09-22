# Cómo contribuir

Esta es una guía de implementación narrativa. Lo que se escribe vive en `input/pagecontent/`, y el orden, los títulos y el menú salen de `sushi-config.yaml`. No hay nada más que tocar para aportar contenido.

Antes de empezar, instale lo que pide el [README](README.md) y ejecute `make tools` una vez para descargar el IG Publisher.

Una buena forma de empezar es [`TODO.md`](TODO.md), que reúne lo que el repositorio tiene pendiente: desde puntos concretos marcados en las páginas, como diagramas por rehacer o una comprobación técnica que falta, hasta capítulos enteros que ya están declarados en `sushi-config.yaml` y esperan a que alguien los escriba. Si toma uno, dígalo en un issue para que nadie trabaje dos veces lo mismo.

Las dudas se preguntan en [Discussions](https://github.com/meddyg/Health-Information-Exchange/discussions), sea sobre la guía o sobre los perfiles en que se apoya. Los issues quedan así para el trabajo concreto, que es lo que se puede tomar, revisar y cerrar.

## Cambios de arquitectura

Todo cambio que toque decisiones en la arquitectura necesita un issue que lo abarque antes de que se escriba una línea. Cuenta como tal cualquier cosa que altere el alcance de la guía, los actores o sus agrupaciones, las transacciones y su reparto entre la infraestructura central y los miembros, o una decisión que ya esté escrita y razonada en el Volumen 1.

La propuesta se sustenta en fuentes, no en preferencias. Sirven los perfiles IHE y las especificaciones FHIR aplicables, los RFC que gobiernen el mecanismo en cuestión y la documentación de los sistemas involucrados, citando siempre la sección exacta y su texto literal, igual que las notas al pie de la guía. Lo que no tenga ese respaldo se sigue discutiendo en el issue y no llega al pull request.

## Ciclo de trabajo

`main` es la rama de producción, la que sirve <https://hix.meddyg.com/fhir/hix/>, y nada llega ahí directamente. Todo cambio se integra a `dev` mediante un pull request, y lo acumulado en `dev` se promueve a `main` cuando se publica una versión.

1. **Nueva rama desde `dev`** con un nombre del estilo `feat/descripcion-corta`, `fix/`, `docs/`, `build/` o `chore/`.
2. **Escriba contra `make preview`**, que recarga al guardar y marca palabra por palabra lo que la página ganó, perdió o cambió respecto a HEAD.
3. **Ejecute `make format`** antes de cada commit; corrige el estilo de las páginas y reporta lo que no puede arreglar solo.
4. **Verifique con `make site`**, que es la build que cuenta y debe terminar sin errores.
5. **Los commits siguen [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/)**, escritos en inglés, en minúscula y en imperativo, como `docs: tighten the identity rules in Volume 1`. Los tipos en uso son `feat` para contenido nuevo de la especificación, `fix` para correcciones, `docs` para la redacción y el material de apoyo, `build` y `ci` para el pipeline de publicación, y `chore` para lo demás. El ámbito es opcional de momento mientras se define el criterio para este.
6. **Abra el pull request contra `dev`** describiendo qué cambia en la especificación, no solo qué archivos toca. El pipeline despliega una vista previa del sitio en `https://pr-N.hix-ig.pages.dev/fhir/hix/` para revisar el resultado antes de integrar.

## Convenciones de las páginas

1. **Cada página empieza con prosa, sin encabezado de nivel uno.** El título lo pone `sushi-config.yaml` y el sitio numera las secciones según el orden declarado ahí.
2. **Una página nueva se registra dos veces** en ese archivo, bajo `pages:` para que exista y bajo `menu:` para que se pueda llegar a ella.
3. **Los enlaces internos apuntan al `.html` renderizado**, como `volume-1-concepts.html#seccion`, nunca al archivo `.md`.
4. **Las tablas llevan `{: .table .table-bordered}`** en la línea siguiente, y las anclas explícitas se declaran igual, con `{: #figura-2-1}`.
5. **Se escribe en español (de momento), en frases completas**, con afirmaciones numeradas cuando la idea se presta y las aclaraciones como notas, no entre paréntesis.
6. **Los actores y transacciones que define una especificación conservan su nombre original en inglés**, por ejemplo Document Registry, nunca «Registro documental».
7. **Toda afirmación sobre lo que exige una especificación va con nota al pie** que enlaza la sección exacta y cita su texto literal, como en `volume-1-concepts.md`.

## Diagramas

Las fuentes están en `_diagrams/`. Las de PlantUML se rendarían con `make diagrams` hacia `input/images/`. Las de draw.io no se pueden exportar automáticamente, entonces si o si hay que exportarlas a mano desde la aplicación.

## Conducta y seguridad

Participar aquí implica respetar el [Código de Conducta](CODE_OF_CONDUCT.md). Los hallazgos de seguridad no se reportan en un issue público, sino por la vía que describe la [política de seguridad](SECURITY.md).
