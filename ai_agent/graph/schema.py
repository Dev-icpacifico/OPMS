from __future__ import annotations

from typing import TypedDict, Literal, List, Dict, Any, Annotated

try:
    # Python 3.11+
    from typing import NotRequired
except Exception:
    # Python <=3.10
    from typing_extensions import NotRequired  # pip install typing\_extensions

from langgraph.graph.message import add_messages


# Si prefieres usar objetos de LangChain:

# from langchain\_core.messages import BaseMessage

# Reducer: tomar siempre el último valor escrito en el mismo tick

def take_last(_old, new):
    return new


# total=False: las claves son opcionales (cada nodo aporta las suyas)

class GlobalState(TypedDict, total=False):
    # Conversación / control
    graph: str
    # Permite múltiples escrituras a 'messages' en el mismo paso (concatena)
    messages: Annotated[List[Dict[str, Any]], add_messages]
    # Alternativa con objetos de LangChain:
    # messages: Annotated[List[BaseMessage], add_messages]

    # Opcional: si insistes en persistir 'next', protégelo con take_last
    next: Annotated[str, take_last]

    task_completed: bool

    # ---- Entrada típica al planner ----
    human_query: str  # pregunta del usuario
    schema_txt: str  # esquema serializado (tablas/columnas/tipos)
    dialect: str  # "sqlite" | "mysql" | "postgresql" | "mssql"
    default_limit: int  # p.ej. 200
    allowed_prefixes: List[str]  # p.ej. ["vw_", "dim_", "fact_"]

    # ---- Salida del planner (Prompt 1) ----
    sql_query: Annotated[str, take_last]
    tables_used: NotRequired[List[str]]
    params: NotRequired[Dict[str, Any]]
    planning_reasoning: NotRequired[str]

    # ---- Resultado de validación y ejecución ----
    sql_executed: NotRequired[Annotated[str, take_last]]  # SQL final tras forzar LIMIT, etc.
    rows: NotRequired[List[Dict[str, Any]]]
    exec_error: NotRequired[Annotated[str, take_last]]  # mensaje si hubo error

    # ---- Señales para el answer (Prompt 2) ----
    chart_hint: NotRequired[Dict[str, Any]]  # {type, x, y, series, note}
    disclaimers: NotRequired[str]
    final_answer: NotRequired[str]


class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal[
        "retriever",  # retriever/doc QA
        "sql_planner",  # NL -> SQL (planner)
        "sql_execute",  # validación + ejecución DB
        "answer",  # redactar respuesta final
        "FINISH"
    ]
