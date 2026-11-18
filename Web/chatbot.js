const formularioChat = document.getElementById("formulario-chat");
const entradaChat = document.getElementById("pregunta-chat");
const mensajesChat = document.getElementById("mensajes-chat");
const botonEnviarChat = document.getElementById("enviar-chat");
let ultimasFuentes = [];

function esSolicitudDeFuentes(texto) {
    const pregunta = texto.toLocaleLowerCase("es");
    return [
        "fuente", "fuentes", "referencia", "referencias",
        "enlace", "enlaces", "link", "links",
        "de donde sacaste", "de dónde sacaste",
        "de donde obtuviste", "de dónde obtuviste"
    ].some((frase) => pregunta.includes(frase));
}

function agregarMensajeChat(texto, tipo) {
    const mensaje = document.createElement("div");
    mensaje.className = "mensaje-chat " + tipo;
    mensaje.textContent = texto;
    mensajesChat.appendChild(mensaje);
    mensajesChat.scrollTop = mensajesChat.scrollHeight;
    return mensaje;
}

function agregarFuentesChat(contenedor, fuentes) {
    if (!fuentes || fuentes.length === 0) return;

    const bloque = document.createElement("div");
    bloque.className = "fuentes-chat";

    const titulo = document.createElement("strong");
    titulo.textContent = "Fuentes consultadas";
    bloque.appendChild(titulo);

    const lista = document.createElement("ul");
    fuentes.forEach((fuente) => {
        const item = document.createElement("li");
        const enlace = document.createElement("a");
        enlace.href = fuente.url;
        enlace.textContent = fuente.title || fuente.url;
        enlace.target = "_blank";
        enlace.rel = "noopener noreferrer";
        item.appendChild(enlace);
        lista.appendChild(item);
    });

    bloque.appendChild(lista);
    contenedor.appendChild(bloque);
    mensajesChat.scrollTop = mensajesChat.scrollHeight;
}

formularioChat.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const pregunta = entradaChat.value.trim();
    if (!pregunta) return;

    agregarMensajeChat(pregunta, "mensaje-usuario");
    entradaChat.value = "";

    // Si el visitante pide las fuentes después de una respuesta,
    // mostramos los enlaces guardados de la última consulta.
    if (esSolicitudDeFuentes(pregunta) && ultimasFuentes.length > 0) {
        const respuestaFuentes = agregarMensajeChat(
            "Estas son las fuentes consultadas para mi respuesta anterior:",
            "mensaje-asistente"
        );
        agregarFuentesChat(respuestaFuentes, ultimasFuentes);
        return;
    }
    entradaChat.disabled = true;
    botonEnviarChat.disabled = true;

    const cargando = agregarMensajeChat("Preparando respuesta…", "mensaje-asistente");

    try {
        const respuesta = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: pregunta })
        });

        const datos = await respuesta.json();
        cargando.remove();

        if (!respuesta.ok) {
            agregarMensajeChat(datos.error || "Ocurrió un error al procesar la pregunta.", "mensaje-error");
            return;
        }

        ultimasFuentes = Array.isArray(datos.sources) ? datos.sources : [];
        const respuestaElemento = agregarMensajeChat(
            datos.answer || "No se recibió una respuesta.",
            "mensaje-asistente"
        );
        if (esSolicitudDeFuentes(pregunta)) {
            agregarFuentesChat(respuestaElemento, ultimasFuentes);
        }
    } catch (error) {
        cargando.remove();
        agregarMensajeChat(
            "No se pudo conectar con el servidor. Comprueba que esté ejecutándose.",
            "mensaje-error"
        );
        console.error(error);
    } finally {
        entradaChat.disabled = false;
        botonEnviarChat.disabled = false;
        entradaChat.focus();
    }
});
