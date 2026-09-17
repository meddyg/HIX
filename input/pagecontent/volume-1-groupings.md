Un actor de HIX no se implementa desde cero. Se implementa agrupando actores de los perfiles IHE que HIX compone, y cada uno de ellos trae consigo sus transacciones, sus opciones y sus requisitos. La [sección 2.2](volume-1-actors.html) dice qué transacciones ejecuta cada actor. Esta sección dice de qué está hecho, es decir, qué actores IHE agrupa y bajo qué opciones. Para quien implementa, es la lista de perfiles que debe leer y de agrupaciones que debe declarar al afirmar su conformidad. Para quien solo quiere entender la arquitectura, basta con la [sección 2.2](volume-1-actors.html) y esta queda como referencia.

Las agrupaciones se describen primero en prosa, actor por actor, y se resumen al final en la [Tabla 2.4-1](volume-1-groupings.html#tabla-2-4-1).

### Lo que casi todos agrupan

Tres perfiles acompañan a casi todos los actores de HIX. Se describen aquí una sola vez y no se repiten en cada actor.

**IUA pone el token en cada transacción.** Todo miembro es un [Authorization Client](appendix-glossary.html#authorization-client) de IUA. Obtiene el token del Authorization Server con [ITI-71](https://profiles.ihe.net/ITI/IUA/index.html#371-get-access-token-iti-71) y lo presenta en cada solicitud con [ITI-72](https://profiles.ihe.net/ITI/IUA/index.html#372-incorporate-access-token-iti-72). Todo actor ante el que un miembro presenta un token, directamente o a través del Record Locator Service, es un [Resource Server](appendix-glossary.html#resource-server) de IUA. Recibe el token con ITI-72 y lo comprueba, con [ITI-102](https://profiles.ihe.net/ITI/IUA/index.html#3102-introspect-token-iti-102) cuando declara la [Token Introspection Option](https://profiles.ihe.net/ITI/IUA/index.html#3424-token-introspection-option). Ambos actores pueden descubrir los endpoints del Authorization Server mediante [ITI-103](https://profiles.ihe.net/ITI/IUA/index.html#3103-get-authorization-server-metadata-iti-103)[^iua-actors]. Un mismo sistema puede ser las dos cosas. El Record Locator Service es Resource Server ante los miembros y Authorization Client ante los custodios y los actores centrales, y un custodio presenta tokens al publicar y los valida al servir documentos. Cómo se autentican entre sí los demás actores centrales queda a criterio de la implementación, porque pueden compartir un mismo sistema, como dice el apartado sobre los despliegues.

**ATNA protege el canal y deja rastro.** Todo sistema que participa en HIX, salvo la aplicación del paciente, es un [Secure Node o Secure Application](appendix-glossary.html#secure-node) de ATNA. Autentica al nodo con el que habla y cifra el canal con [ITI-19](https://profiles.ihe.net/ITI/TF/Volume2/ITI-19.html), bajo la opción [STX: TLS 1.2 Floor using BCP195](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html#9.2.6.4), y registra sus eventos de auditoría con [ITI-20](https://profiles.ihe.net/ITI/TF/Volume2/ITI-20.html), como recursos AuditEvent bajo la opción ATX: FHIR Feed[^atna-fhir-feed] y con el contenido que define BALP. Los actores centrales envían sus eventos al Audit Record Repository de la comunidad. Cada miembro conserva los suyos en su propio repositorio.

**CT mantiene los relojes de acuerdo.** Todo sistema que participa en HIX, salvo la aplicación del paciente, es un [Time Client](appendix-glossary.html#time-client) de CT y sincroniza su reloj con [ITI-1](https://profiles.ihe.net/ITI/TF/Volume2/ITI-1.html). Sin relojes de acuerdo, los eventos de una misma divulgación no podrían ordenarse entre sistemas y la vigencia de dos minutos del token intercambiado no significaría lo mismo en cada extremo.

La aplicación del paciente queda fuera de ATNA y de CT porque corre en el dispositivo de una persona, sin certificado de nodo ni repositorio de auditoría propio. Su actividad queda registrada por los dos actores centrales ante los que actúa, el Authorization Server al lanzarse y el Record Locator Service en cada consulta.

### Miembros

**Custodio.** Es un [Document Source](appendix-glossary.html#document-source) de MHD con la Comprehensive Metadata Option, porque el Document Registry de MHDS exige metadatos completos al publicar[^mhds-source-comprehensive]. Es un [Document Responder](appendix-glossary.html#document-responder) de MHD, que sirve el contenido de sus documentos con ITI-68 cuando el Record Locator Service se lo pide, y por eso también un Resource Server de IUA. Es un [Patient Identity Source](appendix-glossary.html#patient-identity-source) de PIXm, que declara sus identidades locales con ITI-104. Y es un Authorization Client de IUA, que obtiene el token con el que publica y declara. Bajo la Opción de Almacenamiento Central deja de ser Document Responder y Resource Server, porque entrega el contenido al publicar y ya no responde recuperaciones.

**Consumidor.** Es un [Document Consumer](appendix-glossary.html#document-consumer) de MHD, que localiza con ITI-66 e ITI-67 y recupera con ITI-68 a través del Record Locator Service, y un Authorization Client de IUA. Puede agrupar además un [Patient Identifier Cross-reference Consumer](appendix-glossary.html#patient-identifier-cross-reference-consumer) de PIXm, para resolver con ITI-83 un identificador que ya conoce, y, bajo la Opción de Demografía, un [Patient Demographics Consumer](appendix-glossary.html#patient-demographics-consumer) de PDQm, para buscar con ITI-78 a un paciente del que solo conoce sus datos. No es Resource Server, porque no responde transacciones de nadie.

**Aplicación del paciente.** Es un Document Consumer de MHD y un Authorization Client de IUA, y nada más. Obtiene su token con [HIX-2](volume-1-actors.html#hix-2) y desde ahí localiza y recupera como cualquier consumidor, confinada al paciente que la usa.

### Actores centrales

**Record Locator Service.** Hacia los miembros es un [Document Responder](appendix-glossary.html#document-responder) de MHD, que recibe sus localizaciones y recuperaciones, y un Resource Server de IUA con la Token Introspection Option, porque comprueba cada token con ITI-102. Hacia el Document Registry y los custodios es un [Document Consumer](appendix-glossary.html#document-consumer) de MHD, que ejecuta esas mismas transacciones a nombre del solicitante, y un Authorization Client de IUA, que obtiene para cada destino el token intercambiado con [HIX-1](volume-1-actors.html#hix-1). Agrupa además un [Patient Identifier Cross-reference Consumer](appendix-glossary.html#patient-identifier-cross-reference-consumer) de PIXm, con el que resuelve la identidad del paciente con ITI-83, y un [Care Services Selective Consumer](appendix-glossary.html#care-services-selective-consumer) de mCSD, con el que obtiene el endpoint de cada custodio con ITI-90.

**Document Registry.** Es el Document Registry de MHDS. MHDS fija sus agrupaciones[^mhds-groupings] y HIX le añade una, porque el miembro publica con su identidad local y el registro la traduce por él.

- Un [Document Recipient](appendix-glossary.html#document-recipient) de MHD con la [Comprehensive Metadata Option](https://profiles.ihe.net/ITI/MHD/1332_actor_options.html#13321-comprehensive-metadata-option), que recibe las publicaciones.
- Un [Document Responder](appendix-glossary.html#document-responder) de MHD, que responde las localizaciones y, bajo la Opción de Almacenamiento Central, también las recuperaciones.
- Un [Patient Identity Consumer](appendix-glossary.html#patient-identity-consumer) de PMIR, que recibe por ITI-93 las altas, los cambios y las fusiones de las identidades maestras y las aplica a los punteros que conserva[^mhds-pic].
- Un [Care Services Selective Consumer](appendix-glossary.html#care-services-selective-consumer) de mCSD, con el que comprueba que quien publica es un miembro activo, como exige la [UnContained Reference Option](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15024-uncontained-reference-option) de MHDS.
- Un [Patient Identifier Cross-reference Consumer](appendix-glossary.html#patient-identifier-cross-reference-consumer) de PIXm, que HIX añade, con el que resuelve al indexar la identidad local de cada puntero a su identidad maestra y comprueba que la persona existe y está activa en la comunidad, como MHDS exige al validar una publicación[^mhds-subject].
- Un Resource Server de IUA con la [Authorization Server Metadata Option](https://profiles.ihe.net/ITI/IUA/index.html#3421-authorization-server-metadata-option), como exige la [Authorization Option](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15021-authorization-option) de MHDS.

Las otras dos opciones de MHDS quedan a criterio de cada implementación. La [Consent Manager Option](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15022-consent-manager-option), porque la decisión de divulgación puede aplicarla el Record Locator Service o el propio Document Registry cuando conoce las reglas de la comunidad, como explica la [sección 2.1](volume-1-concepts.html), y la [SVCM Validation Option](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15023-svcm-validation-option), que HIX no exige.

**Authorization Server.** Es el [Authorization Server de IUA](https://profiles.ihe.net/ITI/IUA/index.html#34112-authorization-server), con la Authorization Server Metadata Option, porque publica sus endpoints con ITI-103, y con la Token Introspection Option, porque responde ITI-102. Es también un [OpenID Provider](appendix-glossary.html#openid-provider), es decir, un servidor de autorización que además autentica a la persona y acredita esa autenticación con un `id_token`[^oidc-op]. Lo es porque [HIX-2](volume-1-actors.html#hix-2) se apoya en SMART App Launch, y SMART entrega ese `id_token` junto con el token de acceso cuando la aplicación pide el scope `openid`[^smart-openid]. Y agrupa un [Patient Identifier Cross-reference Consumer](appendix-glossary.html#patient-identifier-cross-reference-consumer) de PIXm, con el que resuelve a la identidad maestra la identidad de la persona autenticada para fijar el contexto de paciente.

**Directorio de la comunidad.** Es el [Care Services Selective Supplier](appendix-glossary.html#care-services-selective-supplier) de mCSD. Lo consultan el Record Locator Service, para dirigir cada recuperación, y el Document Registry, para validar a quien publica. No agrupa ningún otro actor.

**Registro de identidad maestra.** Agrupa tres actores que trabajan sobre los mismos datos, y es Resource Server de IUA ante todos ellos.

- El [Patient Identity Registry](appendix-glossary.html#patient-identity-registry) de PMIR, que recibe por ITI-93 las identidades maestras de la fuente autoritativa y las reenvía a quien las consume, como el Document Registry.
- El [Patient Identifier Cross-reference Manager](appendix-glossary.html#patient-identifier-cross-reference-manager) de PIXm, que recibe por ITI-104 las identidades locales que los miembros declaran, las enlaza con la identidad maestra y responde ITI-83.
- El [Patient Demographics Supplier](appendix-glossary.html#patient-demographics-supplier) de PDQm, que responde por ITI-78 las búsquedas por datos demográficos.

**Audit Record Repository.** Es el [Audit Record Repository](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html) de ATNA con la opción ATX: FHIR Feed, que recibe por ITI-20 los eventos de los actores centrales como recursos AuditEvent. No agrupa ningún otro actor.

**Fuente autoritativa de identidad.** Es el [Patient Identity Source](appendix-glossary.html#patient-identity-source) de PMIR, que crea, actualiza, fusiona y desactiva las identidades maestras con ITI-93, y un Authorization Client de IUA, porque lo hace con un token del Authorization Server de la comunidad. Es externa a la comunidad, y HIX no le pide nada que PMIR, IUA, ATNA y CT no pidan a cualquier sistema que participa.

### Resumen

La [Tabla 2.4-1](volume-1-groupings.html#tabla-2-4-1) reúne lo anterior en una sola vista. Las opciones van entre corchetes. ATNA Secure Node o Secure Application y CT Time Client acompañan a todos los actores salvo a la aplicación del paciente y no se repiten en cada fila.

**Tabla 2.4-1:** Actores IHE que agrupa cada actor de HIX
{: #tabla-2-4-1}

| Actor de HIX | Actores agrupados |
| --- | --- |
| Custodio | MHD Document Source [Comprehensive Metadata], PIXm Patient Identity Source, IUA Authorization Client. Salvo bajo la Opción de Almacenamiento Central, también MHD Document Responder e IUA Resource Server |
| Consumidor | MHD Document Consumer, IUA Authorization Client. Opcionalmente PIXm Patient Identifier Cross-reference Consumer y, bajo la Opción de Demografía, PDQm Patient Demographics Consumer |
| Aplicación del paciente | MHD Document Consumer, IUA Authorization Client |
| Record Locator Service | MHD Document Responder, MHD Document Consumer, PIXm Patient Identifier Cross-reference Consumer, mCSD Care Services Selective Consumer, IUA Resource Server [Token Introspection], IUA Authorization Client |
| Document Registry | MHDS Document Registry [Authorization, UnContained Reference], MHD Document Recipient [Comprehensive Metadata], MHD Document Responder, PMIR Patient Identity Consumer, mCSD Care Services Selective Consumer, PIXm Patient Identifier Cross-reference Consumer, IUA Resource Server [Authorization Server Metadata] |
| Authorization Server | IUA Authorization Server [Authorization Server Metadata, Token Introspection], OpenID Provider, PIXm Patient Identifier Cross-reference Consumer |
| Directorio de la comunidad | mCSD Care Services Selective Supplier |
| Registro de identidad maestra | PMIR Patient Identity Registry, PIXm Patient Identifier Cross-reference Manager, PDQm Patient Demographics Supplier, IUA Resource Server |
| Audit Record Repository | ATNA Audit Record Repository [ATX: FHIR Feed] |
| Fuente autoritativa de identidad | PMIR Patient Identity Source, IUA Authorization Client |
{: .table .table-bordered}

### Sobre los despliegues

Las agrupaciones anteriores son lógicas. Un despliegue puede repartir los actores agrupados entre varios sistemas o concentrarlos en uno solo, siempre que el comportamiento observable desde fuera sea el especificado. El Document Registry, el registro de identidad maestra y el directorio pueden vivir en un mismo servidor FHIR central sin que nada de esta sección cambie.

### Referencias

Las citas reproducen el texto publicado por su fuente. Los recortes se marcan con "[...]" y la negrita es de esta guía.

[^iua-actors]: [IUA, Table 34.1-1 IUA Profile - Actors and Transactions](https://profiles.ihe.net/ITI/IUA/index.html#341-iua-actors-transactions-and-content-modules): "Authorization Client \| Get Access Token \| R [...] Incorporate Access Token \| R [...] Get Authorization Server Metadata \| O [...] Resource Server \| Incorporate Access Token \| R [...] Introspect Token \| O (Note 1) [...] Get Authorization Server Metadata \| O [...] Note 1: **Optionality of this transaction is "R" for an actor that supports the Token Introspection Option.**"
[^atna-fhir-feed]: [RESTful ATNA (Query and Feed), Rev. 3.6, §9.2.7.1 ATX: FHIR Feed Option](https://www.ihe.net/uploadedFiles/Documents/ITI/IHE_ITI_Suppl_RESTful-ATNA.pdf): "The ATX: FHIR Feed Option enables **sending ATNA audit records using RESTful capabilities and FHIR resources**. An Audit Record Repository that supports this option shall implement the two RESTful interactions defined in the Record Audit Event [ITI-20] transaction."
[^mhds-groupings]: [MHDS, Table 1:50.3-1 Required Actor Groupings](https://profiles.ihe.net/ITI/MHDS/volume-1.html#1503-mhds-required-actor-groupings): "Document Registry \| Required \| **CT / Time Client** [...] Required \| **ATNA / Secure Node or Secure Application with the STX: TLS 1.2 with the BCP195 Option and the ATX: FHIR Feed Option** [...] Required \| **MHD / Document Responder** [...] Required \| **MHD / Document Recipient with the Comprehensive Metadata Option** [...] Required \| **PMIR / Patient Identity Consumer** [...] if the Authorization Option \| **IUA / Resource Server with the The IUA Authorization Server Metadata Option** [...] if the UnContained References Option \| **mCSD / Care Services Selective Consumer** [...] if the SVCM Validation Option \| SVCM / Terminology Consumer".
[^mhds-pic]: [MHDS, §1:50.1.1.1 Document Registry](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150111-document-registry): "PMIR - Patient Identity Consumer provides **patient identity synchronization and specifically the merge function** to be applied to any data managed in the Document Registry."
[^mhds-subject]: [MHDS Vol. 1, §1:50.1.1.1.1 When the grouped MHD Document Recipient is triggered](https://profiles.ihe.net/ITI/MHDS/volume-1.html#1501111-when-the-grouped-mhd-document-recipient--is-triggered): "The Document Registry SHALL validate that the subject of the DocumentReference, and List Resources is the same Patient, and that **Patient is a recognized and active Patient within the Community**. The Patient identity must be recognized and active by the PMIR Patient Identity Registry in the document sharing community. **This may be accomplished by a query of the PMIR Patient Identity Registry**, by way of a cached internal patient database, or other means."
[^mhds-source-comprehensive]: [MHDS, §1:50.4.2.1 Use Case #1: Publication of a new document with persistence](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150421-use-case-1-publication-of-a-new-document-with-persistence): "**The MHD Comprehensive Metadata Option is required of the MHD Document Source** as the MHD Document Recipient within the MHDS Document Registry will implement the Comprehensive Metadata Option."
[^oidc-op]: [OpenID Connect Core 1.0, §1.2 Terminology](https://openid.net/specs/openid-connect-core-1_0.html#Terminology): "OpenID Provider (OP): **OAuth 2.0 Authorization Server that is capable of Authenticating the End-User** and providing Claims to a Relying Party about the Authentication event and the End-User."
[^smart-openid]: [SMART App Launch, Scopes for requesting identity data](https://build.fhir.org/ig/HL7/smart-app-launch/scopes-and-launch-context.html#scopes-for-requesting-identity-data): "Some apps need to authenticate the end-user. This can be accomplished by **requesting the scope openid**. [...] When these scopes are requested (and the request is granted), **the app will receive an id_token that comes alongside the access token**. This token must be validated according to the OIDC specification."

*[PMIR]: Patient Master Identity Registry, perfil IHE que gestiona la identidad maestra del paciente
*[PIXm]: Patient Identifier Cross-referencing for mobile, perfil IHE que enlaza los identificadores locales de un paciente con su identidad maestra
*[PDQm]: Patient Demographics Query for Mobile, perfil IHE de búsqueda de pacientes por datos demográficos
*[MHD]: Mobile access to Health Documents, perfil IHE para publicar, localizar y recuperar documentos sobre FHIR
*[MHDS]: Mobile Health Document Sharing, perfil IHE que compone MHD, PMIR, mCSD, IUA y ATNA en una comunidad de intercambio de documentos
*[mCSD]: Mobile Care Services Discovery, perfil IHE de directorio de organizaciones, servicios y endpoints
*[IUA]: Internet User Authorization, perfil IHE que aplica OAuth 2.0 a las transacciones sobre FHIR
*[ATNA]: Audit Trail and Node Authentication, perfil IHE de auditoría y seguridad de los nodos
*[BALP]: Basic Audit Log Patterns, perfil IHE con los patrones de AuditEvent de FHIR
*[CT]: Consistent Time, perfil IHE que sincroniza los relojes de los sistemas
*[SVCM]: Sharing Valuesets, Codes, and Maps, perfil IHE de terminología
