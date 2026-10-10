Mediated Token Exchange [HIX-1] es la transacción con la que el Record Locator Service obtiene un token para llamar, en nombre de un solicitante, a un custodio y, según el despliegue, a otro Resource Server central, como fija la [sección 2.2](volume-1-actors.html#record-locator-service). Ningún perfil IHE define esta transacción, y esta página la especifica.

### Alcance

El token que el Record Locator Service obtiene del Authorization Server con HIX-1 es el [token mediado](appendix-glossary.html#token-mediado), que vale ante el destino que nombra su `resource`, nunca ante dos custodios, y para un solo tipo de transacción. Lo necesita porque el [token del solicitante](appendix-glossary.html#token-del-solicitante) nunca sale de la infraestructura central, como fija la [sección 2.6](volume-1-security.html#modelo-de-confianza).

La [Figura 3.2-1](volume-2-hix-1.html#figura-3-2-1) muestra qué token se presenta en cada llamada de una recuperación y ante qué destino vale. También muestra que el token del solicitante no sale de la infraestructura central.

![Recorrido de los tokens en una recuperación](hix-2-hix-1-recorrido.svg)

**Figura 3.2-1:** Recorrido de los tokens en una recuperación
{: #figura-3-2-1}

Solo el Record Locator Service puede solicitar HIX-1.

### Roles de actor

La [Tabla 3.2-1](volume-2-hix-1.html#tabla-3-2-1) muestra el rol de IUA de cada actor de HIX en esta transacción, según la [sección 2.4](volume-1-groupings.html).

**Tabla 3.2-1:** Roles de actor
{: #tabla-3-2-1}

| Actor | Rol | Qué hace |
| --- | --- | --- |
| Record Locator Service | [Authorization Client](https://profiles.ihe.net/ITI/IUA/index.html#34111-authorization-client) | Pide, en nombre de un solicitante, un token para un destino y un solo tipo de transacción |
| Authorization Server | [Authorization Server](https://profiles.ihe.net/ITI/IUA/index.html#34112-authorization-server) | Valida los tokens de la petición y emite el token mediado |
{: .table .table-bordered}

### Estándares referenciados

HIX-1 se apoya en los documentos siguientes.

- [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749), The OAuth 2.0 Authorization Framework, octubre de 2012. Aporta el token endpoint, la autenticación del cliente y la respuesta de error.
- [RFC 8693](https://www.rfc-editor.org/rfc/rfc8693), OAuth 2.0 Token Exchange, enero de 2020. Aporta el grant de intercambio, sus parámetros y el claim `act`.
- [RFC 8707](https://www.rfc-editor.org/rfc/rfc8707), Resource Indicators for OAuth 2.0, febrero de 2020. Aporta el parámetro `resource` y el error `invalid_target`.
- [RFC 9068](https://www.rfc-editor.org/rfc/rfc9068), JSON Web Token (JWT) Profile for OAuth 2.0 Access Tokens, octubre de 2021. Aporta la forma del token mediado y su validación en el destino.
- [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519), JSON Web Token (JWT), mayo de 2015. Aporta los claims del token, entre ellos `aud` y `jti`.
- [IUA](https://profiles.ihe.net/ITI/IUA/index.html), Internet User Authorization, revisión 2.5, junio de 2026. Aporta ITI-71, con el que el Record Locator Service obtiene su token de actor, ITI-72, con el que presenta el token mediado, y las extensiones `ihe_iua` que el token mediado copia del token del solicitante.

> **Nota.** HIX-1 se apoya en ITI-71. El Record Locator Service obtiene con ITI-71 su token de actor, y el intercambio usa el mismo token endpoint del Authorization Server con otro grant. IUA limita [ITI-71](https://profiles.ihe.net/ITI/IUA/index.html#371-get-access-token-iti-71) a los grants Authorization Code y Client Credentials, y de RFC 8693 solo toma el parámetro `requested_token_type` ([IUA, §3.71.4.1.2.1](https://profiles.ihe.net/ITI/IUA/index.html#3714121-client-credential-grant-type)). Admite que sus actores soporten otros grants ([IUA, §34.4.1.1](https://profiles.ihe.net/ITI/IUA/index.html#34411-authorization-grant-types))[^iua-grants], y HIX-1 especifica uno de ellos, el grant Token Exchange de RFC 8693 con un resource indicator de RFC 8707.

### Mensajes

La [Figura 3.2-2](volume-2-hix-1.html#figura-3-2-2) muestra los mensajes de la transacción. Los dos primeros corresponden a [ITI-71](volume-2-authorization.html#iti-71): el Record Locator Service usa el grant Client Credentials para obtener su token de actor si no tiene uno vigente. Los dos últimos corresponden a HIX-1.

![Mediated Token Exchange](hix-2-hix-1.svg)

**Figura 3.2-2:** Mediated Token Exchange
{: #figura-3-2-2}

#### Petición de intercambio {#peticion-de-intercambio}

##### Evento desencadenante

Para llamar a un custodio, el Record Locator Service obtiene un token mediado mediante HIX-1. Para llamar a un actor central desplegado como un sistema distinto lo obtiene también, salvo que la comunidad autorice un token propio, como fija la [sección 2.2](volume-1-actors.html#record-locator-service). Para obtener el token mediado, presenta al Authorization Server su token de actor y el token del solicitante.

Las llamadas internas a un mismo sistema no pasan por HIX-1, como fija la [sección 2.2](volume-1-actors.html#record-locator-service). Si el destino es un custodio, primero aplica la decisión de divulgación: un puntero cuya divulgación se niega no origina ningún intercambio, como fija la [sección 2.2](volume-1-actors.html#record-locator-service). En todos los casos, comprueba antes el token del solicitante con ITI-102.

##### Semántica del mensaje

La petición sigue RFC 8693: un POST al token endpoint del Authorization Server con los parámetros en el body, codificados como `application/x-www-form-urlencoded` ([RFC 8693, §2.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.1))[^rfc8693-request].

> **Nota.** RFC 8693 define `actor_token` como opcional en una solicitud general de Token Exchange ([§2.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.1))[^rfc8693-request]. HIX-1 lo requiere porque usa semántica de delegación, en la que `subject_token` representa al solicitante y `actor_token` al Record Locator Service, que actúa en su nombre ([§1.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-1.1))[^rfc8693-delegation]. Una petición que solo lleva `subject_token` no expresa delegación ([Apéndice A.1.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-a.1.1))[^rfc8693-impersonation]. Además, separa las dos identidades en juego. La autenticación del cliente prueba quién llama al token endpoint, y el `actor_token` aporta el actor de la delegación que queda en el token mediado.

**Tabla 3.2-2:** Parámetros de la petición de intercambio
{: #tabla-3-2-2}

| Parámetro | Valor en HIX |
| --- | --- |
| `grant_type` | `urn:ietf:params:oauth:grant-type:token-exchange` |
| `subject_token` | El token del solicitante, tal como llegó en la petición que el Record Locator Service atiende |
| `subject_token_type` | `urn:ietf:params:oauth:token-type:access_token` |
| `actor_token` | El token de actor, es decir, el token propio del Record Locator Service. Lo obtiene con [ITI-71](volume-2-authorization.html#iti-71) y el grant Client Credentials, con el Authorization Server como `resource` y sin `scope`, porque solo lo presenta ante él. Puede reutilizarlo mientras esté vigente y lo renueva antes de que venza |
| `actor_token_type` | `urn:ietf:params:oauth:token-type:access_token` |
| `resource` | Uno solo. Para un custodio, el endpoint que publica el directorio de la comunidad. Para un actor central, el identificador que la comunidad registra para él en el Authorization Server y que ese actor espera en `aud`. Nunca uno que llegue en la petición del solicitante o en un puntero |
| `scope` | Solo el identificador de la transacción que el Record Locator Service va a realizar, por ejemplo `ITI-68` ante un custodio, `ITI-67` ante el Document Registry o `ITI-90` ante el directorio de la comunidad |
| `requested_token_type` | Opcional. Si se envía, `urn:ietf:params:oauth:token-type:access_token` |
{: .table .table-bordered}

El Record Locator Service se autentica en el token endpoint como cliente confidencial, con el método que acuerde con el Authorization Server ([RFC 6749, §2.3](https://www.rfc-editor.org/rfc/rfc6749.html#section-2.3)).

La petición no incluye la organización, el propósito de uso ni el contexto de paciente. Estos datos se propagan automáticamente desde el token del solicitante al token mediado, como fija la [sección 2.2](volume-1-actors.html#authorization-server).

El `resource` sale del directorio porque el directorio es el único origen de los endpoints que usa la infraestructura central, como fija la [sección 2.2](volume-1-actors.html#directorio-de-la-comunidad). El Authorization Server restringe la audiencia del token a los Resource Servers que asocia a ese `resource`, y a ese único custodio cuando nombra a uno, como recomienda RFC 8707 ([RFC 8707, §2](https://www.rfc-editor.org/rfc/rfc8707.html#section-2)). La petición no lleva `audience`. RFC 8693 lo trataría como otro destino, y el token emitido sería válido en todos los destinos indicados ([RFC 8693, §2.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.1) y [§2.1.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.1.1))[^rfc8707-resource].

RFC 8693 distingue la delegación de la suplantación: en la delegación, quien actúa conserva su identidad y representa a otro. Aquí, `subject_token` representa al solicitante y `actor_token` al Record Locator Service ([RFC 8693, §1.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-1.1)). El claim `act` del token mediado procede del `actor_token` e identifica al actor de la delegación ([RFC 8693, §4.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-4.1))[^rfc8693-delegation]. El destino **SHOULD** comprobar ese claim, como recomienda la [sección 2.6](volume-1-security.html#validacion-en-el-custodio).

##### Acciones esperadas

Además de validar cada token que recibe, como exige RFC 8693 ([RFC 8693, §2.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.1))[^rfc8693-request], el Authorization Server **SHALL** comprobar lo siguiente.

1. Que el `subject_token` y el `actor_token` son access tokens vigentes que emitió él.
2. Que la audiencia del `subject_token` incluye al Record Locator Service, de modo que no se intercambie un token pensado para otro destino.
3. Que el `subject_token` no lleva `act`, es decir, que no es un token mediado. Un token mediado no se vuelve a intercambiar.
4. Que el `actor_token` identifica al Record Locator Service, coincide con el cliente autenticado y tiene como audiencia al Authorization Server.
5. Que hay un solo `resource`, registrado como destino y dentro de la delegación registrada para el Record Locator Service.
6. Que el scope identifica una sola transacción y está contenido en la delegación registrada para el Record Locator Service ante el destino. Además, que está contenido en el scope del `subject_token`, salvo cuando la transacción es ITI-90 y la delegación registrada la permite ante el directorio.

Después emite el token mediado conforme a la [sección 2.2](volume-1-actors.html#authorization-server), que fija su audiencia, sujeto, extensiones, scope y vida. Si alguna comprobación falla, **SHALL** rechazar la petición como indica la [Tabla 3.2-3](volume-2-hix-1.html#tabla-3-2-3). La respuesta de error es la de OAuth 2.0, con el parámetro `error` y el código HTTP 400, salvo que la tabla indique otro.

**Tabla 3.2-3:** Rechazos que HIX añade al intercambio
{: #tabla-3-2-3}

| Condición | Error | Motivo |
| --- | --- | --- |
| Falta el `actor_token` | `invalid_request` | HIX expresa la delegación como la describe RFC 8693, con el `actor_token` en la petición y el claim `act` en el token resultante ([RFC 8693, §1.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-1.1))[^rfc8693-delegation] |
| El `actor_token` no identifica al Record Locator Service | `invalid_request` | El claim `act` sale del `actor_token`, y el destino comprueba que el actor es el Record Locator Service, como fija la [sección 2.6](volume-1-security.html#validacion-en-el-custodio) |
| La petición no lleva exactamente un `resource`, o lleva `audience` | `invalid_target` | Un solo `resource` deja la audiencia en manos del Authorization Server, y `audience` añadiría destinos que él no controla, como explica la [sección 2.6](volume-1-security.html#modelo-de-confianza) |
| El cliente autenticado no es el Record Locator Service | `unauthorized_client` | Solo el Record Locator Service puede pedir un token a nombre de otro, como fija la [sección 2.2](volume-1-actors.html#authorization-server) |
| La autenticación del cliente falla | `invalid_client`, con el código HTTP 401 | RFC 6749 lo exige cuando el cliente se autentica con el header `Authorization`, como en el ejemplo, y lo admite en los demás casos ([RFC 6749, §5.2](https://www.rfc-editor.org/rfc/rfc6749.html#section-5.2))[^rfc8693-error] |
| Un token es inválido o ha expirado, el `subject_token` no tiene al Record Locator Service en su audiencia o ya lleva `act`, o el `actor_token` no tiene al Authorization Server en su audiencia | `invalid_request` | RFC 8693 prevé ese código para un `subject_token` o un `actor_token` que no es válido o que la política no acepta ([RFC 8693, §2.2.2](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.2.2))[^rfc8693-error] |
| El `resource` no es un destino registrado o queda fuera de la delegación | `invalid_target` | RFC 8707 prevé ese código para un destino que el Authorization Server no acepta ([RFC 8707, §2](https://www.rfc-editor.org/rfc/rfc8707.html#section-2))[^rfc8707-resource] |
| El scope está vacío, pide más de una transacción, pide un valor que no es una transacción, como `launch/patient`, no está contenido en la delegación registrada ante el destino, o no está contenido en el scope del solicitante y no es ITI-90 ante el directorio | `invalid_scope` | El token mediado autoriza una sola transacción y cumple los límites de scope de la [sección 2.2](volume-1-actors.html#authorization-server) |
{: .table .table-bordered}

#### Respuesta de intercambio {#respuesta-de-intercambio}

##### Evento desencadenante

El Authorization Server responde a cada petición de intercambio con un token mediado o con un error.

##### Semántica del mensaje

El Authorization Server responde a un intercambio concedido con el código HTTP 200 y un body JSON con los parámetros de la respuesta de RFC 8693 ([RFC 8693, §2.2.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.2.1))[^rfc8693-response]. La [Tabla 3.2-4](volume-2-hix-1.html#tabla-3-2-4) fija sus valores en HIX.

**Tabla 3.2-4:** Parámetros de la respuesta de intercambio
{: #tabla-3-2-4}

| Parámetro | Valor en HIX |
| --- | --- |
| `access_token` | El token mediado, un JWT de acceso conforme a RFC 9068 |
| `issued_token_type` | `urn:ietf:params:oauth:token-type:access_token`, porque es un access token que el Record Locator Service no necesita leer |
| `token_type` | `Bearer`, porque el Record Locator Service lo presenta con ITI-72 |
| `expires_in` | La vida del token en segundos, que no supera los dos minutos ni la vida restante del token del solicitante, como fija la [sección 2.2](volume-1-actors.html#authorization-server) |
| `scope` | Puede omitirse, porque el scope concedido es siempre el pedido, como fija la [sección 2.2](volume-1-actors.html#authorization-server) |
| `refresh_token` | El Authorization Server **SHALL NOT** incluirlo. El token mediado no se renueva, y cada transacción pide el suyo |
{: .table .table-bordered}

El contenido del token mediado se especifica en los requisitos del [Authorization Server](volume-1-actors.html#authorization-server) y lo resume la [Tabla 2.6-1](volume-1-security.html#tabla-2-6-1).

El Authorization Server responde a un intercambio rechazado con la respuesta de error de OAuth 2.0 y el código indicado en la [Tabla 3.2-3](volume-2-hix-1.html#tabla-3-2-3).

##### Acciones esperadas

El Record Locator Service **SHALL** presentar el token mediado mediante ITI-72 únicamente ante el destino indicado en `resource` y en la transacción para la que lo obtuvo, y **SHALL NOT** entregarlo al solicitante, como fija la [sección 2.6](volume-1-security.html#modelo-de-confianza).

Si el intercambio se rechaza, el Record Locator Service **SHALL NOT** llamar al destino, ni con el token del solicitante ni con el token de actor, porque ninguno de los dos vale ante él.

La [Tabla 3.6-3](volume-2-retrieval.html#tabla-3-6-3) fija cómo responde al solicitante si el rechazo ocurre durante una recuperación.

#### Ejemplo {#ejemplo}

El Record Locator Service pide un token para recuperar con ITI-68 un documento de un custodio.

```http
POST /token HTTP/1.1
Authorization: Basic Base64(<client_id>:<client_secret>)
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:token-exchange
&subject_token=<subject_token>
&subject_token_type=urn:ietf:params:oauth:token-type:access_token
&actor_token=<actor_token>
&actor_token_type=urn:ietf:params:oauth:token-type:access_token
&resource=<custodian_endpoint>
&scope=ITI-68
```

El Authorization Server concede el intercambio. El token mediado vive 120 segundos, el máximo que admite HIX, y la respuesta no lleva `refresh_token`.

```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store
Pragma: no-cache

{
  "access_token": "<access_token>",
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "token_type": "Bearer",
  "expires_in": 120,
  "scope": "ITI-68"
}
```

El token mediado de la respuesta se decodifica así. Su `aud` es solo el endpoint del custodio, el mismo que la petición llevaba en `resource`. Su `sub` y sus extensiones de IUA son los del token del solicitante, y `client_id` y `act` nombran al Record Locator Service. `exp` queda 120 segundos después de `iat`.

```json
{
  "alg": "RS256",
  "typ": "at+jwt",
  "kid": "<kid>"
}
```

```json
{
  "iss": "<issuer>",
  "aud": "<custodian_endpoint>",
  "sub": "<requester_client_id>",
  "client_id": "<rls_client_id>",
  "act": {
    "sub": "<rls_client_id>"
  },
  "scope": "ITI-68",
  "iat": 1790788733,
  "exp": 1790788853,
  "jti": "<jti>",
  "extensions": {
    "ihe_iua": {
      "subject_organization_id": "<organization_id>",
      "purpose_of_use": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
          "code": "TREAT",
          "display": "treatment"
        }
      ]
    }
  }
}
```

Si el token del solicitante tiene contexto de paciente, el token mediado lo lleva en el claim `patient`, con el mismo valor que la respuesta de token de [HIX-2](volume-2-hix-2.html#respuesta-de-token).

Si la petición llevara dos `resource`, el Authorization Server la rechazaría con el código HTTP 400 y el error `invalid_target`.

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json
Cache-Control: no-store

{
  "error": "invalid_target"
}
```

### Consideraciones de seguridad

La [sección 2.6](volume-1-security.html) fija cómo el destino [valida](volume-1-security.html#validacion-en-el-custodio) el token mediado, cómo se [contiene una credencial comprometida](volume-1-security.html#contencion-de-una-credencial-comprometida) y qué [riesgos quedan](volume-1-security.html#riesgos-residuales). De ellos, cuatro afectan directamente a esta transacción.

1. Un Record Locator Service comprometido solo puede intercambiar los tokens de solicitantes que recibe, mientras están vigentes y dentro de su scope, salvo ITI-90, que la delegación registrada le permite ante el directorio.
2. Un token mediado robado vale ante el destino que nombra su `resource`, nunca ante dos custodios, para un solo tipo de transacción y durante dos minutos como máximo. El Record Locator Service **SHALL** usar cada token mediado solo en la transacción para la que lo pidió, y el destino **MAY** rechazar un `jti` que ya vio.
3. El Authorization Server **SHALL NOT** revelar en `error_description` qué destinos existen ni el contenido de un token.
4. La vida máxima de dos minutos solo significa lo mismo en cada extremo si los relojes coinciden, y por eso cada actor es Time Client de CT, como fija la [sección 2.4](volume-1-groupings.html#lo-que-casi-todos-agrupan).

#### Consideraciones de auditoría {#consideraciones-de-auditoria}

IHE no define ningún evento de auditoría para un intercambio de tokens. IUA solo define un evento de auditoría para la emisión de tokens en ITI-71 ([IUA, §3.71.5.1](https://profiles.ihe.net/ITI/IUA/index.html#37151-security-audit-considerations))[^iua-audit], y HIX-1 no es ITI-71. La obtención del token de actor sí es un ITI-71, y se registra como indica la [Tabla 3-2](volume-2.html#tabla-3-2).

El Authorization Server **SHALL** registrar cada intercambio, concedido o rechazado. En ese registro **SHALL** enlazar, por su `jti`, el token del solicitante, el token de actor y, si lo emitió, el token mediado ([RFC 7519, §4.1.7](https://www.rfc-editor.org/rfc/rfc7519.html#section-4.1.7))[^jti]. Si rechazó el intercambio, enlaza los tokens de la petición que pueda identificar. El registro no contiene ningún token completo, como dice la regla común de los [registros de auditoría](volume-2.html#registros-de-auditoria).

Ese enlace permite seguir una divulgación desde el token del solicitante hasta el token mediado. El destino también registra este último por su identificador, como fija la [sección 2.6](volume-1-security.html#seguridad-basica).

> **Nota.** El `jti` identifica un token sin reproducirlo. Si el Authorization Server identifica un token opaco por su propio valor, el registro no guarda ese valor sino una evidencia derivada de él. BALP pide vincular el evento al token sin registrar el token completo ([BALP, §3:5.7.5](https://profiles.ihe.net/ITI/BALP/content.html#3575-oauth-security-token))[^balp-token].

### Referencias

Las citas reproducen el texto publicado por su fuente. Los recortes se marcan con "[...]" y la negrita es de esta guía.

[^iua-grants]: [IUA, §34.1.1.1 Authorization Client](https://profiles.ihe.net/ITI/IUA/index.html#34111-authorization-client): "The Get Access Token [ITI-71] transaction **is scoped to the Authorization Code and Client Credential grant types** (see ITI TF-1: 34.4.1.1 Authorization Grant Types)." [§3.71.4.1.2.1 Client Credential grant type](https://profiles.ihe.net/ITI/IUA/index.html#3714121-client-credential-grant-type): "requested_token_type (optional): The requested token format shall be urn:ietf:params:oauth:token-type:jwt, urn:ietf:params:oauth:token-type:saml2 or urn:ietf:params:oauth:token-type:access-token [**RFC 8693 OAuth 2.0 Token Exchange**, Section 3]." [§34.4.1.1 Authorization Grant Types](https://profiles.ihe.net/ITI/IUA/index.html#34411-authorization-grant-types): "This profile specifies the use of the Authorization Code and Client Credential grant types. **Actors of this profile may support other grant types as well.**"
[^rfc8693-request]: [RFC 8693, §2.1 Request](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.1): "The following parameters are included in the HTTP request entity-body using the **"application/x-www-form-urlencoded" format** [...] grant_type REQUIRED. The value **"urn:ietf:params:oauth:grant-type:token-exchange"** indicates that a token exchange is being performed. [...] **Multiple "resource" parameters may be used** to indicate that the issued token is intended to be used at the multiple resources listed. [...] subject_token REQUIRED. A security token that represents the identity of the party on behalf of whom the request is being made. [...] **actor_token OPTIONAL.** A security token that represents the identity of the acting party. [...] In processing the request, **the authorization server MUST perform the appropriate validation procedures for the indicated token type** and, if the actor token is present, also perform the appropriate validation procedures for its indicated token type." [§3 Token Type Identifiers](https://www.rfc-editor.org/rfc/rfc8693.html#section-3): "urn:ietf:params:oauth:token-type:access_token Indicates that the token is **an OAuth 2.0 access token issued by the given authorization server**."
[^rfc8707-resource]: [RFC 8707, §2 Resource Parameter](https://www.rfc-editor.org/rfc/rfc8707.html#section-2): "Its value **MUST be an absolute URI** [...] invalid_target The requested resource is invalid, missing, unknown, or malformed. **The authorization server SHOULD audience-restrict issued access tokens to the resource(s) indicated by the "resource" parameter.**" [RFC 8693, §2.1 Request](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.1): "The "audience" and "resource" parameters may be used together **to indicate multiple target services** with a mix of logical names and resource URIs." [§2.1.1 Relationship between Resource, Audience, and Scope](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.1.1): "The semantics of such a request are that the client is asking for a token with the requested scope that is **usable at all the requested target services**. [...] An authorization server can use the "invalid_target" error code, defined in Section 2.2.2, to inform a client that it requested access to too many target services simultaneously."
[^rfc8693-delegation]: [RFC 8693, §1.1 Delegation vs. Impersonation Semantics](https://www.rfc-editor.org/rfc/rfc8693.html#section-1.1): "With delegation semantics, principal A still has its own identity separate from B, and it is explicitly understood that while B may have delegated some of its rights to A, **any actions taken are being taken by A representing B**. [...] Typically, in the request, the "subject_token" represents the identity of the party on behalf of whom the token is being requested while **the "actor_token" represents the identity of the party to whom the access rights of the issued token are being delegated**. [...] The "actor_token" request parameter, however, does provide a means for providing information about the desired actor, and **the JWT "act" claim can provide a representation of a chain of delegation**." [§4.1 "act" (Actor) Claim](https://www.rfc-editor.org/rfc/rfc8693.html#section-4.1): "The act (actor) claim provides a means within a JWT to express that **delegation has occurred and identify the acting party to whom authority has been delegated**."
[^rfc8693-impersonation]: [RFC 8693, Appendix A.1.1 Token Exchange Request](https://www.rfc-editor.org/rfc/rfc8693.html#section-a.1.1): "In the following token exchange request, a client is requesting a token with impersonation semantics (**delegation is impossible with only a "subject_token" and no "actor_token"**)."
[^rfc8693-error]: [RFC 8693, §2.2.2 Error Response](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.2.2): "If the request itself is not valid or if either the "subject_token" or "actor_token" are invalid for any reason, or are unacceptable based on policy, the authorization server MUST construct an error response, as specified in Section 5.2 of [RFC6749]. **The value of the "error" parameter MUST be the "invalid_request" error code.** If the authorization server is unwilling or unable to issue a token for any target service indicated by the "resource" or "audience" parameters, **the "invalid_target" error code SHOULD be used** in the error response. [...] **Other error codes may also be used, as appropriate.**" [RFC 6749, §5.2 Error Response](https://www.rfc-editor.org/rfc/rfc6749.html#section-5.2): "The authorization server **responds with an HTTP 400 (Bad Request) status code (unless specified otherwise)** and includes the following parameters with the response: **error REQUIRED.** [...] **unauthorized_client** The authenticated client is not authorized to use this authorization grant type. [...] **invalid_scope** The requested scope is invalid, unknown, malformed, or exceeds the scope granted by the resource owner." Sobre invalid_client: "Client authentication failed [...] The authorization server MAY return an HTTP 401 (Unauthorized) status code to indicate which HTTP authentication schemes are supported. **If the client attempted to authenticate via the "Authorization" request header field, the authorization server MUST respond with an HTTP 401 (Unauthorized) status code** and include the "WWW-Authenticate" response header field matching the authentication scheme used by the client."
[^rfc8693-response]: [RFC 8693, §2.2.1 Successful Response](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.2.1): "scope **OPTIONAL if the scope of the issued security token is identical to the scope requested by the client**; otherwise, it is REQUIRED. refresh_token OPTIONAL. A refresh token will typically not be issued when the exchange is of one temporary credential (the subject_token) for a different temporary credential (the issued token) for use in some other context. [...] **Profiles or deployments of this specification should clearly document the conditions under which a client should expect a refresh token** [...]" [§3 Token Type Identifiers](https://www.rfc-editor.org/rfc/rfc8693.html#section-3): "The intent of this specification is that "urn:ietf:params:oauth:token-type:access_token" be an indicator that **the token is a typical OAuth access token issued by the authorization server in question, opaque to the client**, and usable the same manner as any other access token obtained from that authorization server."
[^iua-audit]: [IUA, §3.71.5.1 Security Audit Considerations](https://profiles.ihe.net/ITI/IUA/index.html#37151-security-audit-considerations): "The Authorization Client or Authorization Server that is grouped with an ATNA Secure Node or Secure Application **shall be able to send an audit event as defined below** [...] EventID [...] EV(110114, DCM, "User Authentication") [...] EventTypeCode [...] **EV("ITI-71", IHE, "User Authorization")**".
[^balp-token]: [BALP, §3:5.7.5 OAuth Security Token](https://profiles.ihe.net/ITI/BALP/content.html#3575-oauth-security-token): "There is still a need to include some evidence in the AuditEvent to tie this audit log entry with a specific token, but **the whole token should not be recorded for security reasons**."
[^jti]: [RFC 7519, §4.1.7 "jti" (JWT ID) Claim](https://www.rfc-editor.org/rfc/rfc7519.html#section-4.1.7): "The "jti" (JWT ID) claim **provides a unique identifier for the JWT**." [RFC 9068, §2.2 Data Structure](https://www.rfc-editor.org/rfc/rfc9068.html#section-2.2): "**jti REQUIRED** - as defined in Section 4.1.7 of [RFC7519]."

*[IUA]: Internet User Authorization, perfil IHE que aplica OAuth 2.0 a las transacciones sobre FHIR
*[ATNA]: Audit Trail and Node Authentication, perfil IHE de auditoría y seguridad de los nodos
*[BALP]: Basic Audit Log Patterns, perfil IHE con los patrones de AuditEvent de FHIR
