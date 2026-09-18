HIX es una comunidad de intercambio de documentos clínicos construida sobre el perfil **[MHDS](https://profiles.ihe.net/ITI/MHDS/volume-1.html)** de IHE, con una restricción añadida que define su arquitectura. **La localización y la recuperación de documentos se median de forma centralizada, mientras la custodia de los documentos permanece distribuida** entre los miembros que los producen. Este volumen especifica esa arquitectura, desde los conceptos y decisiones sobre los que se apoya hasta el modelo de confianza que la sostiene, pasando por sus actores, las transacciones que los vinculan, las opciones que admite y los flujos que soporta.

Cada perfil que HIX compone aporta una pieza de esa arquitectura.

- **[MHD](https://profiles.ihe.net/ITI/MHD/index.html)** pone las transacciones con las que se publica, localiza y recupera un documento.
- **[PMIR](https://profiles.ihe.net/ITI/PMIR/index.html)**, **[PIXm](https://profiles.ihe.net/ITI/PIXm/index.html)** y **[PDQm](https://profiles.ihe.net/ITI/PDQm/index.html)** ponen la identidad maestra del paciente y su vínculo con las identidades locales.
- **[mCSD](https://profiles.ihe.net/ITI/mCSD/index.html)** pone el directorio del que la infraestructura central aprende dónde responde cada custodio.
- **[IUA](https://profiles.ihe.net/ITI/IUA/index.html)** y OAuth 2.0 ponen los tokens que cruzan cada límite de confianza, con **[SMART App Launch](https://build.fhir.org/ig/HL7/smart-app-launch/)** cuando quien autoriza es una persona.
- **[ATNA](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html)** con **[BALP](https://profiles.ihe.net/ITI/BALP/index.html)** pone el registro que hace reconstruible cada divulgación.

Lo que ningún perfil cubre, como el intercambio de tokens hacia un custodio o el lanzamiento de la aplicación del paciente, HIX lo especifica como transacción propia, identificada como `HIX-n`, en el Volumen 2.

### Infraestructura Central

<a href="central-architecture-diagram.svg" target="_blank" title="Abrir a tamaño completo en una pestaña nueva">![Infraestructura central de HIX](central-architecture-diagram.svg)</a>

**Figura 2-1:** Infraestructura central de HIX
{: #figura-2-1}

La [Figura 2-1](volume-1.html#figura-2-1) muestra la infraestructura central de la comunidad, es decir, los servicios que HIX opera y las transacciones que los conectan. Es una vista de arquitectura, no de despliegue, y por eso omite las agrupaciones transversales que casi todo actor lleva, como el Time Client de CT. Tampoco dibuja los sistemas de los miembros. Un miembro solo trata con la infraestructura central, nunca con otro miembro. Obtiene sus tokens del Authorization Server, localiza y recupera a través del Record Locator Service, y publica y declara identidades ante la infraestructura central. Los demás componentes de la figura no le exigen ninguna integración adicional.

- El **Record Locator Service** es el mediador de la comunidad. Localiza y recupera documentos en nombre de los miembros y aplica la decisión de divulgación. Ante los miembros actúa como Resource Server; ante los componentes centrales y los custodios, como cliente delegado que opera en nombre del solicitante original.
- El **Authorization Server** es el único emisor de tokens de la comunidad. Emite el token que permite a un miembro acceder al mediador, lo valida mediante introspección cuando el mediador lo presenta y, cada vez que el mediador necesita alcanzar a un custodio o a un componente central, lo intercambia por un token acotado a ese destino, a nombre del miembro.
- El **Document Registry** conserva los punteros a los documentos publicados en la comunidad y resuelve la identidad maestra de cada uno al indexarlo.
- Los **"Shared HIE Services"** completan la infraestructura con el directorio de la comunidad (mCSD), que describe a los miembros y sus endpoints; el registro de identidad maestra (PMIR), que mantiene una identidad por persona; y el Audit Record Repository (ATNA), que concentra los eventos de los componentes centrales. Cada miembro registra su propio lado.
- La **fuente autoritativa de identidad del paciente** es externa a la comunidad y es la única que puede crear identidades maestras. HIX no la designa; la propuesta para Costa Rica es que sea el EDUS, el expediente digital único de la CCSS, porque ya tiene resuelta la identificación de las personas.

Dicho en seis afirmaciones:

1. La comunidad es **la única contraparte** de sus miembros. El Authorization Server emite todo token, el Record Locator Service media toda localización y recuperación, y la infraestructura central valida lo que cada miembro publica y declara. **Ningún miembro interactúa con otro.**
2. El **índice es central y el contenido es del custodio**. Un documento se queda donde se produjo; la comunidad sabe que existe, de quién es y quién lo conserva.
3. La **divulgación se decide una vez por cada consulta**, en la infraestructura central, sobre los metadatos del índice y antes de que se mueva contenido alguno. Localizar y recuperar son dos consultas, y cada una se decide por sí misma.
4. Cada recuperación alcanza al custodio con una **credencial derivada de la petición viva del solicitante**, atada a ese único custodio, con una vida de dos minutos como máximo y verificable por el custodio con las claves públicas del Authorization Server. Ningún participante tiene credenciales permanentes hacia otro.
5. La **identidad maestra del paciente está anclada en la identidad nacional verificada**; los miembros declaran sus identidades locales y la comunidad las vincula. Ningún miembro crea una persona.
6. El **transporte hacia cada custodio se declara en el directorio**, no en los punteros ni en la API. Cuando la comunidad opera sobre una red de intercambio como [X-Road](https://x-road.global/), el endpoint del custodio indica ese canal y el Record Locator Service lo recorre automáticamente, sin que cambie un puntero, un token ni una transacción. X-Road es transporte y confianza entre organizaciones; la semántica del intercambio sigue siendo la de los perfiles FHIR.

> **Nota.** El Record Locator Service no tiene acceso arbitrario a nada, ni siquiera al Document Registry. Solo actúa cuando un miembro se lo pide, con una credencial derivada de esa petición y a nombre de ese miembro. Es el primer PEP de la comunidad, el punto en el que se aplica su política, y por eso cada interacción queda auditable de extremo a extremo.

### Cómo leer este volumen

- **Conceptos y decisiones de arquitectura** explica el porqué de cada decisión, la alternativa que descarta y lo que cuesta.
- **Actores y transacciones** define los actores de HIX, las transacciones que los vinculan y los requisitos normativos de cada uno.
- **Capacidades opcionales de los actores** describe lo que un actor puede declarar además de lo requerido, sin dejar de ser conforme.
- **Agrupaciones de actores requeridas** enumera los actores de otros perfiles que cada actor de HIX agrupa.
- **Casos de uso y flujos** recorre los escenarios que la arquitectura soporta, con el flujo de cada uno.
- **Consideraciones de seguridad** especifica el modelo de confianza, los dos regímenes de token y los controles de seguridad y privacidad.

El Volumen 2 especifica cada transacción y el Volumen 3 el contenido que se intercambia. Este volumen describe qué hace cada actor y por qué; los siguientes, cómo.
