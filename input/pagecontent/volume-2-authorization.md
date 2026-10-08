Get Access Token [ITI-71] e Introspect Token [ITI-102] son las transacciones de IUA con las que el Authorization Server emite y comprueba los tokens. HIX las usa tal como las definen IUA y OAuth 2.0, y estas son las restricciones con que las usa.

1. El `resource` es obligatorio y nombra a la infraestructura central, o al Authorization Server en el token de actor de [HIX-1](volume-2-hix-1.html), nunca a un custodio.
2. El token de un miembro lleva siempre la organización y el propósito de uso que fija el Authorization Server.
3. El Record Locator Service introspecciona cada token una vez por operación.

Cada sección detalla estas restricciones y los rechazos que traen consigo. La [Tabla 2.6-1](volume-1-security.html#tabla-2-6-1) resume qué lleva cada token de HIX y cómo se valida.

### Get Access Token [ITI-71] {#iti-71}

#### Alcance en HIX

Con ITI-71 y el grant Client Credentials obtienen sus tokens los miembros, la fuente autoritativa de identidad, el Record Locator Service, para su token de actor de [HIX-1](volume-2-hix-1.html), y el Authorization Server, para su propia consulta ITI-83. La aplicación del paciente obtiene el suyo con [HIX-2](volume-2-hix-2.html), y el token mediado sale de [HIX-1](volume-2-hix-1.html).

#### Petición

La petición es la de [IUA](https://profiles.ihe.net/ITI/IUA/index.html#3714121-client-credential-grant-type). HIX exige el parámetro `resource` que define RFC 8707 ([RFC 8707, §2](https://www.rfc-editor.org/rfc/rfc8707.html#section-2))[^rfc8707-resource], para limitar dónde se puede usar un access token. En el token de un miembro, el `resource` nombra a la infraestructura central, así que el token vale solo ante sus Resource Servers y nunca ante un custodio ni ante otro Resource Server fuera de ella.

**Ejemplo.** Un laboratorio quiere declarar a un paciente local y publicar un resultado de laboratorio. Para ello pide al Authorization Server, con el grant `client_credentials`, un token para la infraestructura central con los scopes `ITI-104` e `ITI-65`.

```http
POST /token HTTP/1.1
Authorization: Basic Base64(<client_id>:<client_secret>)
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&resource=<central_resource>
&scope=ITI-104 ITI-65
```

El Authorization Server pone en `aud` la lista de Resource Servers centrales que la comunidad define para ese `resource`, como prevé IUA ([IUA, §3.71.4.1.3](https://profiles.ihe.net/ITI/IUA/index.html#371413-expected-actions))[^iua-71-actions]. Cuáles son depende del [despliegue](volume-1-groupings.html#sobre-los-despliegues), y el miembro pide el token de la misma forma en todos los casos.

El token puede ser opaco o un JWT, a elección de la implementación. Si es un JWT, sigue [RFC 9068](https://www.rfc-editor.org/rfc/rfc9068.html#section-2), y un Resource Server central distinto del Record Locator Service puede validarlo por sí mismo con las claves del Authorization Server, como permite la [sección 2.2](volume-1-actors.html#descripcion-de-actores-y-requisitos). Ese Resource Server no ve entonces una revocación hasta que el token expira. El Record Locator Service, que introspecciona siempre, la ve en la operación siguiente.

> **Nota.** RFC 9068 recomienda que el `aud` de un JWT tenga el mismo valor que el `resource`, pero no lo exige ([RFC 9068, §3](https://www.rfc-editor.org/rfc/rfc9068.html#section-3))[^rfc9068-aud]. HIX sigue en esto a IUA, que prevé una lista de Resource Servers para un único `resource`. Lo que RFC 9068 sí exige es que la autorización del token no sea ambigua, y en HIX no lo es, porque cada scope es una transacción que atiende un único Resource Server.

La organización y el propósito de uso los fija el Authorization Server desde su registro, como dice la regla 3 para las [peticiones a un Resource Server](volume-2.html#peticiones-a-un-resource-server). Cómo indica el solicitante que necesita un propósito de emergencia lo decide la comunidad, porque IUA no define ningún mecanismo para ello. El Authorization Server solo lo emite si su registro lo admite para ese cliente, como fija la [sección 2.6](volume-1-security.html#acceso-de-emergencia).

#### Respuesta y rechazos

La respuesta es la definida en [IUA](https://profiles.ihe.net/ITI/IUA/index.html#371422-message-semantics). El token de un miembro incluye siempre las [extensiones de IUA](https://profiles.ihe.net/ITI/IUA/index.html#3714221-json-web-token-option) `subject_organization_id` y `purpose_of_use`, con los valores que el Authorization Server obtiene de su registro, como establece la [sección 2.2](volume-1-actors.html#authorization-server). El token de una persona lleva `purpose_of_use` y el contexto de paciente, y `subject_organization_id` solo si la aplicación tiene una organización registrada, como fija [HIX-2](volume-2-hix-2.html), y el token de actor del Record Locator Service no lleva ninguna de las dos.

Además de las validaciones que define IUA, el Authorization Server **SHALL** rechazar la petición en los casos de la [Tabla 3.1-1](volume-2-authorization.html#tabla-3-1-1). Responde con la [respuesta de error de OAuth 2.0](https://www.rfc-editor.org/rfc/rfc6749.html#section-5.2) y el código de error que indica la tabla, definido en [RFC 8707](https://www.rfc-editor.org/rfc/rfc8707.html#section-2) o en RFC 6749.

**Tabla 3.1-1:** Rechazos que HIX aplica a ITI-71
{: #tabla-3-1-1}

| Condición | Error |
| --- | --- |
| La petición no lleva `resource`, lleva más de uno o nombra uno que el Authorization Server no tiene registrado | `invalid_target` |
| El `resource` nombra a un custodio | `invalid_target`, igual que ante un `resource` no registrado |
| El scope pide una transacción que el registro del Authorization Server no concede a ese cliente | `invalid_scope` |
| El scope pide `launch/patient`, que solo admite la autorización de una persona en [HIX-2](volume-2-hix-2.html) | `invalid_scope` |
| El cliente está deshabilitado | `invalid_client`, con el código HTTP 401 |
{: .table .table-bordered}

> **Nota.** Un `resource` que nombra a un custodio recibe la misma respuesta que uno no registrado. Así nadie puede usar el Authorization Server para averiguar qué custodios hay en la comunidad.

#### Auditoría

La petición se registra con el evento que IUA define para ITI-71, según la [Tabla 3-2](volume-2.html#tabla-3-2).

### Introspect Token [ITI-102] {#iti-102}

#### Alcance en HIX

Con ITI-102 comprueban el token del solicitante los actores centrales que lo reciben directamente. El Record Locator Service lo hace siempre. Los demás, como el Document Registry o el Master Patient Index cuando atienden directamente a los miembros, pueden en cambio validarlo por sí mismos si es un JWT, como fija la [sección 2.2](volume-1-actors.html#descripcion-de-actores-y-requisitos). Un custodio también puede introspeccionar el token mediado, además de validarlo con las claves del Authorization Server, si la comunidad lo admite, como fija la [sección 2.6](volume-1-security.html#validacion-en-el-custodio).

#### Petición

La petición es la de [IUA](https://profiles.ihe.net/ITI/IUA/index.html#3102412-message-semantics), y quien pregunta se identifica con las credenciales que acuerda con el Authorization Server ([IUA, §3.102.5](https://profiles.ihe.net/ITI/IUA/index.html#31025-security-considerations))[^iua-102-security].

El Record Locator Service introspecciona el token en cada operación que atiende y no reutiliza el resultado en operaciones posteriores, como exige la [sección 2.2](volume-1-actors.html#record-locator-service). Así, en cuanto el Authorization Server revoca un token, el Record Locator Service lo rechaza desde la operación siguiente.

> **Nota.** IUA permite cachear el resultado de una introspección hasta el `exp` que trae ([IUA, §3.102.4.2.3](https://profiles.ihe.net/ITI/IUA/index.html#3102423-expected-actions))[^iua-102-rs]. HIX lo desaconseja, porque un resultado `active=true` cacheado sigue aceptando un token que ya fue revocado. Por esta razón, la [sección 2.2](volume-1-actors.html#descripcion-de-actores-y-requisitos) fija que quien introspecciona **SHOULD NOT** reutilizar el resultado en operaciones posteriores.

#### Respuesta y rechazos

La respuesta es la de [IUA](https://profiles.ihe.net/ITI/IUA/index.html#3102422-message-semantics). Solo pueden introspeccionar los actores centrales y, si la comunidad lo admite, los custodios. A cualquier otro el Authorization Server le responde con el código HTTP 401, como prevé IUA para quien no tiene acceso al introspection endpoint ([IUA, §3.102.4.1.3](https://profiles.ihe.net/ITI/IUA/index.html#3102413-expected-actions))[^iua-102-actions].

En el token de una persona, la respuesta lleva además `patient`, como fija [HIX-2](volume-2-hix-2.html).

De la respuesta, el Resource Server toma la organización, el propósito de uso y, si lo hay, el contexto de paciente, y comprueba `aud` y `scope`, como fijan las reglas 1 a 3 para las [peticiones a un Resource Server](volume-2.html#peticiones-a-un-resource-server). Si el token está inactivo o no cumple esas reglas, rechaza la petición con el código HTTP 401, como pide IUA ([IUA, §3.72.4.3](https://profiles.ihe.net/ITI/IUA/index.html#37243-expected-actions))[^iua-72-actions], y con el OperationOutcome que exigen las [respuestas de error FHIR](volume-2.html#respuestas-de-error-fhir). Si el Authorization Server no responde, rechaza la petición con el código HTTP 503, porque no tiene cómo comprobar el token, como fija la [sección 2.2](volume-1-actors.html#descripcion-de-actores-y-requisitos).

**Ejemplo.** Con el token del ejemplo anterior, el laboratorio publica el resultado. Al recibir la publicación, el Document Registry introspecciona el token ante el Authorization Server con sus propias credenciales. En este despliegue el Document Registry y el Master Patient Index atienden directamente a los miembros, así que `aud` nombra a los tres. La extensión `ihe_iua` lleva la organización y el propósito de uso del laboratorio.

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
  "sub": "<lab_client_id>",
  "client_id": "<lab_client_id>",
  "aud": [
    "<rls_audience>",
    "<registry_audience>",
    "<mpi_audience>"
  ],
  "jti": "<jti>",
  "iat": 1790204262,
  "exp": 1790204562,
  "scope": "ITI-104 ITI-65",
  "token_type": "Bearer",
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

#### Auditoría

La introspección no tiene evento propio. Quien la usa registra su resultado en el evento de la transacción que atiende, según la [Tabla 3-2](volume-2.html#tabla-3-2).

### Referencias

Las citas reproducen el texto publicado por su fuente. Los recortes se marcan con "[...]" y la negrita es de esta guía.

[^rfc8707-resource]: [RFC 8707, §2 Resource Parameter](https://www.rfc-editor.org/rfc/rfc8707.html#section-2): "**resource Indicates the target service or resource to which access is being requested.** Its value MUST be an absolute URI [...] The parameter can carry the location of a protected resource, typically as an https URL or **a more abstract identifier**."
[^rfc9068-aud]: [RFC 9068, §3 Requesting a JWT Access Token](https://www.rfc-editor.org/rfc/rfc9068.html#section-3): "If the request includes a "resource" parameter (as defined in [RFC8707]), **the resulting JWT access token "aud" claim SHOULD have the same value as the "resource" parameter in the request.** [...] **The authorization server MUST NOT issue a JWT access token if the authorization granted by the token would be ambiguous.**"
[^iua-71-actions]: [IUA, §3.71.4.1.3 Expected Actions](https://profiles.ihe.net/ITI/IUA/index.html#371413-expected-actions): "**The Authorization Client is recommended to provide a resource value** to limit usability of the requested token to the intended Resource Server. [...] If the Authorization Client presented a resource value in the token request, **the Authorization Server shall limit the list of Resource Server identifiers in the audience claim to only those that are essential to interact with the specified resource** (typically only the Resource Server itself)."
[^iua-72-actions]: [IUA, §3.72.4.3 Expected Actions](https://profiles.ihe.net/ITI/IUA/index.html#37243-expected-actions): "If the token includes a scope claim, **the Resource Server shall verify that the scope covers the transaction to the requested resource** [OAuth 2.1, Section 7]. If the token includes an audience claim, **the Resource Server shall verify that the audience includes the Resource Server itself** [OAuth 2.1, Section 7]. [...] **If the token verification, or scope matching, or the access policy enforcement fails, the Resource Server shall respond with a HTTP 401 (Unauthorized) error.**"
[^iua-102-security]: [IUA, §3.102.5 Security Considerations](https://profiles.ihe.net/ITI/IUA/index.html#31025-security-considerations): "The Resource Server shall securely identify itself towards the Authorization Server by using credentials agreed between the Authorization Server and Resource Server. **At minimum, the Authorization Server and Resource Server shall support the use of Bearer tokens for Resource Server authentication** as defined in [OAuth2.1, Section 7.2]. **To obtain a bearer token, the Resource Server may request such a token from the Authorization Server, reusing the client credential grant flow** as described in the Get Access Token [ITI-71] transaction".
[^iua-102-rs]: [IUA, §3.102.4.2.3 Expected Actions](https://profiles.ihe.net/ITI/IUA/index.html#3102423-expected-actions): "**If the active field is set to "false", the Resource Server shall return HTTP 401 (Not Authorized) for all requests carrying the introspected access token. The Resource Server shall use the introspection results as access token claims in all access control evaluations** [...] The Resource Server may cache introspection results for a given access token in case the introspection result contains an expiry field. **This cache shall not extend the period as defined by the expiry field.**"
[^iua-102-actions]: [IUA, §3.102.4.1.3 Expected Actions](https://profiles.ihe.net/ITI/IUA/index.html#3102413-expected-actions): "Upon receiving the introspect request, the Authorization Server shall evaluate the Resource Server's access to the introspect endpoint. **If access is not allowed, the Authorization Server shall return HTTP 401 (Not Authorized).** The Authorization Server shall: [...] Validate the active state of the token (e.g., check expiry or revocation). **Evaluate configured access policies, taking into account the authorization claims related to the token and the Resource Server identity.** [...] **If the one of the above checks fails the Authorization Server shall return an introspection response with the "active" field set to "false"** as described in RFC7662, Section 2.2."

*[IUA]: Internet User Authorization, perfil IHE que aplica OAuth 2.0 a las transacciones sobre FHIR
