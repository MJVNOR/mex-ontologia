# Open Ontologies Studio instalado para mex-ontologi

**Actualización del modelo:** la copia de trabajo ya incluye páginas y esquemas del portal y tiene 21,617 triples. Las cifras de 8,851 triples de las secciones siguientes describen la instalación inicial. Ver [modelo ampliado y sincronización](modelo-portal.md).

## Instalación

- Aplicación: `open-ontologies-studio`, versión 0.1.0.
- Motor incluido: 2.1.0, compilado desde el código fuente del repositorio.
- Fuente local: `C:\Users\marti\Documents\open-ontologies`.
- Commit de partida: `93295305201c7374988217fd6fa609de0fd643ee`.
- Instalación mediante el instalador NSIS generado, con código de salida 0.
- LLVM instalado con winget; se utilizaron Rust, Node.js, herramientas C++ y Windows SDK ya disponibles.

La aplicación aparece como **open-ontologies-studio**. También se preparó un acceso directo en la carpeta de este proyecto.

## Catálogo que abre

La aplicación carga `data/catalogo/studio-live.ttl`, una copia para trabajar en Studio. Contiene el modelo y los datos del catálogo, con declaraciones de clases y etiquetas adicionales para su árbol e inspector. La copia tiene 8,851 triples y 698 entidades de datos, incluidos 89 conjuntos y 486 recursos.

El RDF original `catalogo.ttl` y el almacén del pipeline permanecen separados. Las ediciones y el guardado automático de Studio afectan su copia de trabajo; no actualizan el portal ni el grafo del pipeline. La aplicación vuelve a cargar esa copia al abrirse.

En **2D**, expandir «Conjunto de datos» para explorar los 89 conjuntos. «Dependencia» muestra las 25 organizaciones. Los recursos se encuentran dentro de Resource → Recurso registrado en CKAN. Seleccionar una entidad abre su inspector.

**3D** permite elegir **Entidades** (predeterminado) o **Clases**. Entidades carga todos los sujetos y objetos con URI y sus relaciones, sin límite fijo de 300; los literales de texto y números se consultan en el inspector. La consulta del catálogo actual devuelve 16,939 entidades y 70,175 relaciones. Clases conserva la proyección del esquema, también sin ese límite. La leyenda del modo live muestra los conteos del grafo cargado.

En **Entidades**, el deslizador **Mostrar** elige cuántas entidades se dibujan, desde 1 hasta el total (inicialmente 1,000). El campo numérico permite escribir una cantidad exacta. La vista prioriza entidades conectadas y muestra solo relaciones cuyos extremos están visibles. Cambiar la cantidad no modifica el grafo guardado.

Las relaciones `rdf:type` se ocultan inicialmente para que las clases comunes no concentren todos los puntos en una esfera; **Incluir tipos (rdf:type)** permite recuperarlas. La selección recorre conexiones en profundidad. Las relaciones se distinguen por color y, en vistas de hasta 2,000 puntos, llevan flechas. Pulsar un nodo aísla sus conexiones dentro del conjunto visible y muestra una tabla de origen, relación y destino. **Volver al conjunto** restaura la selección del deslizador.

La navegación 3D live usa **Rotar** y **Mover**. En Mover, arrastrar con el botón izquierdo desplaza la cámara lateral y verticalmente; el botón derecho o Mayús + arrastrar también desplazan desde Rotar. La rueda cambia el zoom. Haz clic en el fondo del grafo para enfocar el teclado: flechas (o A/D y Q/E) desplazan; W/S avanzan y retroceden conservando la orientación; F o **Centrar** encuadran el conjunto. **Enfocar nodo** acerca la cámara al nodo seleccionado. Los atajos no actúan mientras se escribe en el chat o en los campos de la interfaz.

Pulsar una arista resalta esa conexión y abre **Relación seleccionada**, con origen, relación y destino. **Ver identificadores completos** despliega las URI sin recortar. También se puede abrir este detalle pulsando el nombre de una relación en la tabla de conexiones del nodo. **Cerrar detalle** regresa a la vista previa sin cambiar el encuadre ni el conjunto de puntos.

No se configuró un proveedor de IA ni credenciales. El árbol, inspector y conexión con el motor se verificaron sin depender del chat.

**Configuración posterior de Gemini:** el acceso directo `Abrir Studio.lnk` ahora ejecuta `scripts/abrir_studio_gemini.ps1`, que lee el `.env` local del proyecto y transmite la configuración únicamente al proceso de Studio. Se usa el endpoint oficial `https://generativelanguage.googleapis.com/v1beta/openai` con `gemini-3.5-flash`. El `.env` y sus variantes están excluidos por `.gitignore`; `.env.example` contiene solo una plantilla sin credenciales. No añadir `.env` con `git add -f`.

La clave queda en texto plano en `.env`, según la configuración solicitada. El lanzador valida la clave y la disponibilidad del modelo antes de abrir Studio. Para cambiar clave o modelo, edita `.env`, guarda y cierra Studio y vuelve a abrirlo.

