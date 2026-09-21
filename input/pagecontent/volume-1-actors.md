Esta sección define los actores de HIX y las transacciones que los vinculan. Los actores y transacciones tomados de un perfil IHE conservan el significado que les da su especificación de origen. Las transacciones identificadas como `HIX-n` son propias de esta guía y se especifican en el Volumen 2.

HIX distingue tres clases de actor. Los **actores centrales** los opera la comunidad. Los **actores de miembro** los opera cada organización participante. La **fuente autoritativa de identidad** es externa a la comunidad. Un miembro solo trata con la infraestructura central, nunca con otro miembro. Obtiene sus tokens del Authorization Server, localiza y recupera a través del Record Locator Service, y publica y declara identidades ante la infraestructura central, que valida esas transacciones como describe la [sección 2.1](volume-1-concepts.html).

Las tres pestañas siguientes muestran a los actores de miembro en su escenario típico. La aplicación del paciente es la de una persona que entra a su propio expediente. El hospital es un sistema que consume documentos, en atención normal y en una emergencia, donde por ejemplo busca al paciente por sus datos demográficos con PDQm. El laboratorio es un sistema que publica y custodia documentos.
{: #figuras-2-2}

El propósito de uso no depende del actor sino del caso de uso. Es un código del conjunto [PurposeOfUse](https://terminology.hl7.org/ValueSet-v3-PurposeOfUse.html) de HL7, tomado del sistema [v3-ActReason](https://terminology.hl7.org/CodeSystem-v3-ActReason.html), que el Authorization Server incluye en el token de cada solicitante y que la decisión de divulgación evalúa. No decide qué transacciones puede pedir un solicitante. Eso lo fija el scope de su token. Un mismo hospital consulta con `TREAT` en la atención habitual y con `ETREAT` en una urgencia. HIX usa el conjunto completo de HL7 y no lo restringe. Qué propósitos acepta una comunidad, y con qué condiciones, es política de implementación. La [Tabla 2.2-3](volume-1-actors.html#tabla-2-2-3) solo orienta al lector con los más frecuentes y el caso en el que aparece cada uno[^pou].

> **TODO.** Estos 3 diagramas son un MOCK en pantUML y se DEBEN pasar los tres diagramas de estas pestañas a draw.io, como la [Figura 2-1](volume-1.html#figura-2-1).

<ul class="nav nav-tabs" role="tablist">
  <li class="active"><a href="#tab-actores-paciente" data-toggle="tab">Aplicación del paciente</a></li>
  <li><a href="#tab-actores-hospital" data-toggle="tab">Hospital que consulta</a></li>
  <li><a href="#tab-actores-laboratorio" data-toggle="tab">Laboratorio que publica</a></li>
</ul>

<div class="tab-content">

<div id="tab-actores-paciente" class="tab-pane active" markdown="1">

![Aplicación del paciente ante la comunidad](hix-actores-paciente.svg)

**Figura 2.2-1:** Aplicación del paciente ante la comunidad
{: #figura-2-2-1}

</div>

<div id="tab-actores-hospital" class="tab-pane" markdown="1">

![Hospital que consulta, en atención normal y en emergencia](hix-actores-hospital.svg)

**Figura 2.2-2:** Hospital que consulta, en atención normal y en emergencia (ETREAT con PDQm)
{: #figura-2-2-2}

</div>

<div id="tab-actores-laboratorio" class="tab-pane" markdown="1">

![Laboratorio que publica documentos](hix-actores-laboratorio.svg)

**Figura 2.2-3:** Laboratorio que publica documentos
{: #figura-2-2-3}

</div>

</div>

Las dos tablas siguientes listan las transacciones que definen a cada actor. R significa que la transacción es requerida para declararse conforme con el actor, y O que es opcional. La columna Referencia indica el perfil IHE que define la transacción, o el Volumen 2 de esta guía para las propias de HIX. Los miembros, y los actores centrales ante los que presentan tokens, se agrupan además con IUA, y todos los actores salvo la aplicación del paciente con ATNA y CT. Esas agrupaciones, y las transacciones que traen consigo, se describen en la [sección 2.4](volume-1-groupings.html).

**Tabla 2.2-1:** Actores de miembro
{: #tabla-2-2-1}

| Actor | Transacción | Opcionalidad | Referencia |
| --- | --- | --- | --- |
| Sistema que publica y custodia documentos | Patient Identity Feed FHIR [ITI-104] | R | PIXm |
| | Provide Document Bundle [ITI-65] | R | MHD |
| | Retrieve Document [ITI-68] | R (nota 1) | MHD |
| Sistema que consume documentos | Find Document Lists [ITI-66] | R | MHD |
| | Find Document References [ITI-67] | R | MHD |
| | Retrieve Document [ITI-68] | R | MHD |
| | Mobile Patient Identifier Cross-reference Query [ITI-83] | O | PIXm |
| | Mobile Patient Demographics Query [ITI-78] | O (nota 2) | PDQm |
| | Patient Demographics Match [ITI-119] | O (nota 4) | PDQm |
| Aplicación del paciente | Patient Application Launch \[[HIX-2](volume-1-actors.html#hix-2)\] | R | Vol. 2 |
| | Find Document Lists [ITI-66] | R | MHD |
| | Find Document References [ITI-67] | R | MHD |
| | Retrieve Document [ITI-68] | R | MHD |
{: .table .table-bordered}

**Tabla 2.2-2:** Actores centrales y fuente de identidad
{: #tabla-2-2-2}

| Actor | Transacción | Opcionalidad | Referencia |
| --- | --- | --- | --- |
| Record Locator Service | Find Document Lists [ITI-66] | R | MHD |
| | Find Document References [ITI-67] | R | MHD |
| | Retrieve Document [ITI-68] | R | MHD |
| | Mobile Patient Identifier Cross-reference Query [ITI-83] | R | PIXm |
| | Find Matching Care Services [ITI-90] | R | mCSD |
| | Custodian Token Exchange \[[HIX-1](volume-1-actors.html#hix-1)\] | R | Vol. 2 |
| Document Registry | Provide Document Bundle [ITI-65] | R | MHD |
| | Find Document Lists [ITI-66] | R | MHD |
| | Find Document References [ITI-67] | R | MHD |
| | Retrieve Document [ITI-68] | R (nota 3) | MHD |
| | Mobile Patient Identifier Cross-reference Query [ITI-83] | R | PIXm |
| | Find Matching Care Services [ITI-90] | R | mCSD |
| | Mobile Patient Identity Feed [ITI-93] | R | PMIR |
| Authorization Server | Get Access Token [ITI-71] | R | IUA |
| | Introspect Token [ITI-102] | R | IUA |
| | Get Authorization Server Metadata [ITI-103] | R | IUA |
| | Custodian Token Exchange \[[HIX-1](volume-1-actors.html#hix-1)\] | R | Vol. 2 |
| | Patient Application Launch \[[HIX-2](volume-1-actors.html#hix-2)\] | R | Vol. 2 |
| | Mobile Patient Identifier Cross-reference Query [ITI-83] | R | PIXm |
| Directorio de la comunidad | Find Matching Care Services [ITI-90] | R | mCSD |
| Registro de identidad maestra | Mobile Patient Identity Feed [ITI-93] | R | PMIR |
| | Patient Identity Feed FHIR [ITI-104] | R | PIXm |
| | Mobile Patient Identifier Cross-reference Query [ITI-83] | R | PIXm |
| | Mobile Patient Demographics Query [ITI-78] | R | PDQm |
| | Patient Demographics Match [ITI-119] | R | PDQm |
| Audit Record Repository | Record Audit Event [ITI-20] | R | ATNA |
| Fuente autoritativa de identidad (externa) | Mobile Patient Identity Feed [ITI-93] | R | PMIR |
{: .table .table-bordered}

Notas:

1. No requerido si el custodio declara la Opción de Almacenamiento Central.
2. Requerido si el actor declara la Opción de Demografía.
3. La exige el Document Responder de MHD. El Document Registry solo tiene contenido que servir cuando declara la Opción de Almacenamiento Central.
4. Requerido si el actor declara la Opción de Coincidencia Demográfica.

**Tabla 2.2-3:** Propósitos de uso más frecuentes en HIX
{: #tabla-2-2-3}

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

Las descripciones siguen el orden de las tablas. Dos reglas valen para todos los actores y no se repiten en cada uno. Todo actor que recibe un token **SHALL** comprobar que está destinado a él y **SHALL** rechazar la solicitud si no lo está, como recomienda RFC 9700 para todo [Resource Server](appendix-glossary.html#resource-server) ([RFC 9700, §4.10.2](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.10.2))[^rfc9700-aud]. Que el Authorization Server de la comunidad haya emitido un token no lo hace válido ante cualquier actor. Cada token nombra en su audiencia, el claim `aud`, a los actores ante los que vale, y ante cualquier otro no sirve, aunque lo haya emitido el mismo Authorization Server. Y todo sistema de un miembro y todo actor central registra sus propios eventos de auditoría, como exige la agrupación con ATNA de la [sección 2.4](volume-1-groupings.html).

#### Sistema que publica y custodia documentos

El custodio es el miembro que produce documentos. Los conserva, declara las identidades locales de sus pacientes y publica los punteros a sus documentos con el propósito de uso del caso, normalmente `TREAT`. Agrupa a un [Document Source](appendix-glossary.html#document-source) y un [Document Responder](appendix-glossary.html#document-responder) de MHD, y a un [Patient Identity Source](appendix-glossary.html#patient-identity-source) de PIXm. Responde las recuperaciones que le llegan desde la infraestructura central, y solo desde ella.

El custodio **SHALL** declarar mediante [ITI-104](https://profiles.ihe.net/ITI/PIXm/ITI-104.html) la identidad local de todo paciente sobre el que publique, en su propio dominio de identificadores y con el identificador nacional de la persona. **SHALL** publicar mediante [ITI-65](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-65.html) punteros que lo nombren a él como custodio y lleven etiqueta de confidencialidad, con URL de contenido relativa cuando el contenido queda en él.

El custodio **SHALL** conservar el contenido y responder [ITI-68](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-68.html), salvo que declare la Opción de Almacenamiento Central. **SHALL** validar localmente el token de cada solicitud con las claves que publica el Authorization Server, conforme a la [sección 2.6](volume-1-security.html). **SHALL** rechazar toda solicitud cuyo token no haya sido intercambiado por el Record Locator Service y **SHALL NOT** atender recuperaciones originadas directamente en otro miembro.

#### Sistema que consume documentos

El consumidor es el miembro que consulta el expediente de un paciente. Localiza y recupera documentos a través del Record Locator Service y agrupa a un [Document Consumer](appendix-glossary.html#document-consumer) de MHD. Desde su punto de vista la comunidad es un único servidor FHIR. Actúa con el propósito de uso `TREAT` en la atención habitual y con `ETREAT` cuando atiende una urgencia.

El consumidor **SHALL** obtener un token del Authorization Server destinado al Record Locator Service y **SHALL** presentarlo en toda solicitud. **SHALL** recuperar los documentos únicamente a través de las URL que el Record Locator Service le entrega. Puede resolver la identidad de un paciente con [ITI-83](https://profiles.ihe.net/ITI/PIXm/ITI-83.html) y, si declara la Opción de Demografía, buscarlo por sus datos demográficos con [ITI-78](https://profiles.ihe.net/ITI/PDQm/ITI-78.html). Si declara la Opción de Coincidencia Demográfica, puede pedir además con [ITI-119](https://profiles.ihe.net/ITI/PDQm/ITI-119.html) las identidades que más se parecen a unos datos incompletos. Ambas sirven, por ejemplo, en una urgencia en la que no tiene un identificador fiable, como en la [Figura 2.2-2](volume-1-actors.html#figuras-2-2).

#### Aplicación del paciente

La aplicación del paciente accede al expediente de la persona que la usa, con el contexto de paciente que el Authorization Server fija durante el lanzamiento y el propósito de uso que corresponde a quien actúa, según la [Tabla 2.2-3](volume-1-actors.html#tabla-2-2-3). Agrupa a un Document Consumer de MHD. A partir del lanzamiento, sus consultas y recuperaciones son las de cualquier otro consumidor, confinadas a ese único paciente.

Este actor **SHALL** obtener su token mediante [HIX-2](volume-1-actors.html#hix-2) y **SHALL NOT** solicitar ni asumir un contexto de paciente distinto del que el token declara.

#### Record Locator Service

El Record Locator Service es el mediador de la comunidad. Localiza y recupera documentos en nombre de los miembros y aplica la decisión de divulgación sobre los punteros, antes de mover contenido alguno. Ante los miembros se comporta como un Resource Server de IUA y un Document Responder de MHD. Ante los custodios y los demás actores centrales actúa como Document Consumer de MHD y cliente delegado, en nombre del solicitante original.

El Record Locator Service **SHALL** aceptar únicamente tokens emitidos por el Authorization Server de la comunidad. **SHALL** comprobarlos mediante [ITI-102](https://profiles.ihe.net/ITI/IUA/index.html#3102-introspect-token-iti-102) una vez por operación y **SHALL** tomar de esa respuesta, y no de la solicitud, la organización, el propósito de uso y el contexto de paciente del solicitante.

El Record Locator Service **SHALL** evaluar la decisión de divulgación sobre los punteros antes de originar cualquier recuperación, **SHALL** omitir de la respuesta los punteros cuya divulgación no esté permitida y **SHALL** volver a evaluarla al atender un [ITI-68](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-68.html). La omisión **SHALL NOT** ser distinguible, para el solicitante, de la ausencia del documento, y **SHALL** quedar registrada en la auditoría. **SHALL** aplicar la misma decisión a las listas que devuelve por [ITI-66](https://profiles.ihe.net/ITI/MHD/5.0.0/ITI-66.html), porque una lista revela qué documentos existen. Un puntero cuya divulgación se niega **SHALL NOT** originar consulta al directorio, intercambio de token ni llamada al custodio.

El Record Locator Service **SHALL** entregar a los solicitantes URL de contenido que apunten a sí mismo. **SHALL** resolver el endpoint del custodio en el directorio de la comunidad en cada recuperación y **SHALL NOT** revelar ese endpoint al solicitante.

El Record Locator Service **SHALL** obtener mediante [HIX-1](volume-1-actors.html#hix-1) un token distinto para cada destino que alcance, sea un custodio o un actor central, **SHALL** pedir en cada intercambio únicamente el alcance de la transacción que va a realizar, y **SHALL NOT** reenviar a ninguno el token del solicitante. **SHALL NOT** conservar copias de los documentos que transitan por él ni registrar su contenido. No tiene acceso propio al Document Registry ni al registro de identidad maestra.

Cuando un custodio no responde, el Record Locator Service **SHALL** degradar la respuesta señalando el fallo y **SHALL NOT** hacer fallar la operación completa por ese motivo.

> **Nota.** *Record Locator Service* es el nombre que esta guía da al actor. No es vocabulario IHE. Corresponde al localizador central del modelo Centralized Discovery and Retrieve de IHE, el que permite descubrir dónde están los documentos y recuperarlos del custodio que registró su existencia ([IHE HIE Whitepaper, §2.8](https://profiles.ihe.net/ITI/HIE-Whitepaper/index.html#28-document-sharing-models))[^hie-cdr]. En HIX media además la recuperación, y se implementa agrupando un Document Consumer y un Document Responder de MHD.

#### Document Registry

El [Document Registry](appendix-glossary.html#document-registry) es el registro de documentos de la comunidad. Toma su nombre y su función del Document Registry de MHDS, pero es un actor de HIX, definido por los actores que agrupa en la [sección 2.4](volume-1-groupings.html). Conserva los punteros a los documentos publicados y, bajo la Opción de Almacenamiento Central, el contenido que los custodios le entregan. Recibe por [ITI-93](https://profiles.ihe.net/ITI/PMIR/ITI-93.html) los cambios de las identidades maestras.

El Document Registry **SHALL** registrar cada puntero a nombre de la organización que declara el token, **SHALL** rechazar la publicación cuyo custodio no coincida con ella y **SHALL** validar mediante [ITI-90](https://profiles.ihe.net/ITI/mCSD/ITI-90.html) que esa organización es un miembro activo de la comunidad. **SHALL** aplicar a los punteros y a las listas que conserva las fusiones de identidades maestras que recibe por ITI-93, de modo que ningún puntero quede asociado a una identidad que dejó de existir.

El Document Registry **SHALL** registrar únicamente punteros cuyo `subject` sea la identidad maestra del paciente y que conserven en `sourcepatient` la identidad local con la que el custodio lo nombró. Cuando la publicación nombra al paciente solo con su identidad local, la infraestructura central **SHALL** resolverla mediante [ITI-83](https://profiles.ihe.net/ITI/PIXm/ITI-83.html) y escribir el resultado en `subject` al indexar. Esa consulta comprueba a la vez que la persona existe y está activa en la comunidad, porque PIXm no resuelve una identidad desactivada o eliminada ([PIXm, §2:3.83.4.2.2.5](https://profiles.ihe.net/ITI/PIXm/ITI-83.html#23834225-post-mergedelete))[^pixm-deprecated]. Es la misma comprobación que MHDS pide a su Document Registry antes de indexar, y que admite resolver preguntando al registro de identidad ([MHDS Vol. 1, §1:50.1.1.1.1](https://profiles.ihe.net/ITI/MHDS/volume-1.html#1501111-when-the-grouped-mhd-document-recipient--is-triggered))[^mhds-subject]. Así el miembro publica con sus propios identificadores y la comunidad traduce y valida por él. El Document Registry **SHALL** rechazar la publicación que carezca de etiqueta de confidencialidad o cuyo paciente no pueda resolverse a una identidad maestra. Cuando el contenido queda en el custodio, **SHALL** rechazar además la publicación cuya URL de contenido no sea relativa.

#### Authorization Server

El Authorization Server emite, comprueba e intercambia los tokens que circulan por la comunidad. Es el Authorization Server de IUA. Es el único actor que decide sobre la autorización y el único que conoce a la vez al solicitante, su organización y el alcance que se le concede. No decide sobre consentimiento, relación terapéutica ni identidad de paciente.

El Authorization Server **SHALL** restringir la audiencia de todo token que emite a destinatarios identificados explícitamente, como recomienda RFC 9700 ([RFC 9700, §2.3](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.3))[^rfc9700-aud]. El token del solicitante nombra a los actores centrales que el miembro alcanza directamente y el token intercambiado a un único destino, como fija la [sección 2.6](volume-1-security.html#modelo-de-confianza). **SHALL** atender [HIX-1](volume-1-actors.html#hix-1) únicamente para el Record Locator Service. El token intercambiado **SHALL** llevar como audiencia el único destino indicado en la petición de intercambio, el mismo sujeto, las mismas extensiones de IUA y, si lo hay, el mismo contexto de paciente que el token presentado, y como actor al Record Locator Service, en el claim `act` con el que OAuth 2.0 Token Exchange expresa la delegación ([RFC 8693, §4.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-4.1))[^rfc8693-act]. Su alcance **SHALL** ser el pedido en el intercambio y **SHALL NOT** exceder el del token del solicitante ni el de la delegación registrada, y su vida **SHALL NOT** superar los dos minutos ni la vida restante del token del solicitante. El Authorization Server **SHALL NOT** emitir por ningún otro camino un token cuya audiencia sea un custodio.

El Authorization Server **SHALL** fijar la organización y el propósito de uso del solicitante desde su propio registro y **SHALL NOT** aceptarlos de la solicitud. Cuando una persona se autentica, **SHALL** resolver su identidad verificada a la identidad maestra mediante [ITI-83](https://profiles.ihe.net/ITI/PIXm/ITI-83.html) y **SHALL** fijar ese resultado como contexto de paciente del token, conforme a [HIX-2](volume-1-actors.html#hix-2). **SHALL NOT** emitir un token con contexto de paciente cuando esa identidad no resuelva a una identidad maestra.

#### Directorio de la comunidad

El directorio publica las organizaciones participantes, su pertenencia a la comunidad y los endpoints en los que responden. Es el [Directory](appendix-glossary.html#directory) de mCSD de la comunidad y la única fuente de la que la infraestructura central aprende a quién dirigir una recuperación.

El directorio **SHALL** responder [ITI-90](https://profiles.ihe.net/ITI/mCSD/ITI-90.html) y **SHALL** ser el único origen de los endpoints que usa la infraestructura central. **SHALL** identificar a cada organización con el mismo identificador que el Authorization Server incluye en sus tokens. Los miembros no consultan el directorio. Su contenido se mantiene administrativamente, al incorporar un miembro.

#### Registro de identidad maestra

El registro de identidad maestra agrupa al [Patient Identity Registry](appendix-glossary.html#patient-identity-registry) de PMIR, al [Patient Identifier Cross-reference Manager](appendix-glossary.html#patient-identifier-cross-reference-manager) de PIXm y al [Patient Demographics Supplier](appendix-glossary.html#patient-demographics-supplier) de PDQm. Conserva una identidad maestra por persona, creada por la fuente autoritativa de identidad, y los enlaces con las identidades locales que los miembros declaran.

El registro de identidad maestra **SHALL** crear identidades maestras únicamente a partir de [ITI-93](https://profiles.ihe.net/ITI/PMIR/ITI-93.html) recibido de la fuente autoritativa de identidad. **SHALL** aceptar [ITI-104](https://profiles.ihe.net/ITI/PIXm/ITI-104.html) únicamente en el dominio de identificadores del miembro que lo origina y **SHALL** rechazar la declaración que no pueda vincularse a una identidad maestra existente. Dentro de su propio dominio el miembro gestiona sus identidades locales con libertad, incluida la resolución de sus propios duplicados que define ITI-104. 

Una declaración de un miembro **SHALL NOT** crear, fusionar ni eliminar una identidad maestra. El registro **SHALL NOT** modificar la demografía de la identidad maestra a partir de lo que un miembro declara. **SHALL** responder [ITI-83](https://profiles.ihe.net/ITI/PIXm/ITI-83.html) únicamente con la identidad maestra, nunca con las identidades locales que otros miembros declararon. PIXm admite esa restricción, porque deja que la respuesta sea un subconjunto determinado por política ([PIXm, §2:3.83.4.1.3](https://profiles.ihe.net/ITI/PIXm/ITI-83.html#2383413-expected-actions))[^pixm-subset].

#### Audit Record Repository

El Audit Record Repository es el actor de ATNA que recibe mediante [ITI-20](https://profiles.ihe.net/ITI/TF/Volume2/ITI-20.html) los eventos que registran los actores centrales. Existe para que una divulgación pueda reconstruirse completa desde el lado de la comunidad, con la solicitud del miembro y la recuperación ante el custodio bajo un mismo identificador de correlación. Cada miembro registra su propio lado en su propio registro, como ATNA exige a todo Secure Node o Secure Application.

#### Fuente autoritativa de identidad

La fuente autoritativa de identidad es el sistema, externo a la comunidad, contra el que se verifica la identidad de una persona y del que la comunidad obtiene sus identidades maestras. Es el Patient Identity Source de PMIR. HIX no designa cuál es. La propuesta para Costa Rica es que sea el EDUS, porque ya tiene resuelta la identificación de las personas.

La fuente autoritativa **SHALL** alimentar el registro de identidad maestra mediante [ITI-93](https://profiles.ihe.net/ITI/PMIR/ITI-93.html), con un token emitido por el Authorization Server de la comunidad. Es la única que crea, actualiza, fusiona o desactiva identidades maestras.

### Transacciones propias de HIX

**Custodian Token Exchange [HIX-1].** El Record Locator Service presenta al Authorization Server el token del solicitante, un único destino y el alcance de la transacción que va a realizar, y recibe a cambio el [token intercambiado](appendix-glossary.html#token-intercambiado) para ese destino, sea un custodio o un actor central. Lo que ese token lleva lo fijan los requisitos del [Authorization Server](volume-1-actors.html#authorization-server) y lo resume la [Tabla 2.6-1](volume-1-security.html#tabla-2-6-1). Es un intercambio OAuth 2.0 Token Exchange ([RFC 8693](https://www.rfc-editor.org/rfc/rfc8693)) con resource indicator ([RFC 8707](https://www.rfc-editor.org/rfc/rfc8707)), restringido al mediador. No es una transacción IUA. IUA limita [ITI-71](https://profiles.ihe.net/ITI/IUA/index.html#371-get-access-token-iti-71) a los grants Authorization Code y Client Credentials ([IUA, §34.1.1.1](https://profiles.ihe.net/ITI/IUA/index.html#34111-authorization-client))[^iua-grants] y toma de RFC 8693 solo el parámetro con el que se pide el tipo de token.
{: #hix-1}

**Patient Application Launch [HIX-2].** Una aplicación elegida por una persona obtiene del Authorization Server un token destinado al Record Locator Service cuyo contexto de paciente es la identidad maestra de esa persona. El Authorization Server resuelve esa identidad en el momento del consentimiento. Es la transacción [Get Access Token \[ITI-71\]](https://profiles.ihe.net/ITI/IUA/index.html#371-get-access-token-iti-71) de IUA con el grant Authorization Code, perfilada por [SMART App Launch](https://hl7.org/fhir/smart-app-launch/). HIX le da identificador propio por lo que añade, que es el contexto de paciente que fija el Authorization Server, y no porque sea ajena a IUA. Se especifica en el Volumen 2.
{: #hix-2}

> **Nota.** La incorporación de un miembro, por la que una organización queda descrita en el directorio y reconocida por el Authorization Server, es un procedimiento administrativo y no una transacción.

### Referencias

Las citas reproducen el texto publicado por su fuente. Los recortes se marcan con "[...]" y la negrita es de esta guía.

[^rfc9700-aud]: [RFC 9700, §2.3 Access Token Privilege Restriction](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.3): "In particular, **access tokens SHOULD be audience-restricted to a specific resource server** or, if that is not feasible, to a small set of resource servers." [§4.10.2 Audience-Restricted Access Tokens](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.10.2): "The authorization server associates the access token with the particular resource server, and **the resource server is then supposed to verify the intended audience**. If the access token fails the intended audience validation, **the resource server refuses to serve the respective request**."
[^pou]: [v3-ActReason, TREAT](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-TREAT): "treatment. **To perform one or more operations on information for provision of health care.**" [ETREAT](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-ETREAT): "Emergency Treatment. To perform one or more operations on information for provision of **immediately needed health care for an emergent condition**." [PATRQT](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-PATRQT): "patient requested. To perform one or more operations on information **in response to a patient's request**." [FAMRQT](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-FAMRQT): "family requested. To perform one or more operations on information in response to a request by **a family member authorized by the patient**." [PWATRNY](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-PWATRNY): "power of attorney. To perform one or more operations on information in response to a request by **a person appointed as the patient's legal representative**."
[^rfc8693-act]: [RFC 8693, §1.1 Delegation vs. Impersonation Semantics](https://www.rfc-editor.org/rfc/rfc8693.html#section-1.1): "With delegation semantics, principal A still has its own identity separate from B, and it is explicitly understood that while B may have delegated some of its rights to A, **any actions taken are being taken by A representing B**." [§2.1 Request](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.1): "resource. OPTIONAL. **A URI that indicates the target service or resource where the client intends to use the requested security token.**" [§4.1 "act" (Actor) Claim](https://www.rfc-editor.org/rfc/rfc8693.html#section-4.1): "The act (actor) claim provides a means within a JWT to express that **delegation has occurred and identify the acting party to whom authority has been delegated**."
[^mhds-subject]: [MHDS Vol. 1, §1:50.1.1.1.1 When the grouped MHD Document Recipient is triggered](https://profiles.ihe.net/ITI/MHDS/volume-1.html#1501111-when-the-grouped-mhd-document-recipient--is-triggered): "The Document Registry SHALL validate that the subject of the DocumentReference, and List Resources is the same Patient, and that **Patient is a recognized and active Patient within the Community**. The Patient identity must be recognized and active by the PMIR Patient Identity Registry in the document sharing community. **This may be accomplished by a query of the PMIR Patient Identity Registry**, by way of a cached internal patient database, or other means."
[^iua-grants]: [IUA, §34.1.1.1 Authorization Client](https://profiles.ihe.net/ITI/IUA/index.html#34111-authorization-client): "The Get Access Token [ITI-71] transaction **is scoped to the Authorization Code and Client Credential grant types** (see ITI TF-1: 34.4.1.1 Authorization Grant Types)." [§3.71.4.1.2.1 Client Credential grant type](https://profiles.ihe.net/ITI/IUA/index.html#3714121-client-credential-grant-type): "requested_token_type (optional): The requested token format shall be urn:ietf:params:oauth:token-type:jwt, urn:ietf:params:oauth:token-type:saml2 or urn:ietf:params:oauth:token-type:access-token [**RFC 8693 OAuth 2.0 Token Exchange**, Section 3]."
[^pixm-subset]: [PIXm, §2:3.83.4.1.3 Expected Actions](https://profiles.ihe.net/ITI/PIXm/ITI-83.html#2383413-expected-actions): "**The Patient Identifiers returned may be a subset based on policies that might restrict access to some Patient Identifiers.** For guidance on handling Access Denied, see ITI TF-2: Appendix Z.7."
[^pixm-deprecated]: [PIXm, §2:3.83.4.2.2.5 Post Merge/Delete](https://profiles.ihe.net/ITI/PIXm/ITI-83.html#23834225-post-mergedelete): "Based upon policy, **when the Patient is deprecated or deleted, the response message shall return: 200 OK, and return a Bundle with no patient resource, or 404 Not Found**"
[^hie-cdr]: [IHE HIE Whitepaper, §2.8 Document Sharing Models](https://profiles.ihe.net/ITI/HIE-Whitepaper/index.html#28-document-sharing-models): "**Centralized Discovery and Retrieve** – in this model, a centralized locator is used to discover the location of documents which enables a retrieval of the document from a custodian who has registered existence of the document with the centralized locator".

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
*[PCF]: Privacy Consent on FHIR, perfil IHE de consentimiento del paciente
