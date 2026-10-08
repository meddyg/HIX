Patient Application Launch [HIX-2] es la transacción con la que una aplicación elegida por una persona obtiene del Authorization Server un token destinado al Record Locator Service, cuyo contexto de paciente es la identidad maestra de esa persona. Ningún perfil IHE la define, y esta página la especifica.

### Alcance

Con ese token, la aplicación localiza y recupera como cualquier consumidor, limitada a ese paciente, como describe el caso de [acceso del paciente a su expediente](volume-1-usecases.html#acceso-del-paciente-a-su-expediente).

> **Nota.** El consentimiento del que habla esta página es el de OAuth 2.0, es decir, la aprobación con la que la persona permite a una aplicación actuar en su nombre ante el Record Locator Service. No debe confundirse con el consentimiento del paciente sobre la divulgación de sus documentos, que decide qué puede ver cada solicitante y que describe la [Opción de Consentimiento](volume-1-options.html#opcion-de-consentimiento). HIX-2 no registra ni modifica ese segundo consentimiento.

HIX-2 es [ITI-71](https://profiles.ihe.net/ITI/IUA/index.html#371-get-access-token-iti-71) con el grant Authorization Code y PKCE (Proof Key for Code Exchange), más la renovación del token con el grant de refresh token. IUA limita ITI-71 a los grants Authorization Code y Client Credential, y admite que sus actores soporten otros, como el de refresh token ([IUA, §34.4.1.1](https://profiles.ihe.net/ITI/IUA/index.html#34411-authorization-grant-types))[^iua-grants]. Para el contexto de paciente, HIX-2 adopta determinados elementos de SMART App Launch, que IUA procura no contradecir ([IUA, Relation to SMART-on-FHIR](https://profiles.ihe.net/ITI/IUA/index.html#relation-to-smart-on-fhir))[^iua-smart]. Tiene identificador propio porque en ella el Authorization Server fija el contexto de paciente, algo que ITI-71 no prevé.

HIX-2 aplica las reglas de [ITI-71](volume-2-authorization.html#iti-71) de la página de Autorización, con tres diferencias. El `resource` nombra al Record Locator Service y el `aud` del token solo lo nombra a él. El token lleva el propósito de uso y el contexto de paciente, y la organización solo si el registro del Authorization Server asocia una a la aplicación. Y la aplicación solo puede obtener los scopes de ITI-66, ITI-67 e ITI-68.

#### Decisiones frente a IUA y SMART App Launch {#decisiones}

La [Tabla 3.3-1](volume-2-hix-2.html#tabla-3-3-1) reúne qué toma HIX-2 de IUA y de SMART App Launch y en qué se aparta de ellos. El resto de la página aplica estas decisiones sin repetirlas.

**Tabla 3.3-1:** Decisiones de HIX-2 frente a IUA y SMART App Launch
{: #tabla-3-3-1}

| Aspecto | IUA | SMART App Launch | HIX-2 |
| --- | --- | --- | --- |
| Lanzamiento | No lo define | EHR Launch o Standalone Launch[^smart-standalone] | Solo Standalone Launch, sin el parámetro `launch` |
| Destino del token | `resource`, opcional y de un solo valor[^iua-code-request] | `aud`, obligatorio, con `resource` como sinónimo opcional[^smart-aud] | `resource`, obligatorio y único |
| `redirect_uri` | Obligatorio solo si la aplicación tiene varias URI registradas[^iua-code-request] | Obligatorio[^smart-authorize] | Obligatorio |
| PKCE | `code_challenge` obligatorio y método opcional[^iua-code-request] | Solo `S256`, nunca `plain`[^smart-pkce] | Solo `S256` |
| Scopes | Uno por transacción de MHD, como `ITI-67`[^iua-mhd-scope] | De recurso, de contexto y de identidad[^smart-scopes] | Los identificadores de transacción, `launch/patient` y `fhirUser` de SMART, y `openid` y `offline_access` de OpenID Connect |
| `patient` al renovar | No lo define | Opcional[^smart-refresh] | Obligatorio |
| `fhirUser` en la introspección | No lo define | Recomendado[^smart-introspection] | No exigido |
{: .table .table-bordered}

HIX exige `patient` en toda respuesta de token, también al renovar, para que la aplicación conozca siempre el contexto vigente. SMART lo deja opcional al renovar[^smart-refresh]. No exige `fhirUser` en la introspección, porque el Record Locator Service confina cada operación con `patient`.

SMART App Launch pide el destino con un parámetro llamado `aud` y lo declara equivalente al `resource` de RFC 8707 ([SMART App Launch, Obtain authorization code](https://hl7.org/fhir/smart-app-launch/app-launch.html#obtain-authorization-code))[^smart-aud]. HIX usa `resource`, porque `aud` es el nombre del claim con el que el Authorization Server fija la audiencia del token, que no tiene por qué coincidir con lo que el cliente pidió. El Authorization Server **SHOULD NOT** aceptar el parámetro `aud` en lugar de `resource`. Si una comunidad decide aceptarlo, por ejemplo para admitir aplicaciones SMART ya existentes, el Authorization Server lo trata exactamente como un `resource`.

> **Nota.** SMART App Launch exige a sus servidores aceptar el parámetro `aud` y deja `resource` como sinónimo opcional[^smart-aud]. RFC 8707 separa la intención de la restricción, porque el Authorization Server restringe la audiencia del token a partir del `resource`, la comunica en el claim `aud` y puede usar el mismo valor o derivar de él otro identificador ([RFC 8707, §2](https://www.rfc-editor.org/rfc/rfc8707.html#section-2))[^rfc8707-resource]. Por esta razón, HIX-2 se aparta en este punto de SMART App Launch.

#### Descubrimiento del Authorization Server {#descubrimiento}

SMART App Launch pide que todo endpoint FHIR que exige autorización sirva en su URL base, bajo `/.well-known/smart-configuration`, un documento con los endpoints de autorización y las capacidades que admite ([SMART App Launch, Conformance](https://hl7.org/fhir/smart-app-launch/conformance.html#using-well-known))[^smart-well-known]. Es así como una aplicación SMART encuentra el Authorization Server a partir de la URL que va a consultar.

**Experimental.** El Record Locator Service **SHALL** hacer disponible el documento `/.well-known/smart-configuration` en la URL base FHIR que expone a la aplicación del paciente, y el documento **SHALL** describir los endpoints y las capacidades del Authorization Server. Que lo sirva el propio Record Locator Service o lo redirija al Authorization Server lo decide la implementación. La [Tabla 3.3-2](volume-2-hix-2.html#tabla-3-3-2) dice qué declara HIX en él.

**Tabla 3.3-2:** Contenido del documento `smart-configuration`
{: #tabla-3-3-2}

| Campo | Valor en HIX |
| --- | --- |
| `issuer` y `jwks_uri` | Los del Authorization Server como OpenID Provider |
| `authorization_endpoint` y `token_endpoint` | Los del Authorization Server |
| `grant_types_supported` | `authorization_code` |
| `code_challenge_methods_supported` | Solo `S256` |
| `capabilities` | `launch-standalone`, `context-standalone-patient`, `sso-openid-connect`, `client-public`, `client-confidential-symmetric` y `permission-offline`. Ninguna de las capacidades de scopes de recurso, porque HIX no los usa |
{: .table .table-bordered}

**Ejemplo.** La aplicación pide el documento a partir de la URL base FHIR del Record Locator Service.

```http
GET /.well-known/smart-configuration HTTP/1.1
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "issuer": "<issuer>",
  "jwks_uri": "<jwks_uri>",
  "authorization_endpoint": "<authorization_endpoint>",
  "token_endpoint": "<token_endpoint>",
  "grant_types_supported": ["authorization_code"],
  "code_challenge_methods_supported": ["S256"],
  "capabilities": [
    "launch-standalone",
    "context-standalone-patient",
    "sso-openid-connect",
    "client-public",
    "client-confidential-symmetric",
    "permission-offline"
  ]
}
```

El Authorization Server sigue publicando sus metadatos de IUA con [ITI-103](https://profiles.ihe.net/ITI/IUA/index.html#3103-get-authorization-server-metadata-iti-103), y los dos documentos describen los mismos endpoints.

### Roles de actor

La [Tabla 3.3-3](volume-2-hix-2.html#tabla-3-3-3) muestra los roles de los actores de HIX en la transacción, según la [sección 2.4](volume-1-groupings.html).

**Tabla 3.3-3:** Roles de actor
{: #tabla-3-3-3}

| Actor | Rol | Qué hace |
| --- | --- | --- |
| Aplicación del paciente | [Authorization Client](https://profiles.ihe.net/ITI/IUA/index.html#34111-authorization-client) | Pide, en nombre de la persona que la usa, un token para el Record Locator Service con el contexto de paciente |
| Authorization Server | [Authorization Server](https://profiles.ihe.net/ITI/IUA/index.html#34112-authorization-server) y [OpenID Provider](appendix-glossary.html#openid-provider) | Autentica a la persona, obtiene su autorización, fija el contexto de paciente y emite los tokens |
{: .table .table-bordered}

Durante el lanzamiento, el Authorization Server también actúa como [Patient Identifier Cross-reference Consumer](appendix-glossary.html#patient-identifier-cross-reference-consumer) de PIXm. Resuelve la identidad de la persona ante el Master Patient Index mediante ITI-83, con un token propio que obtiene con el grant Client Credentials, según la [sección 2.2](volume-1-actors.html#authorization-server). Esa consulta no forma parte de HIX-2.

### Estándares referenciados

HIX-2 se apoya en los documentos siguientes.

- [IUA](https://profiles.ihe.net/ITI/IUA/index.html), Internet User Authorization, revisión 2.5, junio de 2026. Aporta ITI-71 con el grant Authorization Code y su evento de auditoría.
- [SMART App Launch](https://hl7.org/fhir/smart-app-launch/), versión 2.2.0, de 2024. Aporta el Standalone Launch, los scopes `launch/patient` y `fhirUser`, el parámetro `patient` y el claim `fhirUser`.
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html), con la fe de erratas 2, diciembre de 2023. Aporta la autenticación de la persona, el `id_token` y los scopes `openid` y `offline_access`.
- [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749), The OAuth 2.0 Authorization Framework, octubre de 2012. Aporta el grant de refresh token y las respuestas de error.
- [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636), Proof Key for Code Exchange by OAuth Public Clients, septiembre de 2015. Aporta `code_challenge`, `code_verifier` y el método `S256`.
- [RFC 8707](https://www.rfc-editor.org/rfc/rfc8707), Resource Indicators for OAuth 2.0, febrero de 2020. Aporta el parámetro `resource` y el error `invalid_target`.
- [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700), Best Current Practice for OAuth 2.0 Security, enero de 2025. Aporta la protección de los refresh tokens de los clientes públicos.

### Mensajes

La [Figura 3.3-1](volume-2-hix-2.html#figura-3-3-1) muestra los mensajes de la transacción. La petición de autorización y su respuesta pasan por el navegador de la persona. Las peticiones de token van directamente al token endpoint. La renovación solo ocurre si la aplicación obtuvo un refresh token.

![Patient Application Launch](hix-2-hix-2.svg)

**Figura 3.3-1:** Patient Application Launch
{: #figura-3-3-1}

#### Petición de autorización {#peticion-de-autorizacion}

##### Evento desencadenante

La aplicación inicia un lanzamiento cuando la persona la abre y no tiene un token vigente para el Record Locator Service ni un refresh token con el que renovarlo. También lo inicia cuando el Authorization Server rechaza una renovación con `invalid_grant`. Redirige el navegador al authorization endpoint, que descubre con el documento `smart-configuration` o con ITI-103, como explica el [descubrimiento del Authorization Server](volume-2-hix-2.html#descubrimiento).

##### Semántica del mensaje

La petición es un GET al authorization endpoint, con los parámetros en la query, como define IUA para el grant Authorization Code ([IUA, §3.71.4.1.2.2](https://profiles.ihe.net/ITI/IUA/index.html#3714122-authorization-code-grant-type))[^iua-code-request]. La [Tabla 3.3-4](volume-2-hix-2.html#tabla-3-3-4) dice qué valor fija HIX en cada parámetro.

**Tabla 3.3-4:** Parámetros de la petición de autorización
{: #tabla-3-3-4}

| Parámetro | Valor en HIX |
| --- | --- |
| `response_type` | `code` |
| `client_id` | El identificador con el que la aplicación está registrada en el Authorization Server |
| `redirect_uri` | Una de las URI de redirección registradas para la aplicación. El Authorization Server **SHALL** compararla por coincidencia exacta, como exige RFC 9700 ([RFC 9700, §2.1](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.1))[^rfc9700-redirect] |
| `state` | Obligatorio, como exige IUA ([IUA, §3.71.4.1.2.2](https://profiles.ihe.net/ITI/IUA/index.html#3714122-authorization-code-grant-type))[^iua-state]. Un valor impredecible que la aplicación genera para cada petición |
| `resource` | Uno solo, el identificador del Record Locator Service como Resource Server |
| `code_challenge` | El reto que la aplicación deriva de su `code_verifier` |
| `code_challenge_method` | `S256` |
| `scope` | `openid`, `fhirUser`, `launch/patient` y los identificadores de las transacciones que la aplicación va a realizar, como `ITI-67` e `ITI-68`. Además, `offline_access` si la aplicación quiere un refresh token |
{: .table .table-bordered}

Ninguno de los scopes de SMART ni de OpenID Connect autoriza operaciones ante el Record Locator Service. Lo que autoriza son los identificadores de transacción, según la regla 2 para las [peticiones a un Resource Server](volume-2.html#peticiones-a-un-resource-server). La aplicación pide solo los que necesita, como IUA exige a todo Authorization Client ([IUA, §3.71.5](https://profiles.ihe.net/ITI/IUA/index.html#3715-security-considerations))[^iua-security]. El Authorization Server **SHALL NOT** conceder a una aplicación del paciente identificadores de transacción distintos de `ITI-66`, `ITI-67` e `ITI-68`, porque la aplicación solo localiza y recupera los documentos de la persona.

**Ejemplo.** La aplicación del paciente pide autorización para buscar y recuperar documentos, y un refresh token.

```http
GET /authorize?response_type=code&client_id=<client_id>&redirect_uri=<redirect_uri>&state=<state>&resource=<rls_resource>&code_challenge=<code_challenge>&code_challenge_method=S256&scope=openid+fhirUser+launch/patient+offline_access+ITI-67+ITI-68 HTTP/1.1
```

##### Acciones esperadas

El Authorization Server valida los parámetros, autentica a la persona y obtiene su autorización para la aplicación, como IUA exige antes de emitir el código ([IUA, §3.71.4.1.3.2](https://profiles.ihe.net/ITI/IUA/index.html#3714132-authorization-code-grant-type))[^iua-code-actions]. Cómo se verifica la identidad de la persona es política de la comunidad, según la [sección 2.6](volume-1-security.html#politicas-y-gestion-de-riesgo).

Si la petición lleva `offline_access`, el Authorization Server **SHALL** obtener en cada lanzamiento el consentimiento de la persona para emitir el refresh token, sin reutilizar uno guardado. La aplicación no necesita enviar `prompt=consent`.

> **Nota.** OpenID Connect exige al OpenID Provider obtener siempre el consentimiento antes de emitir un refresh token para el acceso sin conexión, y advierte que un consentimiento guardado no siempre basta. Para asegurarlo, la petición lleva `prompt=consent`, salvo que otras condiciones del procesamiento permitan el acceso sin conexión ([OpenID Connect Core, §11](https://openid.net/specs/openid-connect-core-1_0.html#OfflineAccess))[^oidc-offline]. En HIX esa condición es que el Authorization Server pide el consentimiento en cada lanzamiento y nunca reutiliza uno guardado, que es lo mismo que obtendría `prompt=consent`. Por esta razón, HIX-2 no exige a la aplicación enviar `prompt=consent`.

Antes de emitir el código, el Authorization Server resuelve mediante ITI-83 la identidad verificada de la persona a su identidad maestra y la fija como contexto de paciente de la autorización, según sus requisitos de la [sección 2.2](volume-1-actors.html#authorization-server). Ese contexto vale para el canje del código y para todas las renovaciones de la misma autorización.

El Authorization Server fija también el propósito de uso desde su propio registro, `PATRQT` cuando quien actúa es la propia persona, según la [Tabla 2.2-3](volume-1-actors.html#tabla-2-2-3). Nunca lo toma de la petición, según la regla 3 para las [peticiones a un Resource Server](volume-2.html#peticiones-a-un-resource-server).

> **Nota.** HIX-2 no fija cómo actúa una persona en nombre de otra, como un familiar autorizado o un representante legal. Si una comunidad lo admite, define cómo se acredita esa relación, qué paciente queda como contexto y qué propósito de uso lleva el token, como `FAMRQT` o `PWATRNY`.

#### Respuesta de autorización {#respuesta-de-autorizacion}

##### Evento desencadenante

El Authorization Server responde cuando concede la autorización o cuando la rechaza.

##### Semántica del mensaje

Si concede la autorización, el Authorization Server redirige el navegador a la `redirect_uri` con `code` y `state`[^iua-code-request]. Si la rechaza, redirige con `error` y el `state` de la petición ([RFC 6749, §4.1.2.1](https://www.rfc-editor.org/rfc/rfc6749.html#section-4.1.2.1))[^rfc6749-authz-error].

Si la `redirect_uri` o el `client_id` faltan o no son válidos, el Authorization Server **SHALL NOT** redirigir el navegador y **SHOULD** informar del error a la persona, como exige RFC 6749[^rfc6749-authz-error].

El Authorization Server **SHALL** rechazar la petición en las condiciones de la [Tabla 3.3-5](volume-2-hix-2.html#tabla-3-3-5). Los códigos son los que prevén RFC 7636 para PKCE[^rfc7636-error], RFC 8707 para el recurso[^rfc8707-resource] y RFC 6749 para los demás[^rfc6749-authz-error].

**Tabla 3.3-5:** Rechazos en el authorization endpoint
{: #tabla-3-3-5}

| Condición | Error | Motivo |
| --- | --- | --- |
| Falta `code_challenge`, o `code_challenge_method` no es `S256` | `invalid_request` | HIX admite solo `S256` |
| La petición no lleva exactamente un `resource`, contando `aud` si la comunidad lo acepta, o ese valor no es el Record Locator Service | `invalid_target` | El token de la aplicación vale solo ante el Record Locator Service, como resume la [Tabla 2.6-1](volume-1-security.html#tabla-2-6-1) |
| El scope pide una transacción distinta de `ITI-66`, `ITI-67` e `ITI-68` | `invalid_scope` | La aplicación del paciente solo localiza y recupera, como fija la [sección 2.4](volume-1-groupings.html#miembros) |
| El scope pide transacciones sin `launch/patient` | `invalid_scope` | Un token con transacciones y sin contexto de paciente no quedaría confinado al expediente de la persona |
| La identidad verificada de la persona no resuelve a una identidad maestra | `access_denied` | El Authorization Server no fija un contexto de paciente sin identidad maestra, como establece la [sección 2.2](volume-1-actors.html#authorization-server) |
| El Master Patient Index no responde | `server_error` | Sin la identidad maestra no hay contexto que fijar. RFC 6749 reserva `temporarily_unavailable` para la sobrecarga o el mantenimiento del propio Authorization Server |
{: .table .table-bordered}

**Ejemplo.** El Authorization Server rechaza un lanzamiento cuya identidad verificada no resuelve a una identidad maestra.

```http
HTTP/1.1 302 Found
Location: <redirect_uri>?error=access_denied&state=<state>
```

##### Acciones esperadas

La aplicación comprueba que `state` coincide con el valor que envió[^smart-authorize]. Si recibe el código, lo canjea en el token endpoint. Si recibe un error, no obtiene token.

#### Petición de token {#peticion-de-token}

##### Evento desencadenante

La aplicación envía la petición con el grant Authorization Code al recibir el código en la redirección. Usa el grant de refresh token cuando vence su token y conserva un refresh token vigente.

##### Semántica del mensaje

La petición es un POST al token endpoint, con los parámetros en el body en formato `application/x-www-form-urlencoded`. El canje del código sigue IUA[^iua-code-request] y SMART App Launch ([SMART App Launch, Obtain access token](https://hl7.org/fhir/smart-app-launch/app-launch.html#obtain-access-token))[^smart-token]. La renovación sigue RFC 6749 ([RFC 6749, §6](https://www.rfc-editor.org/rfc/rfc6749.html#section-6))[^rfc6749-refresh] y SMART App Launch[^smart-refresh]. La [Tabla 3.3-6](volume-2-hix-2.html#tabla-3-3-6) dice qué valor fija HIX en cada parámetro de los dos grants.

**Tabla 3.3-6:** Parámetros de la petición de token
{: #tabla-3-3-6}

| Parámetro | Canje del código | Renovación |
| --- | --- | --- |
| `grant_type` | `authorization_code` | `refresh_token` |
| `code` | El código recibido en la redirección | No se envía |
| `redirect_uri` | La misma de la petición de autorización | No se envía |
| `code_verifier` | El valor del que la aplicación derivó el `code_challenge` | No se envía |
| `refresh_token` | No se envía | El último refresh token que recibió la aplicación |
| `scope` | No se envía | Se omite, o pide una parte del scope concedido |
| `client_id` | Lo envía la aplicación pública. La confidencial se autentica con su credencial[^iua-code-actions] | Igual que en el canje |
{: .table .table-bordered}

SMART App Launch exige el `client_id` en el canje de una aplicación pública[^smart-token]. La aplicación pública **SHALL** enviarlo también al renovar, como admite RFC 6749 ([RFC 6749, §3.2.1](https://www.rfc-editor.org/rfc/rfc6749.html#section-3.2.1))[^rfc6749-client-id], para que el Authorization Server compruebe a qué aplicación emitió el refresh token.

**Ejemplo.** Una aplicación pública canjea el código y, más tarde, renueva su token.

```http
POST /token HTTP/1.1
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=<code>
&redirect_uri=<redirect_uri>
&code_verifier=<code_verifier>
&client_id=<client_id>
```

```http
POST /token HTTP/1.1
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
&refresh_token=<refresh_token>
&client_id=<client_id>
```

##### Acciones esperadas

En el canje, el Authorization Server verifica el código y comprueba que el `code_verifier` corresponde al `code_challenge` de la autorización, como exigen IUA[^iua-code-actions] y SMART App Launch[^smart-authorize].

Al renovar, el Authorization Server valida el refresh token y comprueba que se emitió a esa aplicación[^rfc6749-refresh]. El Authorization Server **SHALL** emitir el token renovado con el contexto de paciente fijado en la autorización, sin volver a consultar ITI-83, y sin ampliar el scope concedido.

Con una aplicación pública, el Authorization Server **SHALL** emitir un refresh token nuevo en cada renovación e invalidar el anterior, o ligar el refresh token a esa instancia de la aplicación, como exige RFC 9700 para los clientes públicos ([RFC 9700, §4.14.2](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.14.2))[^rfc9700-refresh]. Si rota los refresh tokens y recibe uno ya invalidado, **SHALL** revocar el refresh token vigente de esa autorización. RFC 9700 describe esa revocación como la respuesta de la rotación a un refresh token reutilizado[^rfc9700-refresh].

#### Respuesta de token {#respuesta-de-token}

##### Evento desencadenante

El Authorization Server responde a cada petición de token con el token si la concede o con un error si la rechaza.

##### Semántica del mensaje

El Authorization Server responde a una petición concedida con el código HTTP 200, un body JSON y los headers `Cache-Control: no-store` y `Pragma: no-cache` que exige IUA ([IUA, §3.71.4.2.2](https://profiles.ihe.net/ITI/IUA/index.html#371422-message-semantics))[^iua-response]. La [Tabla 3.3-7](volume-2-hix-2.html#tabla-3-3-7) dice qué valor fija HIX en cada parámetro. La respuesta a una renovación tiene la misma forma, salvo por el `id_token`. El Authorization Server **SHALL** incluir `patient` en toda respuesta concedida, también en la de una renovación.

**Tabla 3.3-7:** Parámetros de la respuesta de token
{: #tabla-3-3-7}

| Parámetro | Valor en HIX |
| --- | --- |
| `access_token` | El token de la persona, destinado al Record Locator Service. Lleva el propósito de uso y el contexto de paciente, y la organización solo si el registro del Authorization Server asocia una a la aplicación. Lo resume la [Tabla 2.6-1](volume-1-security.html#tabla-2-6-1) |
| `token_type` | `Bearer`, porque la aplicación lo presenta con ITI-72 |
| `expires_in` | La vida del token en segundos, la que fije el Authorization Server |
| `scope` | Solo los identificadores de transacción concedidos, que pueden diferir de los pedidos |
| `id_token` | El de OpenID Connect, que acredita la autenticación de la persona y lleva `fhirUser`. Al renovar puede faltar, y si viene conserva el `iss` y el `sub` del original[^oidc-refresh] |
| `refresh_token` | Solo si la aplicación pidió `offline_access` y el Authorization Server le concede la renovación |
| `patient` | Siempre, también al renovar. Es el identificador del recurso Patient de la identidad maestra fijada como contexto de paciente |
| `fhirContext` | HIX no lo fija. SMART App Launch lo admite para contexto adicional, y ningún actor de HIX depende de él |
{: .table .table-bordered}

El Authorization Server **SHALL** incluir en el scope del access token solo identificadores de transacción. `openid`, `fhirUser`, `launch/patient` y `offline_access` los consume él al emitir el token y no aparecen en él. El `scope` de la respuesta describe el access token ([RFC 6749, §5.1](https://www.rfc-editor.org/rfc/rfc6749.html#section-5.1))[^rfc6749-token-response], y por eso lleva solo esos identificadores, según la regla 2 para las [peticiones a un Resource Server](volume-2.html#peticiones-a-un-resource-server). La aplicación sabe qué obtuvo de OpenID Connect y de SMART por los parámetros que recibe, es decir, `id_token`, `refresh_token` y `patient`.

La respuesta distingue a quien actúa del paciente cuyo expediente se consulta. `sub` y `fhirUser` identifican a la persona que actúa, y `patient` al paciente. En el acceso propio son la misma persona, pero ningún actor deduce el paciente de `sub` ni de `fhirUser`, y el Record Locator Service confina cada operación solo con `patient`.

**Ejemplo.** El Authorization Server responde al canje del código con el access token, el `id_token`, un refresh token y el contexto de paciente.

```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store
Pragma: no-cache

{
  "access_token": "<access_token>",
  "token_type": "Bearer",
  "expires_in": 300,
  "scope": "ITI-67 ITI-68",
  "id_token": "<id_token>",
  "refresh_token": "<refresh_token>",
  "patient": "<patient_id>"
}
```

Si rechaza la petición, el Authorization Server responde con la respuesta de error de OAuth 2.0 y el código HTTP 400 ([RFC 6749, §5.2](https://www.rfc-editor.org/rfc/rfc6749.html#section-5.2))[^rfc6749-token-error]. **SHALL** rechazarla en las condiciones de la [Tabla 3.3-8](volume-2-hix-2.html#tabla-3-3-8).

**Tabla 3.3-8:** Rechazos en el token endpoint
{: #tabla-3-3-8}

| Condición | Error | Motivo |
| --- | --- | --- |
| El `code_verifier` no corresponde al `code_challenge` de la autorización | `invalid_grant`[^rfc7636-error] | Lo exige PKCE |
| El Authorization Server no puede emitir el token renovado con el contexto de paciente fijado en la autorización | `invalid_grant` | La aplicación vuelve a la petición de autorización, que resuelve el contexto otra vez |
| La renovación pide un scope mayor que el concedido | `invalid_scope` | RFC 6749 no permite ampliar el scope al renovar[^rfc6749-refresh] |
{: .table .table-bordered}

Que solo la autorización de una persona fije un contexto de paciente lo protege la [Tabla 3.1-1](volume-2-authorization.html#tabla-3-1-1) para ITI-71 y la [Tabla 3.2-3](volume-2-hix-1.html#tabla-3-2-3) para HIX-1.

##### Acciones esperadas

La aplicación valida el `id_token` conforme a OpenID Connect, como exige SMART App Launch[^smart-identity]. Presenta el access token con ITI-72 ante el Record Locator Service en las transacciones que su scope autoriza, y ante ningún otro actor. No pide ni asume un paciente distinto del que dice `patient`, como fija la [sección 2.2](volume-1-actors.html#aplicacion-del-paciente). Si recibe un refresh token nuevo al renovar, descarta el anterior[^rfc6749-refresh]. Si una renovación se rechaza con `invalid_grant`, vuelve a la petición de autorización, que resuelve el contexto otra vez.

El Record Locator Service comprueba el token con ITI-102 y toma el contexto de paciente de la respuesta de la introspección, como fija la [sección 2.2](volume-1-actors.html#record-locator-service). El Authorization Server **SHALL** incluir `patient` en esa respuesta. Con él, el Record Locator Service confina cada operación al paciente, como describe la [sección 2.5](volume-1-usecases.html#acceso-del-paciente-a-su-expediente).

**Ejemplo.** Al recibir una búsqueda ITI-67 de la aplicación, el Record Locator Service introspecciona el token con sus propias credenciales. `aud` nombra solo al Record Locator Service, `sub` a la persona que inició sesión y `patient` repite el contexto de paciente. La extensión `ihe_iua` lleva el propósito de uso `PATRQT`, porque quien actúa es la propia persona.

```http
POST /introspect HTTP/1.1
Authorization: Basic Base64(<client_id>:<client_secret>)
Accept: application/json
Content-Type: application/x-www-form-urlencoded

token=<access_token>
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "active": true,
  "iss": "<issuer>",
  "sub": "<person_sub>",
  "client_id": "<patient_app_client_id>",
  "aud": "<rls_audience>",
  "jti": "<jti>",
  "iat": 1790967016,
  "exp": 1790967316,
  "scope": "ITI-67 ITI-68",
  "token_type": "Bearer",
  "patient": "<patient_id>",
  "extensions": {
    "ihe_iua": {
      "purpose_of_use": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
          "code": "PATRQT",
          "display": "patient requested"
        }
      ]
    }
  }
}
```

### Consideraciones de seguridad

La [sección 2.2](volume-1-actors.html#authorization-server) establece los requisitos del Authorization Server para este token. La [sección 2.6](volume-1-security.html#lo-que-un-token-prueba-y-lo-que-no) explica qué prueba el token ante cada destino.

La aplicación no elige el paciente. Ningún parámetro de la petición lo identifica, el Authorization Server lo fija en la autorización y el Record Locator Service limita cada operación a ese contexto.

La renovación no vuelve a resolver el contexto de paciente. Por eso, una fusión posterior de identidades maestras no cambia los tokens de una autorización vigente. Si la identidad del token es la que la fusión absorbió, la aplicación deja de encontrar los documentos de la persona hasta el siguiente inicio de sesión, que vuelve a consultar ITI-83, y, si la fusión es correcta, nunca alcanza los de otra persona. Ese plazo lo acotan la vida del refresh token y su revocación.

El Authorization Server **SHOULD** revocar los refresh tokens de una persona cuando cierra sesión en él, cambia su credencial o retira la autorización a la aplicación. **SHOULD** también dejar vencer el refresh token que la aplicación no usa durante el tiempo que fije la comunidad.

> **Nota.** RFC 9700 deja que el Authorization Server revoque los refresh tokens ante un evento de seguridad, como un cambio de contraseña o un cierre de sesión, y recomienda que venzan cuando el cliente deja de usarlos[^rfc9700-refresh]. La aplicación del paciente suele ser un cliente público, y IUA admite que su refresh token sea de larga vida[^iua-security]. Cada nuevo inicio de sesión vuelve además a resolver la identidad con ITI-83. Por esta razón, HIX-2 recomienda revocar el refresh token en esos casos y dejarlo vencer cuando no se usa.

Del contexto que fija el lanzamiento, solo `patient` pasa al token mediado de [HIX-1](volume-2-hix-1.html), como establece la [sección 2.2](volume-1-actors.html#authorization-server). El `id_token` y `fhirUser` se quedan en la aplicación. Quien confina las consultas a ese expediente es el Record Locator Service, y el custodio **MAY** comprobarlo además, como explica la [sección 2.6](volume-1-security.html#lo-que-un-token-prueba-y-lo-que-no).

#### Consideraciones de auditoría {#consideraciones-de-auditoria}

El Authorization Server registra cada lanzamiento y cada renovación, concedidos o rechazados, con el evento que IUA define para ITI-71 ([IUA, §3.71.5.1](https://profiles.ihe.net/ITI/IUA/index.html#37151-security-audit-considerations))[^iua-audit], como indica la [Tabla 3-2](volume-2.html#tabla-3-2). IUA no define un evento para la renovación, y HIX usa para ella el mismo.

El evento de IUA no incluye al paciente, porque su único Participant Object es el token[^iua-audit-object]. Cuando hay contexto de paciente, el Authorization Server **SHALL** incluir en el evento la identidad maestra como paciente. Los patrones de BALP con paciente sirven de referencia para hacerlo ([BALP, §3:5.7.3](https://profiles.ihe.net/ITI/BALP/content.html#3573-restful-activities))[^balp-rest].

La consulta ITI-83 con la que el Authorization Server resuelve la identidad se registra con su propio evento, como indica la [Tabla 3-2](volume-2.html#tabla-3-2). Ningún registro contiene un token completo ni un refresh token, según la regla común de los [registros de auditoría](volume-2.html#registros-de-auditoria). El perfil de AuditEvent de este evento se especificará en una versión posterior de esta guía.

### Referencias

Las citas reproducen el texto publicado por su fuente. Los recortes se marcan con "[...]" y la negrita es de esta guía.

[^iua-grants]: [IUA, §34.1.1.1 Authorization Client](https://profiles.ihe.net/ITI/IUA/index.html#34111-authorization-client): "The Get Access Token [ITI-71] transaction **is scoped to the Authorization Code and Client Credential grant types** (see ITI TF-1: 34.4.1.1 Authorization Grant Types)." [§34.4.1.1 Authorization Grant Types](https://profiles.ihe.net/ITI/IUA/index.html#34411-authorization-grant-types): "This profile specifies the use of the Authorization Code and Client Credential grant types. **Actors of this profile may support other grant types as well.**"
[^iua-smart]: [IUA, Relation to SMART-on-FHIR](https://profiles.ihe.net/ITI/IUA/index.html#relation-to-smart-on-fhir): "**IUA is not based on SMART-on-FHIR, but does strive to not conflict with that standard.**"
[^iua-mhd-scope]: [IUA, §3.67.5.2 Use with the Internet User Authorization (IUA) Profile](https://profiles.ihe.net/ITI/IUA/index.html#36752-use-with-the-internet-user-authorization-iua-profile): "**scope: ITI-67 This scope request authorizes the full [ITI-67] transaction.**" (énfasis añadido)
[^smart-standalone]: [SMART App Launch, Launch App: Standalone Launch](https://hl7.org/fhir/smart-app-launch/app-launch.html#launch-app-standalone-launch): "In SMART’s standalone launch flow, **a user selects an app from outside the EHR** (for example, by tapping an app icon on a mobile phone home screen)." [Obtain authorization code](https://hl7.org/fhir/smart-app-launch/app-launch.html#obtain-authorization-code): "launch conditional When using the EHR Launch flow, this must match the launch value received from the EHR. **Omitted when using the Standalone Launch.**"
[^iua-code-request]: [IUA, §3.71.4.1.2.2 Authorization Code grant type](https://profiles.ihe.net/ITI/IUA/index.html#3714122-authorization-code-grant-type): "**resource (optional): Single valued identifier of the Resource Server endpoint to be accessed** [...] **code_challenge (required)** [...] **redirect_uri (optional)** [...] This parameter is required if the Authorization Client is registered at the Authorization Server with multiple redirect URI, optional otherwise [...] **code_verifier: The original code verifier string.**" (énfasis añadido)
[^smart-aud]: [SMART App Launch, Obtain authorization code](https://hl7.org/fhir/smart-app-launch/app-launch.html#obtain-authorization-code): "Note that **the aud parameter is semantically equivalent to the resource parameter defined in RFC8707**. [...] For the current release, **servers SHALL support the aud parameter and MAY support a resource parameter as a synonym for aud**."
[^smart-well-known]: [SMART App Launch, FHIR Authorization Endpoint and Capabilities Discovery using a Well-Known Uniform Resource Identifiers (URIs)](https://hl7.org/fhir/smart-app-launch/conformance.html#using-well-known): "**FHIR endpoints requiring authorization SHALL serve a JSON document at the location formed by appending /.well-known/smart-configuration to their base URL.** The server SHALL convey the FHIR OAuth authorization endpoints and any optional SMART Capabilities it supports [...]"
[^smart-authorize]: [SMART App Launch, Obtain authorization code](https://hl7.org/fhir/smart-app-launch/app-launch.html#obtain-authorization-code): "Note on PKCE Support: **the EHR SHALL ensure that the code_verifier is present and valid when the code is exchanged for an access token.** [...] **redirect_uri required** Must match one of the client's pre-registered redirect URIs. [...] **code_challenge_method required** [...] **The app SHALL validate the value of the state parameter upon return to the redirect URL** [...]"
[^smart-pkce]: [SMART App Launch, Considerations for PKCE Support](https://hl7.org/fhir/smart-app-launch/app-launch.html#considerations-for-pkce-support): "**All SMART apps SHALL support Proof Key for Code Exchange (PKCE).** [...] **SMART servers SHALL support the S256 code_challenge_method and SHALL NOT support the plain method.**"
[^smart-scopes]: [SMART App Launch, Scopes for requesting context data](https://hl7.org/fhir/smart-app-launch/scopes-and-launch-context.html#scopes-for-requesting-context-data): "**launch/patient Need patient context at launch time (FHIR Patient resource).**" [Scopes for requesting identity data](https://hl7.org/fhir/smart-app-launch/scopes-and-launch-context.html#scopes-for-requesting-identity-data): "Some apps need to authenticate the end-user. This can be accomplished by **requesting the scope openid**. When the openid scope is requested, apps can also request **the fhirUser scope to obtain a FHIR resource representation of the current user**."
[^smart-refresh]: [SMART App Launch, Refresh access token](https://hl7.org/fhir/smart-app-launch/app-launch.html#refresh-access-token): "**no new permissions can be obtained at refresh time** [...] if the app was launched from within a patient context, **parameters to communicate the context values MAY BE included.**" (énfasis añadido)
[^smart-introspection]: [SMART App Launch, Token Introspection, Conditional fields in the introspection response](https://hl7.org/fhir/smart-app-launch/token-introspection.html#conditional-fields-in-the-introspection-response): "SMART Launch Context. **If a launch context parameter defined in Scopes and Launch Context (e.g., patient or intent) was included in the original access token response, the parameter SHALL be included in the token introspection response.** [...] ID Token Claims. If an id_token was included in the original access token response, the following claims from the ID Token **SHOULD** be included in the Token Introspection response: [...] fhirUser"
[^rfc8707-resource]: [RFC 8707, §2 Resource Parameter](https://www.rfc-editor.org/rfc/rfc8707.html#section-2): "**resource Indicates the target service or resource to which access is being requested.** [...] **invalid_target The requested resource is invalid, missing, unknown, or malformed.** **The authorization server SHOULD audience-restrict issued access tokens to the resource(s) indicated by the "resource" parameter. Audience restrictions can be communicated in JSON Web Tokens [RFC7519] with the "aud" claim** [...] **The authorization server may use the exact "resource" value as the audience or it may map from that value to a more general URI or abstract identifier for the given resource.**"
[^iua-security]: [IUA, §3.71.5 Security Considerations](https://profiles.ihe.net/ITI/IUA/index.html#3715-security-considerations): "Access token should be short-lived with a lifetime of 1 hour or less. [...] **Refresh token may be long lived.** [...] To reduce the attack surface, client claims and authorization grants shall be the minimal; i.e., **the authorization grant scope requested by the Authorization Client shall be the minimal required scope** for the resource request to be used for."
[^iua-code-actions]: [IUA, §3.71.4.1.3.2 Authorization Code grant type](https://profiles.ihe.net/ITI/IUA/index.html#3714132-authorization-code-grant-type): "**The Authorization Server shall authenticate confidential and credential clients** [...] If valid, **the Authorization Server shall authenticate the user and obtain the user consent** [...]" (énfasis añadido)
[^oidc-offline]: [OpenID Connect Core 1.0, §11 Offline Access](https://openid.net/specs/openid-connect-core-1_0.html#OfflineAccess): "**When offline access is requested, a prompt parameter value of consent MUST be used unless other conditions for processing the request permitting offline access to the requested resources are in place. The OP MUST always obtain consent to returning a Refresh Token that enables offline access to the requested resources.** A previously saved user consent is not always sufficient to grant offline access."
[^oidc-refresh]: [OpenID Connect Core 1.0, §12.2 Successful Refresh Response](https://openid.net/specs/openid-connect-core-1_0.html#RefreshTokenResponse): "Upon successful validation of the Refresh Token, the response body is the Token Response of Section 3.1.3.3 [...] **except that it might not contain an id_token**. If an ID Token is returned as a result of a token refresh request, the following requirements apply: **its iss Claim Value MUST be the same as in the ID Token issued when the original authentication occurred, its sub Claim Value MUST be the same as in the ID Token issued when the original authentication occurred** [...]"
[^rfc6749-authz-error]: [RFC 6749, §4.1.2.1 Error Response](https://www.rfc-editor.org/rfc/rfc6749.html#section-4.1.2.1): "If the request fails due to a missing, invalid, or mismatching redirection URI, or if the client identifier is missing or invalid, **the authorization server SHOULD inform the resource owner of the error and MUST NOT automatically redirect the user-agent to the invalid redirection URI.** [...] **temporarily_unavailable** The authorization server is currently unable to handle the request due to a temporary overloading or maintenance of the server." (énfasis añadido)
[^rfc7636-error]: [RFC 7636, §4.4.1 Error Response](https://www.rfc-editor.org/rfc/rfc7636.html#section-4.4.1): "If the server requires Proof Key for Code Exchange (PKCE) by OAuth public clients and the client does not send the "code_challenge" in the request, **the authorization endpoint MUST return the authorization error response with the "error" value set to "invalid_request"**. [...] If the server supporting PKCE does not support the requested transformation, **the authorization endpoint MUST return the authorization error response with "error" value set to "invalid_request"**." [§4.6 Server Verifies code_verifier before Returning the Tokens](https://www.rfc-editor.org/rfc/rfc7636.html#section-4.6): "If the values are not equal, **an error response indicating "invalid_grant"** as described in Section 5.2 of [RFC6749] MUST be returned."
[^smart-token]: [SMART App Launch, Obtain access token](https://hl7.org/fhir/smart-app-launch/app-launch.html#obtain-access-token): "For public apps, **authentication is not required because a client with no secret cannot prove its identity** when it issues a call. [...] For confidential apps, authentication is required. [...] **code_verifier required** This parameter is used to verify against the code_challenge parameter previously provided in the authorize request. **client_id conditional Required for public apps.** Omit for confidential apps."
[^rfc6749-client-id]: [RFC 6749, §3.2.1 Client Authentication](https://www.rfc-editor.org/rfc/rfc6749.html#section-3.2.1): "**A client MAY use the "client_id" request parameter to identify itself when sending requests to the token endpoint.** In the "authorization_code" "grant_type" request to the token endpoint, an unauthenticated client MUST send its "client_id" to prevent itself from inadvertently accepting a code intended for a client with a different "client_id"."
[^rfc6749-refresh]: [RFC 6749, §6 Refreshing an Access Token](https://www.rfc-editor.org/rfc/rfc6749.html#section-6): "**The requested scope MUST NOT include any scope not originally granted by the resource owner, and if omitted is treated as equal to the scope originally granted by the resource owner.** [...] Because refresh tokens are typically long-lasting credentials used to request additional access tokens, **the refresh token is bound to the client to which it was issued**. [...] The authorization server MAY issue a new refresh token, in which case **the client MUST discard the old refresh token and replace it with the new refresh token**."
[^iua-state]: [IUA, §3.71.4.1.2.2 Authorization Code grant type](https://profiles.ihe.net/ITI/IUA/index.html#3714122-authorization-code-grant-type): "state (required): An unguessable value used by the client to track the state between the authorization request and the callback to the redirect URI. While this parameter is optional in the OAuth 2.1 Authorization Framework [...] **it is required in this profile for security reasons**." (énfasis añadido)
[^rfc9700-redirect]: [RFC 9700, §2.1 Protecting Redirect-Based Flows](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.1): "When comparing client redirection URIs against pre-registered URIs, **authorization servers MUST utilize exact string matching** except for port numbers in localhost redirection URIs of native apps" (énfasis añadido)
[^rfc9700-refresh]: [RFC 9700, §4.14.2 Recommendations](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.14.2): "**Authorization servers MUST utilize one of these methods to detect refresh token replay by malicious actors for public clients** [...] The authorization server cannot determine which party submitted the invalid refresh token, **but it will revoke the active refresh token.** [...] **Authorization servers MAY revoke refresh tokens automatically in case of a security event** [...] **Refresh tokens SHOULD expire if the client has been inactive for some time**" (énfasis añadido)
[^iua-response]: [IUA, §3.71.4.2.2 Message Semantics](https://profiles.ihe.net/ITI/IUA/index.html#371422-message-semantics): "scope (required): The scope granted by the Authorization Server. [...] refresh_token (optional): A token provided by the Authorization Server which can be used by the Authorization Client **to obtain new access tokens using the same authorization grant**. [...] **The Authorization Server shall include the HTTP Cache-Control response header field with value no-store and the Pragma response header field value no-cache** to the access token response [...]"
[^rfc6749-token-response]: [RFC 6749, §5.1 Successful Response](https://www.rfc-editor.org/rfc/rfc6749.html#section-5.1): "scope OPTIONAL, if identical to the scope requested by the client; otherwise, REQUIRED. **The scope of the access token** as described by Section 3.3."
[^rfc6749-token-error]: [RFC 6749, §5.2 Error Response](https://www.rfc-editor.org/rfc/rfc6749.html#section-5.2): "The authorization server **responds with an HTTP 400 (Bad Request) status code (unless specified otherwise)** and includes the following parameters with the response: **error REQUIRED.** [...] **invalid_grant** The provided authorization grant (e.g., authorization code, resource owner credentials) or refresh token **is invalid, expired, revoked**, does not match the redirection URI used in the authorization request, or was issued to another client. [...] **invalid_scope** The requested scope is invalid, unknown, malformed, or **exceeds the scope granted by the resource owner**."
[^smart-identity]: [SMART App Launch, Scopes for requesting identity data](https://hl7.org/fhir/smart-app-launch/scopes-and-launch-context.html#scopes-for-requesting-identity-data): "**This token must be validated according to the OIDC specification.** To learn more about the user, the app should treat the fhirUser claim as the URL of a FHIR resource representing the current user."
[^iua-audit]: [IUA, §3.71.5.1 Security Audit Considerations](https://profiles.ihe.net/ITI/IUA/index.html#37151-security-audit-considerations): "The Authorization Client or Authorization Server that is grouped with an ATNA Secure Node or Secure Application **shall be able to send an audit event as defined below** [...] EventID [...] EV(110114, DCM, "User Authentication") [...] EventTypeCode [...] **EV("ITI-71", IHE, "User Authorization")**".
[^iua-audit-object]: [IUA, §3.71.5.1 Security Audit Considerations](https://profiles.ihe.net/ITI/IUA/index.html#37151-security-audit-considerations): "Source (1) Human Requestor (0) Destination (0) Audit Source (Client Authentication Agent) (1) **Participant Object (1)** [...] **Token** [...] ParticipantObjectTypeCode M "2" (System) [...] ParticipantObjectTypeCodeRole M "13" (Security Resource)"
[^balp-rest]: [BALP, §3:5.7.3 RESTful activities](https://profiles.ihe.net/ITI/BALP/content.html#3573-restful-activities): "When a FHIR RESTful interaction happens, **the following AuditEvent patterns can be used**. [...] There are two sets of profiles distinguished by **Patient as a subject** being mandated to be populated."

*[IUA]: Internet User Authorization, perfil IHE que aplica OAuth 2.0 a las transacciones sobre FHIR
*[PIXm]: Patient Identifier Cross-referencing for mobile, perfil IHE que enlaza los MRN de un paciente con su identidad maestra
*[ATNA]: Audit Trail and Node Authentication, perfil IHE de auditoría y seguridad de los nodos
*[BALP]: Basic Audit Log Patterns, perfil IHE con los patrones de AuditEvent de FHIR
