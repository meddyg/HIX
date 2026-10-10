# Pendientes

Este archivo reúne lo que el repositorio tiene marcado como pendiente. Cada entrada dice a qué parte de la guía afecta, para que al resolverla se actualice esa parte y se borre la línea de aquí.

## Marcas en las páginas

1. **Rehacer en draw.io los diagramas de la sección 2.2.** Los tres diagramas de las pestañas son un mock en PlantUML y deben quedar como la Figura 2-1. Afecta a las figuras de la sección 2.2 en `input/pagecontent/volume-1-actors.md`.
2. **Alinear el tratamiento de la aplicación del paciente.** Figura como cliente en el Authorization Server y puede ser un cliente confidencial cuando tiene backend propio, y de eso depende si se la considera miembro y qué le exigen ATNA, CT y la auditoría. Afecta a la sección 2.4 en `input/pagecontent/volume-1-groupings.md` (requiere discusión previa).
3. **Comprobar con pruebas qué guarda el registro de mensajes de X-Road.** Hay que saber si conserva los mensajes completos y cómo se configura, y reflejar el resultado en esa opción y en las decisiones de política de la sección 2.6. Afecta a la Opción de Canal de Interconexión en `input/pagecontent/volume-1-options.md`.
4. **Definir la auditoría de una aplicación del paciente sin backend propio.** La aplicación ya opera casi como un miembro, pero puede no tener backend propio y hacer todo su flujo en el navegador de la persona, y por eso la sección 2.4 la deja por ahora fuera de ATNA y de CT. Hay que probar si ese flujo tiene limitantes y, si no las tiene, auditarla como a un miembro más. Va junto con el punto 2, porque los dos deciden si la aplicación se trata como miembro. Afecta a la Tabla 3-1 y a la auditoría de `input/pagecontent/volume-2.md`.

## Páginas declaradas pero no escritas

La estructura completa de la guía ya está en `sushi-config.yaml`, comentada hasta que cada parte exista. Son diecinueve páginas repartidas así.

1. **Las consideraciones entre perfiles y despliegue del Volumen 1**, una página, en la línea 67.
2. **El Volumen 3 entero**, ocho páginas contando su portada, con los metadatos del puntero, la identidad del paciente, los recursos del directorio, los claims de autorización, el consentimiento y las etiquetas de seguridad, los registros de auditoría y la terminología, desde la línea 83.
3. **La sección de conformidad**, seis páginas con las ediciones soportadas, la matriz de requisitos, las desviaciones respecto a IHE, las extensiones propias y los artefactos, desde la línea 99.
4. **Tres apéndices**, la justificación del diseño, las referencias y el historial de cambios, desde la línea 115.
5. **La página de descargas**, una página, en la línea 121.

Nota: las dependencias del archivo de sushi ya están activas. Queda la integración completa de sus artefactos en la guía para el release formal.

## Capacidades aplazadas a una versión posterior

Son parte de la arquitectura y están anunciadas como tales en la [descripción general](input/pagecontent/index.md), no son omisiones.

1. **Consentimiento anticipado del paciente.** La guía ya dice dónde se aplica la decisión de divulgación y qué información necesita. Quedan el modelo de consentimiento (PCF), su ciclo de vida y sus políticas, a partir de los perfiles IHE aplicables. **(PRIORIDAD)**
2. **Auditoría de operaciones y divulgaciones.** La guía ya establece que hay que registrar las operaciones en ambos extremos. Quedan el modelo de consulta y el comportamiento ante fallos.
3. Versión de la guía en inglés.
