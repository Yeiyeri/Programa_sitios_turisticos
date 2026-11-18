import os
import re

from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "Web")
IMAGE_DIR = os.path.join(BASE_DIR, "Imagenes")

app = Flask(__name__, static_folder=WEB_DIR, static_url_path="")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")

# Nombres y alias admitidos. La pregunta debe mencionar al menos uno.
DESTINOS = {
    "Cabo de la Vela": [
        "cabo de la vela", "el cabo de la vela"
    ],
    "Punta Gallinas": [
        "punta gallinas", "punta gallina"
    ],
    "Santuario de Fauna y Flora Los Flamencos": [
        "santuario de fauna y flora los flamencos",
        "santuario los flamencos", "los flamencos", "flamencos"
    ],
    "Salinas de Manaure": [
        "salinas de manaure", "salina de manaure", "manaure"
    ],
    "Centro Histórico de Cartagena": [
        "centro historico de cartagena", "centro histórico de cartagena",
        "centro de cartagena", "cartagena"
    ],
}


def normalizar(texto):
    """Pasa el texto a minúsculas y elimina tildes para comparar alias."""
    import unicodedata

    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(
        caracter for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )


def detectar_destinos(pregunta):
    texto = normalizar(pregunta)
    encontrados = []

    for destino, alias in DESTINOS.items():
        if any(normalizar(nombre) in texto for nombre in alias):
            encontrados.append(destino)

    return encontrados


def solicita_fuentes(pregunta):
    texto = normalizar(pregunta)
    expresiones = (
        "fuente", "fuentes", "referencia", "referencias",
        "enlace", "enlaces", "link", "links",
        "de donde sacaste", "de donde obtuviste",
        "pagina consultada", "paginas consultadas"
    )
    return any(expresion in texto for expresion in expresiones)


def extraer_fuentes(respuesta):
    """Obtiene las citas web incluidas en las anotaciones de Responses API."""
    datos = respuesta.model_dump()
    fuentes = []
    vistas = set()

    for elemento in datos.get("output", []):
        # Lista completa de páginas recuperadas por la herramienta web.
        if elemento.get("type") == "web_search_call":
            for fuente in elemento.get("action", {}).get("sources", []):
                url = fuente.get("url")
                titulo = fuente.get("title") or url
                if url and url not in vistas:
                    vistas.add(url)
                    fuentes.append({"title": titulo, "url": url})

        # También recoge las citas que el modelo incluyó en su respuesta.
        if elemento.get("type") == "message":
            for contenido in elemento.get("content", []):
                for anotacion in contenido.get("annotations", []):
                    cita = anotacion.get("url_citation", anotacion)
                    url = cita.get("url")
                    titulo = cita.get("title") or url
                    if url and url not in vistas:
                        vistas.add(url)
                        fuentes.append({"title": titulo, "url": url})

    return fuentes


@app.get("/")
def inicio():
    return send_from_directory(WEB_DIR, "index.html")


@app.get("/Imagenes/<path:nombre>")
def imagenes(nombre):
    return send_from_directory(IMAGE_DIR, nombre)


@app.post("/api/chat")
def chat():
    datos = request.get_json(silent=True) or {}
    pregunta = datos.get("question", "")

    if not isinstance(pregunta, str) or not pregunta.strip():
        return jsonify({"error": "Escribe una pregunta para continuar."}), 400

    pregunta = pregunta.strip()

    if len(pregunta) > 1000:
        return jsonify({"error": "La pregunta es demasiado larga. Usa máximo 1000 caracteres."}), 400

    destinos = detectar_destinos(pregunta)

    if not destinos:
        return jsonify({
            "answer": (
                "Puedo ayudarte con información sobre los cinco destinos de "
                "ExploraGuajira: Cabo de la Vela, Punta Gallinas, el Santuario "
                "Los Flamencos, las Salinas de Manaure y el Centro Histórico "
                "de Cartagena. Incluye el nombre de uno de ellos en tu pregunta."
            ),
            "sources": []
        })

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify({
            "error": (
                "El chat ya está preparado, pero todavía falta configurar "
                "la API key de OpenAI. Por ahora no se pueden generar respuestas."
            )
        }), 503

    mostrar_fuentes = solicita_fuentes(pregunta)
    destinos_texto = ", ".join(destinos)

    instrucciones = f"""
Eres el asistente turístico de ExploraGuajira.
Tu único ámbito permitido son estos cinco destinos registrados:
- Cabo de la Vela
- Punta Gallinas
- Santuario de Fauna y Flora Los Flamencos
- Salinas de Manaure
- Centro Histórico de Cartagena

La pregunta ha sido identificada como relacionada con: {destinos_texto}.

Responde únicamente sobre esos destinos. Puedes hablar de su historia,
fauna, flora, cultura, importancia ambiental, social o económica, y actividades
turísticas, siempre que la información esté respaldada por fuentes fiables.
Puedes comparar los destinos registrados entre sí.

No respondas preguntas generales que no traten directamente sobre esos lugares.
Si la pregunta se desvía del tema, explica brevemente el alcance del asistente.
Busca información en la web antes de responder. Prioriza fuentes oficiales,
instituciones públicas, entidades de conservación, universidades y organismos
culturales. No inventes datos. Si no encuentras respaldo suficiente, dilo
claramente y evita presentar suposiciones como hechos.

Responde en español, con lenguaje claro y una extensión moderada.
{"Si el visitante solicita fuentes, menciona que las fuentes consultadas se mostrarán mediante enlaces. Si no las solicita, no agregues una sección de fuentes ni enlaces en el texto." if mostrar_fuentes else "El visitante NO ha solicitado fuentes. No incluyas enlaces, citas visibles ni una sección de referencias en la respuesta."}
"""

    try:
        cliente = OpenAI(api_key=api_key)
        respuesta = cliente.responses.create(
            model=OPENAI_MODEL,
            instructions=instrucciones,
            tools=[{"type": "web_search"}],
            tool_choice="required",
            include=["web_search_call.action.sources"],
            input=pregunta
        )

        # Se envían al navegador para permitir una pregunta posterior como
        # "¿Cuáles son las fuentes?". La interfaz solo las muestra si se piden.
        fuentes = extraer_fuentes(respuesta)

        return jsonify({
            "answer": respuesta.output_text,
            "sources": fuentes
        })

    except Exception:
        app.logger.exception("Error al consultar OpenAI")
        return jsonify({
            "error": (
                "No fue posible consultar el asistente en este momento. "
                "Inténtalo nuevamente más tarde."
            )
        }), 502


if __name__ == "__main__":
    app.run(debug=True)
