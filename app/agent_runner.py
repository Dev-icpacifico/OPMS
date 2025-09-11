from __future__ import annotations
import os
import sqlite3
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

from langchain_core.messages import HumanMessage
from ai_agent.graph.builder import graph
from ai_agent.config.env import DB_PATH_CHECKPOINTER  # ya lo usas en tu checkpointer

SCHEMA_PATH = Path(r"C:\Users\Luis Pizarro\PycharmProjects\OPMS\utils_project\schema_ddbb")
schema_text = SCHEMA_PATH.read_text(encoding="utf-8")

# --------- util: esquema (SQLite de Django/OPMS) ---------

# --------- parámetros por defecto del planner/ejecutor ---------
DEFAULT_LIMIT = int(os.getenv("SQL_DEFAULT_LIMIT", "200"))
ALLOWED_PREFIXES = os.getenv("SQL_ALLOWED_PREFIXES", "vw_,dim_,fact_").split(",")
DIALECT = os.getenv("SQL_DIALECT", "sqlite")  # tu flujo actual usa SQLite


def run_agent(user_id: str, mensaje: str, session_id: str | None = None) -> Dict[str, Any]:
    """
    Ejecuta el grafo con estado inicial consistente con el flujo:
    sara -> supervisor -> (consultas | sql_planner -> sql_execute -> sql_answer)
    Devuelve el estado final completo para que la API pueda elegir qué campos exponer.
    """
    thread_id = session_id or user_id
    config = {"configurable": {"thread_id": thread_id, "user_id": user_id}}

    state: Dict[str, Any] = {
        # conversación
        "messages": [HumanMessage(content=mensaje)],
        "graph": "default",
        "next": "",
        "task_completed": False,
        # entrada para planner SQL
        "human_query": mensaje,
        "schema_txt": schema_text,
        "dialect": DIALECT,
        "default_limit": DEFAULT_LIMIT,
        "allowed_prefixes": ALLOWED_PREFIXES,
    }

    result = graph.invoke(state, config=config)
    return result
