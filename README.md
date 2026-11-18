# ExploraGuajira

ExploraGuajira es un proyecto académico desarrollado en Python y tecnologías web para organizar y presentar información sobre destinos turísticos de Colombia, con énfasis en La Guajira.

El proyecto cuenta con dos formas de uso:

- **Aplicación de consola en Python:** permite listar destinos, consultar sus detalles y filtrarlos por tipo.
- **Aplicación web:** presenta cinco destinos mediante tarjetas, fotografías, ubicaciones en Google Maps, consulta del clima y un asistente turístico con inteligencia artificial.

## 1. Objetivo

Ofrecer una herramienta sencilla para conocer cinco destinos turísticos registrados en el proyecto, consultar información básica sobre ellos y explorar sus ubicaciones. La versión web incorpora además un asistente que responde preguntas relacionadas con esos destinos.

## 2. Funcionalidades

### Aplicación de consola

- Mostrar todos los sitios turísticos registrados.
- Consultar los detalles de un sitio.
- Buscar sitios por tipo: Natural, Histórico o Popular.
- Abrir la imagen del sitio seleccionado.
- Construir un enlace de Google Maps a partir de sus coordenadas.
- Recorrer las opciones mediante un menú interactivo.

### Aplicación web

- Mostrar una presentación de ExploraGuajira.
- Presentar cinco destinos en tarjetas con fotografías, ubicación y descripción.
- Abrir la ubicación de cada destino en Google Maps.
- Mostrar un mapa integrado y actualizarlo al seleccionar otro destino.
- Consultar el clima del destino seleccionado mediante Open-Meteo.
- Mostrar condiciones actuales y un resumen del pronóstico de los próximos días.
- Ofrecer un asistente turístico con una interfaz de chat.

### Asistente turístico

- Recibir preguntas desde la página web.
- Responder únicamente sobre los cinco destinos registrados y temas turísticos relacionados.
- Consultar información en la web mediante OpenAI Responses API y la herramienta `web_search` para las preguntas admitidas.
- Presentar las respuestas en español.
- Mostrar las fuentes consultadas cuando el visitante las solicite.
- Validar las consultas, limitar su longitud y aplicar un límite básico de solicitudes por dirección IP.
- Informar cuando falte la configuración de la API o se presente un error de conexión.

## 3. Destinos registrados

Los cinco destinos incluidos son:

1. **Cabo de la Vela** — Uribia, La Guajira.
2. **Punta Gallinas** — Alta Guajira, La Guajira.
3. **Santuario de Fauna y Flora Los Flamencos** — Camarones, Riohacha.
4. **Salinas de Manaure** — Manaure, La Guajira.
5. **Centro Histórico de Cartagena** — Cartagena de Indias, Bolívar.

En `sitios_turisticos.py` se define la lista `sitios_turisticos`. Cada elemento es un diccionario con información del destino, como nombre, tipo, ubicación, descripción, coordenadas y ruta de imagen.

## 4. Estructura del proyecto

