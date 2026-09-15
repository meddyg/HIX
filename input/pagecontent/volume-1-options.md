Las opciones definen capacidades que un actor puede implementar sin dejar de ser conforme. La Tabla 2.3-1 lista las que cada actor puede declarar. Un actor que declara una opción **SHALL** cumplir todos los requisitos de esa opción.

**Tabla 2.3-1:** Actores y opciones de HIX

| Actor | Opción |
| --- | --- |
| Record Locator Service | Opción de Consentimiento |
| Document Registry | Opción de Almacenamiento Central |
| Sistema que publica y custodia documentos | Opción de Almacenamiento Central |
| | Opción de Transporte Mediado |
| Sistema que consume documentos | Opción de Demografía |
{: .table .table-bordered}

### Opción de Almacenamiento Central

Un [custodio](appendix-glossary.html#custodio) que no puede conservar sus documentos delega el almacenamiento del contenido en la infraestructura central. El documento sigue siendo suyo. Figura como custodio en los metadatos y conserva la responsabilidad sobre su contenido, pero deja de participar en la recuperación.

El custodio que declara esta opción **SHALL** enviar el contenido dentro del [ITI-65](https://profiles.ihe.net/ITI/MHD/ITI-65.html) en lugar de una referencia, y **SHALL NOT** exponer un endpoint de recuperación. El Document Registry que declara esta opción **SHALL** conservar el contenido durante el ciclo de vida que la comunidad establezca y **SHALL** responder [ITI-68](https://profiles.ihe.net/ITI/MHD/ITI-68.html) con el contenido que conserva. El Record Locator Service **SHALL** atender la recuperación sin el salto hacia el custodio.

Esta opción corresponde a la primera de las dos ubicaciones del contenido que describe MHDS ([MHDS Vol. 1, §1:50.1.1.2](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150112-storage-of-binary))[^mhds-storage]. Ambas coexisten en una misma comunidad. El solicitante no distingue cuál se aplica a cada documento y no necesita hacerlo. Qué custodios pueden ejercerla, y quién lo decide, es política de la comunidad.

El expediente electrónico del paciente de Suiza es un ejemplo de comunidad que opera solo con esta ubicación. Cada comunidad suiza mantiene un Document Repository que almacena los binarios de los documentos, y los sistemas de las instituciones le entregan el documento completo al publicarlo ([eHealth Suisse, EPR architecture, §3.3.4](https://www.e-health-suisse.ch/payload/api/documents/file/EPD-Architektur_EN.pdf))[^ch-epr-arch]. El documento vive en la comunidad y la institución no responde recuperaciones. Su acceso móvil se especifica sobre MHD en [CH EPR FHIR](https://fhir.ch/ig/ch-epr-fhir/index.html). Lo que en HIX es una opción por custodio es allí la regla de toda la comunidad.

### Opción de Transporte Mediado

El tramo entre la infraestructura central y el custodio puede recorrer un canal de interconexión distinto de HTTPS directo, cuando la comunidad opera sobre una red de intercambio ya establecida, como X-Road.

El custodio que declara esta opción **SHALL** publicar en el directorio el endpoint que describe ese canal, y **SHALL** aceptar la transacción [ITI-68](https://profiles.ihe.net/ITI/MHD/ITI-68.html) a través de él con el mismo contenido y los mismos requisitos de autorización. El token intercambiado sigue viajando en la solicitud y el custodio sigue validándolo. La identidad que el canal aporta **SHALL NOT** sustituir la validación del token.

El canal y la arquitectura son capas separadas que no se afectan entre sí. El canal resuelve cómo se conectan las organizaciones, cómo se identifican y cómo se cifra el tramo entre ellas. La arquitectura resuelve qué se intercambia y bajo qué reglas, es decir, las transacciones, los punteros, los tokens, la decisión de divulgación y la auditoría. Cambiar de canal no cambia nada de la segunda capa, y nada de la segunda capa exige un canal concreto. Por eso la recuperación sigue siendo mediada, el solicitante sigue sin alcanzar al custodio y ningún puntero cambia. La representación del canal en el directorio se especifica en el Volumen 3.

### Opción de Consentimiento

Habilita la evaluación de una decisión de divulgación por paciente antes de responder una localización o una recuperación.

El Record Locator Service que declara esta opción **SHALL** consultar la decisión aplicable al paciente, al solicitante, a su organización, al propósito de uso que lleva su token y a la etiqueta de confidencialidad de cada puntero, **SHALL** omitir de la respuesta los documentos cuya divulgación no esté permitida, y **SHALL** registrar la omisión en la auditoría. La omisión **SHALL NOT** ser distinguible, para el solicitante, de la ausencia del documento.

El modelo de consentimiento, su ciclo de vida, su representación y sus políticas se especificarán en una versión posterior de esta guía a partir de [PCF](https://profiles.ihe.net/ITI/PCF/index.html). Esta opción declara el punto en el que esa decisión se aplica y la información que necesita. Hasta entonces, la comunidad opera bajo la política de divulgación única que haya acordado, aplicada en el mismo punto.

### Opción de Demografía

Permite a un [consumidor](appendix-glossary.html#consumidor) localizar a un paciente por sus datos demográficos cuando no dispone de un identificador conocido por la comunidad.

El consumidor que declara esta opción **SHALL** presentar al menos un criterio demográfico en cada consulta [ITI-78](https://profiles.ihe.net/ITI/PDQm/ITI-78.html). La infraestructura central **SHALL** responder sobre las identidades maestras, nunca sobre las identidades locales de los miembros, **SHALL** limitar la respuesta a los pacientes que la política de la comunidad permita revelar por esta vía, **SHALL** indicar el grado de coincidencia de cada resultado y **SHALL** rechazar una consulta sin criterio.

### Referencias

Las citas reproducen el texto publicado por su fuente. Los recortes se marcan con "[...]" y la negrita es de esta guía.

[^ch-epr-arch]: [eHealth Suisse, EPR architecture. A detailed description, §3.3.4 XDS Document Repositories](https://www.e-health-suisse.ch/payload/api/documents/file/EPD-Architektur_EN.pdf): "The Document Repository Service implements interfaces to **store and query the binary objects** of the XDS documents. **The data are captured by the connected systems of the (core) communities when documents are saved** and are registered via interfaces." [EPR by example, Provide and Register Document Set [ITI-41], Overview](https://ehealthsuisse.github.io/EPR-by-example/ProvideAndRegister/): "Primary systems shall **provide documents and the related document metadata to a patient EPR**" and provide "the master patient ID [...], the document metadata as defined in the ordinances of the Swiss EPR and **the binary data of the document**."
[^mhds-storage]: [MHDS Vol. 1, §1:50.1.1.2 Storage of Binary](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150112-storage-of-binary): "(1) The Document Source includes the Binary Resource in the [ITI-65] transaction, and the Document Registry is required to store it. (2) **The Community allows the Binary to be stored elsewhere in the Community.** [...] This might be other centralized infrastructure, distributed infrastructure, or **within the system implementing the Document Source**."

*[PMIR]: Patient Master Identity Registry, perfil IHE que gestiona la identidad maestra del paciente
*[PIXm]: Patient Identifier Cross-referencing for mobile, perfil IHE que enlaza los identificadores locales de un paciente con su identidad maestra
*[PDQm]: Patient Demographics Query for Mobile, perfil IHE de búsqueda de pacientes por datos demográficos
*[MHD]: Mobile access to Health Documents, perfil IHE para publicar, localizar y recuperar documentos sobre FHIR
*[MHDS]: Mobile Health Document Sharing, perfil IHE que compone MHD, PMIR, mCSD, IUA y ATNA en una comunidad de intercambio de documentos
*[mCSD]: Mobile Care Services Discovery, perfil IHE de directorio de organizaciones, servicios y endpoints
*[IUA]: Internet User Authorization, perfil IHE que aplica OAuth 2.0 a las transacciones sobre FHIR
*[ATNA]: Audit Trail and Node Authentication, perfil IHE de auditoría y seguridad de los nodos
*[BALP]: Basic Audit Log Patterns, perfil IHE con los patrones de AuditEvent de FHIR
*[PCF]: Privacy Consent on FHIR, perfil IHE de consentimiento del paciente
