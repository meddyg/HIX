# Pendientes

Este archivo reúne lo que el repositorio tiene marcado como pendiente. Cada entrada dice dónde vive, para que al resolverla se borren las dos cosas a la vez, la marca en su archivo y la línea de aquí.

## Marcas en las páginas

1. **Rehacer en draw.io los diagramas de la sección 2.2.** Los tres diagramas de las pestañas son un mock en PlantUML y deben quedar como la Figura 2-1. En `input/pagecontent/volume-1-actors.md:8`.
2. **Alinear el tratamiento de la aplicación del paciente.** Figura como cliente en el Authorization Server y puede ser un cliente confidencial cuando tiene backend propio, y de eso depende si se la considera miembro y qué le exigen ATNA, CT y la auditoría. En `input/pagecontent/volume-1-groupings.md:31` (requiere discusión previa).
3. **Comprobar con pruebas qué guarda el registro de mensajes de X-Road.** Hay que saber si conserva los mensajes completos y cómo se configura, y reflejar el resultado en esa opción y en las decisiones de política de la sección 2.6. En `input/pagecontent/volume-1-options.md:37`.
4. **Definir la auditoría de una aplicación del paciente sin backend propio.** La aplicación ya opera casi como un miembro, pero puede no tener backend propio y hacer todo su flujo en el navegador de la persona, y por eso la sección 2.4 la deja por ahora fuera de ATNA y de CT. Hay que probar si ese flujo tiene limitantes y, si no las tiene, auditarla como a un miembro más. Va junto con el punto 2, porque los dos deciden si la aplicación se trata como miembro. En `input/pagecontent/volume-2.md`, bajo la Tabla 3-1.
5. **Decidir si el Record Locator Service publica `/.well-known/smart-configuration`.** Sin ese documento una aplicación SMART genérica no encuentra el Authorization Server. Si lo publica, falta fijar qué capacidades declara. En `input/pagecontent/volume-2-hix-2.md`, bajo Descubrimiento del Authorization Server.

## Páginas declaradas pero no escritas

La estructura completa de la guía ya está en `sushi-config.yaml`, comentada hasta que cada parte exista. Son diecinueve páginas repartidas así.

1. **Las consideraciones entre perfiles y despliegue del Volumen 1**, una página, en la línea 67.
2. **El Volumen 3 entero**, ocho páginas contando su portada, con los metadatos del puntero, la identidad del paciente, los recursos del directorio, los claims de autorización, el consentimiento y las etiquetas de seguridad, los registros de auditoría y la terminología, desde la línea 83.
3. **La sección de conformidad**, seis páginas con las ediciones soportadas, la matriz de requisitos, las desviaciones respecto a IHE, las extensiones propias y los artefactos, desde la línea 99.
4. **Tres apéndices**, la justificación del diseño, las referencias y el historial de cambios, desde la línea 115.
5. **La página de descargas**, una página, en la línea 121.

Nota: las dependencias en el archivo de sushi están comentadas para evitar problemas con el CI de despliegue durante la escritura de estas páginas. En el release formal se descomentaran y se hará la integration completa a la guía.

## Capacidades aplazadas a una versión posterior

Son parte de la arquitectura y están anunciadas como tales en la [descripción general](input/pagecontent/index.md), no son omisiones.

1. **Consentimiento anticipado del paciente.** La guía ya dice dónde se aplica la decisión de divulgación y qué información necesita. Quedan el modelo de consentimiento (PCF), su ciclo de vida y sus políticas, a partir de los perfiles IHE aplicables. **(PRIORIDAD)**
2. **Auditoría de operaciones y divulgaciones.** La guía ya establece que hay que registrar las operaciones en ambos extremos. Quedan el modelo de consulta y el comportamiento ante fallos.
3. Versión de la guía en inglés.

## Ampliar el canal de interconexión al tramo del consumidor

La [Opción de Canal de Interconexión](input/pagecontent/volume-1-options.md) cubre a todo actor que la comunidad expone, sea un actor central o un custodio que responde recuperaciones. El video de stand ya muestra X-Road también en el tramo entre el hospital que consulta y la comunidad. Hay que decidir cómo lo declara el consumidor, si también en el directorio, y alinear la opción, la tabla de terminología de `input/pagecontent/index.md` y la sección de transporte de `input/pagecontent/volume-1-concepts.md`. Sigue siendo un tramo de un miembro con el centro, así que no reabre la malla entre pares.
