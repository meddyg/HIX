Esta sección describe el modelo de confianza de HIX, los controles que la arquitectura especifica y las decisiones que cada comunidad debe tomar por política. Sigue el orden de las consideraciones de seguridad de MHDS, es decir, políticas y gestión de riesgo, controles técnicos y aplicación al intercambio de documentos ([MHDS Vol. 1, §1:50.5](https://profiles.ihe.net/ITI/MHDS/volume-1.html#1505-mhds-security-considerations))[^mhds-security], e intercala el modelo de confianza de HIX, que MHDS no necesita porque no tiene mediador. Como IHE, esta guía resuelve problemas de interoperabilidad mediante estándares. No define políticas de privacidad ni de seguridad, gestión de riesgo, funcionalidad clínica, controles físicos ni controles generales de red ([MHDS Vol. 1, §1:50.5.1](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15051-policies-and-risk-management))[^mhds-policy]. Lo que sigue separa lo que queda en manos de la comunidad de lo que fija la arquitectura.

### Políticas y gestión de riesgo {#politicas-y-gestion-de-riesgo}

MHDS advierte que el marco de políticas de una comunidad debe definirse antes de construirla[^mhds-security]. Las secciones anteriores dejan a la política de la comunidad una serie de decisiones que aquí se reúnen.

- Qué organizaciones pueden ser miembros, quién lo certifica, bajo qué condiciones dejan de serlo y quién financia la infraestructura central. La [Tabla 2.1-2](volume-1-concepts.html#tabla-2-1-2) de compromisos de la arquitectura lo señala como el riesgo principal de la comunidad a largo plazo.
- Qué propósitos de uso se admiten, con qué condiciones y qué documentos alcanza cada uno, en particular qué permite `ETREAT` frente a `TREAT`, como indica la [Tabla 2.2-3](volume-1-actors.html#tabla-2-2-3).
- Qué política de divulgación aplica mientras el modelo de consentimiento no esté especificado, como señala la [sección 2.3](volume-1-options.html).
- Qué custodios pueden ejercer la Opción de Almacenamiento Central y quién lo decide.
- Cómo se verifica que los custodios etiquetan correctamente la confidencialidad de sus documentos.
- Cómo obtiene una persona la identidad verificada con la que se autentica ante el Authorization Server, como señala la [sección 2.5](volume-1-usecases.html).
- Si un familiar autorizado o un representante legal puede actuar en nombre de una persona, cómo se acredita esa relación y qué paciente queda como contexto de su token, como señala [HIX-2](volume-2-hix-2.html#peticion-de-autorizacion).
- Qué solicitantes pueden buscar pacientes por datos demográficos y qué identidades maestras se les revelan por esa vía, como exigen la Opción de Demografía y la Opción de Coincidencia Demográfica.
- Cuánto tiempo se conservan los registros de auditoría, quién puede consultarlos y qué ocurre con una operación cuando el Audit Record Repository no está disponible.
- Qué constituye un acceso de emergencia, cómo se admite, cómo lo indica el solicitante al pedir el token y qué consecuencias tiene invocarlo.
- Si el acceso de red a los custodios se cierra de modo que la vía mediada sea la única alcanzable, o si esa restricción es solo defensa en profundidad.
- Cómo se protegen y vigilan el Record Locator Service y las claves del Authorization Server, como señala la [sección 2.6.5](volume-1-security.html#riesgos-residuales).
- Qué vida máxima admite el Authorization Server para los tokens de los solicitantes, y si se exige a los custodios rechazar un `jti` que ya vieron.
- Cómo autoriza el Record Locator Service sus llamadas a los actores centrales desplegados como sistemas distintos, con HIX-1, con un token propio o de otra forma que cumpla la [sección 2.2](volume-1-actors.html#record-locator-service), sabiendo que con un token propio un mediador comprometido alcanza lo que ese token permite sin un solicitante, como señala la [sección 2.6.5](volume-1-security.html#riesgos-residuales).
- Si se admite la introspección en el custodio, con la dependencia del Authorization Server en cada recuperación que conlleva, como señala la [sección 2.6.2](volume-1-security.html#validacion-en-el-custodio).

### Modelo de confianza {#modelo-de-confianza}

El límite de confianza pasa entre cada miembro y la infraestructura central, como establece la [sección 2.1](volume-1-concepts.html). Una recuperación cruza ese límite dos veces, del solicitante a la comunidad y de la comunidad al custodio, y cada cruce lleva un token de un régimen distinto. El primero es el token que el solicitante obtiene del Authorization Server, destinado a los Resource Servers centrales, que el Record Locator Service comprueba por introspección. El segundo es el [token mediado](appendix-glossary.html#token-mediado) que el Record Locator Service obtiene con [HIX-1](volume-2-hix-1.html) para cada custodio y cada actor central desplegado como un sistema distinto que alcanza, y que el destino valida por sí mismo. Hacia un actor central, la comunidad puede autorizar en su lugar un token propio del Record Locator Service, como fija la [sección 2.2](volume-1-actors.html#record-locator-service). La [Tabla 2.6-1](volume-1-security.html#tabla-2-6-1) los compara.

**Tabla 2.6-1:** Los dos regímenes de token
{: #tabla-2-6-1}

| | Token del solicitante | Token mediado |
| --- | --- | --- |
| Quién lo obtiene | El miembro con ITI-71, o la aplicación del paciente con [HIX-2](volume-2-hix-2.html) | El Record Locator Service con [HIX-1](volume-2-hix-1.html) |
| Audiencia | Los Resource Servers centrales que define la comunidad, o solo el Record Locator Service si lo obtiene la aplicación del paciente | Un único custodio, o los actores centrales que el Authorization Server asocia al `resource` del intercambio |
| Vida | La que fije el Authorization Server | Dos minutos como máximo, y nunca más que la vida restante del token del solicitante |
| Cómo se valida | El Record Locator Service, por introspección con ITI-102 una vez por operación. Otro Resource Server central, preferiblemente también por introspección, o por sí mismo con la JWT Token Option | En el destino, con las claves que publica el Authorization Server ([JWKs](https://www.rfc-editor.org/info/rfc7517/)), sin necesidad de introspección |
| Sujeto | El sistema del miembro, o la persona que lanzó la aplicación | El mismo |
| Extensiones de IUA | Del miembro, la organización y el propósito de uso. De la aplicación del paciente, el propósito de uso, y la organización si la aplicación tiene una registrada | Las mismas |
| Scope | El concedido al solicitante | Solo el de la transacción que motivó el intercambio |
| Contexto de paciente | Solo si lo obtuvo una aplicación del paciente | El mismo, en el claim `patient`, si lo hay |
| Actor | Ninguno | El Record Locator Service, en el claim `act` |
{: .table .table-bordered}

> **Nota.** El token propio que la [sección 2.2](volume-1-actors.html#record-locator-service) admite para las llamadas a los actores centrales es del primer régimen. El Record Locator Service lo obtiene con ITI-71, con ese actor como audiencia y solo las transacciones autorizadas como scope, nunca ITI-68, y el destino lo valida como el de cualquier solicitante. No nombra a ningún solicitante, y por eso cada llamada se registra bajo el identificador de correlación de la operación que la motivó.

El sujeto del token del solicitante es el sistema del miembro, porque el Authorization Server autentica a ese cliente y no a una persona, y en ese caso IUA pone como sujeto al cliente. La organización y el propósito de uso van en las extensiones que IUA define para el token ([IUA, §3.71.4.2.2.1](https://profiles.ihe.net/ITI/IUA/index.html#3714221-json-web-token-option))[^iua-sub]. Cuando el token lo obtiene una aplicación del paciente, el sujeto es la persona que la lanzó.

El token de un miembro no identifica a la persona que actúa dentro de su organización. IUA define extensiones para ello, como `subject_name` y `subject_role`, pero no define de dónde obtiene el Authorization Server esos datos ni con qué flujo, y HIX tampoco lo fija. Por eso la auditoría de la comunidad llega hasta la organización, y la del miembro, hasta la persona.

De la tabla se siguen cuatro reglas. De cada una conviene decir qué fija HIX, de qué depende y qué queda en manos de la comunidad.

**Un token mediado nunca vale ante dos custodios.** El formato no lo impone. El claim `aud` de un JWT admite una lista de audiencias ([RFC 7519, §4.1.3](https://www.rfc-editor.org/rfc/rfc7519.html#section-4.1.3))[^rfc7519-aud], y RFC 9068 recomienda rellenarlo con el recurso que el cliente indicó al pedir el token ([RFC 9068, §3](https://www.rfc-editor.org/rfc/rfc9068.html#section-3))[^rfc9068-aud]. HIX lo restringe cuando el destino es un custodio, porque de eso depende que un custodio no pueda reutilizarlo ante otro. Ante actores centrales, un mismo `resource` puede corresponder a varios Resource Servers, igual que en el token del miembro. El token de un miembro, en cambio, nombra en `aud` a los Resource Servers centrales que define la comunidad, y nunca a un custodio, y el de la aplicación del paciente nombra solo al Record Locator Service.

> **Nota.** Cómo pide cada cliente su token y qué Resource Servers quedan en su `aud` según el despliegue lo detallan [ITI-71](volume-2-authorization.html#iti-71) y [HIX-2](volume-2-hix-2.html#peticion-de-autorizacion) en el Volumen 2.

**El token del solicitante no sale de la infraestructura central.** El Record Locator Service no lo reenvía a ningún custodio ni actor central. Ante cada custodio presenta un token mediado para ese destino. Ante cada actor central desplegado como un sistema distinto presenta también uno, salvo que la comunidad autorice un token propio, como fija la [sección 2.2](volume-1-actors.html). Así el solicitante nunca tiene una credencial que valga ante un custodio, y un custodio nunca recibe una que valga ante otro.

**El custodio puede validar el token sin preguntar al Authorization Server.** Todo lo que necesita está en el token y en las claves que el Authorization Server publica. Esa publicación es su única dependencia, y la resuelve por adelantado, conservando las claves y renovándolas cuando aparece un identificador de clave que no conoce. La subsección siguiente detalla la validación y dice cuándo una comunidad puede añadirle la introspección.

**El Record Locator Service no accede por cuenta propia a ningún custodio ni al contenido.** No tiene credenciales permanentes hacia ningún custodio, ni hacia el Document Registry para ITI-68. Cada recuperación la hace a nombre de un solicitante, con el token mediado para ese destino, y así queda auditada. De esta forma el Record Locator Service no puede alcanzar documentos sin una petición de un solicitante que lo justifique, y una credencial suya comprometida no da acceso a ningún documento por sí sola. Hacia los demás actores centrales, la guía recomienda el token mediado y la comunidad puede autorizar un token propio, como fija la [sección 2.2](volume-1-actors.html#record-locator-service). El Document Registry, para sus consultas ITI-83 e ITI-90, y el Authorization Server, para su consulta ITI-83, usan un token propio que obtienen con el grant Client Credentials, como fija la [sección 2.2](volume-1-actors.html).

#### Validación en el custodio {#validacion-en-el-custodio}

El custodio recibe el token mediado y lo valida como RFC 9068 pide a todo Resource Server que recibe un access token en forma de JWT ([RFC 9068, §4](https://www.rfc-editor.org/rfc/rfc9068.html#section-4))[^rfc9068-validate]. Eso cubre la firma con las claves que publica el Authorization Server, el rechazo de un `alg` con valor `none`, que el emisor sea exactamente el Authorization Server de la comunidad, que el tipo de token sea `at+jwt`, que la audiencia lo contenga y que el token no haya expirado. HIX añade las comprobaciones siguientes, que el custodio **SHALL** hacer además.

1. Que el algoritmo de firma es uno de los que la comunidad admite.
2. Que la audiencia es exactamente él, y no solo que lo contenga, porque un token mediado para un custodio nunca nombra a otro.
3. Que el momento de emisión es coherente con la vida máxima de dos minutos.
4. Que lleva un sujeto y un identificador de token.
5. Que el cliente al que se emitió es el Record Locator Service.
6. Que el scope cubre la transacción que recibe.

El custodio **SHOULD** comprobar además que el actor declarado en el claim `act` es el Record Locator Service.

Las comprobaciones que más pesan son la audiencia y el cliente. La audiencia sola no basta, porque un token emitido directamente a otro cliente para esa misma audiencia la pasaría. El cliente es lo que vuelve estructural que solo el Record Locator Service pueda alcanzar a un custodio en nombre de alguien, porque el Authorization Server no emite por otro camino un token con esa audiencia. El claim `act` lo confirma, porque es la forma en que OAuth 2.0 Token Exchange declara que hubo delegación y quién actúa ([RFC 8693, §4.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-4.1))[^rfc8693-act].

El custodio **SHALL** validar el token mediado con las claves que publica el Authorization Server, y esa validación basta para aceptarlo. HIX no exige introspección en el custodio. El custodio **MAY** comprobarlo además por introspección, con la [Token Introspection Option](https://profiles.ihe.net/ITI/IUA/index.html#3424-token-introspection-option) de IUA y [ITI-102](https://profiles.ihe.net/ITI/IUA/index.html#3102-introspect-token-iti-102), si la comunidad lo admite. Entonces cada recuperación depende del Authorization Server en el momento de atenderla, y esa dependencia se asume a sabiendas.

#### Lo que un token prueba y lo que no {#lo-que-un-token-prueba-y-lo-que-no}

Un custodio que recibe un token mediado puede comprobar por sí mismo cinco cosas.

- Que lo emitió el Authorization Server de la comunidad.
- Que el Record Locator Service lo pidió en nombre de un solicitante concreto.
- Que vale ante él y ante nadie más.
- Que autoriza solo la transacción para la que se intercambió. El token del solicitante puede llevar varios scopes, pero el Record Locator Service pide en el intercambio únicamente el de la transacción que va a realizar, por ejemplo el de ITI-68 al recuperar. El scope es siempre el identificador de la transacción IHE, también en el token de la aplicación del paciente, como explica [HIX-2](volume-2-hix-2.html).
- Que expira en dos minutos como máximo.

El token no nombra ningún documento. Mientras dura, autoriza esa transacción ante ese custodio, sea cual sea el documento. Tampoco nombra al paciente, porque el token de un miembro no lleva ninguno, como explica la [sección 2.1](volume-1-concepts.html). La excepción es la aplicación del paciente. Su contexto de paciente, fijado con [HIX-2](volume-2-hix-2.html), se conserva en el intercambio. Quien confina las consultas a ese expediente es el Record Locator Service, como punto de aplicación de la política de la comunidad. El custodio **MAY** comprobar además ese contexto por su cuenta, resolviendo con [ITI-83](https://profiles.ihe.net/ITI/PIXm/ITI-83.html) la identidad maestra del paciente de cada documento.

Lo que el token sí aporta es el contexto con el que se decide, en las extensiones de IUA. Quién pide, para qué organización, con qué propósito de uso y, si lo hay, sobre qué paciente. Ese contexto acota lo que puede alcanzarse con el token, y con él se decide qué documento se entrega, en tres capas y en este orden.

1. La [decisión de divulgación](appendix-glossary.html#decision-de-divulgacion), que la infraestructura central aplica sobre los punteros antes de mover contenido.
2. La política local del custodio sobre su propio endpoint.
3. La auditoría, que no previene pero acota y detecta.

#### Contención de una credencial comprometida {#contencion-de-una-credencial-comprometida}

El Authorization Server **SHALL** revocar los tokens vigentes de un cliente al deshabilitarlo, de modo que la siguiente introspección los declare inactivos, que es el estado que RFC 7662 prevé para un token revocado ([RFC 7662, §2.2](https://www.rfc-editor.org/rfc/rfc7662.html#section-2.2))[^rfc7662-active], y ningún intercambio pueda partir de ellos. Un token mediado ya emitido no tiene ciclo de vida propio. El Record Locator Service lo usa una sola vez, en la transacción que lo motivó, y expira en dos minutos como máximo, así que una transacción ya en curso termina.

Lo que contiene una credencial comprometida es que los tokens obtenidos con ella dejen de valer, no que cambie la credencial. Si el Authorization Server los revoca también al rotar el secreto o la clave de un cliente es decisión de su implementación. Si no lo hace, hay que revocarlos aparte.

### Controles técnicos de seguridad y privacidad

HIX especifica los siguientes controles. Cada uno remite a la sección que lo fija.

- **Autenticación de sistemas.** Toda conexión entre dos participantes se autentica en ambos extremos con ATNA, como fija la [sección 2.4](volume-1-groupings.html), salvo la de la aplicación del paciente, que se autentica con su token de [HIX-2](volume-2-hix-2.html). Ningún participante acepta tráfico anónimo. Bajo la [Opción de Canal de Interconexión](volume-1-options.html#opcion-de-canal-de-interconexion), la autenticación mutua del tramo entre organizaciones la aporta la red de intercambio.
- **Autorización.** Toda transacción que inicia un miembro, y toda llamada que el Record Locator Service hace a un custodio o a un actor central, presenta un token emitido por el Authorization Server de la comunidad y destinado a quien la recibe, como fija la [sección 2.2](volume-1-actors.html).
- **Delegación acotada.** El token con el que la comunidad alcanza a un custodio se emite para ese único custodio y un solo tipo de transacción, a nombre del solicitante original y con el Record Locator Service como actor, como fija la [sección 2.2](volume-1-actors.html#authorization-server).
- **Mínimo privilegio.** El scope de un token mediado se limita a la transacción que motivó el intercambio, como fija la [sección 2.2](volume-1-actors.html#authorization-server). Poder localizar un documento nunca da poder para recuperarlo.
- **Confidencialidad en tránsito.** Todo tramo entre participantes viaja cifrado, incluido el que atraviesa un canal de interconexión bajo la Opción de Canal de Interconexión. El tramo entre un custodio y su propio servidor de seguridad es responsabilidad del custodio, como fija la [sección 2.3](volume-1-options.html).
- **Divulgación decidida sobre los punteros.** La política se evalúa en la infraestructura central, una vez por consulta, sobre los metadatos del índice y antes de que se mueva contenido, como fija la [sección 2.1](volume-1-concepts.html).
- **Auditoría en ambos extremos.** El miembro que solicita y la infraestructura central registran la localización. Infraestructura central y custodio registran la recuperación. Ningún tramo queda sin testigo.
- **Trazabilidad entre tramos.** Los registros de una misma divulgación comparten un identificador de correlación, de modo que la interacción completa pueda reconstruirse.
- **Identidad del paciente.** Solo la fuente autoritativa crea identidades maestras. Lo que un miembro declara vincula su identidad local con una de ellas, en su propio dominio, y queda registrado como una afirmación suya.

### Aplicación al intercambio de documentos

#### Seguridad básica {#seguridad-basica}

Todo actor de HIX, salvo la aplicación del paciente, es un Secure Node o Secure Application de ATNA y un Time Client de CT, como fija la [sección 2.4](volume-1-groupings.html). Los actores centrales registran sus eventos en el Audit Record Repository de la comunidad y cada miembro registra los de su lado, con el contenido que cada perfil define para su transacción a partir de los patrones de BALP.

El Record Locator Service **SHALL** registrar tanto la solicitud que recibe como cada recuperación que origina hacia un custodio, bajo un identificador de correlación que él mismo acuña y transmite al custodio, y **SHALL NOT** transmitir hacia el custodio ninguno que el solicitante proponga. Los registros de auditoría **SHALL NOT** contener un token completo ni contenido clínico. BALP pide atar cada evento a su token sin guardar el token ([BALP, §3:5.7.5](https://profiles.ihe.net/ITI/BALP/content.html#3575-oauth-security-token))[^balp-token], y su patrón Minimal lo hace con el `jti`, que guarda en `agent.policy` ([BALP, §3:5.7.5.4](https://profiles.ihe.net/ITI/BALP/content.html#35754-oauth-mapping-to-auditevent))[^balp-jti].

#### Protección según el tipo de documento {#proteccion-segun-el-tipo-de-documento}

La política de la comunidad determina qué solicitante alcanza qué documentos. MHDS lo plantea con una tabla de ejemplo que cruza el código de confidencialidad de cada documento con el rol del solicitante, y señala que ese rol y el propósito de uso llegan en el token de IUA ([MHDS Vol. 1, §1:50.5.3.2](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150532-protecting-different-types-of-documents))[^mhds-doctypes]. La arquitectura ofrece el punto donde aplicarla y los datos con los que evaluarla, es decir, quién solicita, en nombre de qué organización, con qué propósito, sobre qué paciente y con qué etiqueta de confidencialidad. La [Tabla 2.6-2](volume-1-security.html#tabla-2-6-2) es la versión de HIX de ese ejemplo, con el propósito de uso en lugar del rol porque es lo que el token de HIX lleva siempre. Es un ejemplo, no un requisito.

**Tabla 2.6-2:** Ejemplo de política de acceso por etiqueta de confidencialidad
{: #tabla-2-6-2}

| Etiqueta del documento | Solicitante | Resultado |
| --- | --- | --- |
| `N`, normal | Profesional de un miembro con propósito `TREAT` | Permitido |
| `N`, normal | La propia persona con propósito `PATRQT` | Permitido |
| `R`, restringido | Profesional de un miembro con propósito `TREAT` | Permitido con registro reforzado |
| `R`, restringido | La propia persona con propósito `PATRQT` | Según política de la comunidad |
| `V`, muy restringido | Cualquiera salvo el custodio | Denegado, salvo acceso de emergencia |
{: .table .table-bordered}

Cada comunidad define su equivalente y lo aplica en el punto donde toma la decisión de divulgación. La política falla cerrada. Un puntero sin etiqueta se rechaza al publicar, como fija la [sección 2.2](volume-1-actors.html), y el Record Locator Service **SHALL** garantizar que una etiqueta que la política no reconoce se trate como la más restrictiva, también cuando la decisión se evalúa en el Document Registry. FHIR pide a toda guía de implementación decir qué hacer con una etiqueta que no se reconoce, sin prescribir la respuesta ([FHIR R5, Security Labels](https://hl7.org/fhir/R5/security-labels.html))[^fhir-seclabels].

#### Consentimiento del paciente

La decisión base aplica la política única de la comunidad, como fija la [sección 2.2](volume-1-actors.html#record-locator-service). La [Opción de Consentimiento](volume-1-options.html#opcion-de-consentimiento) la extiende al consentimiento de cada paciente, cuyo modelo se especificará a partir de PCF, como explica la [sección 2.1](volume-1-concepts.html#divulgacion).

#### Superficies de identidad {#superficies-de-identidad}

Las transacciones de identidad también divulgan. ITI-83 revela que un identificador corresponde a una persona que la comunidad conoce, e ITI-78 e ITI-119 revelan qué identidades maestras coinciden con unos datos demográficos, o se les parecen. Ninguna revela las identidades locales de otros miembros, como fijan la [sección 2.2](volume-1-actors.html) para ITI-83 y las opciones de Demografía y de Coincidencia Demográfica de la [sección 2.3](volume-1-options.html) para ITI-78 e ITI-119. Estas superficies las habilita el scope del token, no el propósito de uso, y la comunidad decide qué solicitantes pueden ejercerlas y qué identidades maestras se revelan por datos demográficos.

#### Acceso de emergencia {#acceso-de-emergencia}

MHDS pide reconocer los modos de emergencia desde el diseño, y advierte que anular una restricción del paciente por peligro inminente no es romper la política sino una condición explícita dentro de ella ([MHDS Vol. 1, §1:50.5.1](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15051-policies-and-risk-management))[^mhds-emergency]. HIX distingue dos casos con los propósitos de uso de la [Tabla 2.2-3](volume-1-actors.html#tabla-2-2-3). Con `ETREAT`, un profesional autorizado atiende una urgencia y la política de la comunidad decide qué le permite frente a `TREAT`. Con `BTG`, accede quien no está autorizado para ese acceso, con anulación de la política, que es lo que HL7 define para ese código[^btg].

HIX no define cuándo procede ninguno de los dos ni cómo los pide el solicitante, porque IUA no define ningún mecanismo para ello. El Authorization Server **SHALL** emitirlos como propósito de uso solo cuando su registro los admita para ese cliente, y el Record Locator Service **SHALL** registrar en la auditoría el propósito de emergencia con el que divulgó.

### Riesgos residuales {#riesgos-residuales}

La arquitectura no impide que un componente se vea comprometido. Eso depende de cómo se construye, despliega y opera cada sistema, y queda fuera de esta guía, como también queda fuera de IHE y hasta OAuth 2.0. Las causas son las de cualquier sistema, como un supply chain attack sobre una dependencia o una imagen, el robo de credenciales o de claves de firma, una misconfiguration, una vulnerabilidad sin parchar o un insider.

Lo que busca HIX es minimizar la superficie de ataque aplicando least privilege a cada acceso, de modo que un componente comprometido alcance lo menos posible. De ahí salen el token mediado de [HIX-1](volume-2-hix-1.html), que nunca vale ante dos custodios y autoriza un solo tipo de transacción, y las decisiones que esta guía deja a la comunidad, reunidas en la [sección 2.6.1](volume-1-security.html#politicas-y-gestion-de-riesgo).

Para las llamadas del Record Locator Service a los actores centrales desplegados como sistemas distintos, las dos formas de autorización de la [sección 2.2](volume-1-actors.html#record-locator-service) tienen costos distintos. HIX-1 no deja al mediador ninguna credencial que valga sin una petición viva y lleva al destino el sujeto original, pero añade un intercambio por llamada. El token propio ahorra ese intercambio y es más simple de operar, pero es una credencial permanente con la que un mediador comprometido alcanza sin solicitante lo que ese token permite, como consultar el directorio o localizar punteros, aunque nunca un documento; el destino solo ve al mediador como sujeto. La comunidad asume estos costos al elegir cómo autoriza las llamadas.

**Si un componente se ve comprometido**

- **Record Locator Service.** No tiene acceso arbitrario a documentos ni custodios. Solo ve el tráfico que transita por él y los tokens de los solicitantes, y solo alcanza lo que esos tokens permiten mientras están vigentes.
- **Authorization Server.** Puede emitir cualquier token, porque es la raíz de confianza. Nada dentro de HIX lo acota, y proteger sus claves es la primera responsabilidad de la comunidad.
- **Document Registry.** Solo posee metadatos, salvo el contenido que conserva bajo la [Opción de Almacenamiento Central](volume-1-options.html#opcion-de-almacenamiento-central). Expone qué documentos existen de cada persona, pero no la dirección de los custodios.
- **Credenciales robadas de un miembro.** Con ellas se obtienen tokens como ese miembro, con el scope, la organización y los propósitos que su registro admite. Solo se puede afectar a los pacientes y documentos de su propio dominio, y fuera de él solo hacer las consultas que la decisión de divulgación le permita. Ningún token suyo vale ante un custodio. Deshabilitar el cliente revoca sus tokens vigentes, como fija la [sección 2.6.2](volume-1-security.html#contencion-de-una-credencial-comprometida).
- **Credenciales robadas del Record Locator Service.** Con ellas no se alcanza ningún documento ni custodio, porque cada intercambio exige además el token de un solicitante. Por eso el Record Locator Service no puede hacer casi nada sin un miembro que interactúe con él. Si la comunidad le da un token propio hacia actores centrales, con esas credenciales se alcanza lo que ese token permite, como consultar el directorio o localizar punteros, nunca un documento, acotado por la auditoría y por los límites de tasa que fije la comunidad. Cuando el despliegue reúne en un mismo sistema al Record Locator Service y a otros actores centrales, comprometer ese sistema compromete todo lo que reúne, y esa es la contrapartida que acepta quien elige ese despliegue. Deshabilitar el cliente revoca sus tokens vigentes.
- **Un token mediado robado.** Vale ante el destino que nombra su `resource`, nunca ante dos custodios, para un solo tipo de transacción y durante dos minutos como máximo. El custodio **MAY** rechazar un `jti` que ya vio.

**Límites que acota la política de la comunidad**

- **Revocación.** Quien valida el token por sí mismo mediante JWKs no ve una revocación hasta que el token expira.
- **Enumeración.** La búsqueda por datos demográficos permite enumerar pacientes dentro de lo que la política revela.
- **Etiquetado.** Un custodio puede etiquetar mal la confidencialidad de un documento.

### Perfiles y controles

MHDS cierra sus consideraciones de seguridad con la relación entre sus controles y los perfiles IHE que los aportan ([MHDS Vol. 1, §1:50.5.4](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15054-ihe-security-and-privacy-controls)). La [Tabla 2.6-3](volume-1-security.html#tabla-2-6-3) hace lo mismo para HIX.

**Tabla 2.6-3:** Relación entre controles y perfiles o especificaciones
{: #tabla-2-6-3}

| Control | Perfil o especificación que lo aporta |
| --- | --- |
| Autenticación de sistemas | ATNA |
| Autorización y scope | IUA, OAuth 2.0 |
| Delegación acotada y mínimo privilegio | RFC 8693, RFC 8707 |
| Validación local del token mediado | RFC 9068 |
| Introspección de tokens | IUA, RFC 7662 |
| Autorización con participación de la persona | SMART App Launch, OpenID Connect |
| Confidencialidad en tránsito | ATNA |
| Relojes sincronizados | CT |
| Auditoría | ATNA, BALP |
| Identidad del paciente | PMIR, PIXm, PDQm |
| Localización de endpoints | mCSD |
| Divulgación controlada | Opción de Consentimiento, y PCF cuando se especifique |
{: .table .table-bordered}

### Referencias

Las citas reproducen el texto publicado por su fuente. Los recortes se marcan con "[...]" y la negrita es de esta guía.

[^mhds-security]: [MHDS Vol. 1, §1:50.5 MHDS Security Considerations](https://profiles.ihe.net/ITI/MHDS/volume-1.html#1505-mhds-security-considerations): "It is especially important for the reader to understand that **the scope of an IHE profile is only the technical details necessary to ensure interoperability**. It is up to any organization building a community to understand and carefully implement the policies of that community and to perform the appropriate risk analysis. [...] **The policy landscape that the community is built on needs to be defined well before the community is built.**"
[^mhds-policy]: [MHDS Vol. 1, §1:50.5.1 Policies and Risk Management](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15051-policies-and-risk-management): "IHE solves interoperability problems via the implementation of technology standards. **It does not define Privacy or Security Policies**, Risk Management, Healthcare Application Functionality, Operating System Functionality, Physical Controls, or even general Network Controls."
[^mhds-emergency]: [MHDS Vol. 1, §1:50.5.1 Policies and Risk Management](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15051-policies-and-risk-management): "An important set of policies are those around emergency modes. [...] **When these use cases are factored in up-front, the mitigations are reasonable.** [...] Need to override a patient specified privacy block due to eminent danger to that patient – **this override is not a breaking of the policy but would need to be an explicit condition within the policy.**"
[^mhds-doctypes]: [MHDS Vol. 1, §1:50.5.3.2 Protecting different types of documents](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150532-protecting-different-types-of-documents): "This differentiation of the types of data can be represented using a diagram like found in Table 50.5.3.2-1: Sample Access Control Policies, showing an ‘X’ where the defined Role (rows) would have permitted access to data tagged with the given (columns) ConfidentialityCode (U-Unrestricted, L-Low, M-Moderate, N-Normal, R-Restricted, V-Very Restricted). [...] **These roles would be conveyed from the requesting organization through the use of the Internet User Authorization (IUA) Profile.** [...] Additional information can be carried such as the PurposeOfUse, what the user intends to use the data for. Note that **Privacy Policies and Access Control rules can leverage any of the user context, patient identity, or document metadata** discussed above."
[^fhir-seclabels]: [FHIR R5, Security Labels](https://hl7.org/fhir/R5/security-labels.html): "Local agreements and implementation profiles for the use security labels should describe how the security labels connect to the relevant consent and policy statements, and in particular: [...] **What to do if a resource has an unrecognized security label on it** [...]"
[^rfc7519-aud]: [RFC 7519, §4.1.3 "aud" (Audience) Claim](https://www.rfc-editor.org/rfc/rfc7519.html#section-4.1.3): "**In the general case, the "aud" value is an array of case-sensitive strings**, each containing a StringOrURI value. In the special case when the JWT has one audience, the "aud" value MAY be a single case-sensitive string containing a StringOrURI value."
[^rfc9068-aud]: [RFC 9068, §3 Requesting a JWT Access Token](https://www.rfc-editor.org/rfc/rfc9068.html#section-3): "If the request includes a "resource" parameter (as defined in [RFC8707]), **the resulting JWT access token "aud" claim SHOULD have the same value as the "resource" parameter in the request.**"
[^rfc9068-validate]: [RFC 9068, §4 Validating JWT Access Tokens](https://www.rfc-editor.org/rfc/rfc9068.html#section-4): "Resource servers receiving a JWT access token MUST validate it in the following manner. The resource server MUST verify that the "typ" header value is "at+jwt" or "application/at+jwt" and reject tokens carrying any other value. [...] The issuer identifier for the authorization server [...] MUST exactly match the value of the "iss" claim. The resource server MUST validate that **the "aud" claim contains a resource indicator value corresponding to an identifier the resource server expects for itself**. [...] The resource server MUST validate the signature of all incoming JWT access tokens according to [RFC7515] using the algorithm specified in the JWT "alg" Header Parameter. **The resource server MUST reject any JWT in which the value of "alg" is "none".** The resource server MUST use the keys provided by the authorization server. The current time MUST be before the time represented by the "exp" claim."
[^rfc8693-act]: [RFC 8693, §4.1 "act" (Actor) Claim](https://www.rfc-editor.org/rfc/rfc8693.html#section-4.1): "The act (actor) claim provides a means within a JWT to express that **delegation has occurred and identify the acting party to whom authority has been delegated**."
[^rfc7662-active]: [RFC 7662, §2.2 Introspection Response](https://www.rfc-editor.org/rfc/rfc7662.html#section-2.2): "active. REQUIRED. **Boolean indicator of whether or not the presented token is currently active.** [...] a "true" value return for the "active" property will generally indicate that a given token has been issued by this authorization server, **has not been revoked by the resource owner**, and is within its given time window of validity".
[^btg]: [v3-ActReason, BTG](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-BTG): "break the glass. **To perform policy override operations on information for provision of immediately needed health care for an emergent condition** affecting potential harm, death or patient safety **by end users who are not provisioned for this purpose of use**. Includes override of organizational provisioning policies and may include override of subject of care consent directive restricting access." [ETREAT](https://terminology.hl7.org/CodeSystem-v3-ActReason.html#v3-ActReason-ETREAT): "Emergency Treatment. To perform one or more operations on information for provision of **immediately needed health care for an emergent condition**."
[^balp-jti]: [BALP, §3:5.7.5.4 oAuth mapping to AuditEvent](https://profiles.ihe.net/ITI/BALP/content.html#35754-oauth-mapping-to-auditevent): "oAuth field \| Comprehensive AuditEvent \| Minimal AuditEvent [...] **jti (JWT ID) \| agent[user].policy \| agent[user].policy**"
[^balp-token]: [BALP, §3:5.7.5 OAuth Security Token](https://profiles.ihe.net/ITI/BALP/content.html#3575-oauth-security-token): "There is still a need to include some evidence in the AuditEvent to tie this audit log entry with a specific token, but **the whole token should not be recorded for security reasons**."
[^iua-sub]: [IUA, §3.71.4.2.2.1 JSON Web Token Option](https://profiles.ihe.net/ITI/IUA/index.html#3714221-json-web-token-option): "sub (required): **If known, unique identifier of the user; the client_id otherwise** [JWT, Section 4.1]. client_id (required): identifier of the client for which the token is issued." Y en §3.71.4.2.2.1.1 JWT IUA extension: "The Authorization Server and Resource Server shall support the following extensions to the JWT access token: **subject_name** (optional): The user's name as String. **subject_organization_id** (optional): Unique identifier of the user's organization. [...] **subject_role** (optional): Coded values indicating the user's roles. [...] **purpose_of_use** (optional): Purpose of use for the request. [...] The above claims shall be wrapped in an "extensions" object with key 'ihe_iua'".

*[PMIR]: Patient Master Identity Registry, perfil IHE que gestiona la identidad maestra del paciente
*[PIXm]: Patient Identifier Cross-referencing for mobile, perfil IHE que enlaza los MRN de un paciente con su identidad maestra
*[PDQm]: Patient Demographics Query for Mobile, perfil IHE de búsqueda de pacientes por datos demográficos
*[MHD]: Mobile access to Health Documents, perfil IHE para publicar, localizar y recuperar documentos sobre FHIR
*[MHDS]: Mobile Health Document Sharing, perfil IHE que compone MHD, PMIR, mCSD, IUA y ATNA en una comunidad de intercambio de documentos
*[mCSD]: Mobile Care Services Discovery, perfil IHE de directorio de organizaciones, servicios y endpoints
*[IUA]: Internet User Authorization, perfil IHE que aplica OAuth 2.0 a las transacciones sobre FHIR
*[ATNA]: Audit Trail and Node Authentication, perfil IHE de auditoría y seguridad de los nodos
*[BALP]: Basic Audit Log Patterns, perfil IHE con los patrones de AuditEvent de FHIR
*[CT]: Consistent Time, perfil IHE que sincroniza los relojes de los sistemas
*[PCF]: Privacy Consent on FHIR, perfil IHE de consentimiento del paciente
