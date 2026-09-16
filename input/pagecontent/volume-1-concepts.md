Esta sección explica las decisiones que dan forma a esta comunidad. Cada una se presenta con lo que decide, por qué lo decide y lo que cuesta. Son decisiones de arquitectura, no de implementación. Una comunidad puede desplegarlas de muchas maneras, como describe la sección 2.7, sin que cambie nada de lo que aquí se describe. La tabla del final resume los compromisos asumidos.

### Comunidad y límite de confianza

Una comunidad HIX es un conjunto de organizaciones que acuerdan compartir documentos clínicos bajo una política común y a través de una infraestructura común. La pertenencia es explícita. Una organización es miembro cuando figura en el directorio de la comunidad y el Authorization Server reconoce a sus sistemas.

**En una malla de pares, las garantías de la comunidad valen lo que valga su miembro más débil.** Ese es el argumento que decide la topología. Si cada miembro descubre y consulta a los demás, cada uno tiene que implementar el descubrimiento y mantener tantas relaciones de confianza como miembros haya. Cada uno tiene que poner además un punto de aplicación de política, el PEP, delante de sus propios datos, y auditar por su cuenta. La política de la comunidad se aplica entonces en tantos lugares como miembros, con la calidad que cada uno pueda pagar, y basta un miembro mal implementado para que la garantía deje de existir para todos. IHE describe ambas topologías en su whitepaper sobre intercambio de información de salud ([HIE Whitepaper, §2.8](https://profiles.ihe.net/ITI/HIE-Whitepaper/index.html#28-document-sharing-models) y [§3.2](https://profiles.ihe.net/ITI/HIE-Whitepaper/index.html#32-centralized-discovery-and-retrieve))[^hie-wp]. HIX elige la centralizada y absorbe esa complejidad una sola vez, en el centro, donde se puede operar, verificar y auditar.

Por esta razón, la relación de confianza no se establece de forma directa entre los miembros, sino entre cada miembro y la infraestructura central. Un miembro no confía en los demás ni necesita conocerlos. Confía en que la comunidad autoriza, media y registra cada interacción. Integrarse a HIX es integrarse una sola vez, con la comunidad. No hay que integrarse con cada uno de los demás miembros, ni volver a hacerlo cuando entra uno nuevo.

### Mediación central de la localización y la recuperación

Toda localización y toda recuperación pasan por el [Record Locator Service](appendix-glossary.html#record-locator-service), el mediador de la comunidad. Un solicitante obtiene del mediador los punteros que la política le permite ver, y las URL de contenido que recibe apuntan al propio mediador, nunca al custodio. Al recuperar, el mediador alcanza al custodio en nombre del solicitante y le entrega el documento.

MHDS admite que un consumidor alcance directamente al servicio que aloja un documento fuera del Document Registry ([MHDS Vol. 1, §1:50.1.1.2](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150112-storage-of-binary))[^mhds-storage]. HIX no lo admite, y la razón está en el propio perfil. MHDS reconoce, al definir su Consent Manager Option, que esa opción **no protege el contenido almacenado fuera del registro** y que, cuando los documentos se almacenan en otro lugar, cada Document Source carga solo con la protección de sus documentos ([MHDS Vol. 1, §1:50.2.2](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15022-consent-manager-option))[^mhds-consent]. Con custodia distribuida y acceso directo, cada custodio tendría que evaluar la política de la comunidad frente a cada consumidor. La mediación cierra ese hueco. La política de divulgación se aplica en un solo lugar, la infraestructura central, con una única superficie auditable que ve la interacción completa y un único contrato de integración.

El precio es que la infraestructura central se vuelve indispensable para operar, y se dimensiona y protege como tal. Todo byte clínico atraviesa el mediador. La sección 2.6 especifica lo que eso exige.

Mediar no es lo mismo que enrutar. El mediador es imprescindible donde hay que alcanzar a un custodio en nombre de un miembro, es decir, al recuperar, porque es quien obtiene el token delegado para ese custodio y recorre el canal que el directorio declara. La decisión de divulgación sobre los punteros es otra cosa. La toma la infraestructura central antes de mover contenido alguno, y puede tomarla el mediador o un Document Registry que conozca la política de la comunidad, como admiten la Opción de Consentimiento de la sección 2.3 y la Consent Manager Option de MHDS. En las transacciones entre un miembro y un solo componente central, como declarar una identidad, el trabajo es otro. Consiste en comprobar que la petición cumple las reglas de la comunidad para esa transacción, por ejemplo que el miembro solo escribe en su propio dominio de identificadores, y en registrarla. Esa comprobación la puede hacer el mediador o el propio componente, siempre que el componente conozca esas reglas y registre en el mismo repositorio de auditoría. El miembro ejecuta siempre las mismas transacciones, con los mismos mensajes y las mismas reglas. Lo único que cambia es el punto que las valida, el mediador o el componente central.

> **Nota.** El mediador es desacoplable. No añade nada al modelo de MHDS. Solo concentra el PEP y las transacciones que MHDS reparte entre los miembros. Sin él, la comunidad operaría como MHDS estándar, con el mismo flujo, pero cada miembro tendría que aplicar la política, resolver endpoints, obtener credenciales y auditar por su cuenta. Quitar el mediador no cambia la arquitectura, solo mueve el PEP a cada miembro.

### Custodia distribuida y almacenamiento central

El documento permanece donde se produjo. El miembro que lo creó lo conserva, responde por su contenido y participa en cada recuperación que lo alcanza. La infraestructura central mantiene el índice, no una copia del expediente.

MHDS admite dos ubicaciones válidas para el contenido, dentro del Document Registry o en cualquier otro lugar de la comunidad, incluido el sistema del propio Document Source ([MHDS Vol. 1, §1:50.1.1.2](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150112-storage-of-binary))[^mhds-storage]. HIX adopta la segunda como **política por defecto** y ofrece la primera como opción. Un custodio que no puede alojar un endpoint ejerce la Opción de Almacenamiento Central y entrega el contenido a la infraestructura central sin dejar de figurar como custodio.

Las dos ubicaciones tienen ejemplos nacionales. Estonia recupera cada documento del proveedor que lo produjo, como se ve en la sección de transporte. Suiza hace lo contrario. Cada comunidad de su expediente electrónico almacena los binarios en su propio Document Repository y las instituciones le entregan el documento al publicarlo ([eHealth Suisse, EPR architecture, §3.3.4](https://www.e-health-suisse.ch/payload/api/documents/file/EPD-Architektur_EN.pdf))[^ch-epr-arch]. Como la API que ve el solicitante es idéntica bajo ambas ubicaciones, un custodio puede pasar de una a otra sin que ningún miembro lo note. Por eso "el contenido nunca sale del custodio" es una política por defecto y no un principio absoluto. La arquitectura admite las dos y la comunidad decide por custodio.

### Identidad del paciente (PMIR)

Cada miembro **solo conoce y solo usa sus propios identificadores de paciente**. No conoce los de los demás miembros ni necesita conocerlos. Para la comunidad, cada miembro es un **dominio de identificadores** distinto, y un mismo identificador local solo tiene sentido dentro del dominio del miembro que lo asignó. La comunidad no reemplaza esos identificadores. Mantiene una **identidad maestra** por persona y enlaza con ella las identidades locales que los miembros declaran, de modo que cualquier identificador local, de cualquier miembro, resuelve a la misma persona.

La identidad maestra es un recurso `Patient` en un dominio reservado a la identidad verificada, en el que solo escribe la fuente autoritativa. Lleva el identificador nacional de la persona, la cédula en el caso de la figura, que la ancla a alguien real, y los enlaces a sus identidades locales, uno por cada miembro que la haya declarado. No lleva demografía de los miembros. Los nombres y las fechas se quedan en cada miembro. La comunidad guarda identificadores y enlaces.

![Identidad maestra e identidades locales](hix-master-patient-index.svg)

**Figura 2.1-1:** Identidad maestra e identidades locales

La Figura 2.1-1 muestra cómo se construye.

- La **fuente autoritativa de identidad** es quien crea la identidad maestra. Lo hace con el feed **[PMIR](https://profiles.ihe.net/ITI/PMIR/index.html)** ([ITI-93](https://profiles.ihe.net/ITI/PMIR/ITI-93.html)), una vez que comprobó quién es la persona con su identificador nacional. Nadie más puede crear una identidad maestra. HIX no define cuál debe ser esa fuente, pero propone que sea el EDUS, como indica la introducción del volumen.
- Cada **miembro** declara los pacientes de su dominio con el feed **[PIXm](https://profiles.ihe.net/ITI/PIXm/index.html)** ([ITI-104](https://profiles.ihe.net/ITI/PIXm/ITI-104.html)). Envía su identificador local junto con el identificador nacional de la persona, y el registro de identidad enlaza ese identificador local con la identidad maestra que ya existe para esa persona. Si la persona todavía no tiene identidad maestra, la declaración se rechaza. *Un miembro **vincula**, nunca crea.*
- La consulta **determinista** es PIXm ([ITI-83](https://profiles.ihe.net/ITI/PIXm/ITI-83.html)). Recibe un identificador, local o nacional, y devuelve la identidad maestra enlazada a él. Es la vía normal. La usan el Record Locator Service al localizar, el Document Registry al indexar y el Authorization Server al fijar el contexto de paciente, cada vez que necesitan saber quién es un paciente.
- La consulta **probabilística** es **[PDQm](https://profiles.ihe.net/ITI/PDQm/index.html)** ([ITI-78](https://profiles.ihe.net/ITI/PDQm/ITI-78.html)). Recibe datos demográficos y devuelve identidades maestras candidatas con un grado de coincidencia. Es el respaldo cuando no hay un identificador fiable. Busca solo entre identidades maestras. Como cualquier otra transacción, la habilita el scope del token del solicitante. El propósito de uso no la habilita ni la bloquea, se evalúa después, en la decisión de divulgación.

> **Nota.** Un miembro no puede crear una persona, fusionar dos ni escribir en el dominio de otro. Y ninguna de las dos consultas prueba una identidad. Eso solo lo hace la fuente autoritativa.

### El puntero

La unidad del índice es el puntero, un [`DocumentReference`](https://hl7.org/fhir/R5/documentreference.html) de FHIR R5 que describe un documento sin contenerlo. Toda decisión de la comunidad se toma sobre el puntero, antes de mover un byte del documento, así que lo que el puntero lleva es una decisión de arquitectura. Estos son sus elementos.

- **`subject`** apunta a la identidad maestra del paciente, nunca a una identidad local. Lo escribe el Document Registry al indexar, con la consulta determinista, a partir de la identidad local que el miembro declara en `sourcepatient`. El miembro no lo declara ni necesita conocer la identidad maestra.
- **`sourcepatient`** es una extensión que apunta a la identidad local, es decir, al paciente tal como lo declaró el miembro, con su identificador en su propio dominio. Es la extensión estándar [`documentreference-sourcepatient`](https://hl7.org/fhir/extensions/StructureDefinition-documentreference-sourcepatient.html), que en R5 reemplaza a `context.sourcePatientInfo`. Conserva la traza de qué miembro declaró a quién y permite volver a resolver `subject` si un enlace de identidad cambia.
- **`custodian.identifier`** nombra a la organización responsable con el mismo identificador que lleva su token y que publica el directorio. Nunca es una referencia a un recurso.
- **`content.attachment.url`** es una ruta relativa. Un puntero nunca contiene una dirección física ni nada que identifique un transporte. La dirección se resuelve en el directorio en cada recuperación.
- **`securityLabel`** lleva la [etiqueta de confidencialidad](https://hl7.org/fhir/R5/security-labels.html) del documento, un código del sistema [v3-Confidentiality](https://terminology.hl7.org/CodeSystem-v3-Confidentiality.html) de HL7, como `N` para normal, `R` para restringido o `V` para muy restringido. Es obligatorio desde la primera publicación. Sin la etiqueta en el índice, decidir si un documento se puede divulgar exigiría leerlo primero, y añadirla después obligaría a releer todos los documentos en los custodios.
- **`identifier`** es el identificador de negocio del documento y es estable, para que republicar el mismo documento actualice su puntero en lugar de duplicarlo.

El resto de elementos, como `status`, `type` o `date`, son los metadatos habituales de MHD y se especifican en el Volumen 3.

### Directorio de la comunidad (mCSD)

El directorio describe las organizaciones participantes, su pertenencia a la comunidad y los endpoints en los que responden. Es la fuente de la que la infraestructura central aprende a quién dirigir una recuperación, por qué canal y qué opciones ejerce cada custodio.

Los miembros no consultan el directorio, porque nunca se comunican entre sí. Lo consulta el mediador, en cada operación, para saber a qué custodio dirigirse y en qué endpoint. Por eso incorporar un miembro no exige reconfigurar nada. Basta con darlo de alta en el directorio para que el mediador pueda alcanzarlo. La resolución es estricta. El directorio debe devolver exactamente una organización activa con exactamente un endpoint activo. Si devuelve cero o más de uno, el mediador trata al custodio como no disponible en lugar de elegir por su cuenta.

El directorio fija dos valores que se usan tal cual en toda la comunidad. El **identificador de la organización** es el mismo que el Authorization Server incluye en los tokens del miembro para decir en nombre de qué organización actúa, y el mismo que sus punteros llevan en `custodian.identifier`. La **dirección del endpoint** es la URL a la que el mediador llama, la audiencia del token que obtiene para ese custodio y la base contra la que se resuelven las rutas relativas de sus punteros. Como token, puntero y directorio parten del mismo valor, no pueden desincronizarse.

### Autorización y delegación

HIX usa OAuth 2.0 ([RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)) según lo perfila [IUA](https://profiles.ihe.net/ITI/IUA/index.html). La idea de fondo es sencilla. Para hablar con la comunidad, un sistema necesita un token, y todos los tokens los emite un único Authorization Server.

Un miembro obtiene un token para hablar con el Record Locator Service, y solo con él. Ese token no sirve ante ningún custodio, y el miembro nunca recibe uno que sirva. El mediador comprueba cada token que recibe preguntando al Authorization Server si sigue siendo válido. Esa consulta es la introspección de [RFC 7662](https://www.rfc-editor.org/rfc/rfc7662), que IUA recoge como la transacción Introspect Token ([ITI-102](https://profiles.ihe.net/ITI/IUA/index.html#3102-introspect-token-iti-102)).

Cuando una operación exige llegar a un custodio, el mediador no reutiliza el token del miembro. Lo **intercambia** por otro, siguiendo OAuth 2.0 Token Exchange ([RFC 8693](https://www.rfc-editor.org/rfc/rfc8693)). Es decir, presenta al Authorization Server el token del miembro y pide a cambio un token nuevo, hecho a la medida de esa llamada. El token nuevo vale para un solo custodio, que se indica con un resource indicator ([RFC 8707](https://www.rfc-editor.org/rfc/rfc8707)). Vale para una sola transacción. Dura como mucho dos minutos, y nunca más que el token original. Y lleva dentro quién pidió, el miembro, y quién actúa en su nombre, el mediador, en el claim `act` que la RFC define para eso.

El custodio valida ese token por su cuenta, con las claves públicas del Authorization Server, sin llamar a nadie. Así sabe quién pregunta, en nombre de quién actúa la comunidad y para qué.

Lo mismo vale hacia los componentes centrales. El mediador no tiene acceso propio al Document Registry ni al registro de identidad maestra. Actúa ante ellos con tokens intercambiados de la misma forma, a nombre del miembro que lo pidió. Un puntero queda registrado a nombre de su custodio, no del mediador. El mediador es el primer punto de aplicación de la política de la comunidad, no un participante con autoridad propia.

La Figura 2.1-2 resume el recorrido de los tokens. Un solo token entra por la izquierda, el del miembro, y de él derivan tantos tokens de un solo destino como custodios y componentes centrales haga falta alcanzar.

![Delegación de tokens en HIX](hix-delegacion.svg)

**Figura 2.1-2:** Delegación de tokens en HIX

Tres reglas hacen que el mínimo privilegio sea estructural, en lugar de depender de la buena conducta de cada parte.

- **Un token, un destino.** Un token que valiera en dos custodios permitiría a uno de ellos usarlo contra el otro.
- **Solo el mediador puede intercambiar.** Ningún otro participante puede pedir un token a nombre de un tercero, y los custodios no aceptan tokens llegados por otro camino.
- **La autoridad nunca crece.** El token intercambiado solo permite lo que el miembro ya podía, lo que la comunidad delega al mediador y lo que el custodio ofrece. Poder localizar un documento nunca da poder para recuperarlo.

Un token dice quién pide, qué puede pedir, ante quién y hasta cuándo. El token de un miembro **no nombra a ningún paciente**. Solo lo hace el de una persona que entra a su propio expediente con [SMART App Launch](https://build.fhir.org/ig/HL7/smart-app-launch/scopes-and-launch-context.html), y ahí el paciente en contexto sirve para confinar el token a ese expediente. La cuenta con la que esa persona entra no es un identificador de paciente. El Authorization Server resuelve el paciente en contexto contra la identidad maestra con la consulta determinista. En ambos casos, **tener un token da derecho a preguntar, no a ver**. Qué documentos se entregan lo decide la infraestructura central, puntero por puntero. Esa separación es la idea más importante de este volumen.

### Divulgación

La decisión de divulgación se toma en la infraestructura central, **sobre los punteros y antes de recuperar contenido alguno**. La toma el mediador o, cuando la comunidad la sitúa allí, el Document Registry. Quien la toma combina dos fuentes. Del token toma lo que el Authorization Server avaló del solicitante, es decir, su organización, su propósito de uso y, cuando existe, el paciente en contexto. Del puntero toma el paciente, la etiqueta de confidencialidad, el tipo de documento y el custodio. Nada de lo que el solicitante afirme de sí mismo en la petición cuenta.

Ese orden es lo que hace que centralizar valga su costo. Un puntero cuya divulgación se niega no genera ninguna recuperación, ninguna consulta al directorio y ningún token. La decisión se toma una vez por consulta, y un documento atraviesa dos, porque revelar que existe ya es una divulgación. Al localizar, se filtran los punteros de la respuesta. Al recuperar, el mediador vuelve a evaluar el puntero pedido antes de alcanzar al custodio. Un puntero negado no aparece en la respuesta ni se anuncia como negado.

El punto de partida es un entorno de consentimiento implícito, con una política única para toda la comunidad. MHDS lo describe en su Consent Manager Option como el entorno en el que se permite divulgar mientras el paciente no haya registrado un consentimiento ([MHDS Vol. 1, §1:50.2.2](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15022-consent-manager-option))[^mhds-implied]. El destino es [PCF](https://profiles.ihe.net/ITI/PCF/volume-1.html#1534-pcf-overview), donde las directivas de consentimiento de cada paciente se evalúan en cada petición ([PCF Vol. 1, §1:53.4](https://profiles.ihe.net/ITI/PCF/volume-1.html#1534-pcf-overview))[^pcf]. La Opción de Consentimiento del Record Locator Service declara dónde se aplica esa decisión y qué información necesita. **El modelo de consentimiento se especificará en una versión posterior de esta guía a partir de PCF.**

### Auditoría en ambos extremos

Cada participante registra lo que hace. Es lo que [ATNA](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html) exige a cada sistema que participa en una transacción, lo que el perfil llama [Secure Node o Secure Application](appendix-glossary.html#secure-node) ([ITI TF-1, §9.1.1.1](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html#9.1.1.1))[^atna-node] y lo que MHDS exige a su Document Registry ([MHDS Vol. 1, §1:50.1.1.1](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150111-document-registry))[^mhds-audit]. Los registros siguen los patrones de [BALP](https://profiles.ihe.net/ITI/BALP/index.html), que definen cómo se escribe un `AuditEvent` de FHIR para cada tipo de evento. La infraestructura central registra la solicitud que recibe del miembro y la recuperación que ella misma inicia hacia el custodio. El custodio registra la entrega.

Los registros de una misma divulgación comparten un identificador de correlación. El mediador lo genera al recibir la solicitud y lo transmite al custodio en cada llamada. BALP prevé este uso y reserva un elemento del `AuditEvent` para guardar el identificador de la petición y correlacionar los registros de cliente y servidor ([BALP, §3:5.7.3.1](https://profiles.ihe.net/ITI/BALP/content.html#35731-x-request-id-header))[^balp-corr]. Así una divulgación se puede reconstruir completa desde sus dos lados.

El token intercambiado nombra al solicitante original y al mediador como actor. Por eso el custodio registra quién pidió el documento y en nombre de quién actuó la comunidad, y no solo que lo pidió la comunidad.

Ningún registro contiene tokens ni contenido clínico. Todos los componentes centrales registran en el mismo [Audit Record Repository](appendix-glossary.html#audit-record-repository) de ATNA, el repositorio de auditoría de la comunidad. Como además toda divulgación pasa por el mediador, la pregunta "quién accedió al expediente de esta persona" se responde con una sola consulta a ese repositorio. Eso no exime a ningún custodio de registrar su lado.

### Transporte y redes de intercambio

La dirección física de un custodio vive únicamente en el directorio. El puntero lleva una organización y una ruta relativa. El mediador resuelve la dirección en cada recuperación y llega al custodio por el canal que el directorio declara para él. Ese canal puede ser una conexión directa o una red de intercambio ya establecida, como [X-Road](https://x-road.global/). En ambos casos el puntero, la API que ven los miembros y el modelo de tokens son los mismos. Cambiar de canal es cambiar un dato del directorio.

Una red de intercambio resuelve cómo se conectan las organizaciones y cómo se identifican entre sí. No dice nada de documentos, punteros ni consentimiento. Por eso HIX la usa solo por debajo del mediador. Si los miembros la usaran para hablar entre sí, volverían a la malla de pares que HIX descarta. Estonia sigue este mismo patrón. Su registro nacional de salud recupera los datos de cada proveedor cuando se necesitan y los presenta en un formato común ([e-Estonia](https://e-estonia.com/solutions/healthcare/e-health-records/))[^estonia], con X-Road como transporte. El token delegado sigue viajando por ese canal y el custodio sigue validándolo. La identidad que la red asigna a cada organización no lo sustituye.

### Compromisos asumidos

IHE deja la gobernanza fuera de su alcance. Declara que no define políticas de privacidad ni de seguridad, y que el marco de políticas de una comunidad debe definirse antes de construirla ([MHDS Vol. 1, §1:50.5.1](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15051-policies-and-risk-management))[^mhds-policy]. Por eso, de los compromisos de la tabla, la apuesta por la operación del centro es el que más pesa.

**Tabla 2.1-1:** Compromisos de la arquitectura

| Compromiso | Qué se acepta | Cómo se mitiga |
| --- | --- | --- |
| Acoplamiento de disponibilidad | Una recuperación mediada necesita al mediador, al Authorization Server y al custodio a la vez | Un custodio caído degrada la respuesta, no la hace fallar. Cualquier custodio puede pasar a almacenamiento central sin que nadie lo note |
| Contenido en tránsito por el centro | Todo byte clínico atraviesa el mediador, que lo ve en claro | El mediador no guarda ni registra contenido. El canal entre organizaciones va cifrado. El índice se gobierna como dato sensible |
| Authorization Server en el camino crítico | Cada localización exige una introspección y cada recuperación, además, un intercambio de tokens | Se dimensiona con la misma disponibilidad que el mediador. Un token derivado vale para un solo destino y dura como mucho dos minutos, así que un token filtrado tiene una ventana de uso corta y conocida |
| Apuesta por la operación del centro | La garantía de la comunidad vale lo que valga la operación de su infraestructura central. Un centro bien operado supera a una federación operada a medias, y un centro mal operado es peor que esa federación | Quién certifica miembros, quién responde al paciente y quién financia el centro se fija en la gobernanza de la comunidad, antes de construirla. Es su riesgo principal a largo plazo |
{: .table .table-bordered}

### Referencias

Las citas reproducen el texto publicado por su fuente. Los recortes se marcan con "[...]" y la negrita es de esta guía.

[^mhds-consent]: [MHDS Vol. 1, §1:50.2.2 Consent Manager Option](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15022-consent-manager-option): "Note that this option **does not protect Binary content stored outside of the Document Registry** [...]. When documents are stored outside of the Document Registry, **the Document Source system takes on the burden of protecting the document**."
[^mhds-storage]: [MHDS Vol. 1, §1:50.1.1.2 Storage of Binary](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150112-storage-of-binary): "(1) The Document Source includes the Binary Resource in the [ITI-65] transaction, and the Document Registry is required to store it. (2) **The Community allows the Binary to be stored elsewhere in the Community.** [...] This might be other centralized infrastructure, distributed infrastructure, or **within the system implementing the Document Source**. [...] the service hosting the Binary shall: [...] **provide access to the community members**".
[^hie-wp]: [IHE HIE Whitepaper, §2.8 Document Sharing Models](https://profiles.ihe.net/ITI/HIE-Whitepaper/index.html#28-document-sharing-models): "the centralized model **requires knowledge only of the centralized locator** [...]. For Push and Federated approaches **a detailed directory of participating entitles** [sic] is typically used". [§3.2 Centralized Discovery and Retrieve](https://profiles.ihe.net/ITI/HIE-Whitepaper/index.html#32-centralized-discovery-and-retrieve): "a centralized locator is used to discover the location of documents which enables **a retrieval of the document from a custodian** who has registered existence of the document with the centralized locator".
[^mhds-implied]: [MHDS Vol. 1, §1:50.2.2 Consent Manager Option](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15022-consent-manager-option): "The grouped IUA Authorization Server SHALL support consent configuration to enable Implied Consent and Explicit Consent environments. **Implied Consent environments allow disclosure when no Consent has been recorded for that patient**, Explicit Consent environments Deny disclosure when no Consent has been recorded for that patient."
[^pcf]: [PCF Vol. 1, §1:53.4 PCF Overview](https://profiles.ihe.net/ITI/PCF/volume-1.html#1534-pcf-overview): "The PCF Profile enables authorized access to data according to terms agreed by the Patient and the Organization protecting the data." [§1:53.1.1.3 Consent Authorization Server](https://profiles.ihe.net/ITI/PCF/volume-1.html#153113-consent-authorization-server): "The Consent Authorization Server **makes authorization decisions based on a given access requested context** (e.g., oAuth, query/operation parameters), organizational policies, and **current active Consent resources**."
[^atna-node]: [ITI TF-1, §9.1.1.1 Secure Node](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html#9.1.1.1): "Detect and report a Record Audit Event as specified in ITI TF-2: 3.20 for: **all of the activity-related events for the Secure Node** [...] **all transaction-related events for the Secure Node**".
[^mhds-audit]: [MHDS Vol. 1, §1:50.1.1.1 Document Registry](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150111-document-registry): "The Document Registry **SHALL record all security relevant events** to ATNA Audit Record Repository with the “ATX: FHIR Feed” Option."
[^mhds-policy]: [MHDS Vol. 1, §1:50.5 MHDS Security Considerations](https://profiles.ihe.net/ITI/MHDS/volume-1.html#1505-mhds-security-considerations): "**The policy landscape that the community is built on needs to be defined well before the community is built.**" [§1:50.5.1 Policies and Risk Management](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15051-policies-and-risk-management): "IHE solves interoperability problems via the implementation of technology standards. **It does not define Privacy or Security Policies**, Risk Management, Healthcare Application Functionality, Operating System Functionality, Physical Controls, or even general Network Controls."
[^balp-corr]: [BALP, §3:5.7.3.1 X-Request-Id header](https://profiles.ihe.net/ITI/BALP/content.html#35731-x-request-id-header): "Where it is known that an http RESTful transaction included an X-Request-Id, that value should be recorded in an .entity dedicated to X-Request-Id. **This ID can be used to correlated AuditEvents from client and server**, and may aid with correlation on further activities recorded caused by the transaction."
[^ch-epr-arch]: [eHealth Suisse, EPR architecture. A detailed description, §3.3.4 XDS Document Repositories](https://www.e-health-suisse.ch/payload/api/documents/file/EPD-Architektur_EN.pdf): "The Document Repository Service implements interfaces to **store and query the binary objects** of the XDS documents. **The data are captured by the connected systems of the (core) communities when documents are saved** and are registered via interfaces."
[^estonia]: [e-Estonia, e-Health Record](https://e-estonia.com/solutions/healthcare/e-health-records/): "the e-Health Record actually **retrieves data as necessary from various providers**, who may be using different systems" and "presents it in a standard format".

*[PMIR]: Patient Master Identity Registry, perfil IHE que gestiona la identidad maestra del paciente
*[PIXm]: Patient Identifier Cross-referencing for mobile, perfil IHE que enlaza los identificadores locales de un paciente con su identidad maestra
*[PDQm]: Patient Demographics Query for Mobile, perfil IHE de búsqueda de pacientes por datos demográficos
*[MHD]: Mobile access to Health Documents, perfil IHE para publicar, localizar y recuperar documentos sobre FHIR
*[MHDS]: Mobile Health Document Sharing, perfil IHE que compone MHD, PMIR, mCSD, IUA y ATNA en una comunidad de intercambio de documentos
*[mCSD]: Mobile Care Services Discovery, perfil IHE de directorio de organizaciones, servicios y endpoints
*[IUA]: Internet User Authorization, perfil IHE que aplica OAuth 2.0 a las transacciones sobre FHIR
*[ATNA]: Audit Trail and Node Authentication, perfil IHE de auditoría y seguridad de los nodos
*[BALP]: Basic Audit Log Patterns, perfil IHE con los patrones de AuditEvent de FHIR
*[PCF]: Privacy Consent on FHIR, perfil IHE de consentimiento del paciente
