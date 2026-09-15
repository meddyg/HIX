HIX es una comunidad de intercambio de documentos clínicos construida sobre el perfil **[MHDS](https://profiles.ihe.net/ITI/MHDS/volume-1.html)** de IHE, con una restricción añadida que define su arquitectura. **La localización y la recuperación de documentos se median de forma centralizada, mientras la custodia de los documentos permanece distribuida** entre los miembros que los producen. Este volumen especifica esa arquitectura, desde los conceptos y decisiones sobre los que se apoya hasta el modelo de confianza que la sostiene, pasando por sus actores, las transacciones que los vinculan, las opciones que admite y los flujos que soporta.

Cada perfil que HIX compone aporta una pieza de esa arquitectura. [MHD](https://profiles.ihe.net/ITI/MHD/index.html) pone las transacciones con las que se publica, localiza y recupera un documento; [PMIR](https://profiles.ihe.net/ITI/PMIR/index.html), [PIXm](https://profiles.ihe.net/ITI/PIXm/index.html) y [PDQm](https://profiles.ihe.net/ITI/PDQm/index.html), la identidad maestra del paciente y su vínculo con las identidades locales; [mCSD](https://profiles.ihe.net/ITI/mCSD/index.html), el directorio del que la infraestructura central aprende dónde responde cada custodio; [IUA](https://profiles.ihe.net/ITI/IUA/index.html) y OAuth 2.0, los tokens que cruzan cada límite de confianza, con [SMART App Launch](https://build.fhir.org/ig/HL7/smart-app-launch/) cuando quien autoriza es una persona; y [ATNA](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html) con [BALP](https://profiles.ihe.net/ITI/BALP/index.html), el registro que hace reconstruible cada divulgación. Lo que ningún perfil cubre, como el intercambio de tokens hacia un custodio o el lanzamiento de la aplicación del paciente, HIX lo especifica como transacción propia, identificada como `HIX-n`, en el Volumen 2.

### Infraestructura Central

![Infraestructura central de HIX](central-architecture-diagram.svg)

**Figura 2-1:** Infraestructura central de HIX

La Figura 2-1 muestra la infraestructura central de la comunidad, es decir, los servicios que HIX opera y las transacciones que los conectan. Es una vista de arquitectura, no de despliegue, y por eso omite las agrupaciones transversales que todo actor lleva, como CT Time Client (Consistent Time). Tampoco dibuja los sistemas de los miembros. Un miembro solo se comunica con dos de los componentes de la figura, el Record Locator Service y el Authorization Server; los demás están detrás del Record Locator Service.

- El **Record Locator Service** es el mediador de la comunidad y el único punto de entrada de los miembros para toda transacción clínica y de identidad. Ante los miembros actúa como Resource Server; ante los servicios centrales y los custodios, como cliente delegado que opera en nombre del solicitante original.
- El **Authorization Server (STS)** es el único emisor de tokens de la comunidad. Emite el token que permite a un miembro acceder al mediador, lo valida mediante introspección cuando el mediador lo presenta y, cada vez que el mediador necesita alcanzar a un custodio o a un servicio central, lo intercambia por un token acotado a ese destino, a nombre del miembro.
- El **Document Registry** conserva los punteros a los documentos publicados en la comunidad. Solo el mediador puede alcanzarlo.
- Los **"Shared HIE Services"** completan la infraestructura con el directorio de la comunidad (mCSD), que describe a los miembros y sus endpoints; el registro de identidad maestra (PMIR), que mantiene una identidad por persona; y el repositorio de auditoría (ATNA), que concentra los eventos de ambos extremos de cada divulgación. Ningún miembro los consulta directamente.
- La **fuente autoritativa de identidad del paciente** es externa a la comunidad y es la única que puede crear identidades maestras. HIX no la designa; la propuesta para Costa Rica es que sea el EDUS, el expediente digital único de la CCSS, porque ya tiene resuelta la identificación de las personas.

Dicho en seis afirmaciones:

1. La comunidad expone exactamente **dos caras** a sus miembros. El Record Locator Service atiende toda transacción clínica y de identidad, y el Authorization Server emite todo token. **Ningún miembro interactúa con otro.**
2. El **índice es central y el contenido es del custodio**. Un documento se queda donde se produjo; la comunidad sabe que existe, de quién es y quién lo conserva.
3. La **divulgación se decide una sola vez**, en el mediador, sobre los metadatos del índice y antes de que se mueva contenido alguno.
4. Cada recuperación alcanza al custodio con una **credencial derivada de la petición viva del solicitante**, atada a ese único custodio, con una vida de segundos y verificable sin llamar a nadie. Ningún participante tiene credenciales permanentes hacia otro.
5. La **identidad maestra del paciente está anclada en la identidad nacional verificada**; los miembros declaran sus identidades locales y la comunidad las vincula. Ningún miembro crea una persona.
6. El **transporte hacia cada custodio se declara en el directorio**, no en los punteros ni en la API. Cuando la comunidad opera sobre una red de intercambio como [X-Road](https://x-road.global/), el endpoint del custodio indica ese canal y el Record Locator Service lo recorre automáticamente, pasando del TLS directo al canal mTLS de la red sin que cambie un puntero, un token ni una transacción. X-Road es transporte y confianza entre organizaciones; la semántica del intercambio sigue siendo la de los perfiles FHIR.

> **Nota.** El Record Locator Service no tiene acceso arbitrario a nada, ni siquiera al Document Registry. Solo actúa cuando un miembro se lo pide, con una credencial derivada de esa petición y a nombre de ese miembro. Es el primer punto de aplicación de la política de la comunidad (PEP), y por eso cada interacción queda auditable de extremo a extremo.

### Cómo leer este volumen

- **Conceptos y decisiones de arquitectura** explica el porqué de cada decisión, la alternativa que descarta y lo que cuesta.
- **Actores y transacciones** define los actores de HIX, las transacciones que los vinculan y los requisitos normativos de cada uno.
- **Capacidades opcionales de los actores** describe lo que un actor puede declarar además de lo requerido, sin dejar de ser conforme.
- **Agrupaciones de actores requeridas** enumera los actores de otros perfiles que cada actor de HIX agrupa.
- **Casos de uso y flujos** recorre los escenarios que la arquitectura soporta, con el flujo de cada uno.
- **Consideraciones de seguridad** especifica el modelo de confianza, los tres regímenes de token, lo que la arquitectura garantiza y lo que no.
- **Consideraciones entre perfiles y despliegue** muestra cómo se combinan los perfiles en sistemas concretos y qué modelos de despliegue admite la comunidad.

El Volumen 2 especifica cada transacción y el Volumen 3 el contenido que se intercambia. Este volumen describe qué hace cada actor y por qué; los siguientes, cómo.
