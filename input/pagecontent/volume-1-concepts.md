Esta sección explica las decisiones que dan forma a esta comunidad. Cada una se presenta con lo que decide, por qué lo decide y lo que cuesta. Son decisiones de arquitectura, no de implementación. Una comunidad puede desplegarlas de muchas maneras (véase la sección 2.7) sin que cambie nada de lo que aquí se describe. Las dos tablas del final resumen las alternativas descartadas y los compromisos asumidos.

### Comunidad y límite de confianza

Una comunidad HIX es un conjunto de organizaciones que acuerdan compartir documentos clínicos bajo una política común y a través de una infraestructura común. La pertenencia es explícita. Una organización es miembro cuando figura en el directorio de la comunidad y el Authorization Server reconoce a sus sistemas.

**En una malla de pares, las garantías de la comunidad valen lo que valga su miembro más débil.** Ese es el argumento que decide la topología. Si cada participante descubre y consulta a los demás, cada uno tiene que implementar el descubrimiento, mantener tantas relaciones de confianza como miembros haya, poner un punto de aplicación de política delante de sus propios datos y auditar por su cuenta. La política de la comunidad se aplica entonces en tantos lugares como miembros, con la calidad que cada uno pueda pagar, y basta un miembro mal implementado para que la garantía deje de existir para todos. IHE describe ambas topologías en su whitepaper sobre intercambio de información de salud ([HIE Whitepaper, §2.8](https://profiles.ihe.net/ITI/HIE-Whitepaper/index.html#28-document-sharing-models) y [§3.2](https://profiles.ihe.net/ITI/HIE-Whitepaper/index.html#32-centralized-discovery-and-retrieve))[^hie-wp]. HIX elige la centralizada y absorbe esa complejidad una sola vez, en el centro, donde se puede operar, verificar y auditar.

Por esta razón, la relación de confianza no se establece de forma directa entre los miembros, sino entre cada participante y la infraestructura central. Un miembro no confía en los demás ni necesita conocerlos; confía en que la comunidad autoriza, media y registra cada interacción. Integrarse a HIX es integrarse una sola vez, con la comunidad. No hay que integrarse con cada uno de los demás miembros, ni volver a hacerlo cuando entra uno nuevo.

### Mediación central de la localización y la recuperación

Toda localización y toda recuperación pasan por el Record Locator Service. Un solicitante obtiene del mediador los punteros que la política le permite ver, y las URL de contenido que recibe apuntan al propio mediador, nunca al custodio. Al recuperar, el mediador alcanza al custodio en nombre del solicitante y le entrega el documento.

MHDS admite que un consumidor alcance directamente al servicio que aloja un documento fuera del registro ([MHDS Vol. 1, §1:50.1.1.2](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150112-storage-of-binary))[^mhds-storage]. HIX no lo admite, y la razón está en el propio perfil. MHDS reconoce, al definir su Consent Manager Option, que esa opción **no protege el contenido almacenado fuera del registro** y que, cuando los documentos se almacenan en otro lugar, cada Document Source carga solo con la protección de sus documentos ([MHDS Vol. 1, §1:50.2.2](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15022-consent-manager-option))[^mhds-consent]. Con custodia distribuida y acceso directo, cada custodio tendría que evaluar la política de la comunidad frente a cada consumidor. La mediación cierra ese hueco. Existe un único punto donde se aplica la política de divulgación, una única superficie auditable que ve la interacción completa y un único contrato de integración.

El precio es que la infraestructura central se vuelve indispensable para operar, y se dimensiona y protege como tal. Todo byte clínico transita el mediador. La sección 2.6 especifica lo que eso exige.

> **Nota.** El mediador es desacoplable. No añade semántica propia; solo concentra el PEP y las transacciones que MHDS reparte entre los miembros. Sin él, la comunidad operaría como MHDS estándar, con el mismo flujo, pero cada miembro tendría que aplicar la política, resolver endpoints, obtener credenciales y auditar por su cuenta. Quitar el mediador no cambia la arquitectura; mueve el PEP a cada miembro.

### Custodia distribuida y colocación central

El documento permanece donde se produjo. El miembro que lo creó lo conserva, responde por su contenido y participa en cada recuperación que lo alcanza. La infraestructura central mantiene el índice, no una copia del expediente.

MHDS nombra dos colocaciones del contenido como alternativas de primera clase, dentro del registro central o en cualquier otro lugar de la comunidad, incluido el sistema del propio Document Source ([MHDS Vol. 1, §1:50.1.1.2](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150112-storage-of-binary))[^mhds-storage]. HIX adopta la segunda como **política por defecto** y ofrece la primera como opción. Un custodio que no puede alojar un endpoint ejerce la Opción de Colocación Central y entrega el contenido a la infraestructura central sin dejar de figurar como custodio.

Como la API que ve el solicitante es idéntica bajo ambas colocaciones, un custodio puede pasar de una a otra sin que ningún miembro lo note. Por eso "el contenido nunca sale del custodio" es una política por defecto y no un principio absoluto. La arquitectura admite las dos y la comunidad decide por custodio.

### Identidad del paciente (PMIR)

Cada miembro **solo conoce y solo usa sus propios identificadores de paciente**. No conoce los de los demás miembros ni necesita conocerlos. Para la comunidad, cada miembro es un **dominio de identificadores** distinto, y un mismo identificador local solo tiene sentido dentro del dominio del miembro que lo asignó. La comunidad no reemplaza esos identificadores. Mantiene una **identidad maestra** por persona y enlaza con ella las identidades locales que los miembros declaran, de modo que cualquier identificador local, de cualquier miembro, resuelve a la misma persona.

La identidad maestra es un registro de paciente en un dominio reservado a la identidad verificada, en el que solo escribe la fuente autoritativa. Lleva el identificador nacional de la persona, que la ancla a alguien real, y los enlaces a sus identidades locales, uno por cada miembro que la haya declarado. No lleva demografía de los miembros. Los nombres y las fechas se quedan en cada miembro; la comunidad guarda identificadores y enlaces.

![Identidad maestra e identidades locales](hix-master-patient-index.svg)

**Figura 2.1-1:** Identidad maestra e identidades locales

La Figura 2.1-1 muestra cómo se construye. Las declaraciones de los miembros llegan al registro a través del Record Locator Service, que la figura omite en ese papel.

- La **fuente autoritativa de identidad** es quien crea la identidad maestra. Lo hace con el feed **[PMIR](https://profiles.ihe.net/ITI/PMIR/index.html)** ([ITI-93](https://profiles.ihe.net/ITI/PMIR/ITI-93.html)), una vez que comprobó quién es la persona con su identificación nacional. Nadie más puede crear una identidad maestra y como se menciona anteriormente, HIX no define cuál debe ser esa fuente pero propone que sea el EDUS.
- Cada **miembro** declara los pacientes de su dominio con el feed **[PIXm](https://profiles.ihe.net/ITI/PIXm/index.html)** ([ITI-104](https://profiles.ihe.net/ITI/PIXm/ITI-104.html)). Envía su identificador local junto con la identificación nacional de la persona, y el registro enlaza ese identificador local con la identidad maestra que ya existe para esa persona. Si la persona todavía no tiene identidad maestra, la declaración se rechaza. *Un miembro **vincula**, nunca crea.*
- La consulta **determinista** es PIXm ([ITI-83](https://profiles.ihe.net/ITI/PIXm/ITI-83.html)). Recibe un identificador, local o nacional, y devuelve la identidad maestra enlazada a él. Es la vía normal. La usan el Record Locator Service y el Authorization Server cada vez que necesitan saber quién es un paciente.
- La consulta **probabilística** es **[PDQm](https://profiles.ihe.net/ITI/PDQm/index.html)** ([ITI-78](https://profiles.ihe.net/ITI/PDQm/ITI-78.html)). Recibe datos demográficos y devuelve identidades maestras candidatas con un grado de coincidencia. Es el respaldo cuando no hay un identificador fiable. Busca solo entre identidades maestras y se permite según el rol y el propósito de uso de quien consulta.

> **Nota.** Un miembro no puede crear una persona, fusionar dos ni escribir en el dominio de otro. La cuenta de una persona en el Authorization Server no es un identificador de paciente. Y ninguna de las dos consultas prueba una identidad; eso solo lo hace la fuente autoritativa.

### El puntero

La unidad del índice es el puntero, un [`DocumentReference`](https://hl7.org/fhir/R5/documentreference.html) de FHIR R5 que describe un documento sin contenerlo. Toda decisión de la comunidad se toma sobre el puntero, antes de mover un byte del documento, así que lo que el puntero lleva es una decisión de arquitectura. Estos son sus elementos.

- **`subject`** apunta a la identidad maestra del paciente, nunca a una identidad local. Lo escribe el mediador al indexar, a partir del paciente fuente. El miembro no lo declara.
- **`extension` `sourcepatient`** apunta al paciente tal como lo declaró el miembro, con su identificador en su propio dominio. Es la extensión estándar [`documentreference-sourcepatient`](https://hl7.org/fhir/extensions/StructureDefinition-documentreference-sourcepatient.html), que en R5 reemplaza a `context.sourcePatientInfo`. Conserva la traza de qué miembro declaró a quién y permite reconciliar si un enlace de identidad cambia.
- **`custodian.identifier`** nombra a la organización responsable con el mismo identificador que lleva su token y que publica el directorio. Nunca es una referencia a un recurso.
- **`content.attachment.url`** es una ruta relativa. Un puntero nunca contiene una dirección física ni nada que identifique un transporte. La dirección se resuelve en el directorio en cada recuperación.
- **`securityLabel`** lleva la [etiqueta de confidencialidad](https://hl7.org/fhir/R5/security-labels.html) del documento, un código del sistema [v3-Confidentiality](https://terminology.hl7.org/CodeSystem-v3-Confidentiality.html) de HL7, como `N` para normal, `R` para restringido o `V` para muy restringido. Es obligatorio desde la primera publicación. Sin la etiqueta en el índice, decidir si un documento se puede divulgar exigiría leerlo primero, y añadirla después obligaría a releer todos los documentos en los custodios.
- **`identifier`** es el identificador de negocio del documento y es estable, para que republicar el mismo documento actualice su puntero en lugar de duplicarlo.

El resto de elementos, como `status`, `type` o `date`, son los metadatos habituales de MHD y se especifican en el Volumen 3.

### Directorio de la comunidad (mCSD)

El directorio describe las organizaciones participantes, su pertenencia a la comunidad y los endpoints en los que responden. Es la fuente de la que la infraestructura central aprende a quién dirigir una recuperación, por qué canal y qué opciones ejerce cada custodio.

Los miembros no consultan el directorio, porque nunca se comunican entre sí. Lo consulta el mediador, en cada operación, para saber a qué custodio dirigirse y en qué endpoint. Por eso incorporar un miembro no exige reconfigurar nada. Basta con darlo de alta en el directorio para que el mediador pueda alcanzarlo. La resolución es estricta. El directorio debe devolver exactamente una organización activa con exactamente un endpoint activo. Si devuelve cero o más de uno, el mediador trata al custodio como no disponible en lugar de elegir por su cuenta.

El directorio fija dos valores que el resto de la comunidad repite sin traducción. El **identificador de la organización** es el mismo que el Authorization Server incluye en los tokens del miembro para decir en nombre de qué organización actúa, y el mismo que sus punteros llevan en `custodian.identifier`. La **dirección del endpoint** es la URL a la que el mediador llama, la audiencia del token que obtiene para ese custodio y la base contra la que se resuelven las rutas relativas de sus punteros. Como token, puntero y directorio parten del mismo literal, no pueden desincronizarse.

### Autorización y delegación

HIX usa OAuth 2.0 ([RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)) según lo perfila [IUA](https://profiles.ihe.net/ITI/IUA/index.html). La idea de fondo es sencilla. Para hablar con la comunidad, un sistema necesita un token, y todos los tokens los emite un único Authorization Server.

Un miembro obtiene un token para hablar con el Record Locator Service, y solo con él. Ese token no sirve ante ningún custodio, y el miembro nunca recibe uno que sirva. El mediador comprueba cada token que recibe preguntando al Authorization Server si sigue siendo válido. Esa consulta es la introspección de [RFC 7662](https://www.rfc-editor.org/rfc/rfc7662), que IUA recoge como la transacción Introspect Token ([ITI-102](https://profiles.ihe.net/ITI/IUA/index.html#3102-introspect-token-iti-102)).

Cuando una operación exige llegar a un custodio, el mediador no reutiliza el token del miembro. Lo **intercambia** por otro, siguiendo OAuth 2.0 Token Exchange ([RFC 8693](https://www.rfc-editor.org/rfc/rfc8693)). Es decir, presenta al Authorization Server el token del miembro y pide a cambio un token nuevo, hecho a la medida de esa llamada. El token nuevo vale para un solo custodio, que se indica con un resource indicator ([RFC 8707](https://www.rfc-editor.org/rfc/rfc8707)). Vale para una sola transacción. Dura como mucho dos minutos, y nunca más que el token original. Y lleva dentro quién pidió, el miembro, y quién actúa en su nombre, el mediador, en el claim `act` que la RFC define para eso.

El custodio valida ese token por su cuenta, con las claves públicas del Authorization Server, sin llamar a nadie. Así sabe quién pregunta, en nombre de quién actúa la comunidad y para qué.

Lo mismo vale hacia los servicios centrales. El mediador no tiene acceso propio al Registro documental ni al registro de identidad maestra. Publica, busca y resuelve con tokens intercambiados de la misma forma, a nombre del miembro que lo pidió. Un puntero queda registrado a nombre de su custodio, no del mediador. El mediador es el primer punto de aplicación de la política de la comunidad, no un participante con autoridad propia.

La Figura 2.1-2 resume el recorrido de los tokens. Un solo token entra por la izquierda, el del miembro, y de él derivan tantos tokens de un solo destino como custodios y servicios centrales haga falta alcanzar.

![Delegación de tokens en HIX](hix-delegacion.svg)

**Figura 2.1-2:** Delegación de tokens en HIX

Tres reglas hacen que el mínimo privilegio sea estructural, en lugar de depender de la buena conducta de cada parte.

- **Un token, un destino.** Un token que valiera en dos custodios permitiría usarlo contra el otro.
- **Solo el mediador puede intercambiar.** Ningún otro participante puede pedir un token a nombre de un tercero, y los custodios no aceptan tokens llegados por otro camino.
- **La autoridad nunca crece.** El token intercambiado solo permite lo que el miembro ya podía, lo que la comunidad delega al mediador y lo que el custodio ofrece. Poder localizar un documento nunca da poder para recuperarlo.

Un token dice quién pide, qué puede pedir, ante quién y hasta cuándo. El token de un miembro **no nombra a ningún paciente**. Solo lo hace el de una persona que entra a su propio expediente con [SMART App Launch](https://build.fhir.org/ig/HL7/smart-app-launch/scopes-and-launch-context.html), y ahí el paciente en contexto sirve para confinar el token a ese expediente. En ambos casos, **tener un token da derecho a preguntar, no a ver**. Qué documentos se entregan lo decide el mediador, puntero por puntero. Esa separación es la idea más importante de este volumen.

### Referencias

Las citas reproducen el texto publicado por su fuente; los recortes se marcan con "[...]" y la negrita es de esta guía.

[^mhds-consent]: [MHDS Vol. 1, §1:50.2.2 Consent Manager Option](https://profiles.ihe.net/ITI/MHDS/volume-1.html#15022-consent-manager-option): "Note that this option **does not protect Binary content stored outside of the Document Registry** [...]. When documents are stored outside of the Document Registry, **the Document Source system takes on the burden of protecting the document**."
[^mhds-storage]: [MHDS Vol. 1, §1:50.1.1.2 Storage of Binary](https://profiles.ihe.net/ITI/MHDS/volume-1.html#150112-storage-of-binary): "(1) The Document Source includes the Binary Resource in the [ITI-65] transaction, and the Document Registry is required to store it. (2) **The Community allows the Binary to be stored elsewhere in the Community.** [...] This might be other centralized infrastructure, distributed infrastructure, or **within the system implementing the Document Source**. [...] the service hosting the Binary shall: [...] **provide access to the community members**".
[^hie-wp]: [IHE HIE Whitepaper, §2.8 Document Sharing Models](https://profiles.ihe.net/ITI/HIE-Whitepaper/index.html#28-document-sharing-models): "the centralized model **requires knowledge only of the centralized locator** [...]. For Push and Federated approaches **a detailed directory of participating entitles** [sic] is typically used". [§3.2 Centralized Discovery and Retrieve](https://profiles.ihe.net/ITI/HIE-Whitepaper/index.html#32-centralized-discovery-and-retrieve): "a centralized locator is used to discover the location of documents which enables **a retrieval of the document from a custodian** who has registered existence of the document with the centralized locator".
