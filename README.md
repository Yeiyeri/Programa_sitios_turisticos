# ExploraGuajira

ExploraGuajira es un proyecto académico desarrollado con Python y tecnologías web para organizar y presentar información sobre destinos turísticos de Colombia, con énfasis en La Guajira.

La aplicación permite explorar destinos turísticos mediante tarjetas informativas, fotografías, ubicaciones en Google Maps, consulta del clima y un asistente turístico con inteligencia artificial.

## 1. Objetivo

Ofrecer una herramienta web que facilite el conocimiento de destinos turísticos, permitiendo consultar información básica, explorar sus ubicaciones geográficas y obtener respuestas sobre sus características e importancia.

## 2. Funcionalidades

### Aplicación web

- Presentar información de cinco destinos turísticos.
- Mostrar tarjetas con fotografías, ubicación y descripción.
- Cargar los destinos desde un archivo JSON centralizado.
- Consultar las ubicaciones mediante Google Maps.
- Actualizar el mapa según el destino seleccionado.
- Consultar las condiciones climáticas mediante Open-Meteo.
- Mostrar temperatura, sensación térmica, humedad, viento y pronóstico de los próximos días.
- Ofrecer un asistente turístico con inteligencia artificial.

### Asistente turístico

- Recibir preguntas desde la interfaz web.
- Responder preguntas relacionadas con los cinco destinos registrados.
- Consultar información mediante OpenAI Responses API y la herramienta `web_search`.
- Presentar respuestas en español.
- Mostrar fuentes consultadas cuando el visitante las solicite.
- Validar las preguntas y limitar su longitud.
- Aplicar un límite básico de solicitudes por dirección IP.
- Informar cuando se presenten errores de conexión o configuración.

## 3. Destinos registrados

Los cinco destinos incluidos son:

1. **Cabo de la Vela** — Uribia, La Guajira.
2. **Punta Gallinas** — Alta Guajira, La Guajira.
3. **Santuario de Fauna y Flora Los Flamencos** — Camarones, Riohacha.
4. **Salinas de Manaure** — Manaure, La Guajira.
5. **Centro Histórico de Cartagena** — Cartagena de Indias, Bolívar.

La información de los destinos se encuentra centralizada en `datos/destinos.json`.

## 4. Estructura del proyecto