```text
Programa_sitios_turisticos/
├── .github/
│   └── workflows/
│       └── pruebas-chatbot.yml
├── Imagenes/
│   ├── Centro_historico_cartagena.jpg
│   ├── Salinas_de_manaure.jpg
│   ├── Santuario_fauna_y_flora_los_flamencos.jpg
│   ├── cabo_de_la_vela.jpg
│   └── punta_gallinas.jpg
├── tests/
│   └── test_servidor.py
├── Web/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   ├── chatbot.css
│   └── chatbot.js
├── .env.example
├── .gitignore
├── main.py
├── servidor.py
├── sitios_turisticos.py
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

### Responsabilidad de los archivos principales

- **`main.py`**: contiene el menú y las funciones de la aplicación de consola. Utiliza Pillow para abrir las imágenes.
- **`sitios_turisticos.py`**: almacena la lista de destinos y sus datos.
- **`servidor.py`**: crea el servidor Flask, sirve la página web, expone la ruta `/api/chat` y se comunica con OpenAI.
- **`Web/index.html`**: define la estructura de la página y las secciones de destinos, mapas, clima y asistente.
- **`Web/style.css`**: define los estilos generales de la página.
- **`Web/script.js`**: controla el selector de destinos, el mapa y la consulta del clima.
- **`Web/chatbot.js`**: envía preguntas al servidor y presenta respuestas y fuentes.
- **`Web/chatbot.css`**: define los estilos de la interfaz del asistente.
- **`Imagenes/`**: contiene las fotografías de los destinos.
- **`tests/test_servidor.py`**: contiene las pruebas automatizadas del servidor.
- **`requirements.txt`**: enumera las dependencias necesarias para ejecutar la aplicación.
- **`requirements-dev.txt`**: incorpora las dependencias de desarrollo y pruebas.
- **`.env.example`**: plantilla de configuración de variables de entorno, sin credenciales reales.
- **`.gitignore`**: excluye archivos locales como el entorno virtual y `.env`.
- **`.github/workflows/pruebas-chatbot.yml`**: configura la ejecución automatizada de las pruebas en GitHub Actions.

Es importante respetar los nombres y las mayúsculas de las carpetas y archivos al escribir las rutas de las imágenes.

## 5. Requisitos

- Python instalado.
- Un navegador web actualizado.
- Conexión a Internet para cargar Google Maps, consultar Open-Meteo y utilizar el asistente.
- Una clave API válida de OpenAI para generar respuestas del asistente.

La consulta del clima utiliza Open-Meteo y no requiere una clave API propia. El asistente sí necesita la variable `OPENAI_API_KEY` configurada en el entorno.

## 6. Instalación y configuración

Los siguientes comandos se ejecutan desde la carpeta principal del repositorio.

### 6.1. Crear y activar un entorno virtual

En Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación del entorno, se puede utilizar la terminal de CMD:

```bat
.venv\Scripts\activate.bat
```

### 6.2. Instalar las dependencias

Para ejecutar la aplicación:

```bash
python -m pip install -r requirements.txt
```

Para instalar también las herramientas de pruebas:

```bash
python -m pip install -r requirements-dev.txt
```

`requirements-dev.txt` incluye las dependencias de `requirements.txt` y agrega pytest.

### 6.3. Configurar la API de OpenAI

1. Copia el archivo `.env.example` y crea, en la raíz del proyecto, un archivo llamado `.env`.
2. Abre `.env` y configura las variables:

```env
OPENAI_API_KEY=tu_clave_api
OPENAI_MODEL=gpt-5.5
```

3. Guarda el archivo.

La clave debe mantenerse privada. No la escribas en archivos HTML o JavaScript, no la subas a GitHub y no la compartas en capturas o conversaciones. El archivo `.env` está excluido mediante `.gitignore`; el archivo `.env.example` solo contiene nombres de variables y valores de ejemplo.

La creación y administración de una cuenta API y cualquier configuración de pagos deben realizarse con el acompañamiento de un padre, madre o tutor, de acuerdo con los requisitos de edad aplicables.

## 7. Cómo ejecutar el proyecto

### 7.1. Iniciar la aplicación web y el asistente

Desde la carpeta principal, con el entorno virtual activado, ejecuta:

```bash
python servidor.py
```

Abre en el navegador:

```text
http://127.0.0.1:5000
```

Flask sirve `Web/index.html` en la ruta principal y los recursos estáticos de la carpeta `Web/`. La ruta `POST /api/chat` recibe las preguntas del asistente.

Mantén abierta la terminal mientras utilizas la página. Para detener el servidor, vuelve a esa terminal y presiona `Ctrl + C`.

Si no se ha configurado `OPENAI_API_KEY`, la página web podrá abrirse, pero el asistente no podrá generar respuestas y mostrará un aviso de configuración.

### 7.2. Ejecutar la aplicación de consola

En otra terminal, desde la carpeta principal y con las dependencias instaladas, ejecuta:

```bash
python main.py
```

El menú permite:

1. Mostrar todos los sitios turísticos.
2. Consultar los detalles de un sitio.
3. Buscar sitios por tipo.
4. Salir.

La aplicación de consola es independiente del servidor web.

## 8. Clima y mapas

La página utiliza un mapa de Google Maps insertado mediante un `iframe`. Cuando el visitante selecciona otro destino, JavaScript actualiza la ubicación del mapa.

La consulta del clima se realiza desde `Web/script.js` mediante el servicio Open-Meteo. Se utilizan las coordenadas del destino seleccionado y la zona horaria `America/Bogota`. La interfaz presenta temperatura, sensación térmica, humedad, viento y un resumen del pronóstico de los días siguientes.

Estas funciones necesitan conexión a Internet. Si el servicio externo no responde, la página muestra un mensaje indicando que no fue posible cargar la información.

## 9. Alcance y validaciones del asistente

El asistente está limitado a preguntas sobre estos cinco destinos: Cabo de la Vela, Punta Gallinas, Santuario de Fauna y Flora Los Flamencos, Salinas de Manaure y Centro Histórico de Cartagena.

El servidor aplica una validación inicial basada en palabras clave: la pregunta debe mencionar uno de los destinos reconocidos y contener términos relacionados con turismo, geografía, historia, cultura, ambiente o economía. Esta validación es una barrera sencilla y no un clasificador semántico infalible. Las instrucciones enviadas al modelo también delimitan el contenido de las respuestas.

Otras validaciones implementadas:

- La pregunta debe ser texto y no puede estar vacía.
- La longitud máxima es de 1000 caracteres.
- El cuerpo de la solicitud tiene un tamaño máximo configurado en Flask.
- Se aplica un límite de 12 solicitudes por minuto y por dirección IP.
- Las fuentes se extraen y se validan para aceptar únicamente URL HTTP o HTTPS.
- Las fuentes no se muestran en la respuesta inicial, salvo que el visitante las solicite.

### Consideraciones técnicas

- Cada consulta admitida requiere una llamada a OpenAI con la herramienta de búsqueda web obligatoria. El uso de la API y de la búsqueda puede tener costos según las condiciones de la cuenta y los precios vigentes.
- El límite de solicitudes se almacena en memoria. Para un despliegue con varios procesos o instancias debe utilizarse un mecanismo compartido, por ejemplo Redis.
- El servidor incluido utiliza el servidor de desarrollo de Flask. Antes de publicar el proyecto en Internet se debe configurar un servidor WSGI de producción, HTTPS, controles de seguridad y un limitador de solicitudes apropiado.
- No se debe publicar el archivo `.env` ni registrar claves API en el repositorio.

## 10. Pruebas automatizadas e integración continua

Las pruebas del servidor se encuentran en `tests/test_servidor.py`.

Instala las dependencias de desarrollo:

```bash
python -m pip install -r requirements-dev.txt
```

Ejecuta las pruebas desde la raíz del proyecto:

```bash
python -m pytest -q
```

La configuración de GitHub Actions está en `.github/workflows/pruebas-chatbot.yml`. El flujo instala las dependencias y ejecuta pytest en los eventos configurados para las ramas `main` y `chatbot-ia`, y para solicitudes de integración dirigidas a `main`.

Las pruebas automatizadas verifican comportamientos del servidor. No sustituyen las pruebas manuales de la página web, la conexión con OpenAI ni la disponibilidad de servicios externos.

## 11. Ramas de trabajo

El desarrollo del asistente se realiza en la rama `chatbot-ia`. Los cambios de esta rama no se incorporan a `main` automáticamente; su integración debe realizarse mediante una revisión y una decisión explícita del equipo del proyecto.

Para cambiar a la rama del asistente:

```bash
git switch chatbot-ia
git pull origin chatbot-ia
```

## 12. Estado del proyecto

El proyecto integra actualmente:

- Aplicación de consola en Python.
- Página web con cinco destinos turísticos.
- Mapa interactivo de Google Maps.
- Consulta del clima mediante Open-Meteo.
- Asistente turístico conectado a un backend Flask y OpenAI.
- Validaciones básicas de alcance, longitud de preguntas, frecuencia de solicitudes y enlaces de fuentes.
- Pruebas automatizadas y flujo de integración continua con GitHub Actions.

ExploraGuajira continúa siendo un proyecto académico en evolución. Las funcionalidades externas dependen de la conexión a Internet y de la disponibilidad y configuración de sus respectivos servicios.
