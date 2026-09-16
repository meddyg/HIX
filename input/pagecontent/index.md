HIX define una arquitectura de referencia para comunidades que comparten documentos clínicos. No propone un estándar nuevo sino que toma como fundamento el perfil **[Mobile Health Document Sharing (MHDS)](https://profiles.ihe.net/ITI/MHDS/volume-1.html)** de IHE y articula los perfiles, estándares y especificaciones necesarios para operarlo sobre FHIR.

### Propósito y alcance

Esta guía describe los roles de la comunidad, sus límites de confianza y la relación entre sus componentes. Explica, entre otras decisiones, por qué la localización y la recuperación se median de forma centralizada; por qué la custodia documental se mantiene distribuida por defecto; y cómo **[IUA](https://profiles.ihe.net/ITI/IUA/index.html)** y **[OAuth 2.0](https://www.rfc-editor.org/info/rfc6749/)** establecen la base de autorización y delegación entre los participantes, incorporando **[SMART on FHIR](https://build.fhir.org/ig/HL7/smart-app-launch/)** en los flujos interactivos en los que la autorización requiere la participación de un usuario, a través de un **User Agent** y el *front-channel* de autorización.

Esta arquitectura abarca las siguientes capacidades dentro de la comunidad:

- publicación, indexación, localización y recuperación de documentos clínicos;
- custodia distribuida de documentos y almacenamiento central cuando corresponda;
- transporte seguro hacia los custodios, HTTPS directo o **[X-Road](https://x-road.global/)**
  según declare el directorio, sin alterar la topología de la comunidad;
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
  modelo de consulta y el comportamiento ante fallos se especificarán
  posteriormente.

### Convenciones de la especificación

Las palabras clave **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY** y **OPTIONAL**, cuando aparecen íntegramente en mayúsculas, se interpretan conforme a [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) y [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

Estas palabras expresan requisitos normativos de **HIX**. El resto del lenguaje utilizado en esta guía es descriptivo, salvo que se indique explícitamente lo contrario.

Cuando HIX incorpora o referencia requisitos definidos por un perfil IHE, una especificación HL7 FHIR o un RFC, dichos requisitos conservan la fuerza normativa establecida por su especificación de origen.

#### Terminología y abreviaturas

HIX utiliza terminología definida por IHE, HL7 FHIR y OAuth 2.0. Salvo que se
indique lo contrario, los nombres de perfiles y actores conservan el significado
establecido por su especificación de origen.

En esta guía, un **perfil IHE** define un conjunto de capacidades y
transacciones, mientras que un **actor IHE** representa el rol que un sistema
desempeña dentro de dicho perfil.

| Término | Significado |
| --- | --- |
| **[MHDS](https://profiles.ihe.net/ITI/MHDS/volume-1.html)** — *Mobile Health Document Sharing* | Perfil IHE que define una comunidad de intercambio de documentos clínicos basada en FHIR y la composición de perfiles necesaria para operarla. |
| **[MHD](https://profiles.ihe.net/ITI/MHD/index.html)** — *Mobile access to Health Documents* | Perfil IHE para publicar, localizar y recuperar documentos clínicos mediante FHIR. HIX usa sus actores **Document Source**, **Document Consumer**, **Document Recipient** y **Document Responder**. |
| **[PMIR](https://profiles.ihe.net/ITI/PMIR/index.html)** — *Patient Master Identity Registry* | Perfil IHE para gestionar y sincronizar identidades maestras de pacientes. |
| **[PIXm](https://profiles.ihe.net/ITI/PIXm/index.html)** — *Patient Identifier Cross-referencing for mobile* | Perfil IHE con el que cada miembro declara sus identidades locales de paciente y resuelve un identificador a la identidad maestra. |
| **[PDQm](https://profiles.ihe.net/ITI/PDQm/index.html)** — *Patient Demographics Query for Mobile* | Perfil IHE para localizar a un paciente por sus datos demográficos cuando no se dispone de un identificador conocido por la comunidad. |
| **[mCSD](https://profiles.ihe.net/ITI/mCSD/index.html)** — *Mobile Care Services Discovery* | Perfil IHE utilizado para consultar organizaciones participantes, servicios y endpoints. En HIX, el endpoint de cada custodio declara además el canal de transporte por el que se lo alcanza. |
| **[ATNA](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html)** — *Audit Trail and Node Authentication* | Perfil IHE que aporta la autenticación de nodos, la confidencialidad en tránsito y el registro de eventos de auditoría. |
| **[CT](https://profiles.ihe.net/ITI/TF/Volume1/ch-7.html)** — *Consistent Time* | Perfil IHE que mantiene sincronizados los relojes de todos los sistemas de la comunidad, para que los eventos de auditoría y la vigencia de los tokens signifiquen lo mismo en cada extremo. |
| **[BALP](https://profiles.ihe.net/ITI/BALP/index.html)** — *Basic Audit Log Patterns* | Perfil IHE que define el contenido de los eventos de auditoría FHIR por transacción. |
| **[IUA](https://profiles.ihe.net/ITI/IUA/index.html)** — *Internet User Authorization* | Perfil IHE utilizado por HIX como base de autorización para las interacciones protegidas entre sus participantes. Sus requisitos aplican a todos los flujos de autorización de HIX. |
| **[SMART on FHIR](https://build.fhir.org/ig/HL7/smart-app-launch/app-launch.html)** | Especificación de HL7 utilizada adicionalmente en los flujos interactivos en los que la autorización requiere la participación de un usuario a través de un `User Agent`. |
| **[X-Road](https://x-road.global/)** | Capa de intercambio de datos entre organizaciones sobre transporte mTLS entre servidores de seguridad. HIX la admite como canal hacia un custodio, declarado en el directorio; no aporta semántica documental. |
| **RLS** — *Record Locator Service* | Componente central de HIX responsable de localizar los documentos clínicos disponibles para un paciente y mediar su recuperación desde los custodios correspondientes. |
{: .table .table-bordered}

Los siguientes términos relacionados con OAuth 2.0 y la arquitectura de autorización de HIX se utilizan a lo largo de la guía:

| Término | Significado |
| --- | --- |
| **Client** | Aplicación que solicita acceso a un recurso protegido. |
| **AS / STS** — *Authorization Server / Security Token Service* | Función responsable de la autorización y de la emisión o intercambio de tokens utilizados entre los participantes de HIX. |
| **RS** — *Resource Server* | Servicio que protege recursos y evalúa los tokens presentados para autorizar el acceso. |
| **Access token** | Credencial presentada por un `Client` ante un `Resource Server` para solicitar acceso. |
| **Audience** | Identificador del `Resource Server` al que está destinado un token. |
| **Scope** | Alcance del acceso solicitado o concedido al `Client`. |
| **PEP** — *Policy Enforcement Point* | Punto donde se aplica una decisión de política sobre una solicitud: permitir, denegar o filtrar. En HIX el Record Locator Service es el primer PEP de la comunidad; cada custodio es además PEP de su propio endpoint. |
| **PDP** — *Policy Decision Point* | Punto donde se toma la decisión que el PEP aplica. En HIX la decisión de divulgación se toma en el Record Locator Service; el Authorization Server decide sobre la autorización, nunca sobre la divulgación. |
{: .table .table-bordered}

### Cómo leer esta guía

HIX organiza sus requisitos en diferentes niveles de abstracción. Los volúmenes de esta guía deben leerse de forma complementaria y no como especificaciones independientes.
