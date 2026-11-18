import os
import sys
from pathlib import Path

import pytest

# Asegura que el módulo del servidor (en la raíz del proyecto) sea importable
# cuando pytest ejecuta los archivos dentro de la carpeta tests.
RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_PROYECTO))

import servidor


@pytest.fixture(autouse=True)
def limpiar_limites():
    with servidor._rate_limit_lock:
        servidor._solicitudes_por_ip.clear()
    yield
    with servidor._rate_limit_lock:
        servidor._solicitudes_por_ip.clear()


@pytest.fixture
def cliente(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    return servidor.app.test_client()


def test_pregunta_sin_destino_no_consulta_api(cliente):
    respuesta = cliente.post("/api/chat", json={"question": "¿Qué es el turismo?"})
    assert respuesta.status_code == 200
    assert "cinco destinos" in respuesta.get_json()["answer"]


def test_pregunta_fuera_de_tema_aunque_mencione_destino(cliente):
    respuesta = cliente.post(
        "/api/chat",
        json={"question": "Explícame cálculo diferencial en Cabo de la Vela"}
    )
    assert respuesta.status_code == 200
    assert "solo respondo preguntas" in respuesta.get_json()["answer"]


def test_pregunta_tematica_llega_a_comprobacion_de_api_key(cliente):
    respuesta = cliente.post(
        "/api/chat",
        json={"question": "Cuéntame la historia y cultura de Cabo de la Vela"}
    )
    assert respuesta.status_code == 503
    assert "API key" in respuesta.get_json()["error"]


@pytest.mark.parametrize("pregunta", ["", "   ", None, 123])
def test_pregunta_vacia_o_tipo_invalido(cliente, pregunta):
    respuesta = cliente.post("/api/chat", json={"question": pregunta})
    assert respuesta.status_code == 400


def test_pregunta_demasiado_larga(cliente):
    respuesta = cliente.post(
        "/api/chat",
        json={"question": "Cabo de la Vela " + ("x" * 1000)}
    )
    assert respuesta.status_code == 400


def test_limite_de_solicitudes_por_ip(cliente):
    pregunta = {"question": "Historia de Cabo de la Vela"}
    for _ in range(servidor.RATE_LIMIT_REQUESTS):
        respuesta = cliente.post("/api/chat", json=pregunta)
        assert respuesta.status_code == 503
    respuesta = cliente.post("/api/chat", json=pregunta)
    assert respuesta.status_code == 429


def test_url_web_valida():
    assert servidor.url_web_valida("https://example.com/pagina")
    assert servidor.url_web_valida("http://example.com")
    assert not servidor.url_web_valida("javascript:alert(1)")
    assert not servidor.url_web_valida("file:///etc/passwd")
    assert not servidor.url_web_valida("https:///sin-host")


def test_extraer_fuentes_descarta_protocolos_no_web():
    class RespuestaFalsa:
        def model_dump(self):
            return {
                "output": [
                    {
                        "type": "web_search_call",
                        "action": {
                            "sources": [
                                {"title": "Correcta", "url": "https://example.com"},
                                {"title": "No válida", "url": "javascript:alert(1)"}
                            ]
                        }
                    },
                    {
                        "type": "message",
                        "content": [
                            {
                                "annotations": [
                                    {"url_citation": {"title": "También correcta", "url": "http://example.org"}},
                                    {"url_citation": {"title": "No válida", "url": "data:text/html,abc"}}
                                ]
                            }
                        ]
                    }
                ]
            }

    fuentes = servidor.extraer_fuentes(RespuestaFalsa())
    assert [fuente["url"] for fuente in fuentes] == [
        "https://example.com", "http://example.org"
    ]
