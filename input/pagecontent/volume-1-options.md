Las opciones definen capacidades que un actor puede añadir a las que se le exigen. La [Tabla 2.3-1](volume-1-options.html#tabla-2-3-1) lista las que cada actor puede declarar. Un actor que declara una opción **SHALL** cumplir todos sus requisitos.

**Tabla 2.3-1:** Actores y opciones de HIX
{: #tabla-2-3-1}

| Actor | Opción |
| --- | --- |
| Record Locator Service | Opción de Consentimiento |
| | Opción de Canal de Interconexión |
| Document Registry | Opción de Almacenamiento Central |
| | Opción de Consentimiento |
| | Opción de Canal de Interconexión |
| Registro de identidad maestra | Opción de Canal de Interconexión |
| Authorization Server | Opción de Canal de Interconexión |
| Sistema que publica y custodia documentos | Opción de Almacenamiento Central |
| | Opción de Canal de Interconexión |
| Sistema que consume documentos | Opción de Demografía |
| | Opción de Coincidencia Demográfica |
{: .table .table-bordered}

### Opción de Almacenamiento Central {#opcion-de-almacenamiento-central}

Un [custodio](appendix-glossary.html#custodio) que no puede conservar sus documentos delega el almacenamiento del contenido en la infraestructura central. El documento sigue siendo suyo. Figura como custodio en los metadatos y conserva la responsabilidad sobre su contenido, pero deja de participar en la recuperación.

El custodio **SHALL** declarar esta opción solo si el Document Registry de la comunidad también la declara. El custodio que la declara **SHALL** enviar el contenido dentro del [ITI-65](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-65.html) en lugar de una referencia, y **SHOULD NOT** exponer un endpoint de recuperación, porque las recuperaciones ya no pasan por él. El Document Registry que declara esta opción **SHALL** conservar el contenido durante el ciclo de vida que la comunidad establezca y **SHALL** responder [ITI-68](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-68.html) con el contenido que conserva. El Record Locator Service atiende entonces la recuperación desde el Document Registry, como fija la [sección 2.2](volume-1-actors.html#record-locator-service).

Esta opción corresponde a la primera de las dos ubicaciones del contenido que describe MHDS ([MHDS Vol. 1, §1:50.1.1.2](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150112-storage-of-binary))[^mhds-storage]. Ambas coexisten en una misma comunidad, como explica la [sección 2.1](volume-1-concepts.html#custodia-distribuida-y-almacenamiento-central). El solicitante no distingue cuál se aplica a cada documento y no necesita hacerlo. Qué custodios pueden ejercerla, y quién lo decide, es política de la comunidad.

### Opción de Canal de Interconexión {#opcion-de-canal-de-interconexion}

Las transacciones de la comunidad pueden recorrer un canal de interconexión distinto de HTTPS directo, cuando la comunidad opera sobre una red de intercambio ya establecida, como X-Road. Todo actor que la comunidad expone a otros participantes queda entonces bajo ese canal, sea un actor central o un custodio que responde recuperaciones.

El actor que declara esta opción **SHALL** atender y originar a través del canal las mismas transacciones, con el mismo contenido y los mismos requisitos de autorización. El custodio que la declara **SHALL** publicar en el directorio el endpoint que describe ese canal. El token sigue viajando en la solicitud y quien la recibe sigue validándolo. La identidad que el canal aporta **SHALL NOT** sustituir la validación del token.

El canal no cambia nada de la arquitectura. Resuelve cómo se conectan, se identifican y cifran su tramo las organizaciones, y las transacciones, los punteros, los tokens, la decisión de divulgación y la auditoría siguen siendo los mismos, como explica la [sección 2.1](volume-1-concepts.html). La representación del canal en el directorio se especificará más adelante en esta guía.

Una red como X-Road autentica y cifra el tramo entre los servidores de seguridad de las dos organizaciones ([X-Road, Arquitectura §3.3](https://docs.x-road.global/Architecture/arc-g_x-road_arhitecture.html#33-message-transport-protocol))[^xroad-transport]. El tramo entre el sistema del custodio y su propio servidor de seguridad queda dentro de su organización, y protegerlo es responsabilidad del custodio. Esta guía no lo especifica.

> **TODO.** Comprobar con pruebas sobre X-Road qué guarda su registro de mensajes, para ver si guarda los mensajes completos, y cómo se configura. Reflejar el resultado en esta opción y en las decisiones de política de la [sección 2.6](volume-1-security.html).

### Opción de Consentimiento {#opcion-de-consentimiento}

Habilita la evaluación de una decisión de divulgación por paciente antes de responder una localización o una recuperación. La decisión base, con la política única de la comunidad, es un requisito de la [sección 2.2](volume-1-actors.html#record-locator-service). Esta opción la extiende al consentimiento de cada paciente.

El actor que declara esta opción, sea el Record Locator Service o el Document Registry, **SHALL** consultar la decisión aplicable al paciente, al solicitante, a su organización, al propósito de uso que lleva su token y a la etiqueta de confidencialidad de cada puntero. **SHALL** omitir de la respuesta los documentos cuya divulgación no esté permitida, con las garantías que la [sección 2.2](volume-1-actors.html#record-locator-service) exige a toda omisión, es decir, que no se distinga de la ausencia del documento y que quede registrada en la auditoría.

El modelo de consentimiento, su ciclo de vida, su representación y sus políticas se especificarán en una versión posterior de esta guía a partir de [PCF](https://profiles.ihe.net/ITI/PCF/index.html). Esta opción declara el punto en el que esa decisión se aplica y la información que necesita. Hasta entonces, la comunidad opera bajo la política de divulgación única que haya acordado, aplicada en el mismo punto.

En qué punto se aplica, en el Record Locator Service o en el Document Registry, lo decide la comunidad, como explica la [sección 2.1](volume-1-concepts.html). MHDS resuelve este mismo problema de otro modo, con un Authorization Server agrupado con su Document Registry que gestiona el consentimiento. HIX no sigue ese camino, por las razones que da la [misma sección](volume-1-concepts.html#relacion-con-mhds).

### Opción de Demografía {#opcion-de-demografia}

Permite a un [consumidor](appendix-glossary.html#consumidor) localizar a un paciente por sus datos demográficos cuando no dispone de un identificador conocido por la comunidad. Corresponde a la [Patient Search Option](https://profiles.ihe.net/ITI/PDQm/volume-1.html#13821-patient-search-option) de PDQm.

El consumidor que declara esta opción **SHALL** presentar al menos un criterio que nombre o describa a la persona en cada consulta [ITI-78](https://profiles.ihe.net/ITI/PDQm/ITI-78.html). Qué parámetros cuentan como criterio lo fija la [sección 3.4](volume-2-identity.html#iti-78). Es una búsqueda determinista. Cada criterio filtra, y ningún resultado lleva grado de coincidencia. Las reglas que el registro de identidad maestra aplica a su respuesta, como devolver solo identidades maestras y limitarlas según la política de la comunidad, las fija la [sección 2.2](volume-1-actors.html#registro-de-identidad-maestra).

### Opción de Coincidencia Demográfica {#opcion-de-coincidencia-demografica}

Permite a un [consumidor](appendix-glossary.html#consumidor) encontrar a un paciente a partir de datos demográficos incompletos o inexactos, con la coincidencia probabilística del registro de identidad maestra. Corresponde a la [Match Operation Option](https://profiles.ihe.net/ITI/PDQm/volume-1.html#13822-match-operation-option) de PDQm.

El consumidor que declara esta opción **SHALL** presentar en cada [ITI-119](https://profiles.ihe.net/ITI/PDQm/ITI-119.html) los datos del paciente que busca. Un resultado de esta búsqueda es un candidato, no una identidad confirmada. Las reglas que el registro de identidad maestra aplica a su respuesta, como devolver solo identidades maestras e indicar el grado de coincidencia de cada una, las fija la [sección 2.2](volume-1-actors.html#registro-de-identidad-maestra).

### Referencias

Las citas reproducen el texto publicado por su fuente. Los recortes se marcan con "[...]" y la negrita es de esta guía.

[^mhds-storage]: [MHDS Vol. 1, §1:50.1.1.2 Storage of Binary](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150112-storage-of-binary): "(1) The Document Source includes the Binary Resource in the [ITI-65] transaction, and the Document Registry is required to store it. (2) **The Community allows the Binary to be stored elsewhere in the Community.** [...] This might be other centralized infrastructure, distributed infrastructure, or **within the system implementing the Document Source**."
[^xroad-transport]: [X-Road, Arquitectura §3.3 Message Transport Protocol](https://docs.x-road.global/Architecture/arc-g_x-road_arhitecture.html#33-message-transport-protocol): "The X-Road Message Transport Protocol is used by security server to exchange service requests and service responses. [...] The protocol is based on HTTPS and **uses mutual certificate-based TLS authentication**."

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
