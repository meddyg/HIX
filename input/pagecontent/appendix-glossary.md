Este glosario reúne, en una línea cada uno, los actores y términos que usa esta guía. Los actores propios de HIX se definen en la [sección 2.2](volume-1-actors.html). Los actores IHE enlazan a la página del perfil que los define.

### Actores de HIX

**Record Locator Service.** El mediador de la comunidad. Localiza y recupera documentos en nombre de los miembros y aplica la decisión de divulgación sobre los punteros. Es un nombre propio de esta guía, no vocabulario IHE.
{: #record-locator-service}

**Document Registry.** El registro de documentos de la comunidad. Conserva los punteros a los documentos publicados y, bajo la Opción de Almacenamiento Central, el contenido que los custodios le entregan. Toma su nombre y su función del [Document Registry de MHDS](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150111-document-registry), pero es un actor de HIX, definido por los actores que agrupa.
{: #document-registry}

**[Authorization Server](https://profiles.ihe.net/ITI/IUA/index.html).** El Authorization Server de IUA. Emite, comprueba e intercambia los tokens que circulan por la comunidad.
{: #authorization-server}

**Directorio de la comunidad.** Publica las organizaciones participantes, su pertenencia a la comunidad y los endpoints en los que responden. Es el Directory de mCSD.
{: #directorio-de-la-comunidad}

**Registro de identidad maestra.** Conserva una identidad maestra por persona y sus enlaces con las identidades locales. Agrupa al Patient Identity Registry de PMIR, al Patient Identifier Cross-reference Manager de PIXm y al Patient Demographics Supplier de PDQm.
{: #registro-de-identidad-maestra}

**[Audit Record Repository](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html).** El actor de ATNA que recibe los eventos de auditoría de los actores centrales.
{: #audit-record-repository}

**Fuente autoritativa de identidad.** Sistema externo a la comunidad que verifica la identidad de las personas y crea las identidades maestras. Es el Patient Identity Source de PMIR. HIX propone que sea el EDUS.
{: #fuente-autoritativa-de-identidad}

**Custodio.** El sistema que publica y custodia documentos. Miembro que produce documentos, los conserva, declara las identidades locales de sus pacientes y publica los punteros.
{: #custodio}

**Consumidor.** El sistema que consume documentos. Miembro que localiza y recupera documentos de un paciente a través del Record Locator Service.
{: #consumidor}

**Aplicación del paciente.** Aplicación con la que una persona, o quien ella autoriza, accede a su propio expediente con el contexto de paciente que fija el Authorization Server.
{: #aplicacion-del-paciente}

### Actores IHE que HIX agrupa

**[Document Source](https://profiles.ihe.net/ITI/MHD/5.0.0/1331_actors_and_transactions.html).** Actor de MHD que publica documentos y sus punteros con ITI-65.
{: #document-source}

**[Document Consumer](https://profiles.ihe.net/ITI/MHD/5.0.0/1331_actors_and_transactions.html).** Actor de MHD que localiza listas y documentos con ITI-66 e ITI-67 y recupera documentos con ITI-68.
{: #document-consumer}

**[Document Responder](https://profiles.ihe.net/ITI/MHD/5.0.0/1331_actors_and_transactions.html).** Actor de MHD que responde la localización y la recuperación de documentos.
{: #document-responder}

**[Document Recipient](https://profiles.ihe.net/ITI/MHD/5.0.0/1331_actors_and_transactions.html).** Actor de MHD que recibe las publicaciones ITI-65.
{: #document-recipient}

**[Patient Identity Source](https://profiles.ihe.net/ITI/PMIR/volume-1.html).** Actor de PMIR y de PIXm que alimenta identidades de paciente, con ITI-93 o ITI-104.
{: #patient-identity-source}

**[Patient Identity Registry](https://profiles.ihe.net/ITI/PMIR/volume-1.html).** Actor de PMIR que conserva las identidades maestras que recibe por ITI-93.
{: #patient-identity-registry}

**[Patient Identity Consumer](https://profiles.ihe.net/ITI/PMIR/volume-1.html).** Actor de PMIR que recibe por ITI-93 los cambios de las identidades maestras, en particular las fusiones, y los aplica a sus propios datos.
{: #patient-identity-consumer}

**[Patient Identifier Cross-reference Manager](https://profiles.ihe.net/ITI/PIXm/volume-1.html).** Actor de PIXm que recibe identidades locales por ITI-104, las enlaza con la identidad maestra y responde ITI-83.
{: #patient-identifier-cross-reference-manager}

**[Patient Identifier Cross-reference Consumer](https://profiles.ihe.net/ITI/PIXm/volume-1.html).** Actor de PIXm que resuelve un identificador con ITI-83.
{: #patient-identifier-cross-reference-consumer}

**[Patient Demographics Supplier](https://profiles.ihe.net/ITI/PDQm/volume-1.html).** Actor de PDQm que responde búsquedas por datos demográficos con ITI-78.
{: #patient-demographics-supplier}

**[Patient Demographics Consumer](https://profiles.ihe.net/ITI/PDQm/volume-1.html).** Actor de PDQm que busca pacientes por datos demográficos con ITI-78.
{: #patient-demographics-consumer}

**[Directory](https://profiles.ihe.net/ITI/mCSD/volume-1.html#146111-directory).** Actor de mCSD que publica el directorio y responde ITI-90. Hasta mCSD 3 se llamaba Care Services Selective Supplier, y así lo nombra todavía MHDS.
{: #directory}

**[Query Client](https://profiles.ihe.net/ITI/mCSD/volume-1.html#146112-query-client).** Actor de mCSD que consulta el directorio con ITI-90. Hasta mCSD 3 se llamaba Care Services Selective Consumer, y así lo nombra todavía MHDS.
{: #query-client}

**[Authorization Client](https://profiles.ihe.net/ITI/IUA/index.html).** Actor de IUA que obtiene tokens con ITI-71 y los presenta con ITI-72.
{: #authorization-client}

**[Resource Server](https://profiles.ihe.net/ITI/IUA/index.html).** Actor de IUA que recibe un token con ITI-72, comprueba que está destinado a él y lo valida, en su caso con ITI-102.
{: #resource-server}

**[Secure Node y Secure Application](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html).** Actores de ATNA. Todo sistema que participa en una transacción, obligado a registrar sus eventos de auditoría con ITI-20 y a comunicarse por canales seguros.
{: #secure-node}

**[Time Client](https://profiles.ihe.net/ITI/TF/Volume1/ch-7.html).** Actor de CT que sincroniza el reloj de su sistema con el Time Server de la comunidad mediante ITI-1.
{: #time-client}

### Términos de esta guía

**Identidad maestra.** La identidad verificada de una persona, única en la comunidad, creada por la fuente autoritativa de identidad. Lleva el identificador nacional y los enlaces a las identidades locales.
{: #identidad-maestra}

**Identidad local.** El paciente tal como lo conoce un miembro, con el identificador de su propio dominio. Cada miembro la declara y la enlaza con la identidad maestra.
{: #identidad-local}

**Puntero.** El `DocumentReference` que describe un documento sin contenerlo. Sobre él se toma toda decisión de la comunidad antes de mover contenido.
{: #puntero}

**Decisión de divulgación.** La evaluación que hace la infraestructura central, en el mediador o en el Document Registry, puntero por puntero y antes de recuperar, de si un documento puede entregarse a quien lo pide.
{: #decision-de-divulgacion}

**Propósito de uso.** Código del conjunto PurposeOfUse de HL7 que dice para qué se accede. Viaja en el token y lo evalúa la decisión de divulgación.
{: #proposito-de-uso}

**Scope.** El alcance de un token en OAuth 2.0. Fija qué transacciones puede pedir su portador.
{: #scope}

**[OpenID Provider](https://openid.net/specs/openid-connect-core-1_0.html#Terminology).** Authorization Server de OAuth 2.0 que además autentica a la persona y acredita esa autenticación con un `id_token`, según OpenID Connect. En HIX lo es el Authorization Server de la comunidad.
{: #openid-provider}

**Token del solicitante.** El token que un miembro obtiene con ITI-71, o la aplicación del paciente con [HIX-2](volume-1-actors.html#hix-2), destinado al Record Locator Service. Lleva el sujeto, la organización, el propósito de uso, el alcance y, en el caso de la aplicación del paciente, el contexto de paciente.
{: #token-del-solicitante}

**Token intercambiado.** El token que el mediador obtiene con [HIX-1](volume-1-actors.html#hix-1) para un único destino y una sola transacción, con el solicitante original como sujeto y el mediador como actor.
{: #token-intercambiado}

**PEP.** Punto de aplicación de política. El lugar donde se comprueba que una petición cumple las reglas de la comunidad. En HIX, el primero es el mediador.
{: #pep}

**PDP.** Punto de decisión de política. El lugar donde se toma la decisión que el PEP aplica. En HIX, la decisión de divulgación se toma en la infraestructura central, en el mediador o en el Document Registry.
{: #pdp}

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
