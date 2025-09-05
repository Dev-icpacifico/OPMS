from __future__ import annotations
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent_runner import run_agent

app = FastAPI(title="OPMS Agents API")

class ChatRequest(BaseModel):
    user_id: str
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    respuesta: str
    rows: Optional[List[Dict[str, Any]]] = None
    sql_query: Optional[str] = None
    sql_executed: Optional[str] = None
    exec_error: Optional[str] = None

@app.post("/chat/", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    if not payload.message or not payload.message.strip():
        raise HTTPException(status_code=400, detail="Mensaje vacío.")

    result = run_agent(payload.user_id, payload.message, payload.session_id)

    # último mensaje (respuesta natural del answer_agent o del retriever)
    last_msg = ""
    msgs = result.get("messages", [])
    if msgs:
        last = msgs[-1]
        # LangChain messages tienen .content; si viniera como dict, adaptamos:
        last_msg = getattr(last, "content", None) or (last.get("content") if isinstance(last, dict) else "")

    return ChatResponse(
        respuesta=last_msg,
        rows=result.get("rows"),
        sql_query=result.get("sql_query"),
        sql_executed=result.get("sql_executed"),
        exec_error=result.get("exec_error"),
    )