Studio también lee esa configuración al iniciarse directamente desde el ejecutable o el menú Inicio: `agent-env-path.txt`, junto al ejecutable instalado, contiene únicamente la ruta absoluta al `.env`. El proceso del agente recibe las variables permitidas, incluida `ONTO_NODE_BINARY`; la clave permanece en `.env` y no se incorpora a la compilación. Un archivo configurado que falte o esté incompleto produce un error visible en el chat, en lugar de volver silenciosamente al modelo `default`. El antiguo acceso `Abrir Studio sin Gemini.lnk` conserva su nombre histórico, pero apunta al mismo ejecutable y ahora también lee la configuración guardada.

Se verificó la apertura directa del ejecutable instalado, sin el lanzador: el chat mostró `Model: gemini-3.5-flash` y respondió a un saludo con «Hola, un saludo cordial», sin modificar el grafo. Pasaron las 9 pruebas de configuración y rutas del agente. La recuperación de relaciones se corrigió posteriormente y se comprobó con la pregunta del diccionario descrita en la sección de recuperación de evidencia.

Comprobación de configuración sin mostrar la clave:

```powershell
./scripts/abrir_studio_gemini.ps1 -Comprobar
./scripts/abrir_studio_gemini.ps1 -Validar
```

Referencia del endpoint y modelo: https://ai.google.dev/gemini-api/docs/openai

Se corrigió el inicio del agente en Windows: se normaliza el prefijo de ruta `\\?\` antes de entregar el archivo JavaScript a Node. El lanzador permite seleccionar el ejecutable real de Node mediante `ONTO_NODE_BINARY` y `scripts/studio-gemini.json`. Además se omite el parámetro local `chat_template_kwargs` al llamar a Gemini, se omiten herramientas vacías y se limita la espera de generación a 90 segundos. Las 12 pruebas del agente y las 6 pruebas de resolución de rutas del chat pasaron.

La consulta de modelos confirmó que la API acepta la clave. Gemini 3.8 Flash agotó los plazos de prueba y Studio mostró HTTP 503 por alta demanda del modelo. Se cambió a Gemini 3.5 Flash: una generación mínima respondió y una pregunta de solo lectura recorrió el sidecar completo y terminó con `done` y `mutated: false`. La recuperación actual encontró 16 entidades pero ninguna relación en esa pregunta; no se verificó que pueda responder agregaciones o conteos del catálogo. La actualización del ejecutable instalado y del sidecar se hizo directamente; los instaladores anteriores no incluyen necesariamente estos últimos ajustes. Para regenerarlos, ejecuta `scripts/compilar-studio.cmd` sin argumentos. El parámetro `--no-bundle` permite reconstruir solo la aplicación.

### Recuperación de evidencia para el chat

El chat ofrece `Copiar` en cada mensaje y `Copiar todo` en la cabecera. El primer botón copia el texto del mensaje con sus enlaces Markdown; el segundo copia la conversación en orden, indicando Usuario, Asistente o Sistema. Ambos muestran `Copiado` al completar la operación y permiten reintentar si el portapapeles falla.

Se corrigió el recuperador del sidecar para conservar acentos e identificadores como `año_matrimonio`, priorizar identificadores específicos, mantener las URI completas y usarlas como referencias SPARQL válidas. Ahora recorre hasta dos saltos para alcanzar definiciones y fuentes. Los errores de consulta se muestran como errores, en lugar de convertirse en listas vacías. Las respuestas almacenadas se identifican por pregunta, evidencia, modelo e instrucciones, de modo que una respuesta previa sin evidencia no reaparece al corregir el grafo o el recuperador. Varias fuentes de procedencia ya no se presentan por sí solas como una contradicción.

Pasaron las 18 pruebas del agente. La prueba aislada con la pregunta «¿Qué significa la variable año_matrimonio según su diccionario? Consulta el grafo y muestra la evidencia.» recuperó 229 relaciones y respondió «Año de registro», tipo «Numérico entero», formato «NNNN», obligatoriedad «Si», citando la definición y el CSV de origen. El grafo permaneció sin cambios. Resultado: `reports/chat-recuperacion.json`.

Para repetir la prueba, que inicia y cierra su propio motor en memoria en un puerto independiente:

```powershell
./.venv/Scripts/python.exe scripts/comprobar_recuperacion_chat.py
```

### Panel de validación SHACL

El botón superior `Paneles` muestra u oculta el bloque completo `Findings / Validation`. Al ocultarlo se amplía el espacio del grafo; al mostrarlo se conserva la pestaña seleccionada y el resultado de validación de esa sesión.

En modo live se oculta `Corpus`: el motor no expone una lectura de cuerpos de documentos compatible con ese panel. El lector de documentos se conserva en replay, donde usa el bundle precomputado. La revisión de hallazgos en live es de solo lectura; sus acciones `Accept` / `Reject` y el libro de decisiones también se reservan al replay, porque no existe una operación de persistencia para esas decisiones en live. No se añadieron documentos ficticios ni herramientas MCP inexistentes. Las 56 pruebas del frontend y TypeScript pasaron después de este ajuste.

La pestaña `Validation` ahora ejecuta `onto_shacl` sobre el grafo cargado, con un archivo de reglas editable que inicialmente toma `VITE_SHAPES_PATH`. Muestra el archivo utilizado, la fecha de ejecución, los nodos objetivo sumados por regla, los incumplimientos reportados y el informe completo del motor. El resultado deja de ser concluyente cuando no se comprobaron nodos, se omitieron restricciones, faltan coincidencias o la cobertura es incompleta. Hay que repetirlo después de editar el grafo. La conformidad cubre únicamente las reglas seleccionadas.

La comparación de dos corpus precomputados se conserva en el replay. También se retiró `Compare` del modo live, donde aún no tiene implementación. En la comprobación contra el motor activo, las reglas `data/catalogo/shapes.ttl` evaluaron 695 nodos objetivo y reportaron cero incumplimientos. Las 56 pruebas del frontend y TypeScript pasaron.

### Acceso al chat

Se retiró la pestaña `Chat` del panel de demostración en modo live: llamaba a `DemoSource.ask()`, que rechaza las solicitudes en ese modo y mostraba el mensaje técnico «Chat does not run through DemoSource in live mode». El chat real se abre con el botón `Chat` de la barra superior y usa `send_chat_message` y los eventos `agent-message` del sidecar. La pestaña de demostración se conserva en modo replay.

Se recompiló Studio y se actualizó el ejecutable instalado. Se guardó el grafo y se creó un respaldo `data/backups/studio-antes-chat-*.ttl` antes del reinicio; el ejecutable anterior se conserva como `open-ontologies-studio.exe.antes-chat.bak` junto al instalado. Pasaron las 48 pruebas de frontend y TypeScript. La corrección no configura un proveedor de IA: el sidecar usa por defecto `http://localhost:8081/v1`, donde no se encontró un servidor durante esta revisión.

