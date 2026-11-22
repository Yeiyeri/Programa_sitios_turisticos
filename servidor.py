import os
import re
import threading
import time
import unicodedata
from collections import defaultdict, deque
from urllib.parse import urlparse
import json

from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "Web")
IMAGE_DIR = os.path.join(BASE_DIR, "Imagenes")
DATOS_DIR = os.path.join(BASE_DIR, "datos")
DESTINOS_FILE = os.path.join(DATOS_DIR, "destinos.json")

app = Flask(__name__, static_folder=WEB_DIR, static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")

def cargar_destinos():
    """Carga los destinos turísticos desde el archivo JSON."""
    try:
        with open(DESTINOS_FILE, "r", encoding="utf-8") as archivo:
            destinos = json.load(archivo)

        if not isinstance(destinos, list):
            raise ValueError("El JSON debe contener una lista de destinos.")

        for destino in destinos:
            campos_obligatorios = (
                "nombre", "tipo", "ubicacion", "descripcion",
                "latitud", "longitud", "imagen", "alias"
            )

            if not all(campo in destino for campo in campos_obligatorios):
                raise ValueError(
                    f"Faltan campos obligatorios en un destino: {destino}"
                )

        return destinos

    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(
            f"No se pudieron cargar los destinos: {error}"
        ) from error


DESTINOS_DATOS = cargar_destinos()

DESTINOS = {
    destino["nombre"]: destino["alias"]
    for destino in DESTINOS_DATOS
}

# Términos que indican una consulta turística, geográfica, histórica,
# cultural, ambiental o económica sobre los destinos registrados.
TEMAS_PERMITIDOS = (
    "historia", "historico", "cultura", "cultural", "wayuu", "indigena",
    "tradicion", "tradiciones", "fauna", "flora", "animal", "animales",
    "ave", "aves", "flamenco", "ecosistema", "biodiversidad", "naturaleza",
    "ambiente", "ambiental", "conservacion", "economia", "economico",
    "importancia", "turismo", "turistico", "turistica", "visitar", "visita",
    "viajar", "viaje", "actividad", "actividades", "atractivo", "atractivos",
    "paisaje", "playa", "playas", "mar", "desierto", "sal", "salina",
    "ubicacion", "donde queda", "como llegar", "hospedaje", "alojamiento",
    "gastronomia", "comida", "clima", "geografia", "geografico",
    "comparar", "comparacion", "diferencia", "diferencias", "recomendacion",
    "recomendar", "que es", "quien", "cuando", "cuentame", "hablame",
    "informacion", "informar", "conocer", "explorar", "recorrido", "ruta",
    "seguridad para turistas", "horario", "entrada", "precio", "costo",
)

# Límite sencillo por dirección IP: 12 solicitudes por minuto.
# Para despliegues con varios procesos/servidores debe sustituirse por un
# limitador compartido (por ejemplo Redis); este contador vive en memoria.
RATE_LIMIT_REQUESTS = 12
RATE_LIMIT_WINDOW_SECONDS = 60
_solicitudes_por_ip = defaultdict(deque)
_rate_limit_lock = threading.Lock()


def normalizar(texto):
    """Convierte a minúsculas y elimina tildes."""
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(
        caracter for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )


def detectar_destinos(pregunta):
    texto = normalizar(pregunta)
    encontrados = []
    for destino, alias in DESTINOS.items():
        for nombre in alias:
            patron = r"(?<![a-z0-9])" + re.escape(normalizar(nombre)) + r"(?![a-z0-9])"
            if re.search(patron, texto):
                encontrados.append(destino)
                break
    return encontrados


def pregunta_dentro_del_tema(pregunta):
    """Evita enviar al modelo preguntas ajenas aunque mencionen un destino.

    Se usan límites de palabra para no aceptar coincidencias accidentales,
    como 'diferencia' dentro de 'diferencial'.
    """
    texto = normalizar(pregunta)
    return any(
        re.search(
            r"(?<![a-z0-9])" + re.escape(termino) + r"(?![a-z0-9])",
            texto
        )
        for termino in TEMAS_PERMITIDOS
    )


def solicita_fuentes(pregunta):
    texto = normalizar(pregunta)
    expresiones = (
        "fuente", "fuentes", "referencia", "referencias",
        "enlace", "enlaces", "link", "links",
        "de donde sacaste", "de donde obtuviste",
        "pagina consultada", "paginas consultadas"
    )
    return any(expresion in texto for expresion in expresiones)


def url_web_valida(url):
    """Acepta únicamente enlaces web HTTP o HTTPS con host."""
    if not isinstance(url, str):
        return False
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except ValueError:
        return False


def extraer_fuentes(respuesta):
    """Obtiene fuentes web y valida las URL antes de devolverlas."""
    datos = respuesta.model_dump()
    fuentes = []
    vistas = set()

    for elemento in datos.get("output", []):
        if elemento.get("type") == "web_search_call":
            for fuente in elemento.get("action", {}).get("sources", []):
                url = fuente.get("url")
                titulo = fuente.get("title") or url
                if url_web_valida(url) and url not in vistas:
                    vistas.add(url)
                    fuentes.append({"title": str(titulo), "url": url})

        if elemento.get("type") == "message":
            for contenido in elemento.get("content", []):
                for anotacion in contenido.get("annotations", []):
                    cita = anotacion.get("url_citation", anotacion)
                    url = cita.get("url")
                    titulo = cita.get("title") or url
                    if url_web_valida(url) and url not in vistas:
                        vistas.add(url)
                        fuentes.append({"title": str(titulo), "url": url})

    return fuentes


def excede_limite(ip, ahora=None):
    """Devuelve True si la IP superó la cuota de solicitudes por ventana."""
    ahora = time.monotonic() if ahora is None else ahora
    with _rate_limit_lock:
        solicitudes = _solicitudes_por_ip[ip]
        while solicitudes and ahora - solicitudes[0] >= RATE_LIMIT_WINDOW_SECONDS:
            solicitudes.popleft()
        if len(solicitudes) >= RATE_LIMIT_REQUESTS:
            return True
        solicitudes.append(ahora)
        return False


@app.get("/")
def inicio():
    return send_from_directory(WEB_DIR, "index.html")

@app.get("/api/destinos")
def obtener_destinos():
    """Devuelve los destinos turísticos registrados."""
    return jsonify(DESTINOS_DATOS)

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

    ip = request.remote_addr or "desconocida"
    if excede_limite(ip):
        return jsonify({
            "error": "Has enviado demasiadas preguntas. Espera un minuto antes de intentarlo de nuevo."
        }), 429

    destinos = detectar_destinos(pregunta)
    if not destinos or not pregunta_dentro_del_tema(pregunta):
        return jsonify({
            "answer": (
                "Soy el asistente turístico de ExploraGuajira y solo respondo "
                "preguntas sobre la historia, cultura, fauna, flora, geografía, "
                "importancia y actividades turísticas de estos cinco destinos: "
                "Cabo de la Vela, Punta Gallinas, el Santuario Los Flamencos, "
                "las Salinas de Manaure y el Centro Histórico de Cartagena. "
                "Formula una pregunta dentro de ese tema e incluye el destino."
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
    nombres_destinos = "\n".join(
    f"- {destino['nombre']}" for destino in DESTINOS_DATOS
)

    instrucciones = f"""
    Eres el asistente turístico de ExploraGuajira.
    Tu único ámbito permitido son estos destinos registrados:

    {nombres_destinos}

    La pregunta ha sido identificada como relacionada con: {destinos_texto}.
    Responde únicamente sobre esos destinos. Puedes hablar de su historia, fauna,
    flora, cultura, importancia ambiental, social o económica, geografía y
    actividades turísticas, y compararlos entre sí.

    La validación del servidor no sustituye tu criterio: si la pregunta no trata
    directamente sobre esos destinos o sus temas turísticos, recházala brevemente.
    Busca información en la web antes de responder. Prioriza fuentes oficiales,
    instituciones públicas, entidades de conservación, universidades y organismos
    culturales. No inventes datos. Si no encuentras respaldo suficiente, dilo
    claramente y evita presentar suposiciones como hechos.

    Responde en español, con lenguaje claro y una extensión moderada.
    {"Si el visitante solicita fuentes, indica que las fuentes consultadas se mostrarán mediante enlaces." if mostrar_fuentes else "El visitante NO ha solicitado fuentes. No incluyas enlaces, citas visibles ni una sección de referencias."}
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
        fuentes = extraer_fuentes(respuesta)
        return jsonify({"answer": respuesta.output_text, "sources": fuentes})
    except Exception:
        app.logger.exception("Error al consultar OpenAI")
        return jsonify({
            "error": (
                "No fue posible consultar el asistente en este momento. "
                "Inténtalo nuevamente más tarde."
            )
        }), 502


if __name__ == "__main__":
    app.run(debug=False)
