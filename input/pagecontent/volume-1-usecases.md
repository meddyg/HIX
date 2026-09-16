Esta sección recorre los casos de uso que la arquitectura soporta. Cada uno se cuenta desde el punto de vista de quien lo vive y se acompaña del flujo entre actores, con las transacciones y el orden en que ocurren. El detalle de cada transacción está en el Volumen 2.

Los casos siguen las tres historias de las figuras de la sección 2.2, el laboratorio que publica, el hospital que consulta y la persona que accede a lo suyo, precedidas por la identidad del paciente, que es condición de todas. La publicación, la consulta y el acceso del paciente son independientes entre sí y ocurren en cualquier orden y con cualquier frecuencia. La incorporación de un miembro, que precede a todo, es un procedimiento administrativo y se describe en la sección 2.7.

### Identidad del paciente

#### Descripción del caso de uso

Una persona existe en la comunidad desde que la fuente autoritativa de identidad la alimenta al registro de identidad maestra. El custodio que la atiende declara a la comunidad qué [identidad local](appendix-glossary.html#identidad-local) le corresponde. El registro vincula esa identidad con la [identidad maestra](appendix-glossary.html#identidad-maestra) y, desde entonces, los documentos que ese custodio publique con su identificador local quedan asociados a la misma persona que los publicados por los demás miembros.

Un miembro que solo conoce su propio identificador de una persona, o el nacional, pregunta con él y obtiene la identidad maestra enlazada, que es como la comunidad la nombra. No obtiene los identificadores de los demás miembros. Un miembro que no dispone de ningún identificador conocido por la comunidad puede, si declara la Opción de Demografía, buscar por datos demográficos entre las identidades maestras.

Lo que un miembro declara vincula. Nunca crea una persona, nunca fusiona dos y nunca modifica lo que la identidad maestra dice de ella.

#### Flujo del proceso

![Alimentación y resolución de la identidad del paciente](hix-flujo-identidad.svg)

**Figura 2.5-1:** Alimentación y resolución de la identidad del paciente

1. La fuente autoritativa de identidad alimenta la identidad maestra de la persona mediante [ITI-93](https://profiles.ihe.net/ITI/PMIR/ITI-93.html).
2. El custodio declara su identidad local mediante [ITI-104](https://profiles.ihe.net/ITI/PIXm/ITI-104.html) ante la infraestructura central, en su propio dominio de identificadores y con el identificador nacional de la persona. La infraestructura central comprueba que el dominio corresponde a la organización del token, y el registro de identidad maestra vincula la identidad local con la maestra. Si la persona no existe en la comunidad, rechaza la declaración e indica el motivo.
3. Un consumidor resuelve su identificador a la identidad maestra mediante [ITI-83](https://profiles.ihe.net/ITI/PIXm/ITI-83.html) ante la infraestructura central y, si declara la Opción de Demografía, busca por datos demográficos mediante [ITI-78](https://profiles.ihe.net/ITI/PDQm/ITI-78.html).

### Publicación de un documento

#### Descripción del caso de uso

Un laboratorio termina un resultado y lo publica en la comunidad. Envía los metadatos y conserva el documento. Desde ese momento el resultado es localizable por cualquier miembro autorizado, sin que el laboratorio deba anticipar quién lo buscará ni conocer a nadie más que a la comunidad. Lo publica con el [propósito de uso](appendix-glossary.html#proposito-de-uso) de la atención, `TREAT`.

El laboratorio nombra al paciente con su identificador local, se nombra a sí mismo como [custodio](appendix-glossary.html#custodio), indica dónde está el documento con una ruta relativa a su propio endpoint y etiqueta su confidencialidad. La comunidad comprueba que el laboratorio publica solo por sí mismo y solo sobre pacientes que él mismo declaró, resuelve la identidad maestra y registra el [puntero](appendix-glossary.html#puntero). Si rechaza la publicación, dice por qué. Conviene que el laboratorio no dé por publicado un documento hasta recibir la confirmación.

#### Flujo del proceso

![Publicación de un documento](hix-flujo-publicacion.svg)

**Figura 2.5-2:** Publicación de un documento

1. El custodio conserva el documento en su repositorio y obtiene del Authorization Server un token para publicar.
2. El custodio publica los metadatos mediante [ITI-65](https://profiles.ihe.net/ITI/MHD/ITI-65.html) ante la infraestructura central. Bajo la Opción de Almacenamiento Central, incluye el contenido.
3. El Document Registry comprueba que el custodio del puntero es la organización que el token declara y que esa organización es un miembro activo según el directorio, que la URL de contenido es relativa y que el puntero lleva etiqueta de confidencialidad. Rechaza la publicación que no cumpla alguna de esas condiciones e indica el motivo.
4. El Document Registry resuelve el paciente local a la identidad maestra mediante [ITI-83](https://profiles.ihe.net/ITI/PIXm/ITI-83.html), la escribe como sujeto del puntero, lo registra a nombre del custodio y responde. Si el paciente no resuelve a una identidad maestra, rechaza la publicación.

### Consulta del expediente por un profesional

#### Descripción del caso de uso

Un profesional de un hospital atiende a la misma persona y necesita su historial. Consulta la comunidad con el identificador que su propio sistema conoce y con el propósito de uso de la atención habitual, `TREAT`. Obtiene la lista de documentos que la política le permite ver y recupera el que le interesa. No sabe, ni necesita saber, qué organización lo custodia.

La recuperación atraviesa dos tramos autorizados. El del profesional ante la comunidad, con un token destinado al Record Locator Service. Su sujeto es el sistema del hospital, porque es el cliente que el Authorization Server autentica, y la organización, el profesional y el propósito de uso van en las extensiones que IUA define para el token ([IUA, §3.71.4.2.2.1](https://profiles.ihe.net/ITI/IUA/index.html#3714221-json-web-token-option))[^iua-sub]. Y el de la comunidad ante el custodio, con un [token que el Record Locator Service obtiene por intercambio](appendix-glossary.html#token-intercambiado) para ese único custodio. Ese token conserva el sujeto y las extensiones del original, nombra al Record Locator Service como actor y vence a los dos minutos como máximo. El custodio valida ese token por sí mismo y entrega el documento a la comunidad, que lo entrega al profesional.

Si un custodio no responde, el profesional recibe un resultado que lo dice, junto con todo lo demás que pidió. Un custodio caído degrada la respuesta y nunca la hace fallar.

En una urgencia la historia cambia en dos puntos. El profesional consulta con el propósito de uso `ETREAT`, y qué permite frente a `TREAT` lo fija la política de la comunidad, por ejemplo divulgar documentos que en atención habitual exigirían un consentimiento. Y si la persona llega sin un identificador fiable, el hospital puede buscarla por sus datos demográficos bajo la Opción de Demografía, como en la Figura 2.2-2. La búsqueda la habilita el scope del token, no el propósito. El propósito se evalúa después, en la [decisión de divulgación](appendix-glossary.html#decision-de-divulgacion).

#### Flujo del proceso

![Localización y recuperación mediada](hix-flujo-localizacion.svg)

**Figura 2.5-3:** Localización y recuperación mediada

1. El [consumidor](appendix-glossary.html#consumidor) obtiene del Authorization Server un token destinado al Record Locator Service y localiza mediante [ITI-67](https://profiles.ihe.net/ITI/MHD/ITI-67.html). En una urgencia sin identificador conocido, busca antes a la persona por datos demográficos mediante ITI-78 ante la infraestructura central.
2. El Record Locator Service comprueba el token mediante [ITI-102](https://profiles.ihe.net/ITI/IUA/index.html#3102-introspect-token-iti-102), resuelve la identidad maestra mediante ITI-83, consulta el Document Registry mediante ITI-67, evalúa la decisión de divulgación sobre cada puntero y devuelve los divulgados, con URL de contenido que apuntan a sí mismo.
3. El consumidor recupera mediante [ITI-68](https://profiles.ihe.net/ITI/MHD/ITI-68.html) sobre una de esas URL.
4. El Record Locator Service relee el puntero, vuelve a evaluar la divulgación, resuelve el endpoint del custodio en el directorio mediante [ITI-90](https://profiles.ihe.net/ITI/mCSD/ITI-90.html) y obtiene mediante [HIX-1] un token para ese custodio.
5. El Record Locator Service recupera el documento del custodio mediante ITI-68. El custodio valida el token sin llamar al Authorization Server y entrega el documento, que el Record Locator Service entrega al consumidor. Bajo la Opción de Almacenamiento Central, lo recupera del Document Registry en lugar del custodio, con un token intercambiado para él.

### Acceso del paciente a su expediente

#### Descripción del caso de uso

Una persona abre una aplicación de su elección y accede a sus propios documentos. La aplicación no la opera la comunidad y no tiene autoridad permanente sobre nada, solo lo que esta persona le concedió y mientras dure.

La persona tiene una identidad verificada ante el Authorization Server. Cómo la obtiene es política de la comunidad. Al lanzar la aplicación, el Authorization Server la autentica, resuelve esa identidad a la identidad maestra y emite un token cuyo contexto de paciente es ella misma. La aplicación no elige a qué paciente accede. El contexto viene fijado en el token y el Record Locator Service confina cada consulta a ese paciente. El propósito de uso dice quién actúa, `PATRQT` si es la propia persona, `FAMRQT` si es un familiar que ella autorizó y `PWATRNY` si es su representante legal. A partir de ahí, sus consultas y recuperaciones son las de cualquier otro solicitante.

Este caso es el que permite a HIX servir a la persona lo que es suyo, y no solo lo que la política de la comunidad permite entre organizaciones.

#### Flujo del proceso

![Acceso del paciente a su expediente](hix-flujo-paciente.svg)

**Figura 2.5-4:** Acceso del paciente a su expediente

1. La [aplicación del paciente](appendix-glossary.html#aplicacion-del-paciente) inicia [HIX-2]. El Authorization Server autentica a la persona, obtiene su autorización para la aplicación, resuelve su identidad verificada a la identidad maestra mediante ITI-83 y emite el token con ese contexto de paciente y el propósito de uso que corresponde a quien actúa.
2. La aplicación localiza y recupera mediante ITI-67 e ITI-68 a través del Record Locator Service, que confina cada operación al paciente del contexto.

### Casos previstos

Los siguientes casos forman parte de la arquitectura y se especificarán en versiones posteriores de esta guía. La arquitectura ya fija dónde se aplican y qué información necesitan.

- **Consentimiento anticipado del paciente.** La persona registra una directiva que permite o restringe la divulgación de sus documentos por clase de solicitante, propósito de uso, categoría de documento y ventana de validez. Se evalúa en cada operación bajo la Opción de Consentimiento.
- **Administración del consentimiento desde una aplicación.** La persona concede a una aplicación de su elección permiso para leer y escribir sus directivas.
- **Acceso solicitado por un miembro cuando no hay directiva.** Un miembro dirige a la persona al Authorization Server, que autoriza ese acceso específico. El token resultante lleva el contexto de paciente y la divulgación avanza bajo una autoridad que un momento antes no existía.
- **Acceso con anulación de la política.** Un profesional accede a documentos que la política ordinaria no le permitiría, declarando el propósito de uso `BTG`. Cómo se admite y cómo se audita lo fija cada comunidad, como indica la Tabla 2.2-3.
- **Identidad del personal sanitario.** El Authorization Server federa hacia el proveedor de identidad de cada institución en lugar de alojar cuentas de profesionales.

### Referencias

Las citas reproducen el texto publicado por su fuente. Los recortes se marcan con "[...]" y la negrita es de esta guía.

[^iua-sub]: [IUA, §3.71.4.2.2.1 JSON Web Token Option](https://profiles.ihe.net/ITI/IUA/index.html#3714221-json-web-token-option): "sub (required): **If known, unique identifier of the user; the client_id otherwise** [JWT, Section 4.1]. client_id (required): identifier of the client for which the token is issued." Y en §3.71.4.2.2.1.1 JWT IUA extension: "The Authorization Server and Resource Server shall support the following extensions to the JWT access token: **subject_name** (optional): The user's name as String. **subject_organization_id** (optional): Unique identifier of the user's organization. [...] **subject_role** (optional): Coded values indicating the user's roles. [...] **purpose_of_use** (optional): Purpose of use for the request. [...] The above claims shall be wrapped in an "extensions" object with key 'ihe_iua'".

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
