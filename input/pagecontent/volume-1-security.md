Esta sección describe el modelo de confianza de HIX, los controles que la arquitectura especifica y las decisiones que cada comunidad debe tomar por política. Sigue el orden de las consideraciones de seguridad de MHDS, es decir, políticas y gestión de riesgo, controles técnicos y aplicación al intercambio de documentos ([MHDS Vol. 1, §1:50.5](https://profiles.ihe.net/ITI/MHDS/volume-1.html#1505-mhds-security-considerations))[^mhds-security]. Como IHE, esta guía resuelve problemas de interoperabilidad mediante estándares. No define políticas de privacidad ni de seguridad, gestión de riesgo, funcionalidad clínica, controles físicos ni controles generales de red ([MHDS Vol. 1, §1:50.5.1](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15051-policies-and-risk-management))[^mhds-policy]. Lo que sigue separa lo que queda en manos de la comunidad de lo que fija la arquitectura.

### Políticas y gestión de riesgo

MHDS advierte que el marco de políticas de una comunidad debe definirse antes de construirla[^mhds-security]. Las secciones anteriores dejan a la política de la comunidad una serie de decisiones que aquí se reúnen.

- Qué organizaciones pueden ser miembros, quién lo certifica, bajo qué condiciones dejan de serlo y quién financia la infraestructura central. La [Tabla 2.1-1](volume-1-concepts.html#tabla-2-1-1) de compromisos de la arquitectura lo señala como el riesgo principal de la comunidad a largo plazo.
- Qué propósitos de uso se admiten, con qué condiciones y qué documentos alcanza cada uno, en particular qué permite `ETREAT` frente a `TREAT`, como indica la [Tabla 2.2-3](volume-1-actors.html#tabla-2-2-3).
- Qué política de divulgación aplica mientras el modelo de consentimiento no esté especificado, y en qué punto se aplica, en el Record Locator Service o en el Document Registry, como admite la sección 2.3.
- Qué custodios pueden ejercer la Opción de Almacenamiento Central y quién lo decide.
- Cómo se verifica que los custodios etiquetan correctamente la confidencialidad de sus documentos.
- Cómo obtiene una persona la identidad verificada con la que se autentica ante el Authorization Server, como señala la sección 2.5.
- Qué solicitantes pueden buscar pacientes por datos demográficos y qué identidades maestras se les revelan por esa vía, como exige la Opción de Demografía.
- Cuánto tiempo se conservan los registros de auditoría, quién puede consultarlos y qué ocurre con una operación cuando el Audit Record Repository no está disponible.
- Qué constituye un acceso de emergencia, cómo se admite y qué consecuencias tiene invocarlo.
- Si el acceso de red a los custodios se cierra de modo que la vía mediada sea la única alcanzable, o si esa restricción es solo defensa en profundidad.
- Si se admite la introspección en el custodio, con la dependencia del Authorization Server en cada recuperación que conlleva, como señala la sección 2.6.2.

### Modelo de confianza

El límite de confianza pasa entre cada miembro y la infraestructura central, como establece la sección 2.1. Una recuperación cruza ese límite dos veces, del solicitante a la comunidad y de la comunidad al custodio, y cada cruce lleva un token de un régimen distinto. El primero es el token que el solicitante obtiene del Authorization Server, destinado al Record Locator Service y comprobado por introspección. El segundo es el [token intercambiado](appendix-glossary.html#token-intercambiado) que el Record Locator Service obtiene con [HIX-1](volume-1-actors.html#hix-1) para cada destino que alcanza, sea un custodio o un actor central, y que el destino valida por sí mismo. La [Tabla 2.6-1](volume-1-security.html#tabla-2-6-1) los compara.

**Tabla 2.6-1:** Los dos regímenes de token
{: #tabla-2-6-1}

| | Token del solicitante | Token intercambiado |
| --- | --- | --- |
| Quién lo obtiene | El miembro con ITI-71, o la aplicación del paciente con [HIX-2](volume-1-actors.html#hix-2) | El Record Locator Service con [HIX-1](volume-1-actors.html#hix-1) |
| Audiencia | El Record Locator Service | Un único destino, custodio o actor central |
| Vida | La que fije el Authorization Server | Dos minutos como máximo, y nunca más que la vida restante del token del solicitante |
| Cómo se valida | Por introspección en el Authorization Server con ITI-102, una vez por operación | En el destino, con las claves que publica el Authorization Server ([JWKs](https://www.rfc-editor.org/info/rfc7517/)), sin necesidad de introspección |
| Qué lleva | El sujeto, que es el sistema del miembro o la persona que lanzó la aplicación, la organización y el propósito de uso en las extensiones de IUA, el alcance concedido y, si lo obtuvo una aplicación del paciente, el contexto de paciente | El mismo sujeto, las mismas extensiones y, si lo hay, el mismo contexto de paciente, solo el alcance de la transacción que motivó el intercambio y el Record Locator Service como actor en el claim `act` |
{: .table .table-bordered}

De la tabla se siguen cuatro reglas. De cada una conviene decir qué fija HIX, de qué depende y qué queda en manos de la comunidad.

**Un token intercambiado vale ante un solo destino.** El formato no lo impone. El claim `aud` de un JWT admite una lista de audiencias ([RFC 7519, §4.1.3](https://www.rfc-editor.org/rfc/rfc7519.html#section-4.1.3))[^rfc7519-aud], y el Authorization Server lo rellena con el recurso que el cliente indicó al pedir el token ([RFC 9068, §3](https://www.rfc-editor.org/rfc/rfc9068.html#section-3))[^rfc9068-aud]. HIX lo restringe para el token intercambiado, porque [HIX-1](volume-1-actors.html#hix-1) pide un destino por intercambio y de esa restricción depende que un custodio no pueda reutilizar el token ante otro. El token del solicitante nombra a los actores centrales que el miembro alcanza directamente. En la arquitectura de este volumen es solo el Record Locator Service. Si la arquitectura cambiara y el miembro alcanzara otro actor central, por ejemplo el registro de identidad maestra, su token nombraría a ambos en `aud`, como el formato permite, sin que cambie nada más de este capítulo.

**El token del solicitante no sale de la infraestructura central.** El Record Locator Service no lo reenvía a ningún custodio ni actor central. Ante cada destino presenta un token intercambiado para ese destino, como fija la sección 2.2. Así el solicitante nunca tiene una credencial que valga ante un custodio, y un custodio nunca recibe una que valga ante otro.

**El custodio puede validar el token sin preguntar al Authorization Server.** Todo lo que necesita está en el token y en las claves que el Authorization Server publica. Esa publicación es su única dependencia, y la resuelve por adelantado, conservando las claves y renovándolas cuando aparece un identificador de clave que no conoce. HIX exige esa validación local y no exige introspección en el custodio. Una comunidad puede admitirla además, con la Token Introspection Option de IUA, y quien lo hace acepta que cada recuperación dependa entonces del Authorization Server en ese momento. La subsección siguiente detalla la validación.

**El Record Locator Service no actúa por cuenta propia ante los actores centrales.** No tiene credenciales permanentes hacia el Document Registry ni hacia el registro de identidad maestra. Cada acceso lo hace a nombre de un solicitante, con el token intercambiado para ese destino, y así queda auditado. De esta forma se evita el acceso arbitrario entre los componentes centrales. Ninguno puede consultar a otro sin una petición de un solicitante que lo justifique, y una credencial del mediador comprometida no da acceso a nada por sí sola, porque no existe ninguna que valga sin ese intercambio.

#### Validación en el custodio

El custodio recibe el token intercambiado y lo valida como RFC 9068 pide a todo Resource Server que recibe un token de acceso en forma de JWT ([RFC 9068, §4](https://www.rfc-editor.org/rfc/rfc9068.html#section-4))[^rfc9068-validate], más las comprobaciones que HIX añade sobre la delegación. El custodio **SHALL** comprobar, como mínimo, lo siguiente.

1. La firma, con las claves que publica el Authorization Server, y que el algoritmo es uno de los que la comunidad admite.
2. Que el emisor es exactamente el Authorization Server de la comunidad.
3. Que el tipo de token es el de un token de acceso.
4. Que la audiencia es exactamente él.
5. Que el token no ha expirado y que su momento de emisión es coherente con su vida máxima.
6. Que lleva un sujeto y un identificador de token.
7. Que el cliente al que se emitió es el Record Locator Service.
8. Que el actor declarado en el claim `act` es el Record Locator Service.
9. Que el alcance cubre la transacción que recibe.

Las tres comprobaciones que más pesan son la audiencia, el cliente y el actor. La audiencia sola no basta, porque un token emitido directamente a otro cliente para esa misma audiencia la pasaría. El cliente y el actor son lo que vuelve estructural que solo el Record Locator Service pueda alcanzar a un custodio en nombre de alguien, porque el claim `act` es la forma en que OAuth 2.0 Token Exchange declara que hubo delegación y quién actúa ([RFC 8693, §4.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-4.1))[^rfc8693-act].

El custodio **SHALL** validar el token intercambiado con las claves que publica el Authorization Server, y esa validación basta para aceptarlo. HIX no exige introspección en el custodio. El custodio **MAY** comprobarlo además por introspección, con la [Token Introspection Option](https://profiles.ihe.net/ITI/IUA/index.html#3424-token-introspection-option) de IUA y [ITI-102](https://profiles.ihe.net/ITI/IUA/index.html#3102-introspect-token-iti-102), si la comunidad lo admite. Entonces cada recuperación depende del Authorization Server en el momento de atenderla, y esa dependencia se asume a sabiendas.

#### Lo que un token prueba y lo que no

Un custodio que recibe un token intercambiado puede comprobar por sí mismo cinco cosas.

- Que lo emitió el Authorization Server de la comunidad.
- Que el Record Locator Service lo pidió en nombre de un solicitante concreto.
- Que vale ante él y ante nadie más.
- Que autoriza solo la transacción para la que se intercambió. El token del solicitante puede llevar varios scopes, pero el Record Locator Service pide en el intercambio únicamente el de la transacción que va a realizar, por ejemplo el de ITI-68 al recuperar.
- Que expira en dos minutos como máximo.

El token no nombra ningún documento. Mientras dura, autoriza esa transacción ante ese custodio, sea cual sea el documento. Tampoco nombra al paciente, porque el token de un miembro no lleva ninguno, como explica la sección 2.1. La excepción es la aplicación del paciente. Su contexto de paciente, fijado con [HIX-2](volume-1-actors.html#hix-2), se conserva en el intercambio y limita al custodio a ese expediente.

Lo que el token sí aporta es el contexto con el que se decide, en las extensiones de IUA. Quién pide, para qué organización, con qué propósito de uso y, si lo hay, sobre qué paciente. Ese contexto acota lo que puede alcanzarse con el token, y con él se decide qué documento se entrega, en tres capas y en este orden.

1. La [decisión de divulgación](appendix-glossary.html#decision-de-divulgacion), que la infraestructura central aplica sobre los punteros antes de mover contenido.
2. La política local del custodio sobre su propio endpoint.
3. La auditoría, que no previene pero acota y detecta.

En resumen, el token prueba quién pide, en nombre de quién actúa la comunidad, ante quién vale, hasta cuándo y con qué contexto. Qué se entrega lo deciden esas tres capas a partir de ese contexto.

#### Contención de una credencial comprometida

Deshabilitar un cliente en el Authorization Server **SHALL** revocar sus tokens vigentes, de modo que la siguiente introspección los declare inactivos, que es el estado que RFC 7662 prevé para un token revocado ([RFC 7662, §2.2](https://www.rfc-editor.org/rfc/rfc7662.html#section-2.2))[^rfc7662-active], y ningún intercambio pueda partir de ellos. Un token ya intercambiado no tiene ciclo de vida propio. El Record Locator Service lo usa una sola vez, en la recuperación que lo motivó, y expira en dos minutos como máximo. Revocar el token del solicitante impide todo intercambio nuevo, y la recuperación que ya estaba en curso termina. Lo que contiene una credencial comprometida es que los tokens obtenidos con ella dejen de valer, no que cambie la credencial. Si el Authorization Server revoca también esos tokens al rotar el secreto o la clave de un cliente es decisión de su implementación. Si no lo hace, hay que revocarlos aparte.

### Controles técnicos de seguridad y privacidad

HIX especifica los siguientes controles. Cada uno remite a la sección que lo fija.

- **Autenticación de sistemas.** Toda conexión entre dos participantes se autentica en ambos extremos con ATNA, como fija la sección 2.4. Ningún participante acepta tráfico anónimo.
- **Autorización.** Toda transacción presenta un token emitido por el Authorization Server de la comunidad y destinado a quien la recibe, como fija la sección 2.2.
- **Delegación acotada.** El token con el que la comunidad alcanza a un custodio se emite para esa recuperación, conserva el sujeto y las extensiones del solicitante original y declara al Record Locator Service como actor.
- **Mínimo privilegio.** El alcance de un token intercambiado se limita a la transacción que motivó el intercambio y nunca excede el del solicitante, el de la delegación registrada ni las capacidades del destino. Poder localizar un documento nunca da poder para recuperarlo.
- **Confidencialidad en tránsito.** Todo tramo viaja cifrado, incluido el que atraviesa un canal de interconexión bajo la Opción de Transporte Mediado.
- **Divulgación decidida sobre los punteros.** La política se evalúa en la infraestructura central, una vez por consulta, sobre los metadatos del índice y antes de que se mueva contenido, como fija la sección 2.1.
- **Auditoría en ambos extremos.** El miembro que solicita y la infraestructura central registran la localización. Infraestructura central y custodio registran la recuperación. Ningún tramo queda sin testigo.
- **Trazabilidad entre tramos.** Los registros de una misma divulgación comparten un identificador de correlación, de modo que la interacción completa pueda reconstruirse.
- **Identidad del paciente.** Solo la fuente autoritativa crea identidades maestras. Lo que un miembro declara vincula su identidad local con una de ellas, en su propio dominio, y queda registrado como una afirmación suya.

### Aplicación al intercambio de documentos

#### Seguridad básica

Todo actor de HIX, salvo la aplicación del paciente, es un Secure Node o Secure Application de ATNA y un Time Client de CT, como fija la sección 2.4. Los actores centrales registran sus eventos en el Audit Record Repository de la comunidad y cada miembro en el suyo, con el contenido que BALP define para cada transacción.

El Record Locator Service **SHALL** registrar tanto la solicitud que recibe como cada recuperación que origina hacia un custodio, bajo un identificador de correlación que él mismo acuña y transmite al custodio, y **SHALL NOT** transmitir hacia el custodio ninguno que el solicitante proponga. Ningún registro de auditoría **SHALL** contener valores de credenciales ni contenido clínico.

#### Protección según el tipo de documento

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

Cada comunidad define su equivalente y lo aplica en el punto donde toma la decisión de divulgación. Lo que sí es requisito es que la política falle cerrada. Un puntero sin etiqueta se rechaza al publicar, como fija la sección 2.2, y una etiqueta que la política no reconoce se trata como la más restrictiva. FHIR pide a toda guía de implementación decir qué hacer con una etiqueta que no se reconoce, sin prescribir la respuesta ([FHIR R5, Security Labels](https://hl7.org/fhir/R5/security-labels.html))[^fhir-seclabels].

#### Consentimiento del paciente

La decisión de divulgación necesita conocer al paciente, al solicitante, su organización, el propósito de uso que lleva su token y la etiqueta de confidencialidad de cada puntero. La Opción de Consentimiento de la sección 2.3 describe ese punto de aplicación y la información que necesita, y el destino es PCF, como explica la sección 2.1.

Mientras el modelo de consentimiento no esté especificado, la comunidad opera bajo la política de divulgación que haya acordado. Esa política debe estar documentada y ser la misma para todos los miembros.

#### Superficies de identidad

Las transacciones de identidad también divulgan. ITI-83 revela que un identificador corresponde a una persona que la comunidad conoce, e ITI-78 revela qué identidades maestras coinciden con unos datos demográficos. Ninguna revela las identidades locales de otros miembros, como fijan la sección 2.2 para ITI-83 y la Opción de Demografía de la sección 2.3 para ITI-78. Estas superficies las habilita el scope del token, no el propósito de uso, y la comunidad decide qué solicitantes pueden ejercerlas y qué identidades maestras se revelan por datos demográficos, como exige la Opción de Demografía.

#### Acceso de emergencia

MHDS pide reconocer los modos de emergencia desde el diseño, y advierte que anular una restricción del paciente por peligro inminente no es romper la política sino una condición explícita dentro de ella ([MHDS Vol. 1, §1:50.5.1](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15051-policies-and-risk-management))[^mhds-emergency]. HIX distingue dos casos con los propósitos de uso de la [Tabla 2.2-3](volume-1-actors.html#tabla-2-2-3). Con `ETREAT`, un profesional autorizado atiende una urgencia y la política de la comunidad decide qué le permite frente a `TREAT`. Con `BTG`, accede quien no está autorizado para ese acceso, con anulación de la política, que es lo que HL7 define para ese código[^btg].

HIX no define cuándo procede ninguno de los dos. Sí exige que sean declarados y no inferidos. El solicitante **SHALL** pedir el propósito de emergencia al obtener el token, el Authorization Server **SHALL** emitirlo como propósito de uso del token solo cuando su registro lo admita para ese solicitante, y el evento **SHALL** registrarse con auditoría reforzada que permita revisarlo después.

### Perfiles y controles

MHDS cierra sus consideraciones de seguridad con la relación entre sus controles y los perfiles IHE que los aportan ([MHDS Vol. 1, §1:50.5.4](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15054-ihe-security-and-privacy-controls)). La [Tabla 2.6-3](volume-1-security.html#tabla-2-6-3) hace lo mismo para HIX.

**Tabla 2.6-3:** Relación entre controles y perfiles o especificaciones
{: #tabla-2-6-3}

| Control | Perfil o especificación que lo aporta |
| --- | --- |
| Autenticación de sistemas | ATNA |
| Autorización y alcance | IUA, OAuth 2.0 |
| Delegación acotada y mínimo privilegio | RFC 8693, RFC 8707 |
| Validación local del token intercambiado | RFC 9068 |
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
