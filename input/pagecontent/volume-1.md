HIX es una comunidad de intercambio de documentos clínicos sobre FHIR. Sigue el modelo que IHE llama **Centralized Discovery and Retrieve**, en el que un localizador central permite descubrir dónde están los documentos y recuperarlos del custodio que registró su existencia ([IHE HIE Whitepaper, §2.8](https://profiles.ihe.net/ITI/HIE-Whitepaper/index.html#28-document-sharing-models))[^hie-cdr]. HIX lo aplica con una precisión. También la recuperación pasa por ese localizador, de modo que **la localización y la recuperación se median de forma centralizada, mientras la custodia de los documentos permanece distribuida** entre los miembros que los producen.

IHE realiza ese modelo sobre FHIR con **[MHDS](https://profiles.ihe.net/ITI/MHDS/volume-1.html)**. HIX lo toma como arquitectura de referencia, sin declarar conformidad con él, y compone directamente los perfiles que resuelven cada pieza, por las razones que da la [sección 2.1](volume-1-concepts.html#relacion-con-mhds).

Cada perfil que HIX compone aporta una pieza de esa arquitectura.

- **[MHD](https://profiles.ihe.net/ITI/MHD/5.0.0/index.html)** pone las transacciones con las que se publica, localiza y recupera un documento.
- **[PMIR](https://profiles.ihe.net/ITI/PMIR/index.html)**, **[PIXm](https://profiles.ihe.net/ITI/PIXm/index.html)** y **[PDQm](https://profiles.ihe.net/ITI/PDQm/index.html)** ponen la identidad maestra del paciente y su vínculo con las identidades locales.
- **[mCSD](https://profiles.ihe.net/ITI/mCSD/index.html)** pone el directorio del que la infraestructura central aprende dónde responde cada custodio.
- **[IUA](https://profiles.ihe.net/ITI/IUA/index.html)** y OAuth 2.0 ponen los tokens que cruzan cada límite de confianza, con **[SMART App Launch](https://hl7.org/fhir/smart-app-launch/)** cuando quien autoriza es una persona.
- **[ATNA](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html)** con **[BALP](https://profiles.ihe.net/ITI/BALP/index.html)** pone el registro que hace reconstruible cada divulgación.

Lo que ningún perfil cubre, como el intercambio de tokens hacia un custodio o el lanzamiento de la aplicación del paciente, HIX lo especifica como transacción propia, identificada como `HIX-n`, en el Volumen 2.

### Infraestructura Central

<a href="central-architecture-diagram.svg" target="_blank" title="Abrir a tamaño completo en una pestaña nueva">![Infraestructura central de HIX](central-architecture-diagram.svg)</a>

**Figura 2-1:** Infraestructura central de HIX
{: #figura-2-1}

La [Figura 2-1](volume-1.html#figura-2-1) muestra la infraestructura central de la comunidad, es decir, los servicios que HIX opera y las transacciones que los conectan. Es una vista de arquitectura, no de despliegue. Omite las agrupaciones transversales que casi todo actor lleva, como el Time Client de CT, y no dibuja los sistemas de los miembros, que solo tratan con la infraestructura central y nunca entre sí.

- El **Record Locator Service** es el mediador de la comunidad. Localiza y recupera documentos en nombre de los miembros y aplica la decisión de divulgación.
- El **Authorization Server** es el único emisor de tokens de la comunidad. Emite el token con el que un miembro llega al mediador y lo intercambia por otro, acotado a un destino, cada vez que el mediador tiene que alcanzar a un custodio o a un componente central.
- El **Document Registry** conserva los punteros a los documentos publicados, cada uno con la identidad maestra del paciente como sujeto.
- Los **Shared HIE Services** de la figura completan la infraestructura. El directorio de la comunidad describe a los miembros y sus endpoints, el registro de identidad maestra mantiene una identidad por persona y el Audit Record Repository concentra los eventos de los componentes centrales.
- La **fuente autoritativa de identidad** es externa a la comunidad y la única que puede crear identidades maestras. HIX no la designa. Propone que en Costa Rica sea el EDUS, el expediente digital único de la CCSS, que ya tiene resuelta la identificación de las personas.

Dicho en seis afirmaciones.

1. La comunidad es **la única contraparte** de sus miembros. **Ningún miembro interactúa con otro.**
2. El **índice es central y el contenido es del custodio**. Un documento se queda donde se produjo, y la comunidad sabe que existe, de quién es y quién lo conserva.
3. La **divulgación se decide una vez por cada consulta**, en la infraestructura central, sobre los metadatos del índice y antes de mover contenido alguno. Localizar y recuperar son dos consultas.
4. Cada recuperación alcanza al custodio con una **credencial derivada de la petición viva del solicitante**, el [token intercambiado](appendix-glossary.html#token-intercambiado), que vale para ese único custodio, dura dos minutos como máximo y el custodio verifica por sí mismo. Ningún participante tiene credenciales permanentes hacia otro, ni siquiera el mediador.
5. La **identidad maestra del paciente está anclada en la identidad nacional verificada**. Los miembros declaran sus identidades locales, la comunidad las vincula y ningún miembro crea una persona.
6. El **transporte hacia cada custodio se declara en el directorio**, no en los punteros ni en la API. Una red de intercambio como [X-Road](https://x-road.global/) puede llevar ese tramo sin que cambie un puntero, un token ni una transacción.

### Cómo leer este volumen

- **Conceptos y decisiones de arquitectura** explica el porqué de cada decisión, la alternativa que descarta y lo que cuesta.
- **Actores y transacciones** define los actores de HIX, las transacciones que los vinculan y los requisitos normativos de cada uno.
- **Capacidades opcionales de los actores** describe lo que un actor puede declarar además de lo requerido, sin dejar de ser conforme.
- **Agrupaciones de actores requeridas** enumera los actores de otros perfiles que cada actor de HIX agrupa.
- **Casos de uso y flujos** recorre los escenarios que la arquitectura soporta, con el flujo de cada uno.
- **Consideraciones de seguridad** especifica el modelo de confianza, los dos regímenes de token y los controles de seguridad y privacidad.

El Volumen 2 especifica cada transacción. Este volumen describe qué hace cada actor y por qué, y el siguiente, cómo.

### Referencias

[^hie-cdr]: [IHE HIE Whitepaper, §2.8 Document Sharing Models](https://profiles.ihe.net/ITI/HIE-Whitepaper/index.html#28-document-sharing-models): "**Centralized Discovery and Retrieve** – in this model, a centralized locator is used to discover the location of documents which enables a retrieval of the document from a custodian who has registered existence of the document with the centralized locator". [§3 Document Sharing Profiles](https://profiles.ihe.net/ITI/HIE-Whitepaper/index.html#3-document-sharing-profiles) asocia ese modelo a "Mobile access to Health Documents (MHD), Mobile Health Document Sharing (MHDS), and Cross-Enterprise Document Sharing (XDS)".
