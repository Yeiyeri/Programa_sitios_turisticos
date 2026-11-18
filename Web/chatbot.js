const formularioChat = document.getElementById("formulario-chat");
const entradaChat = document.getElementById("pregunta-chat");
const mensajesChat = document.getElementById("mensajes-chat");
const botonEnviarChat = document.getElementById("enviar-chat");

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

        const respuestaElemento = agregarMensajeChat(
            datos.answer || "No se recibió una respuesta.",
            "mensaje-asistente"
        );
        agregarFuentesChat(respuestaElemento, datos.sources);
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
