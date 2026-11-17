# ExploraGuajira

ExploraGuajira es un proyecto académico que comenzó como una aplicación de consola desarrollada en Python y que actualmente está evolucionando hacia una página web. Su propósito es organizar y presentar información básica sobre destinos turísticos, principalmente de La Guajira.

La versión web permite explorar cinco destinos mediante tarjetas con fotografías y descripciones, abrir sus ubicaciones en Google Maps y consultar un mapa integrado que cambia según el destino seleccionado.

## 1. Objetivo del proyecto

El objetivo es ofrecer una forma sencilla y visual de conocer lugares de interés turístico. El proyecto conserva su versión inicial de consola en Python y cuenta con una primera interfaz web desarrollada con HTML, CSS y JavaScript.

## 2. Funcionalidades implementadas hasta el momento

### Versión de consola (Python)

- Mostrar los sitios turísticos registrados.
- Consultar los detalles de un sitio.
- Filtrar los sitios por tipo: Natural, Histórico o Popular.
- Abrir la imagen del sitio seleccionado.
- Construir y mostrar un enlace de Google Maps a partir de sus coordenadas.
- Recorrer las opciones mediante un menú interactivo.

### Versión web (HTML, CSS y JavaScript)

- Mostrar una sección de presentación de ExploraGuajira.
- Presentar cinco destinos turísticos en tarjetas con imagen, nombre, ubicación y descripción.
- Incluir enlaces «Ver ubicación» que abren Google Maps para cada destino.
- Mostrar Google Maps dentro de la página mediante un elemento `iframe`.
- Permitir seleccionar un destino en una lista desplegable y actualizar el mapa sin salir de la página.
- Adaptar la distribución de las tarjetas y algunos elementos a pantallas más pequeñas mediante reglas CSS `@media`.

La consulta del clima todavía no está implementada. Los enlaces de navegación «Clima» y «Acerca de» están presentes en la barra, pero sus secciones aún están pendientes de desarrollo.

## 3. Estructura del proyecto

La estructura de trabajo actual es:

```text
Programa_sitios_turisticos/
├── main.py
├── sitios_turisticos.py
├── README.md
├── .gitignore
├── Imagenes/
│   ├── Centro_historico_cartagena.jpg
│   ├── Salinas_de_manaure.jpg
│   ├── Santuario_fauna_y_flora_los_flamencos.jpg
│   ├── cabo_de_la_vela.jpg
│   └── punta_gallinas.jpg
└── Web/
    ├── index.html
    ├── style.css
    └── script.js
```

### Responsabilidad de los archivos

- **`main.py`**: contiene las funciones y el menú de la aplicación de consola.
- **`sitios_turisticos.py`**: almacena la lista de destinos turísticos y sus datos.
- **`Imagenes/`**: contiene las fotografías utilizadas en la página web.
- **`Web/index.html`**: define la estructura y el contenido de la interfaz web.
- **`Web/style.css`**: define los colores, la distribución, las tarjetas, los botones y los ajustes para pantallas pequeñas.
- **`Web/script.js`**: controla el selector de destinos y actualiza la dirección del mapa integrado.
- **`README.md`**: contiene la documentación general del proyecto.
- **`.gitignore`**: excluye archivos temporales, entornos virtuales y configuración local.

Es importante respetar los nombres y las mayúsculas de las carpetas y archivos al escribir las rutas de las imágenes.

## 4. Datos de los destinos turísticos

En `sitios_turisticos.py` se define una lista llamada `sitios_turisticos`. Cada elemento es un diccionario con información de un lugar.

Los diccionarios utilizan estas claves:

| Clave | Función |
|---|---|
| `nombre` | Nombre del destino. |
| `tipo` | Categoría: Natural, Histórico o Popular. |
| `ubicacion` | Ubicación escrita del sitio. |
| `descripcion` | Descripción breve del lugar. |
| `latitud` | Coordenada de latitud. |
| `longitud` | Coordenada de longitud. |
| `imagen` | Ruta del archivo de imagen asociado. |

Los cinco destinos registrados son:

1. **Cabo de la Vela** — Uribia, La Guajira.
2. **Punta Gallinas** — Alta Guajira, La Guajira.
3. **Santuario de Fauna y Flora Los Flamencos** — Camarones, Riohacha.
4. **Salinas de Manaure** — Manaure, La Guajira.
5. **Centro Histórico de Cartagena** — Cartagena de Indias, Bolívar.

Se utiliza una lista para reunir los destinos y recorrerlos mediante ciclos. Los diccionarios permiten acceder a cada dato mediante una clave, por ejemplo `sitio["nombre"]` o `sitio["latitud"]`.

**Nota sobre las rutas de imágenes:** la página web utiliza rutas relativas desde `Web/`, como `../Imagenes/cabo_de_la_vela.jpg`. En cambio, los registros Python actualmente contienen rutas que comienzan por `imagenes/`. Conviene mantener o unificar estas rutas al revisar la compatibilidad de la versión de consola en distintos sistemas operativos.

## 5. Organización de la versión de consola

El archivo `main.py` importa la lista de `sitios_turisticos.py` y contiene estas funciones:

- **`mostrar_sitios()`**: recorre la lista y muestra el nombre y el tipo de cada destino.
- **`mostrar_detalles()`**: muestra la lista numerada, solicita una selección, presenta los datos del destino, abre su imagen con Pillow y muestra un enlace de Google Maps.
- **`mostrar_por_tipo()`**: permite elegir una categoría y muestra los destinos que coinciden con ella.
- **`menu()`**: mantiene el menú activo con un ciclo `while` y ejecuta la función correspondiente a la opción elegida.

El bloque `if __name__ == "__main__":` inicia el menú cuando se ejecuta directamente el archivo `main.py`.