## Ajustes locales en Studio

Se mantuvo la aplicación nativa y se aplicaron correcciones de integración en su copia local:

- Aceptar las respuestas SPARQL del motor sin perder nodos.
- Eliminar duplicados en la consulta de clases.
- Usar la URI completa como identidad del árbol: un conjunto y su registro pueden compartir UUID y son entidades distintas.
- Inicialmente se amplió el límite de individuos a 2,000. La corrección posterior eliminó ese recorte global y comprobó los 15,904 individuos del grafo; ver [studio-limite-individuos.md](studio-limite-individuos.md).
- Cargar la copia de trabajo y las reglas SHACL de este proyecto mediante variables de compilación.
- Recargar los paneles después de conectar y cargar los datos, evitando errores de inicio prematuros.
- Encontrar el motor junto al ejecutable instalado.
- Ejecutar el motor y el proceso Node sin ventanas de consola persistentes.

Las variables están en `studio/.env.local` dentro del repositorio de Open Ontologies:

```dotenv
VITE_SHAPES_PATH=C:/Users/marti/Documents/MEX-Ontologi/data/catalogo/shapes.ttl
VITE_LIVE_FILE=C:/Users/marti/Documents/MEX-Ontologi/data/catalogo/studio-live.ttl
```

Los cambios de código están respaldados en `reports/studio-ajustes-locales.patch`. El parche no incluye `.env.local`, que está ignorado por Git. No se publicaron cambios en el repositorio remoto.

## Comprobaciones realizadas

- Compilación del motor y de la aplicación de Windows.
- Generación de instaladores MSI y NSIS.
- 48 pruebas de frontend aprobadas.
- Conexión HTTP y MCP con el motor compilado; conteos verificados contra el catálogo.
- Apertura de la aplicación instalada y carga de la copia de trabajo.
- Comprobación visual de «Connected», los conjuntos y las entidades del árbol, sin el fallo de UUID compartidos.
- Activación de la vista 3D nativa.

## Reconstrucción

Desde la carpeta MEX-Ontologi:

```powershell
cmd.exe /d /c scripts\compilar-motor-studio.cmd
cmd.exe /d /c scripts\compilar-studio.cmd
```

Los scripts contienen las rutas de Visual Studio y del repositorio de este equipo. La compilación usa los archivos de bloqueo de Cargo y las dependencias de npm instaladas desde su lockfile.

Instaladores generados:

- `C:\Users\marti\Documents\open-ontologies\studio\src-tauri\target\release\bundle\nsis\open-ontologies-studio_0.1.0_x64-setup.exe`
- `C:\Users\marti\Documents\open-ontologies\studio\src-tauri\target\release\bundle\msi\open-ontologies-studio_0.1.0_x64_en-US.msi`

Si se cambia la ubicación del proyecto, hay que actualizar las variables de compilación y reconstruir Studio. Para refrescar los metadatos desde la API, se ejecuta el pipeline; la copia editable de Studio no se reemplaza automáticamente, para conservar las ediciones hechas en ella.
