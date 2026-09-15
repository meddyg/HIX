Esta sección define los actores de HIX y las transacciones que los vinculan. Los actores y transacciones tomados de un perfil IHE conservan el significado que les da su especificación de origen. Las transacciones identificadas como `HIX-n` son propias de esta guía y se especifican en el Volumen 2.

HIX distingue tres clases de actor. Los **actores centrales** los opera la comunidad. Los **actores de miembro** los opera cada organización participante. La **fuente autoritativa de identidad** es externa a la comunidad. Un miembro solo trata con la infraestructura central, nunca con otro miembro. Obtiene sus tokens del Authorization Server, localiza y recupera a través del Record Locator Service, y publica y declara identidades ante la infraestructura central, que valida esas transacciones como describe la sección 2.1.

Las tres pestañas siguientes muestran a los actores de miembro en su escenario típico. La aplicación del paciente es la de una persona que entra a su propio expediente. El hospital es un sistema que consume documentos, en atención normal y en una emergencia, donde por ejemplo busca al paciente por sus datos demográficos con PDQm. El laboratorio es un sistema que publica y custodia documentos.

El propósito de uso no depende del actor sino del caso de uso. Es un código del conjunto [PurposeOfUse](https://terminology.hl7.org/ValueSet-v3-PurposeOfUse.html) de HL7, tomado del sistema [v3-ActReason](https://terminology.hl7.org/CodeSystem-v3-ActReason.html), que el Authorization Server incluye en el token de cada solicitante y que la decisión de divulgación evalúa. No decide qué transacciones puede pedir un solicitante. Eso lo fija el scope de su token. Un mismo hospital consulta con `TREAT`, tratamiento, en la atención habitual y con `ETREAT`, tratamiento de emergencia, en una urgencia. Una aplicación entra a un expediente a petición del paciente, `PATRQT`, de un familiar autorizado por él, `FAMRQT`, o de su representante legal, `PWATRNY`. Un laboratorio publica con `TREAT`. HIX usa el conjunto completo de HL7 y no lo restringe. Qué propósitos acepta una comunidad, y con qué condiciones, es política de implementación. La Tabla 2.2-3 solo orienta al lector con los más frecuentes y el caso en el que aparece cada uno[^pou].

<ul class="nav nav-tabs" role="tablist">
  <li class="active"><a href="#tab-actores-paciente" data-toggle="tab">Aplicación del paciente</a></li>
  <li><a href="#tab-actores-hospital" data-toggle="tab">Hospital que consulta</a></li>
  <li><a href="#tab-actores-laboratorio" data-toggle="tab">Laboratorio que publica</a></li>
</ul>

<div class="tab-content">

<div id="tab-actores-paciente" class="tab-pane active" markdown="1">

![Aplicación del paciente ante la comunidad](hix-actores-paciente.svg)

**Figura 2.2-1:** Aplicación del paciente ante la comunidad

</div>

<div id="tab-actores-hospital" class="tab-pane" markdown="1">

![Hospital que consulta, en atención normal y en emergencia](hix-actores-hospital.svg)

**Figura 2.2-2:** Hospital que consulta, en atención normal y en emergencia (ETREAT con PDQm)

</div>

<div id="tab-actores-laboratorio" class="tab-pane" markdown="1">

![Laboratorio que publica documentos](hix-actores-laboratorio.svg)

**Figura 2.2-3:** Laboratorio que publica documentos

</div>

</div>

Las dos tablas siguientes listan las transacciones que definen a cada actor. R significa que la transacción es requerida para declararse conforme con el actor, y O que es opcional. La columna Referencia indica el perfil IHE que define la transacción, o el Volumen 2 de esta guía para las propias de HIX. Todos los actores de HIX se agrupan además con IUA y con ATNA. Esas agrupaciones, y las transacciones que traen consigo, se listan en la sección 2.4.

**Tabla 2.2-1:** Actores de miembro

| Actor | Transacción | Opcionalidad | Referencia |
| --- | --- | --- | --- |
| Sistema que publica y custodia documentos | Patient Identity Feed FHIR [ITI-104] | R | PIXm |
| | Provide Document Bundle [ITI-65] | R | MHD |
| | Retrieve Document [ITI-68] | R (nota 1) | MHD |
| Sistema que consume documentos | Find Document References [ITI-67] | R | MHD |
| | Retrieve Document [ITI-68] | R | MHD |
| | Find Document Lists [ITI-66] | O | MHD |
| | Patient Identifier Cross-reference Query [ITI-83] | O | PIXm |
| | Patient Demographics Query for Mobile [ITI-78] | O (nota 2) | PDQm |
| Aplicación del paciente | Patient Application Launch [HIX-2] | R | Vol. 2 |
| | Find Document References [ITI-67] | R | MHD |
| | Retrieve Document [ITI-68] | R | MHD |
| | Find Document Lists [ITI-66] | O | MHD |
{: .table .table-bordered}

**Tabla 2.2-2:** Actores centrales y fuente de identidad

| Actor | Transacción | Opcionalidad | Referencia |
| --- | --- | --- | --- |
| Record Locator Service | Find Document References [ITI-67] | R | MHD |
| | Retrieve Document [ITI-68] | R | MHD |
| | Patient Identifier Cross-reference Query [ITI-83] | R | PIXm |
| | Find Matching Care Services [ITI-90] | R | mCSD |
| | Custodian Token Exchange [HIX-1] | R | Vol. 2 |
| Document Registry | Provide Document Bundle [ITI-65] | R | MHD |
| | Find Document Lists [ITI-66] | R | MHD |
| | Find Document References [ITI-67] | R | MHD |
| | Retrieve Document [ITI-68] | R (nota 3) | MHD |
| | Find Matching Care Services [ITI-90] | R | mCSD |
| Authorization Server | Get Access Token [ITI-71] | R | IUA |
| | Introspect Token [ITI-102] | R | IUA |
| | Get Authorization Server Metadata [ITI-103] | R | IUA |
| | Custodian Token Exchange [HIX-1] | R | Vol. 2 |
| | Patient Application Launch [HIX-2] | R | Vol. 2 |
| | Patient Identifier Cross-reference Query [ITI-83] | R | PIXm |
| Directorio de la comunidad | Find Matching Care Services [ITI-90] | R | mCSD |
| Registro de identidad maestra | Mobile Patient Identity Feed [ITI-93] | R | PMIR |
| | Patient Identity Feed FHIR [ITI-104] | R | PIXm |
| | Patient Identifier Cross-reference Query [ITI-83] | R | PIXm |
| | Patient Demographics Query for Mobile [ITI-78] | R | PDQm |
| Audit Record Repository | Record Audit Event [ITI-20] | R | ATNA |
| Fuente autoritativa de identidad (externa) | Mobile Patient Identity Feed [ITI-93] | R | PMIR |
{: .table .table-bordered}

Notas:

1. No requerido si el custodio declara la Opción de Colocación Central.
2. Requerido si el actor declara la Opción de Demografía.
3. El Document Registry responde [ITI-68] solo para el contenido colocado centralmente.

**Tabla 2.2-3:** Propósitos de uso más frecuentes en HIX

| Código | Nombre en HL7 | Caso en el que aparece |
| --- | --- | --- |
| [`TREAT`](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-TREAT) | treatment | Atención habitual de un paciente. Con él consulta un hospital y publica un laboratorio |
| [`ETREAT`](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-ETREAT) | Emergency Treatment | Atención inmediata de una urgencia. Qué permite frente a `TREAT` lo fija la política de la comunidad. Por ejemplo, divulgar documentos que en atención habitual exigirían un consentimiento, aunque el paciente esté plenamente identificado |
| [`BTG`](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-BTG) | break the glass | Urgencia atendida por quien no está autorizado para ese acceso, con anulación de la política. Cómo se admite y se audita lo fija cada comunidad |
| [`COC`](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-COC) | coordination of care | Coordinación de la atención de una persona entre varias organizaciones |
| [`PATRQT`](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-PATRQT) | patient requested | Acceso de una persona a su propio expediente |
| [`FAMRQT`](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-FAMRQT) | family requested | Acceso de un familiar autorizado por el paciente |
| [`PWATRNY`](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-PWATRNY) | power of attorney | Acceso del representante legal del paciente, como el padre o la madre de un menor |
| [`HOPERAT`](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-HOPERAT) | healthcare operations | Actividades administrativas y contractuales de la organización |
| [`HPAYMT`](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-HPAYMT) | healthcare payment | Actividades financieras relacionadas con el pago de la atención |
| [`HRESCH`](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-HRESCH) | healthcare research | Investigación en salud |
| [`PUBHLTH`](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-PUBHLTH) | public health | Actividades de salud pública, como la notificación de enfermedades de declaración obligatoria |
{: .table .table-bordered}

### Descripción de actores y requisitos

Las descripciones siguen el orden de las tablas. Dos reglas valen para todos los actores y no se repiten en cada uno. Todo actor que recibe un token **SHALL** comprobar que está destinado a él y **SHALL** rechazar la solicitud si no lo está, como recomienda RFC 9700 para todo Resource Server ([RFC 9700, §4.10.2](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.10.2))[^rfc9700-aud]. Que el Authorization Server de la comunidad haya emitido un token no lo hace válido ante cualquier actor. Cada token nombra en su audiencia, el claim `aud`, al único actor ante el que vale. Un token válido ante un miembro o ante un componente central no sirve ante ningún otro, aunque lo haya emitido el mismo Authorization Server. Y todo actor registra sus propios eventos de auditoría, como exige la agrupación con ATNA de la sección 2.4.

#### Sistema que publica y custodia documentos

El custodio es el miembro que produce documentos. Los conserva, declara las identidades locales de sus pacientes y publica los punteros a sus documentos con el propósito de uso del caso, normalmente `TREAT`. Agrupa a un Document Source y un Document Responder de MHD, y a un Patient Identity Source de PIXm. Responde las recuperaciones que le llegan desde la infraestructura central, y solo desde ella.

El custodio **SHALL** declarar mediante [ITI-104](https://profiles.ihe.net/ITI/PIXm/ITI-104.html) la identidad local de todo paciente sobre el que publique, en su propio dominio de identificadores y con el identificador nacional de la persona. **SHALL** publicar mediante [ITI-65](https://profiles.ihe.net/ITI/MHD/ITI-65.html) punteros que lo nombren a él como custodio, con URL de contenido relativa y etiqueta de confidencialidad.

El custodio **SHALL** conservar el contenido y responder [ITI-68](https://profiles.ihe.net/ITI/MHD/ITI-68.html), salvo que declare la Opción de Colocación Central. **SHALL** validar el token de cada solicitud sin depender del Authorization Server en ese momento, conforme a la sección 2.6. **SHALL** rechazar toda solicitud cuyo token no haya sido intercambiado por el Record Locator Service y **SHALL NOT** atender recuperaciones originadas directamente en otro miembro.

#### Sistema que consume documentos

El consumidor es el miembro que consulta el expediente de un paciente. Localiza y recupera documentos a través del Record Locator Service y agrupa a un Document Consumer de MHD. Desde su punto de vista la comunidad es un único servidor FHIR. Actúa con el propósito de uso `TREAT` en la atención habitual y con `ETREAT` cuando atiende una urgencia.

El consumidor **SHALL** obtener un token del Authorization Server destinado al Record Locator Service y **SHALL** presentarlo en toda solicitud. **SHALL** recuperar los documentos únicamente a través de las URL que el Record Locator Service le entrega. Puede resolver la identidad de un paciente con [ITI-83](https://profiles.ihe.net/ITI/PIXm/ITI-83.html) y, si declara la Opción de Demografía, buscarlo por sus datos demográficos con [ITI-78](https://profiles.ihe.net/ITI/PDQm/ITI-78.html), por ejemplo en una urgencia en la que no tiene un identificador fiable, como en la Figura 2.2-2.

#### Aplicación del paciente

La aplicación del paciente accede al expediente de la persona que la usa, con el contexto de paciente que el Authorization Server fija durante el lanzamiento y un propósito de uso a petición del paciente, `PATRQT`, de un familiar que él autorizó, `FAMRQT`, o de su representante legal, `PWATRNY`. Agrupa a un Document Consumer de MHD. A partir del lanzamiento, sus consultas y recuperaciones son las de cualquier otro consumidor, confinadas a ese único paciente.

Este actor **SHALL** obtener su token mediante [HIX-2] y **SHALL NOT** solicitar ni asumir un contexto de paciente distinto del que el token declara.

#### Record Locator Service

El Record Locator Service es el mediador de la comunidad. Localiza y recupera documentos en nombre de los miembros y aplica la decisión de divulgación sobre los punteros, antes de mover contenido alguno. Ante los miembros se comporta como un Resource Server de IUA y un Document Responder de MHD. Ante los custodios y los demás actores centrales actúa como Document Consumer de MHD y cliente delegado, en nombre del solicitante original.

El Record Locator Service **SHALL** aceptar únicamente tokens emitidos por el Authorization Server de la comunidad. **SHALL** comprobarlos mediante [ITI-102](https://profiles.ihe.net/ITI/IUA/index.html#3102-introspect-token-iti-102) una vez por operación y **SHALL** tomar de esa respuesta, y no de la solicitud, la organización, el propósito de uso y el contexto de paciente del solicitante.

El Record Locator Service **SHALL** evaluar la decisión de divulgación sobre los punteros antes de originar cualquier recuperación, **SHALL** omitir de la respuesta los punteros cuya divulgación no esté permitida y **SHALL** volver a evaluarla al atender un [ITI-68](https://profiles.ihe.net/ITI/MHD/ITI-68.html). Un puntero cuya divulgación se niega **SHALL NOT** originar consulta al directorio, intercambio de token ni llamada al custodio.

El Record Locator Service **SHALL** entregar a los solicitantes URL de contenido que apunten a sí mismo. **SHALL** resolver el endpoint del custodio en el directorio de la comunidad en cada recuperación y **SHALL NOT** revelar ese endpoint al solicitante. **SHALL** obtener mediante [HIX-1] un token distinto para cada destino que alcance, sea un custodio o un actor central, y **SHALL NOT** reenviar a ninguno el token del solicitante. No tiene acceso propio al Document Registry ni al registro de identidad maestra.

Cuando un custodio no responde, el Record Locator Service **SHALL** degradar la respuesta señalando el fallo y **SHALL NOT** hacer fallar la operación completa por ese motivo.

> **Nota.** *Record Locator Service* es el nombre que esta guía da al actor. No es vocabulario IHE. En términos de MHDS, es el intermediario que media la localización y la recuperación entre los miembros, el Document Registry y los custodios, agrupado con un Document Consumer y un Document Responder de MHD.

#### Document Registry

El Document Registry es el MHDS Document Registry de la comunidad. Conserva los punteros a los documentos publicados y, bajo la Opción de Colocación Central, el contenido que los custodios le entregan.

El Document Registry **SHALL** registrar cada puntero a nombre de la organización que declara el token, **SHALL** rechazar la publicación cuyo custodio no coincida con ella y **SHALL** validar mediante [ITI-90](https://profiles.ihe.net/ITI/mCSD/ITI-90.html) que esa organización es un miembro activo de la comunidad, conforme a la UnContained References Option de MHDS.

Al indexar, el Document Registry **SHALL** escribir en `subject` la identidad maestra del paciente, resuelta a partir de la identidad local declarada en `sourcepatient`. **SHALL** rechazar la publicación cuya URL de contenido no sea relativa, que carezca de etiqueta de confidencialidad o cuyo paciente no pueda resolverse a una identidad maestra.

#### Authorization Server

El Authorization Server emite, comprueba e intercambia los tokens que circulan por la comunidad. Es el Authorization Server de IUA. Es el único actor que decide sobre la autorización y el único que conoce a la vez al solicitante, su organización y el alcance que se le concede. No decide sobre consentimiento, relación terapéutica ni identidad de paciente.

El Authorization Server **SHALL** emitir tokens destinados a un único destinatario, identificado explícitamente, como recomienda RFC 9700 ([RFC 9700, §2.3](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.3))[^rfc9700-aud]. **SHALL** atender [HIX-1] únicamente para el Record Locator Service. El token intercambiado **SHALL** llevar como audiencia el único destino indicado en la petición de intercambio, como sujeto al solicitante original y como actor al Record Locator Service, en el claim `act` con el que OAuth 2.0 Token Exchange expresa la delegación ([RFC 8693, §4.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-4.1))[^rfc8693-act]. Su alcance **SHALL NOT** exceder el del token del solicitante ni el de la delegación registrada, y su vida **SHALL NOT** superar los dos minutos ni la vida restante del token del solicitante. El Authorization Server **SHALL NOT** emitir por ningún otro camino un token cuya audiencia sea un custodio.

El Authorization Server **SHALL** fijar la organización y el propósito de uso del solicitante desde su propio registro y **SHALL NOT** aceptarlos de la solicitud. Cuando una persona se autentica, **SHALL** resolver su identidad verificada a la identidad maestra mediante [ITI-83](https://profiles.ihe.net/ITI/PIXm/ITI-83.html) y **SHALL** fijar ese resultado como contexto de paciente del token, conforme a [HIX-2].

#### Directorio de la comunidad

El directorio publica las organizaciones participantes, su pertenencia a la comunidad y los endpoints en los que responden. Es el Care Services Selective Supplier de mCSD de la comunidad y la única fuente de la que la infraestructura central aprende a quién dirigir una recuperación.

El directorio **SHALL** responder [ITI-90](https://profiles.ihe.net/ITI/mCSD/ITI-90.html) y **SHALL** ser el único origen de los endpoints que usa la infraestructura central. **SHALL** identificar a cada organización con el mismo identificador que el Authorization Server incluye en sus tokens. Los miembros no consultan el directorio. Su contenido se mantiene administrativamente, al incorporar un miembro, como describe la sección 2.7.

#### Registro de identidad maestra

El registro de identidad maestra agrupa al Patient Identity Registry de PMIR, al Patient Identifier Cross-reference Manager de PIXm y al Patient Demographics Supplier de PDQm. Conserva una identidad maestra por persona, creada por la fuente autoritativa de identidad, y los enlaces con las identidades locales que los miembros declaran.

El registro de identidad maestra **SHALL** crear identidades maestras únicamente a partir de [ITI-93](https://profiles.ihe.net/ITI/PMIR/ITI-93.html) recibido de la fuente autoritativa de identidad. **SHALL** aceptar [ITI-104](https://profiles.ihe.net/ITI/PIXm/ITI-104.html) únicamente en el dominio de identificadores del miembro que lo origina y **SHALL** rechazar la declaración que no pueda vincularse a una identidad maestra existente, que use `link` entre pacientes o que pretenda fusionar o eliminar identidades. **SHALL NOT** modificar la demografía de la identidad maestra a partir de lo que un miembro declara.

#### Audit Record Repository

El Audit Record Repository es el actor de ATNA que recibe mediante [ITI-20](https://profiles.ihe.net/ITI/TF/Volume2/ITI-20.html) los eventos que registran los actores centrales. Existe para que una divulgación pueda reconstruirse completa desde el lado de la comunidad, con la solicitud del miembro y la recuperación ante el custodio bajo un mismo identificador de correlación. Cada miembro registra su propio lado en su propio registro, como ATNA exige a todo sistema que participa en una transacción.

#### Fuente autoritativa de identidad

La fuente autoritativa de identidad es el sistema, externo a la comunidad, contra el que se verifica la identidad de una persona y del que la comunidad obtiene sus identidades maestras. Es el Patient Identity Source de PMIR. HIX no designa cuál es. La propuesta para Costa Rica es que sea el EDUS, porque ya tiene resuelta la identificación de las personas.

La fuente autoritativa **SHALL** alimentar el registro de identidad maestra mediante [ITI-93](https://profiles.ihe.net/ITI/PMIR/ITI-93.html), con un token emitido por el Authorization Server de la comunidad. Es la única que crea, actualiza, fusiona o desactiva identidades maestras.

### Transacciones propias de HIX

**Custodian Token Exchange [HIX-1].** El Record Locator Service presenta al Authorization Server el token del solicitante y un único destino, y recibe un token acotado a ese destino, con el solicitante como sujeto y el Record Locator Service como actor. El destino es un custodio o un actor central. Es un intercambio OAuth 2.0 Token Exchange ([RFC 8693](https://www.rfc-editor.org/rfc/rfc8693)) con resource indicator ([RFC 8707](https://www.rfc-editor.org/rfc/rfc8707)), restringido al mediador. No es una transacción IUA. IUA limita [ITI-71](https://profiles.ihe.net/ITI/IUA/index.html#371-get-access-token-iti-71) a los grants Authorization Code y Client Credentials ([IUA, §34.1.1.1](https://profiles.ihe.net/ITI/IUA/index.html#34111-authorization-client))[^iua-grants] y toma de RFC 8693 solo el parámetro con el que se pide el tipo de token.

**Patient Application Launch [HIX-2].** Una aplicación elegida por una persona obtiene del Authorization Server un token destinado al Record Locator Service cuyo contexto de paciente es la identidad maestra de esa persona. El Authorization Server resuelve esa identidad en el momento del consentimiento. El flujo se basa en [SMART App Launch](https://build.fhir.org/ig/HL7/smart-app-launch/) y se especifica en el Volumen 2.

> **Nota.** La incorporación de un miembro, por la que una organización queda descrita en el directorio y reconocida por el Authorization Server, es un procedimiento administrativo y no una transacción. Se describe en la sección 2.7.

### Referencias

Las citas reproducen el texto publicado por su fuente. Los recortes se marcan con "[...]" y la negrita es de esta guía.

[^rfc9700-aud]: [RFC 9700, §2.3 Access Token Privilege Restriction](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.3): "In particular, **access tokens SHOULD be audience-restricted to a specific resource server** or, if that is not feasible, to a small set of resource servers." [§4.10.2 Audience-Restricted Access Tokens](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.10.2): "The authorization server associates the access token with the particular resource server, and **the resource server is then supposed to verify the intended audience**. If the access token fails the intended audience validation, **the resource server refuses to serve the respective request**."
[^pou]: [v3-ActReason, TREAT](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-TREAT): "treatment. **To perform one or more operations on information for provision of health care.**" [ETREAT](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-ETREAT): "Emergency Treatment. To perform one or more operations on information for provision of **immediately needed health care for an emergent condition**." [PATRQT](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-PATRQT): "patient requested. To perform one or more operations on information **in response to a patient's request**." [FAMRQT](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-FAMRQT): "family requested. To perform one or more operations on information in response to a request by **a family member authorized by the patient**." [PWATRNY](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-PWATRNY): "power of attorney. To perform one or more operations on information in response to a request by **a person appointed as the patient's legal representative**."
[^rfc8693-act]: [RFC 8693, §1.1 Delegation vs. Impersonation Semantics](https://www.rfc-editor.org/rfc/rfc8693.html#section-1.1): "With delegation semantics, principal A still has its own identity separate from B, and it is explicitly understood that while B may have delegated some of its rights to A, **any actions taken are being taken by A representing B**." [§2.1 Request](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.1): "resource. OPTIONAL. **A URI that indicates the target service or resource where the client intends to use the requested security token.**" [§4.1 "act" (Actor) Claim](https://www.rfc-editor.org/rfc/rfc8693.html#section-4.1): "The act (actor) claim provides a means within a JWT to express that **delegation has occurred and identify the acting party to whom authority has been delegated**."
[^iua-grants]: [IUA, §34.1.1.1 Authorization Client](https://profiles.ihe.net/ITI/IUA/index.html#34111-authorization-client): "The Get Access Token [ITI-71] transaction **is scoped to the Authorization Code and Client Credential grant types** (see ITI TF-1: 34.4.1.1 Authorization Grant Types)." [§3.71.4.1.2.1 Client Credential grant type](https://profiles.ihe.net/ITI/IUA/index.html#3714121-client-credential-grant-type): "requested_token_type (optional): The requested token format shall be urn:ietf:params:oauth:token-type:jwt, urn:ietf:params:oauth:token-type:saml2 or urn:ietf:params:oauth:token-type:access-token [**RFC 8693 OAuth 2.0 Token Exchange**, Section 3]."
