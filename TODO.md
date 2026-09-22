# Pendientes

Este archivo reúne lo que el repositorio tiene marcado como pendiente. Cada entrada dice dónde vive, para que al resolverla se borren las dos cosas a la vez, la marca en su archivo y la línea de aquí.

## Marcas en las páginas

1. **Rehacer en draw.io los diagramas de la sección 2.2.** Los tres diagramas de las pestañas son un mock en PlantUML y deben quedar como la Figura 2-1. En `input/pagecontent/volume-1-actors.md:8`.
2. **Alinear el tratamiento de la aplicación del paciente.** Figura como cliente en el Authorization Server y puede ser un cliente confidencial cuando tiene backend propio, y de eso depende si se la considera miembro y qué le exigen ATNA, CT y la auditoría. En `input/pagecontent/volume-1-groupings.md:31` (requiere discusión previa).
3. **Comprobar con pruebas qué guarda el registro de mensajes de X-Road.** Hay que saber si conserva los mensajes completos y cómo se configura, y reflejar el resultado en esa opción y en las decisiones de política de la sección 2.6. En `input/pagecontent/volume-1-options.md:37`.

## Páginas declaradas pero no escritas

La estructura completa de la guía ya está en `sushi-config.yaml`, comentada hasta que cada parte exista. Son treinta páginas repartidas así.

1. **El Volumen 2 entero**, once páginas contando su portada y el índice de transacciones, con ITI-65, ITI-67, ITI-68, ITI-83, ITI-104, ITI-90 y las tres transacciones propias HIX-1, HIX-2 y HIX-3, desde la línea 69.
2. **La sección de conformidad**, seis páginas con las ediciones soportadas, la matriz de requisitos, las desviaciones respecto a IHE, las extensiones propias y los artefactos, desde la línea 107.

Nota: las dependencias en el archivo de sushi están comentadas para evitar problemas con el CI de despliegue durante la escritura de estas páginas. En el release formal se descomentaran y se hará la integration completa a la guía.

## Capacidades aplazadas a una versión posterior

Son parte de la arquitectura y están anunciadas como tales en la [descripción general](input/pagecontent/index.md), no son omisiones.

1. **Consentimiento anticipado del paciente.** La guía ya dice dónde se aplica la decisión de divulgación y qué información necesita. Quedan el modelo de consentimiento (PCF), su ciclo de vida y sus políticas, a partir de los perfiles IHE aplicables. **(PRIORIDAD)**
2. **Auditoría de operaciones y divulgaciones.** La guía ya establece que hay que registrar las operaciones en ambos extremos. Quedan el modelo de consulta y el comportamiento ante fallos.
3. Versión de la guía en inglés.
