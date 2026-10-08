El [Volumen 1](volume-1.html) fija la arquitectura de HIX, es decir, qué actores tiene la comunidad, qué hace cada uno y por qué. Este volumen entra en el detalle de las transacciones entre esos actores. De cada una dice qué lleva la petición, qué se responde, cuándo se rechaza y qué se registra. Cuando una regla ya está en el Volumen 1, aquí se enlaza en lugar de repetirla.

Solo dos transacciones se especifican completas, [Mediated Token Exchange \[HIX-1\]](volume-2-hix-1.html) y [Patient Application Launch \[HIX-2\]](volume-2-hix-2.html), porque son propias de HIX y ningún perfil las define. Las demás vienen de perfiles IHE, y HIX las usa tal como las definen. De ellas este volumen solo dice con qué restricciones las usa la comunidad y lo muestra con ejemplos. Lo que este volumen no dice se aplica tal como lo publican IHE y OAuth 2.0.

### Cómo leer este volumen

- **[Autorización](volume-2-authorization.html)** dice con qué restricciones usa HIX ITI-71 e ITI-102, con los que el Authorization Server emite y comprueba los tokens.
- **[Mediated Token Exchange \[HIX-1\]](volume-2-hix-1.html)** especifica completo el intercambio con el que el Record Locator Service obtiene un token para cada destino.
- **[Patient Application Launch \[HIX-2\]](volume-2-hix-2.html)** especifica completo el lanzamiento con el que la aplicación del paciente obtiene su token.
- **[Identidad del paciente](volume-2-identity.html)** dice con qué restricciones usa HIX ITI-93, ITI-104, ITI-83, ITI-78 e ITI-119.
- **[Publicación](volume-2-publication.html)** dice con qué restricciones usa HIX ITI-65.
- **[Localización y recuperación](volume-2-retrieval.html)** dice con qué restricciones usa HIX ITI-66, ITI-67, ITI-68 e ITI-90.

Cada página abre con lo que comparten sus transacciones. Después dedica una sección a cada transacción IHE, siempre con los mismos cuatro apartados y en el orden en que una transacción IHE presenta su alcance, sus mensajes y su auditoría.