```text
Programa_sitios_turisticos/
├── .github/
│   └── workflows/
│       └── pruebas-chatbot.yml
├── datos/
│   └── destinos.json
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
│   ├── chatbot.css
│   ├── script.js
│   └── chatbot.js
├── .env.example
├── .gitignore
├── servidor.py
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

### Responsabilidad de los archivos principales

- **`servidor.py`**: configura Flask, sirve la aplicación web, carga los destinos, expone las rutas de la API y gestiona las consultas del asistente.
- **`datos/destinos.json`**: almacena la información centralizada de los destinos turísticos.
- **`Web/index.html`**: define la estructura de la página.
- **`Web/style.css`**: contiene los estilos generales de la aplicación.
- **`Web/chatbot.css`**: contiene los estilos de la interfaz del asistente.
- **`Web/script.js`**: carga los destinos, genera las tarjetas, actualiza el mapa y consulta el clima.
- **`Web/chatbot.js`**: gestiona el envío de preguntas y la presentación de respuestas y fuentes.
- **`Imagenes/`**: almacena las fotografías de los destinos.
- **`tests/test_servidor.py`**: contiene las pruebas automatizadas del servidor.
- **`requirements.txt`**: contiene las dependencias necesarias para ejecutar la aplicación.
- **`requirements-dev.txt`**: contiene las dependencias adicionales para desarrollo y pruebas.
- **`.env.example`**: proporciona una plantilla para configurar las variables de entorno.
- **`.gitignore`**: excluye archivos locales y datos que no deben subirse al repositorio.

## 5. Requisitos

- Python instalado.
- Navegador web actualizado.
- Conexión a Internet para Google Maps, Open-Meteo y el asistente.
- Clave API de OpenAI configurada para utilizar el asistente.

La consulta del clima utiliza Open-Meteo y no requiere una clave API propia.

## 6. Instalación y configuración

Los siguientes comandos se ejecutan desde la carpeta principal del proyecto.

### 6.1. Crear y activar un entorno virtual

En Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 6.2. Instalar las dependencias

Para ejecutar la aplicación:

```powershell
python -m pip install -r requirements.txt
```

Para instalar también las herramientas de pruebas:

```powershell
python -m pip install -r requirements-dev.txt
```

### 6.3. Configurar OpenAI

1. Copiar `.env.example` y crear un archivo `.env` en la raíz del proyecto.
2. Configurar la variable de entorno:

```env
OPENAI_API_KEY=tu_clave_api
```

3. Guardar el archivo.

La clave debe mantenerse privada y no debe publicarse en GitHub ni incluirse en archivos HTML o JavaScript.

## 7. Ejecución del proyecto

Con el entorno virtual activado, ejecutar:

```powershell
python servidor.py
```

Abrir en el navegador:

```text
http://127.0.0.1:5000
```

Flask sirve la página web y proporciona los siguientes servicios:

- `GET /api/destinos`: devuelve los destinos registrados en el archivo JSON.
- `POST /api/chat`: recibe y procesa las preguntas del asistente turístico.

Mantener abierta la terminal mientras se utiliza la aplicación.

Para detener el servidor, presionar `Ctrl + C`.

## 8. Clima y mapas

La aplicación utiliza Google Maps mediante un mapa integrado en la página. Cuando el visitante selecciona otro destino, JavaScript actualiza su ubicación utilizando las coordenadas almacenadas en el JSON.

La consulta del clima se realiza mediante Open-Meteo. Se utilizan las coordenadas del destino seleccionado y la zona horaria `America/Bogota`.

La interfaz presenta las condiciones actuales y un resumen del pronóstico de los días siguientes.

## 9. Alcance y validaciones del asistente

El asistente está limitado a preguntas relacionadas con los cinco destinos turísticos registrados.

El servidor realiza una validación inicial de las preguntas mediante palabras clave relacionadas con los destinos y temas turísticos permitidos.

También implementa:

- Validación del contenido de las preguntas.
- Restricción de preguntas vacías.
- Longitud máxima de 1000 caracteres.
- Límite de solicitudes por dirección IP.
- Validación de las fuentes para aceptar únicamente enlaces HTTP o HTTPS.
- Manejo de errores de conexión y configuración.

### Consideraciones técnicas

- Las consultas al asistente utilizan OpenAI Responses API y búsqueda web.
- El uso de la API puede generar costos según las condiciones de la cuenta.
- El límite de solicitudes se almacena en memoria.
- Para publicar el proyecto en Internet se requiere configurar un servidor de producción, HTTPS y controles de seguridad adicionales.
- No se debe publicar el archivo `.env`.

## 10. Pruebas automatizadas e integración continua

Las pruebas automatizadas se encuentran en `tests/test_servidor.py`.

Para ejecutarlas:

```powershell
python -m pytest -q
```

El proyecto también cuenta con una configuración de GitHub Actions para ejecutar pruebas automatizadas.

Las pruebas verifican el comportamiento del servidor, pero no sustituyen las comprobaciones manuales de la página web y los servicios externos.

## 11. Estado del proyecto

ExploraGuajira integra actualmente:

- Aplicación web desarrollada con Flask.
- Cinco destinos turísticos registrados.
- Datos centralizados mediante JSON.
- Tarjetas dinámicas con fotografías y descripciones.
- Integración con Google Maps.
- Consulta del clima mediante Open-Meteo.
- Asistente turístico con OpenAI.
- Validaciones básicas de seguridad y alcance.
- Pruebas automatizadas.

ExploraGuajira es un proyecto académico