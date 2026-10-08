HIX define una arquitectura de referencia para comunidades que comparten documentos clínicos. No propone un estándar nuevo. Articula los perfiles de IHE, los estándares y las especificaciones necesarios para operar una comunidad así sobre FHIR, y sigue el modelo de comunidad de **[Mobile Health Document Sharing (MHDS)](https://profiles.ihe.net/ITI/MHDS/volume-1.html)**, que toma como referencia sin declarar conformidad con él.

Sin una comunidad, cada organización tiene que integrarse con cada una de las demás, y la política de acceso se aplica en tantos lugares como organizaciones haya, con la calidad que cada una pueda pagar. HIX concentra esa integración y esa política en una infraestructura central, con la que cada organización se integra una sola vez, como explica la [sección 2.1](volume-1-concepts.html#limite-de-confianza).

### Propósito y alcance

Esta guía describe los roles de la comunidad, sus límites de confianza y la relación entre sus componentes. Explica, entre otras decisiones, por qué la localización y la recuperación se median de forma centralizada, por qué la custodia documental se mantiene distribuida por defecto y cómo **[IUA](https://profiles.ihe.net/ITI/IUA/index.html)** y **[OAuth 2.0](https://www.rfc-editor.org/info/rfc6749/)** establecen la base de autorización y delegación entre los participantes. Cuando la autorización requiere la participación de una persona, incorpora **[SMART App Launch](https://hl7.org/fhir/smart-app-launch/)** en el flujo interactivo que esa persona completa desde su navegador.

Esta arquitectura abarca las siguientes capacidades dentro de la comunidad:

- Publicación, indexación, localización y recuperación de documentos clínicos.
- Custodia distribuida de documentos y almacenamiento central cuando corresponda.
- Transporte seguro hacia los custodios, HTTPS directo o **[X-Road](https://x-road.global/)** según declare el directorio, sin alterar la topología de la comunidad.
- Identidad maestra de pacientes y vinculación con las identidades locales.
- Directorio de organizaciones participantes, servicios y endpoints.
- Autorización y divulgación controlada de documentos.

#### Capacidades en desarrollo

Las siguientes capacidades forman parte de la arquitectura HIX, pero su especificación detallada se definirá en una versión posterior de esta guía. La arquitectura ya establece los límites, los puntos de integración y los flujos que permiten incorporarlas sin alterar la topología mediada de la comunidad.

- **Consentimiento anticipado del paciente.** HIX define dónde se aplica la decisión de divulgación y qué información necesita. El modelo de consentimiento, su ciclo de vida y sus políticas se especificarán a partir de los perfiles IHE aplicables.
- **Auditoría de operaciones y divulgaciones.** HIX define la necesidad de registrar las operaciones en ambos extremos de la interacción. El modelo de consulta y el comportamiento ante fallos se especificarán posteriormente.

Los casos previstos para versiones posteriores se listan en la [sección 2.5](volume-1-usecases.html#casos-previstos) del Volumen 1.

### Convenciones de la especificación

Las palabras clave **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY** y **OPTIONAL**, cuando aparecen íntegramente en mayúsculas, se interpretan conforme a [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) y [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

Estas palabras expresan requisitos normativos de **HIX**. El resto del lenguaje utilizado en esta guía es descriptivo, salvo que se indique explícitamente lo contrario.

Cuando HIX incorpora o referencia requisitos definidos por un perfil IHE, una especificación HL7 FHIR o un RFC, dichos requisitos conservan la fuerza normativa establecida por su especificación de origen.

Un requisito que empieza con la etiqueta **Experimental.** es una propuesta de esta versión para un punto en el que los estándares no dan una respuesta única. Es normativo como cualquier otro, pero puede cambiar con la experiencia de implementación.

#### Terminología y abreviaturas

HIX utiliza terminología definida por IHE, HL7 FHIR y OAuth 2.0. Salvo que se
indique lo contrario, los nombres de perfiles y actores conservan el significado
establecido por su especificación de origen.

En esta guía, un **perfil IHE** define un conjunto de capacidades y
transacciones, mientras que un **actor IHE** representa el rol que un sistema
desempeña dentro de dicho perfil.

| Término | Significado |
| --- | --- |
| **[MHDS](https://profiles.ihe.net/ITI/MHDS/volume-1.html)** — *Mobile Health Document Sharing* | Perfil IHE que define una comunidad de intercambio de documentos clínicos basada en FHIR y la composición de perfiles necesaria para operarla. HIX lo toma como arquitectura de referencia. |
| **[MHD](https://profiles.ihe.net/ITI/MHD/5.0.0/index.html)** — *Mobile access to Health Documents* | Perfil IHE para publicar, localizar y recuperar documentos clínicos mediante FHIR. HIX usa sus actores **Document Source**, **Document Consumer**, **Document Recipient** y **Document Responder**. |
| **[PMIR](https://profiles.ihe.net/ITI/PMIR/index.html)** — *Patient Master Identity Registry* | Perfil IHE para gestionar y sincronizar identidades maestras de pacientes. |
| **[PIXm](https://profiles.ihe.net/ITI/PIXm/index.html)** — *Patient Identifier Cross-referencing for mobile* | Perfil IHE con el que cada miembro declara sus identidades locales de paciente y resuelve un identificador a la identidad maestra. |
| **[PDQm](https://profiles.ihe.net/ITI/PDQm/index.html)** — *Patient Demographics Query for Mobile* | Perfil IHE para localizar a un paciente por sus datos demográficos cuando no se dispone de un identificador conocido por la comunidad. |
| **[mCSD](https://profiles.ihe.net/ITI/mCSD/index.html)** — *Mobile Care Services Discovery* | Perfil IHE utilizado para consultar organizaciones participantes, servicios y endpoints. En HIX, el endpoint de cada custodio declara además el canal de transporte por el que se lo alcanza. |
| **[ATNA](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html)** — *Audit Trail and Node Authentication* | Perfil IHE que aporta la autenticación de nodos, la confidencialidad en tránsito y el registro de eventos de auditoría. |
| **[CT](https://profiles.ihe.net/ITI/TF/Volume1/ch-7.html)** — *Consistent Time* | Perfil IHE que mantiene sincronizados los relojes de todos los sistemas de la comunidad, para que los eventos de auditoría y la vigencia de los tokens signifiquen lo mismo en cada extremo. |
| **[BALP](https://profiles.ihe.net/ITI/BALP/index.html)** — *Basic Audit Log Patterns* | Perfil IHE de contenido que define patrones reutilizables de `AuditEvent`. De ellos derivan los eventos de auditoría que cada perfil especifica para sus transacciones. |
| **[IUA](https://profiles.ihe.net/ITI/IUA/index.html)** — *Internet User Authorization* | Perfil IHE utilizado por HIX como base de autorización para las interacciones protegidas entre sus participantes. [HIX-1](volume-2-hix-1.html) se apoya además en [RFC 8693](https://www.rfc-editor.org/rfc/rfc8693) y [RFC 8707](https://www.rfc-editor.org/rfc/rfc8707). |
| **[SMART App Launch](https://hl7.org/fhir/smart-app-launch/app-launch.html)** | Especificación de HL7 que HIX usa en los flujos interactivos en los que la autorización requiere la participación de una persona desde su navegador. |
| **[X-Road](https://x-road.global/)** | Capa de intercambio de datos entre organizaciones sobre transporte mTLS entre servidores de seguridad. HIX la admite como canal entre los participantes, declarado en el directorio. No aporta semántica documental. |
| **Record Locator Service** | Actor propio de HIX, no de IHE, responsable de localizar los documentos clínicos disponibles para un paciente y mediar su recuperación desde los custodios correspondientes. En términos IHE agrupa un Document Responder y un Document Consumer de MHD. |
{: .table .table-bordered}

Los demás términos, como los de OAuth 2.0 y los propios de HIX, se definen en el [glosario](appendix-glossary.html).

### Cómo leer esta guía

HIX organiza sus requisitos en diferentes niveles de abstracción. Los volúmenes de esta guía deben leerse de forma complementaria y no como especificaciones independientes.

- El **[Volumen 1](volume-1.html)** describe la arquitectura, es decir, qué hace cada actor y por qué. Sus secciones se numeran 2.x.
- El **[Volumen 2](volume-2.html)** detalla las transacciones. Especifica completas las propias de HIX y, de las demás, dice con qué restricciones las usa. Sus secciones se numeran 3.x.
- Los **apéndices** reúnen el material de apoyo, por ahora el [glosario](appendix-glossary.html).

Quien quiere entender la arquitectura puede leer la [sección 2](volume-1.html), la [2.1](volume-1-concepts.html) y la [2.6](volume-1-security.html), y después la [sección 3](volume-2.html), la [3.2](volume-2-hix-1.html) y la [3.3](volume-2-hix-2.html). Quien implementa un miembro puede empezar por la [sección 2.2](volume-1-actors.html) y la [2.4](volume-1-groupings.html), y seguir con la página del Volumen 2 de cada transacción que implementa.

### Otros formatos

La guía se publica también en formatos pensados para leerla fuera del sitio.

- **Para asistentes de IA.** [llms.txt](https://hix.meddyg.com/fhir/hix/llms.txt) es un índice en texto plano con una línea por página, que dice de qué trata cada una y enlaza a su versión en Markdown. Un implementador puede dárselo a su agente para que lea solo las páginas que necesita. [llms-full.txt](https://hix.meddyg.com/fhir/hix/llms-full.txt) reúne la guía completa en un solo archivo. Los dos se generan de forma automática en cada publicación, a partir de las mismas páginas que forman este sitio. No hay una segunda redacción, así que su contenido no puede apartarse del de la guía.
- **Para leer sin conexión.** El PDF y el documento de Word de cada versión se adjuntan a su publicación en [GitHub](https://github.com/meddyg/Health-Information-Exchange/releases).

> **Nota.** Estos archivos sirven para asistir al implementador, no para sustituirlo. Un asistente de IA puede equivocarse al leer o al resumir. El criterio técnico y la responsabilidad sobre lo que se implementa recaen siempre en quien implementa, y el texto que obliga es el de esta guía.

### Dependencias

HIX es una guía sobre FHIR R5 que se basa en perfiles IHE publicados sobre R4. De los que compone, MHD está publicado sobre R5 y los demás solo sobre R4. HIX sigue sus modelos, transacciones y vocabulario sobre R5 sin declarar conformidad con sus artefactos R4, como explica la [sección 2.1](volume-1-concepts.html#relacion-con-mhds). IUA, ATNA y CT no se distribuyen como paquetes FHIR, y por eso no figuran aquí aunque HIX los use. MHDS tampoco figura, porque HIX lo toma como referencia y no depende de su paquete.

{% include dependency-table.xhtml %}