1. **Alcance en HIX.** Quién inicia la transacción y quién la responde, en términos de actores HIX.
2. **Petición.** Los parámetros y elementos que HIX fija, con enlace a la sección exacta del perfil.
3. **Respuesta y rechazos.** Las condiciones de rechazo que HIX aplica, cada una con su motivo.
4. **Auditoría.** Una remisión a la [Tabla 3-2](volume-2.html#tabla-3-2), salvo que HIX añada algo.

HIX-1 y HIX-2 no siguen esa plantilla abreviada sino la completa de IHE, desde el alcance y los roles de actor hasta las consideraciones de seguridad y la auditoría.

### Reglas comunes {#reglas-comunes}

Las reglas de esta sección se aplican a varias transacciones. Provienen del Volumen 1, salvo la regla sobre respuestas FHIR, que se establece aquí.

#### Peticiones a un Resource Server {#peticiones-a-un-resource-server}

El Resource Server **SHALL** rechazar la petición que no cumpla estas reglas.

1. Lleva un token conforme a ITI-72 cuya audiencia incluye a ese Resource Server, según la [sección 2.2](volume-1-actors.html#descripcion-de-actores-y-requisitos).
2. El scope del token incluye el identificador de la transacción IHE, por ejemplo `ITI-67`. Esto también se aplica al token de una aplicación del paciente, según la [sección 2.6](volume-1-security.html#modelo-de-confianza).
3. El Resource Server toma del token los datos del solicitante: su organización, su propósito de uso y, si corresponde, el contexto de paciente. No los toma de la petición, como establece la [sección 2.2](volume-1-actors.html#record-locator-service). El Authorization Server fija la organización desde su propio registro y solo emite propósitos de uso que su registro admite, según sus [requisitos](volume-1-actors.html#authorization-server).

#### Respuestas de error FHIR {#respuestas-de-error-fhir}

Todo actor que rechaza una transacción FHIR **SHALL** incluir un OperationOutcome en la respuesta, junto con el status code del error.

#### Identificador de correlación {#identificador-de-correlacion}

El Record Locator Service genera el identificador de correlación y lo envía al custodio en el header `X-Request-Id`, como detalla [Localización y recuperación](volume-2-retrieval.html#iti-68). No reenvía un identificador propuesto por el solicitante, según la [sección 2.6](volume-1-security.html#seguridad-basica).

#### Registros de auditoría {#registros-de-auditoria}

Ningún registro de auditoría contiene un token completo ni contenido clínico, según la [sección 2.6](volume-1-security.html#seguridad-basica).

### Índice de transacciones {#indice-de-transacciones}

La [Tabla 3-1](volume-2.html#tabla-3-1) reúne las veinte transacciones de HIX, agrupadas por la página que las especifica. De cada una dice el perfil que la define, qué actor la inicia y cuál la responde, y su nombre enlaza a su especificación. Las del último grupo HIX las usa sin restricciones propias, y por eso su nombre enlaza a IHE. La tabla incluye las transacciones de las Tablas [2.2-1](volume-1-actors.html#tabla-2-2-1) y [2.2-2](volume-1-actors.html#tabla-2-2-2) y las que traen consigo las agrupaciones de la [Tabla 2.4-2](volume-1-groupings.html#tabla-2-4-2).

**Tabla 3-1:** Transacciones de HIX
{: #tabla-3-1}

| Transacción | Perfil | Inicia | Responde |
| --- | --- | --- | --- |
| **Tokens y autorización** | | | |
| [Get Access Token \[ITI-71\]](volume-2-authorization.html#iti-71) | IUA | Custodio, consumidor, fuente autoritativa de identidad, Record Locator Service y el propio Authorization Server para su consulta ITI-83 | Authorization Server |
| [Introspect Token \[ITI-102\]](volume-2-authorization.html#iti-102) | IUA | Record Locator Service, Document Registry y Master Patient Index, y el custodio cuando la comunidad admite la introspección | Authorization Server |
| [Mediated Token Exchange \[HIX-1\]](volume-2-hix-1.html) | HIX | Record Locator Service | Authorization Server |
| [Patient Application Launch \[HIX-2\]](volume-2-hix-2.html) | HIX | Aplicación del paciente | Authorization Server |
| [Incorporate Access Token \[ITI-72\]](volume-2.html#peticiones-a-un-resource-server) | IUA | Todo Authorization Client, es decir, los miembros, la aplicación del paciente, la fuente autoritativa de identidad y el Record Locator Service | Todo Resource Server, es decir, el Record Locator Service, el custodio, el Document Registry y el Master Patient Index |
| **Identidad del paciente** | | | |
| [Mobile Patient Identity Feed \[ITI-93\]](volume-2-identity.html#iti-93) | PMIR | Fuente autoritativa de identidad, y el Master Patient Index hacia el Document Registry | Master Patient Index y Document Registry |
| [Patient Identity Feed FHIR \[ITI-104\]](volume-2-identity.html#iti-104) | PIXm | Custodio | Master Patient Index |
| [Mobile Patient Identifier Cross-reference Query \[ITI-83\]](volume-2-identity.html#iti-83) | PIXm | Consumidor, Record Locator Service, Document Registry y Authorization Server, y opcionalmente el custodio | Master Patient Index |
| [Mobile Patient Demographics Query \[ITI-78\]](volume-2-identity.html#iti-78) | PDQm | Consumidor | Master Patient Index |
| [Patient Demographics Match \[ITI-119\]](volume-2-identity.html#iti-119) | PDQm | Consumidor | Master Patient Index |
| **Publicación** | | | |
| [Provide Document Bundle \[ITI-65\]](volume-2-publication.html#iti-65) | MHD | Custodio | Document Registry |
| **Localización y recuperación** | | | |
| [Find Document Lists \[ITI-66\]](volume-2-retrieval.html#iti-66) | MHD | Consumidor y aplicación del paciente, y el Record Locator Service hacia el Document Registry | Record Locator Service y Document Registry |
| [Find Document References \[ITI-67\]](volume-2-retrieval.html#iti-67) | MHD | Consumidor y aplicación del paciente, y el Record Locator Service hacia el Document Registry | Record Locator Service y Document Registry |
| [Retrieve Document \[ITI-68\]](volume-2-retrieval.html#iti-68) | MHD | Consumidor y aplicación del paciente, y el Record Locator Service hacia el custodio o, bajo la Opción de Almacenamiento Central, el Document Registry | Record Locator Service y custodio, o el Document Registry bajo la Opción de Almacenamiento Central |
| [Find Matching Care Services \[ITI-90\]](volume-2-retrieval.html#iti-90) | mCSD | Record Locator Service y Document Registry | Directorio de la comunidad |
| **Auditoría** | | | |
| [Record Audit Event \[ITI-20\]](volume-2.html#auditoria) | ATNA | Todo actor salvo la aplicación del paciente | El Audit Record Repository de la comunidad, o el del propio miembro |
| **Sin restricciones de HIX** | | | |
| [Subscribe to Patient Updates \[ITI-94\]](https://profiles.ihe.net/ITI/PMIR/ITI-94.html) | PMIR | Patient Identity Subscriber, que puede ser el Document Registry o la operación de la comunidad | Master Patient Index |
| [Get Authorization Server Metadata \[ITI-103\]](https://profiles.ihe.net/ITI/IUA/index.html#3103-get-authorization-server-metadata-iti-103) | IUA | Todo Authorization Client y todo Resource Server | Authorization Server |
| [Maintain Time \[ITI-1\]](https://profiles.ihe.net/ITI/TF/Volume2/ITI-1.html#3.1) | CT | Todo actor salvo la aplicación del paciente | Time Server que designa la comunidad |
| [Authenticate Node \[ITI-19\]](https://profiles.ihe.net/ITI/TF/Volume2/ITI-19.html#3.19) | ATNA | Todo actor salvo la aplicación del paciente, al abrir una conexión | El actor con el que se conecta |
{: .table .table-bordered}

El scope de cada transacción es su identificador, como fija la regla 2 para las [peticiones a un Resource Server](volume-2.html#peticiones-a-un-resource-server). [HIX-2](volume-2-hix-2.html) es la única excepción, y detalla su scope en su página. Pide además `openid`, `fhirUser`, `launch/patient` y, para renovar el token, `offline_access`.

ITI-71, HIX-1, ITI-72, ITI-102, ITI-103, ITI-20, ITI-1 e ITI-19 no tienen scope propio. ITI-71 y HIX-1 son las que piden los scopes, ITI-72 la que los transporta, y las demás forman parte de la infraestructura de seguridad de la comunidad. En HIX-1, el Record Locator Service pide el scope de la transacción que va a realizar ante el destino.

> **TODO.** Falta definir cómo se audita la aplicación del paciente. Ya opera casi como un miembro, pero puede no tener backend propio y hacer todo su flujo en el navegador, y por eso la [sección 2.4](volume-1-groupings.html#lo-que-casi-todos-agrupan) la deja por ahora fuera de ATNA y de CT. Hay que probar si ese flujo tiene limitantes y, si no las tiene, auditarla como a un miembro más.

### Auditoría {#auditoria}

Todo actor de HIX, salvo la aplicación del paciente, registra sus eventos como recursos AuditEvent con Record Audit Event [ITI-20], como fija la [sección 2.4](volume-1-groupings.html#lo-que-casi-todos-agrupan). Los actores centrales los envían al Audit Record Repository de la comunidad y cada miembro registra los de su lado. Este volumen especifica ITI-20 aquí, una sola vez, para todas las transacciones.

ITI-20 se usa bajo la opción ATX: FHIR Feed. Un evento suelto viaja con la interacción Send Audit Resource Request, que es un `create` de FHIR, y varios juntos con Send Audit Bundle Request, que es un `batch` ([RESTful ATNA, §3.20.4.2 y §3.20.4.4](https://www.ihe.net/uploadedFiles/Documents/ITI/IHE_ITI_Suppl_RESTful-ATNA.pdf))[^atna-feed]. HIX la usa sin parámetros ni condiciones de rechazo propios. Lo que HIX fija es el contenido de los eventos, con las reglas comunes del [identificador de correlación](volume-2.html#identificador-de-correlacion) y de los [registros de auditoría](volume-2.html#registros-de-auditoria).

El contenido de cada evento es el que el perfil de la transacción define en su sección de auditoría. La mayoría de los perfiles lo construye sobre los patrones de BALP para las interacciones REST de FHIR, que son Create, Read, Update, Delete y Query, cada uno con una variante para cuando hay un paciente identificado ([BALP, §3:5.7.3](https://profiles.ihe.net/ITI/BALP/content.html#3573-restful-activities))[^balp-rest]. La [Tabla 3-2](volume-2.html#tabla-3-2) dice qué evento corresponde a cada transacción y quién lo registra.

**Tabla 3-2:** Eventos de auditoría por transacción
{: #tabla-3-2}

| Transacción | Patrón BALP | Quién registra |
| --- | --- | --- |
| ITI-71 | Ninguno. IUA define su propio evento, User Authentication con el subtipo ITI-71 ([IUA, §3.71.5.1](https://profiles.ihe.net/ITI/IUA/index.html#37151-security-audit-considerations))[^iua-audit] | El Authorization Server y el cliente que pide el token |
| ITI-72 | Ninguno propio. El Resource Server registra la identidad del token en el evento de la transacción que lo lleva ([IUA, §3.72.5.1](https://profiles.ihe.net/ITI/IUA/index.html#37251-security-audit-considerations))[^iua-audit], y en un AuditEvent la añade con uno de los patrones OAuth Security Token de BALP ([BALP, §3:5.7.5](https://profiles.ihe.net/ITI/BALP/content.html#3575-oauth-security-token))[^balp-token] | El cliente y el Resource Server |
| ITI-102 | Ninguno propio. El Resource Server usa el resultado de la introspección como atributos del evento ([IUA, §3.102.5.1](https://profiles.ihe.net/ITI/IUA/index.html#310251-security-audit-considerations))[^iua-audit] | El Record Locator Service, y el Document Registry, el Master Patient Index y el custodio cuando la usan |
| HIX-1 | IHE no define ningún evento para un intercambio de tokens. Lo especifica [Mediated Token Exchange \[HIX-1\]](volume-2-hix-1.html#consideraciones-de-auditoria) | El Authorization Server |
| HIX-2 | El evento de ITI-71 ([IUA, §3.71.5.1](https://profiles.ihe.net/ITI/IUA/index.html#37151-security-audit-considerations))[^iua-audit]. Lo detalla [Patient Application Launch \[HIX-2\]](volume-2-hix-2.html#consideraciones-de-auditoria) | El Authorization Server |
| ITI-93 | Ninguno. PMIR define su propio evento, un Patient Record de ITI-20 que registran igual quien lo envía y quien lo recibe ([PMIR, §2:3.93.5.1](https://profiles.ihe.net/ITI/PMIR/ITI-93.html#239351-security-audit-considerations))[^pmir-audit] | La fuente autoritativa de identidad, el Master Patient Index y el Document Registry |
| ITI-104 | PatientCreate o PatientUpdate, según la operación ([PIXm, §2:3.104.5.1](https://profiles.ihe.net/ITI/PIXm/ITI-104.html#2310451-security-audit-considerations))[^pixm-audit] | El custodio y el Master Patient Index |
| ITI-83 | PatientQuery ([PIXm, §2:3.83.5.1](https://profiles.ihe.net/ITI/PIXm/ITI-83.html#238351-security-audit-considerations))[^pixm-audit] | Quien consulta y el Master Patient Index |
| ITI-78 | Query ([PDQm, §2:3.78.5.1](https://profiles.ihe.net/ITI/PDQm/ITI-78.html#237851-security-audit-considerations))[^pdqm-audit] | El consumidor y el Master Patient Index |
| ITI-119 | Query ([PDQm, §2:3.119.5.1](https://profiles.ihe.net/ITI/PDQm/ITI-119.html#2311951-security-audit-considerations))[^pdqm-audit] | El consumidor y el Master Patient Index |
| ITI-65 | Ninguno. MHD define su propio evento, con criterios similares a los de ITI-41 ([MHD, §2:3.65.5.1](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-65.html#236551-security-audit-considerations))[^mhd-audit] | El custodio y el Document Registry |
| ITI-66 | PatientQuery, en la versión que publica MHD ([MHD, §2:3.66.5.1](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-66.html#236651-security-audit-considerations))[^mhd-audit] | El consumidor, el Record Locator Service en sus dos papeles y el Document Registry |
| ITI-67 | PatientQuery, en la versión que publica MHD ([MHD, §2:3.67.5.1](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-67.html#236751-security-audit-considerations))[^mhd-audit] | El consumidor, el Record Locator Service en sus dos papeles y el Document Registry |
| ITI-68 | PatientRead, en la versión que publica MHD ([MHD, §2:3.68.5.1](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-68.html#236851-security-audit-considerations))[^mhd-audit] | El consumidor, el Record Locator Service en sus dos papeles y el custodio, o el Document Registry bajo la Opción de Almacenamiento Central |
| ITI-90 | Query o Read, según la interacción ([mCSD, §2:3.90.5.1](https://profiles.ihe.net/ITI/mCSD/ITI-90.html#239051-security-audit-considerations))[^mcsd-audit] | El Record Locator Service, el Document Registry y el directorio de la comunidad |
{: .table .table-bordered}

El Record Locator Service registra la solicitud que recibe y cada recuperación que origina hacia un custodio, bajo un mismo identificador de correlación, como fija la [sección 2.6](volume-1-security.html#seguridad-basica). En ITI-66, ITI-67 e ITI-68 la tabla le da dos papeles, porque MHD pide registrar tanto al Document Responder, que es su papel ante el solicitante, como al Document Consumer, que es su papel ante el Document Registry o el custodio ([MHD, §2:3.67.5.1.1 y §2:3.67.5.1.2](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-67.html#2367511-document-consumer-audit))[^mhd-roles]. La aplicación del paciente no registra eventos. Su actividad la registran el Authorization Server al lanzarla y el Record Locator Service en cada consulta, como dice la [sección 2.4](volume-1-groupings.html#lo-que-casi-todos-agrupan).

ITI-103, ITI-1 e ITI-19 no tienen fila, porque su especificación no define un evento propio. Los eventos generales de seguridad, como un fallo de autenticación de un nodo, son los de la tabla de ITI-20 que todo Secure Node o Secure Application debe poder registrar ([ITI TF-2, §3.20.4.1.1.1](https://profiles.ihe.net/ITI/TF/Volume2/ITI-20.html#3.20.4.1.1.1))[^iti20-triggers].


### Referencias

Las citas reproducen el texto publicado por su fuente. Los recortes se marcan con "[...]" y la negrita es de esta guía.

[^atna-feed]: [RESTful ATNA (Query and Feed), Rev. 3.6, §3.20.4.2 Send Audit Resource Request Message – FHIR Feed Interaction](https://www.ihe.net/uploadedFiles/Documents/ITI/IHE_ITI_Suppl_RESTful-ATNA.pdf): "A Secure Node, Secure Application or Audit Record Forwarder, that supports the ATX: FHIR Feed Option, uses this message to **post a single AuditEvent Resource** to the Audit Record Repository **using a FHIR create interaction** [...]". §3.20.4.4 Send Audit Bundle Request Message – FHIR Feed Interaction: "A Secure Node, Secure Application or Audit Record Forwarder that supports the ATX: FHIR Feed Option uses this message to **post a Bundle of AuditEvent Resources** to the Audit Record Repository **using a FHIR batch interaction** [...]"
[^balp-rest]: [BALP, §3:5.7.3 RESTful activities](https://profiles.ihe.net/ITI/BALP/content.html#3573-restful-activities): "When a FHIR RESTful interaction happens, **the following AuditEvent patterns can be used**. [...] There are two sets of profiles distinguished by **Patient as a subject** being mandated to be populated." La tabla de esa sección nombra los patrones Create, Read, Update, Delete y Query, y sus variantes PatientCreate, PatientRead, PatientUpdate, PatientDelete y PatientQuery.
[^iua-audit]: [IUA, §3.71.5.1 Security Audit Considerations](https://profiles.ihe.net/ITI/IUA/index.html#37151-security-audit-considerations): "The Authorization Client or Authorization Server that is grouped with an ATNA Secure Node or Secure Application **shall be able to send an audit event as defined below** [...] EventID [...] **EV(110114, DCM, "User Authentication")** [...] EventTypeCode [...] **EV("ITI-71", IHE, "User Authorization")**". [§3.72.5.1 Security Audit Considerations](https://profiles.ihe.net/ITI/IUA/index.html#37251-security-audit-considerations): "When an ATNA Audit message needs to be generated by the Resource Server and the user is authenticated by way of a JWT Token, **the ATNA Audit message UserName element shall record the JWT Token information** [...]". [§3.102.5.1 Security Audit Considerations](https://profiles.ihe.net/ITI/IUA/index.html#310251-security-audit-considerations): "**Resource Servers shall use the introspection results as authorization claims when formulating audit messages**, as specified in ITI TF-2 3.72.5.1."
[^balp-token]: [BALP, §3:5.7.5 OAuth Security Token](https://profiles.ihe.net/ITI/BALP/content.html#3575-oauth-security-token): "**There are three patterns defined: opaque, minimal, and comprehensive.** [...] The profiling AuditEvent defined here is **the AuditEvent that the Client and Server would record when using IUA with the ITI TF-2: 3.72 Incorporate Access Token [ITI-72]** to secure some RESTful transaction."
[^pmir-audit]: [PMIR, §2:3.93.5.1 Security Audit Considerations](https://profiles.ihe.net/ITI/PMIR/ITI-93.html#239351-security-audit-considerations): "The Mobile Patient Identity Feed transaction is **a Patient Record Message event** as defined in ITI TF-2: 3.20.4.1.1.1-1. **Note that the same audit message is recorded by both Supplier and Consumer.** The difference being the Audit Source element. [...] The actors involved shall record audit events according to the Audit Event for Mobile Patient Identity Feed by the Supplier and Consumer." Ese perfil, [IHE.PMIR.Feed.Audit](https://profiles.ihe.net/ITI/PMIR/StructureDefinition-IHE.PMIR.Feed.Audit.html), deriva directamente de AuditEvent y no de un patrón de BALP.
[^pixm-audit]: [PIXm, §2:3.104.5.1 Security Audit Considerations](https://profiles.ihe.net/ITI/PIXm/ITI-104.html#2310451-security-audit-considerations): "The Security audit logging will conform to the RESTful interactions following **IHE-BALP Basic Audit Logging Patterns**." §2:3.104.5.1.2 Patient Identifier Cross-reference Manager Audit: "The Patient Identifier Cross-Reference Manager can distinguish a Create and Update so **is expected to record Create and Update specifically**." [§2:3.83.5.1 Security Audit Considerations](https://profiles.ihe.net/ITI/PIXm/ITI-83.html#238351-security-audit-considerations) dice lo mismo para ITI-83, y su perfil [IHE.PIXm.Query.Audit.Manager](https://profiles.ihe.net/ITI/PIXm/StructureDefinition-IHE.PIXm.Query.Audit.Manager.html) dice "**Build off of the IHE BasicAudit Patient Query event**".
[^pdqm-audit]: [PDQm, §2:3.78.5.1 Security Audit Considerations](https://profiles.ihe.net/ITI/PDQm/ITI-78.html#237851-security-audit-considerations): "The Mobile Patient Demographics Query Transaction is **a Query Information event** as defined in Table 3.20.4.1.1.1-1. **The actors involved SHALL record audit events** according to the following". [§2:3.119.5.1](https://profiles.ihe.net/ITI/PDQm/ITI-119.html#2311951-security-audit-considerations) dice lo mismo para ITI-119. Sus perfiles, como [IHE.PDQm.Query.Audit.Supplier](https://profiles.ihe.net/ITI/PDQm/StructureDefinition-IHE.PDQm.Query.Audit.Supplier.html), dicen "**Build off of the IHE BasicAudit Query event**".
[^mhd-audit]: [MHD, §2:3.65.5.1 Security Audit Considerations](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-65.html#236551-security-audit-considerations): "**The security audit criteria are similar to those for the Provide and Register Document Set-b [ITI-41] transaction** as this transaction does export a document." Sus perfiles, como [IHE.MHD.ProvideBundle.Audit.Recipient](https://profiles.ihe.net/ITI/MHD/5.0.0/StructureDefinition-IHE.MHD.ProvideBundle.Audit.Recipient.html), derivan directamente de AuditEvent. Para ITI-67, el perfil [IHE.MHD.FindDocumentReferences.Audit.Responder](https://profiles.ihe.net/ITI/MHD/5.0.0/StructureDefinition-IHE.MHD.FindDocumentReferences.Audit.Responder.html) dice "**Build off of the IHE BasicAudit PatientQuery event**", como los de ITI-66, y para ITI-68 [IHE.MHD.RetrieveDocument.Audit.Responder](https://profiles.ihe.net/ITI/MHD/5.0.0/StructureDefinition-IHE.MHD.RetrieveDocument.Audit.Responder.html) dice "**Build off of the IHE BasicAudit PatientRead event**". MHD 5.0.0 publica esos patrones en su propio paquete, sobre FHIR R5.
[^mhd-roles]: [MHD, §2:3.67.5.1.1 Document Consumer Audit](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-67.html#2367511-document-consumer-audit): "**The Document Consumer when grouped with ATNA Secure Node or Secure Application Actor shall be able to record** a Find Document References Consumer Audit Event Log." [§2:3.67.5.1.2 Document Responder Audit](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-67.html#2367512-document-responder-audit): "**The Document Responder when grouped with ATNA Secure Node or Secure Application Actor shall be able to record** a Find Document References Responder Audit Event Log." Las secciones [§2:3.66.5.1](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-66.html#236651-security-audit-considerations) y [§2:3.68.5.1](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-68.html#236851-security-audit-considerations) dicen lo mismo para ITI-66 e ITI-68.
[^mcsd-audit]: [mCSD, §2:3.90.5.1 Security Audit Considerations](https://profiles.ihe.net/ITI/mCSD/ITI-90.html#239051-security-audit-considerations): "Note that when grouped with ATNA Secure Node or Secure Application Actor, **the same audit message is recorded by both Directory and Query Client**. [...] the actors involved shall be able to record audit events according to the **Audit Event for Find Matching Care Services for Read** by the Directory and Query Client or the **Audit Event for Find Matching Care Services for Query** by the Directory and Query Client." Esos perfiles derivan de los patrones Read y Query de BALP.
[^iti20-triggers]: [ITI TF-2, §3.20.4.1.1.1 DICOM and IHE Audit Event messages](https://profiles.ihe.net/ITI/TF/Volume2/ITI-20.html#3.20.4.1.1.1): "An actor in any IHE profile, when grouped with a Secure Node or Secure Application, **shall be able to report the relevant events defined in Table 3.20.4.1.1.1-1** (previously Table 3.20.6-1). This table of auditable events is not exhaustive. **Additional reportable events are often identified for specific events in other IHE profiles**, and are documented in that profile or transaction." La tabla incluye "Node-Authentication-failure", "A secure node authentication failure has occurred during TLS negotiation, e.g., invalid certificate."

*[PMIR]: Patient Master Identity Registry, perfil IHE que gestiona la identidad maestra del paciente
*[PIXm]: Patient Identifier Cross-referencing for mobile, perfil IHE que enlaza los identificadores locales de un paciente con su identidad maestra
*[PDQm]: Patient Demographics Query for Mobile, perfil IHE de búsqueda de pacientes por datos demográficos
*[MHD]: Mobile access to Health Documents, perfil IHE para publicar, localizar y recuperar documentos sobre FHIR
*[mCSD]: Mobile Care Services Discovery, perfil IHE de directorio de organizaciones, servicios y endpoints
*[IUA]: Internet User Authorization, perfil IHE que aplica OAuth 2.0 a las transacciones sobre FHIR
*[ATNA]: Audit Trail and Node Authentication, perfil IHE de auditoría y seguridad de los nodos
*[BALP]: Basic Audit Log Patterns, perfil IHE con los patrones de AuditEvent de FHIR
*[CT]: Consistent Time, perfil IHE que sincroniza los relojes de los sistemas
