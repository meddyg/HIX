HIX define una arquitectura de referencia para comunidades que comparten documentos clínicos. No propone un estándar nuevo sino que toma como fundamento el perfil [Mobile Health Document Sharing (MHDS)](https://profiles.ihe.net/ITI/MHDS/volume-1.html) de IHE y articula los perfiles, estándares y especificaciones necesarios para operarlo sobre FHIR.

### Propósito y alcance

Esta guía describe los roles de la comunidad, sus límites de confianza y la relación entre sus componentes. Explica, entre otras decisiones, por qué la localización y la recuperación se median de forma centralizada; por qué la custodia documental se mantiene distribuida por defecto; y cómo se componen [IUA](https://profiles.ihe.net/ITI/IUA/index.html), [SMART on FHIR](https://build.fhir.org/ig/HL7/smart-app-launch/) y [OAuth 2.0](https://www.rfc-editor.org/info/rfc6749/) para establecer las reglas de autorización y delegación entre los participantes.

Esta arquitectura abarca las siguientes capacidades dentro de la comunidad:
- publicación, indexación, localización y recuperación de documentos clínicos;
- custodia distribuida de documentos y colocación central cuando corresponda;
- transporte seguro entre la infraestructura central y los custodios, mediante
  HTTPS directo o X-Road, sin alterar la topología mediada de la comunidad;
- identidad maestra de pacientes y vinculación con las identidades locales;
- directorio de organizaciones participantes, servicios y endpoints;
- autorización y divulgación controlada de documentos;

#### Capacidades en desarrollo

Las siguientes capacidades forman parte de la arquitectura HIX, pero su especificación detallada se definirá en una versión posterior de esta guía. La arquitectura ya establece los límites, los puntos de integración y los flujos que permiten incorporarlas sin alterar la topología mediada de la comunidad.

- **Consentimiento anticipado del paciente.** HIX define dónde se aplica la
  decisión de divulgación y qué información necesita; el modelo de
  consentimiento, su ciclo de vida y sus políticas se especificarán a partir
  de los perfiles IHE aplicables.
- **Auditoría de operaciones y divulgaciones.** HIX define la necesidad de
  registrar las operaciones en ambos extremos de la interacción; el
  repositorio central, el modelo de consulta y el comportamiento ante fallos
  se especificarán posteriormente.

### Convenciones de la especificación

Las palabras clave **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY** y **OPTIONAL**, cuando aparecen íntegramente en mayúsculas, se interpretan conforme a [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) y [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

Estas palabras expresan requisitos normativos de **HIX**. El resto del lenguaje utilizado en esta guía es descriptivo, salvo que se indique explícitamente lo contrario.

Cuando HIX incorpora o referencia requisitos definidos por un perfil IHE, una especificación HL7 FHIR o un RFC, dichos requisitos conservan la fuerza normativa establecida por su especificación de origen.

### Como leer esta guía

HIX organiza sus requisitos en diferentes niveles de abstracción. Los volúmenes de esta guía deben leerse de forma complementaria y no como especificaciones independientes.
