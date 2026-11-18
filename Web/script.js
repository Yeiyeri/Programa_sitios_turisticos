const selector = document.getElementById("destino-mapa");
const mapa = document.getElementById("mapa-google");

selector.addEventListener("change", function () {

    const destino = selector.value;

    const ubicacion = encodeURIComponent(destino);

    mapa.src = `https://www.google.com/maps?q=${ubicacion}&output=embed`;

    // Actualiza el clima del destino elegido
    cargarClima(selector.selectedOptions[0]);

});

/* ---------- Clima (API Open-Meteo, no requiere clave) ---------- */

// Códigos de clima de Open-Meteo -> texto e ícono
const CLIMA_CODIGOS = {
    0: ["Despejado", "☀️"],
    1: ["Mayormente despejado", "🌤️"],
    2: ["Parcialmente nublado", "⛅"],
    3: ["Nublado", "☁️"],
    45: ["Niebla", "🌫️"],
    48: ["Niebla con escarcha", "🌫️"],
    51: ["Llovizna ligera", "🌦️"],
    53: ["Llovizna", "🌦️"],
    55: ["Llovizna intensa", "🌧️"],
    61: ["Lluvia ligera", "🌦️"],
    63: ["Lluvia", "🌧️"],
    65: ["Lluvia fuerte", "🌧️"],
    80: ["Chubascos ligeros", "🌦️"],
    81: ["Chubascos", "🌧️"],
    82: ["Chubascos fuertes", "⛈️"],
    95: ["Tormenta eléctrica", "⛈️"],
    96: ["Tormenta con granizo", "⛈️"],
    99: ["Tormenta con granizo fuerte", "⛈️"]
};

const DIAS_SEMANA = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];

function infoClima(codigo) {
    return CLIMA_CODIGOS[codigo] || ["Sin datos", "❔"];
}

function porId(id) {
    return document.getElementById(id);
}

// Recibe la <option> seleccionada, que trae data-lat, data-lon y data-nombre
async function cargarClima(opcion) {
    const estado = porId("clima-estado");
    const nombre = opcion.dataset.nombre;

    estado.className = "clima-estado";
    estado.textContent = "Cargando clima de " + nombre + "…";
    porId("clima-destino").textContent = "Clima en " + nombre;
    porId("clima-hoy").hidden = true;
    porId("clima-subtitulo").hidden = true;
    const url = "https://api.open-meteo.com/v1/forecast"
        + "?latitude=" + opcion.dataset.lat
        + "&longitude=" + opcion.dataset.lon
        + "&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m"
        + "&daily=temperature_2m_max,temperature_2m_min"
        + "&hourly=weather_code,precipitation_probability"
        + "&timezone=America%2FBogota&forecast_days=7";

    try {
        const respuesta = await fetch(url);
        if (!respuesta.ok) {
            throw new Error("Error HTTP " + respuesta.status);
        }
        const datos = await respuesta.json();

        // Evita mostrar datos viejos si el usuario cambió de destino mientras cargaba
        if (selector.selectedOptions[0] !== opcion) {
            return;
        }

        mostrarClimaHoy(datos.current);
        mostrarClimaDias(datos.daily, datos.hourly);
        estado.textContent = "";
    } catch (error) {
        // Ignora errores de solicitudes de destinos que ya no están seleccionados
        if (selector.selectedOptions[0] !== opcion) {
            return;
        }

        estado.className = "clima-estado error";
        estado.textContent = "No se pudo cargar el clima. Revisa tu conexión e intenta de nuevo.";
        console.error(error);
    }
}

function mostrarClimaHoy(actual) {
    const [texto, icono] = infoClima(actual.weather_code);

    porId("clima-icono").textContent = icono;
    porId("clima-temp").textContent = Math.round(actual.temperature_2m) + "°C";
    porId("clima-cond").textContent = texto;
    porId("clima-sens").textContent = Math.round(actual.apparent_temperature) + "°C";
    porId("clima-hum").textContent = actual.relative_humidity_2m + "%";
    porId("clima-viento").textContent = Math.round(actual.wind_speed_10m) + " km/h";
    porId("clima-hoy").hidden = false;
}

function crearTexto(etiqueta, clase, texto) {
    const elemento = document.createElement(etiqueta);
    elemento.className = clase;
    elemento.textContent = texto;
    return elemento;
}

// Resume un día con las horas de 6 a.m. a 8 p.m.:
// - condición: la que más se repite (si empatan, la menos severa)
// - lluvia: promedio de la probabilidad de esas horas
function resumenDelDia(horario, fecha) {
    const conteo = {};
    let sumaLluvia = 0;
    let cantidadLluvia = 0;

    for (let i = 0; i < horario.time.length; i++) {
        if (!horario.time[i].startsWith(fecha)) {
            continue;
        }

        const hora = Number(horario.time[i].slice(11, 13));
        if (hora < 6 || hora > 20) {
            continue;
        }

        const codigo = horario.weather_code?.[i];
        if (codigo !== null && codigo !== undefined) {
            conteo[codigo] = (conteo[codigo] || 0) + 1;
        }

        const probabilidad = horario.precipitation_probability?.[i];
        if (typeof probabilidad === "number" && Number.isFinite(probabilidad)) {
            sumaLluvia += probabilidad;
            cantidadLluvia++;
        }
    }

    let codigoFrecuente = null;
    let maximo = 0;

    for (const codigo of Object.keys(conteo).map(Number).sort((a, b) => a - b)) {
        if (conteo[codigo] > maximo) {
            maximo = conteo[codigo];
            codigoFrecuente = codigo;
        }
    }

    return {
        codigo: codigoFrecuente,
        lluvia: cantidadLluvia
            ? Math.round(sumaLluvia / cantidadLluvia)
            : null
    };
}

// El índice 0 es hoy (ya está arriba); aquí se muestran los días siguientes
function mostrarClimaDias(diario, horario) {
    const contenedor = porId("clima-dias");
    contenedor.replaceChildren();

    for (let i = 1; i < diario.time.length; i++) {
        const fecha = new Date(diario.time[i] + "T00:00:00");
        const resumen = resumenDelDia(horario, diario.time[i]);
        const [texto, icono] = infoClima(resumen.codigo);
        const lluvia = resumen.lluvia === null ? "Sin datos" : resumen.lluvia + "%";

        const tarjeta = document.createElement("article");
        tarjeta.className = "clima-dia";

        const temps = crearTexto("div", "clima-dia-temps", Math.round(diario.temperature_2m_max[i]) + "° ");
        temps.appendChild(crearTexto("span", "", Math.round(diario.temperature_2m_min[i]) + "°"));

        tarjeta.append(
            crearTexto("div", "clima-dia-nombre", i === 1 ? "Mañana" : DIAS_SEMANA[fecha.getDay()]),
            crearTexto("div", "clima-dia-icono", icono),
            crearTexto("div", "clima-dia-cond", texto),
            temps,
            crearTexto("div", "clima-dia-lluvia", "Lluvia: " + lluvia)
        );
        contenedor.appendChild(tarjeta);
    }

    porId("clima-subtitulo").hidden = false;
}

// Clima del destino que aparece seleccionado al abrir la página
cargarClima(selector.selectedOptions[0]);
