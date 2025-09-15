import json
import time
import uuid
from typing import Dict, Any, Iterable

import requests
from django.contrib.auth.decorators import login_required
from django.http import (
    JsonResponse,
    StreamingHttpResponse,
    HttpResponseBadRequest,
)
from django.shortcuts import render

from .settings_chat import AGENTS_CHAT_ENDPOINT, AGENTS_EXTRA_HEADERS

# Buffer temporal de “turnos” (token → message del usuario)
_LAST_USER_TEXT: Dict[str, str] = {}

def sse_pack(event: str, data: Dict[str, Any]) -> str:
    return f"event: {event}\n" + "data: " + json.dumps(data, ensure_ascii=False) + "\n\n"

@login_required
def chat_page(request):
    """
    /chat/ — vista principal. Un hilo “lógico” por session_id (usamos la sesión Django).
    """
    # Usamos la sesión de Django como session_id para tu API
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key
    return render(request, "chat/chat.html", {
        "history_url": "/chat/history",
        "post_url": "/chat/messages",
        "session_id": session_id,
    })

@login_required
def get_history(request):
    """
    MVP: no pedimos historial al backend (si más adelante expones history, lo conectamos aquí).
    """
    return JsonResponse({"messages": [], "next_cursor": None})

@login_required
def post_message(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")
    try:
        body = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("JSON inválido")

    text = (body.get("message") or "").strip()
    if not text:
        return HttpResponseBadRequest("Falta 'message'")

    # Generamos un token de stream y guardamos el texto temporalmente
    stream_token = str(uuid.uuid4())
    _LAST_USER_TEXT[stream_token] = text

    return JsonResponse({
        "status": "accepted",
        "stream_url": f"/chat/stream?token={stream_token}"
    })

@login_required
def stream_response(request):
    """
    Abre SSE al navegador.
    - Llama a TU API con: { user_id, message, session_id }
    - Recibe ChatResponse (JSON final)
    - Emite meta → token* (simulado) → final
    """
    token = request.GET.get("token")
    if not token or token not in _LAST_USER_TEXT:
        return HttpResponseBadRequest("Token inválido o expirado")

    user_text = _LAST_USER_TEXT.pop(token)
    # Usamos el id del usuario Django como user_id; si prefieres otro, ajusta aquí:
    user_id = str(request.user.id)
    session_id = request.session.session_key  # el mismo que enviamos desde la página

    def event_stream():
        yield sse_pack("meta", {
            "started_at": int(time.time() * 1000),
            "model": "agents-api",
        })

        # Llamada a TU API
        try:
            resp = requests.post(
                AGENTS_CHAT_ENDPOINT,
                headers={"Content-Type": "application/json", **AGENTS_EXTRA_HEADERS},
                json={
                    "user_id": user_id,
                    "message": user_text,
                    "session_id": session_id,  # tu API permite null; aquí enviamos la sesión de Django
                },
                timeout=300,
            )
            resp.raise_for_status()
        except requests.HTTPError as he:
            yield sse_pack("error", {"code": "HTTP_ERROR", "message": str(he)})
            return
        except Exception as ex:
            yield sse_pack("error", {"code": "EXCEPTION", "message": str(ex)})
            return

        # Parseamos ChatResponse
        try:
            data = resp.json()
        except Exception:
            yield sse_pack("error", {"code": "BAD_JSON", "message": "Respuesta no es JSON"})
            return

        respuesta = (data.get("respuesta") or "").strip()
        exec_error = data.get("exec_error")
        sql_query = data.get("sql_query")
        sql_executed = data.get("sql_executed")
        rows = data.get("rows")

        # SSE simulado: “streameamos” la respuesta palabra por palabra
        acc = []
        for tok in respuesta.split():
            acc.append(tok)
            yield sse_pack("token", {"delta": tok + " "})
            time.sleep(0.01)  # animación suave; ajusta si quieres

        # Adjuntamos metadatos útiles al final (si existen)
        final_payload: Dict[str, Any] = {
            "content": " ".join(acc).strip(),
            "usage": {},
            "ended_at": int(time.time() * 1000),
            "meta": {
                "exec_error": exec_error,
                "sql_query": sql_query,
                "sql_executed": sql_executed,
            }
        }
        # Si quieres mostrar una vista rápida de 'rows' en el cliente, puedes mandarlas aquí.
        # Por ahora, solo indicamos cuántas filas vinieron.
        if isinstance(rows, list):
            final_payload["meta"]["rows_count"] = len(rows)

        yield sse_pack("final", final_payload)

    resp = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    resp["Cache-Control"] = "no-cache"
    resp["X-Accel-Buffering"] = "no"
    return resp