## 6. Organización de la versión web

La carpeta `Web/` contiene tres archivos que trabajan en conjunto.

### 6.1. HTML: `index.html`

Define la estructura de la página:

- **Barra de navegación:** contiene enlaces a Inicio, Destinos, Mapas, Clima y Acerca de.
- **Presentación:** muestra el título «Descubre La Guajira», un texto introductorio y una imagen destacada.
- **Destinos:** presenta cinco tarjetas. Cada tarjeta contiene una fotografía, el nombre del lugar, su ubicación, una descripción y un enlace para abrir su localización en Google Maps.
- **Mapas:** contiene una lista desplegable y un mapa insertado mediante un `iframe`.

Las imágenes de la web se referencian con rutas relativas. Por ejemplo:

```html
<img src="../Imagenes/cabo_de_la_vela.jpg"
     alt="Paisaje del Cabo de la Vela">
```

### 6.2. CSS: `style.css`

Controla la presentación visual de la página. Actualmente incluye:

- Barra de navegación verde y enlaces con efecto al pasar el cursor.
- Distribución de la portada con Flexbox.
- Cuadrícula de tarjetas con CSS Grid.
- Fotografías recortadas para mantener una presentación uniforme.
- Botones verdes para abrir las ubicaciones.
- Contenedor del mapa con bordes redondeados y sombra.
- Estilos para la lista desplegable de destinos.
- Reglas `@media` para reorganizar las tarjetas y ajustar los espacios en pantallas pequeñas.

### 6.3. JavaScript: `script.js`

Permite que el mapa cambie cuando el visitante selecciona otro destino.

El archivo obtiene los elementos HTML mediante sus identificadores:

- `destino-mapa`: identifica la lista desplegable.
- `mapa-google`: identifica el `iframe` que contiene el mapa.

Después escucha el evento `change` del selector. Cuando cambia la opción, obtiene el destino seleccionado, adapta el texto para utilizarlo en una URL mediante `encodeURIComponent()` y actualiza el atributo `src` del mapa.

El archivo JavaScript se conecta desde `index.html`, justo antes de cerrar la etiqueta `body`:

```html
<script src="script.js"></script>
```

### 6.4. ¿Cómo se integra Google Maps?

En esta etapa se utiliza un mapa insertado con un `iframe` y la dirección de Google Maps con el parámetro `output=embed`. JavaScript actualiza la búsqueda que se muestra en ese marco cuando cambia la selección.

Esta solución permite mostrar un mapa dentro de la página sin implementar todavía Google Maps JavaScript API. Los enlaces «Ver ubicación» de las tarjetas, por su parte, abren Google Maps en otra pestaña.

## 7. Requisitos

### Para la versión web

- Un navegador web actualizado.
- Los archivos HTML, CSS y JavaScript dentro de la carpeta `Web/`.
- Las fotografías en la carpeta `Imagenes/`, con los nombres que aparecen en las rutas del HTML.
- Conexión a Internet para cargar Google Maps.

No se necesita instalar un paquete de Python para abrir la versión web actual.

### Para la versión de consola

- Python 3.
- Pillow, utilizada por `main.py` para abrir las imágenes.

Instalación de Pillow:

```bash
python -m pip install Pillow
```

## 8. Cómo ejecutar el proyecto

### Abrir la página web

1. Abre la carpeta principal del proyecto en Visual Studio Code.
2. Entra en la carpeta `Web/`.
3. Abre `index.html` en un navegador. También puedes utilizar Live Server si tienes instalada esa extensión.
4. Comprueba que se carguen las imágenes y las cinco tarjetas.
5. En la sección Mapas, selecciona diferentes destinos y verifica que el mapa se actualice.

Si una fotografía no aparece, revisa que el nombre del archivo y la ruta de `src` coincidan exactamente con los archivos de `Imagenes/`.

### Ejecutar la aplicación de consola

1. Abre una terminal en la carpeta principal del proyecto.
2. Si todavía no está instalada, instala Pillow.
3. Ejecuta:

```bash
python main.py
```

El menú permite mostrar todos los destinos, consultar los detalles de uno, filtrar por categoría o salir.

## 9. Alcance actual y trabajo pendiente

### Lo que ya está desarrollado

- Estructura de datos turística en Python mediante una lista de diccionarios.
- Menú de consola para listar, consultar y filtrar destinos.
- Página web inicial con navegación y presentación.
- Cinco tarjetas de destinos con imágenes y descripciones.
- Enlaces individuales a las ubicaciones de Google Maps.
- Mapa integrado en la página.
- Selector que cambia el destino mostrado en el mapa.
- Estilos visuales y adaptación básica a pantallas pequeñas.

### Lo que falta por desarrollar

- Conectar la información de `sitios_turisticos.py` con la página web. Actualmente, las tarjetas HTML y las opciones del selector están escritas manualmente.
- Implementar una consulta del clima mediante un servicio o API meteorológica.
- Crear el contenido de las secciones Clima y Acerca de.
- Evaluar futuras mejoras de interacción y presentación.

Por ahora, la versión web es una interfaz estática con interacción en el navegador. Todavía no existe una conexión entre la página y un servidor backend en Python, ni una base de datos.

## 10. Conclusión

ExploraGuajira ha pasado de una primera aplicación de consola en Python a una versión web inicial desarrollada con HTML, CSS y JavaScript. La aplicación de consola permite consultar y filtrar los destinos registrados, mientras que la página web presenta esos lugares mediante tarjetas, enlaces a Google Maps y un mapa integrado que cambia según la selección del visitante.

El proyecto continúa en desarrollo. Los siguientes avances previstos son conectar los datos de Python con la web e incorporar la consulta del clima de los destinos.
