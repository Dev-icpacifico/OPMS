from __future__ import annotations

import json
from typing import Literal, Dict, Any
from langchain_core.messages import HumanMessage

from ai_agent.utils.utils_sql import parse_planner_payload  # ajusta ruta real
# from ai_agent.graph.types import Command, END  # ajusta al import real
from langchain_core.messages import AIMessage
from langgraph.graph import END
from langgraph.types import Command

from ai_agent.agents.llm import get_llm_by_type
from ai_agent.agents.retriever_agent import retriever_agent
from ai_agent.agents.sql_agent import answer_agent
from ai_agent.config.agents import AGENT_LLM_MAP
from ai_agent.graph.schema import GlobalState, Router
from ai_agent.prompts.template import apply_prompt_template
from ai_agent.utils.sql_runner import run_query, get_schema_tables
from ai_agent.utils.utils_sql import parse_planner_payload


def _last_human_text(state) -> str:
    for m in reversed(state.get("messages", [])):
        if isinstance(m, HumanMessage):
            return (m.content or "").strip()
    return ""

def sarams(state: GlobalState) -> Command[Literal["supervisor", "__end__"]]:
    print("Este es el mensaje que recibe SaraMS:\n", state.get("messages"))

    # 1) Refrescar la pregunta del usuario para ESTE turno
    last_human = _last_human_text(state)
    local_state = dict(state)
    if last_human:
        local_state.update({
            "human_query": last_human,
            # limpiar efímeros del turno anterior (opcional pero recomendado)
            "exec_error": "",
            "rows": [],
            "sql_executed": "",
            # si quieres: "sql_query": "",
        })

    # 2) Prompt de Sara con el GlobalState ACTUALIZADO
    messages = apply_prompt_template("sarams", local_state)
    response = get_llm_by_type(AGENT_LLM_MAP["sarams"]).invoke(messages)

    # 3) Intentar interpretar JSON; si no, fallback a supervisor
    goto = "supervisor"  # por diseño, Sara -> Supervisor en el flujo normal
    try:
        data = json.loads(response.content)
        goto = data.get("next") or "supervisor"
        if goto == "FINISH":
            print("🟢 SaraMS FINALIZA EL FLUJO")
            return Command(
                goto=END,
                update={
                    # agrega la respuesta de Sara al historial
                    "messages": [AIMessage(content=data.get("response", ""))],
                    "task_completed": True,
                    # propaga el refresh de human_query/limpieza
                    "human_query": local_state.get("human_query", ""),
                    "exec_error": local_state.get("exec_error", ""),
                    "rows": local_state.get("rows", []),
                    "sql_executed": local_state.get("sql_executed", ""),
                },
            )
        print(f"🔁 SaraMS DERIVA A: {goto}")
    except Exception as e:
        print("❌ ERROR en JSON de SaraMS:", e)
        # si no hubo JSON, seguimos al supervisor igual
        goto = "supervisor"

    # 4) Ruta normal: derivar (típicamente al supervisor) manteniendo contexto
    return Command(
        goto=goto,
        update={
            # agrega SIEMPRE el mensaje de Sara al historial para contexto
            "messages": [AIMessage(content=getattr(response, "content", str(response)))],
            # propaga el refresh de human_query/limpieza efímera
            "human_query": local_state.get("human_query", ""),
            "exec_error": local_state.get("exec_error", ""),
            "rows": local_state.get("rows", []),
            "sql_executed": local_state.get("sql_executed", ""),
        },
    )
# def supervisor(state: GlobalState) -> Command[Literal["consultas", "sql_planner", "__end__"]]:

def _last_human_text(state) -> str:
    for m in reversed(state.get("messages", [])):
        if isinstance(m, HumanMessage):
            return m.content.strip()
    return ""

def supervisor(state: GlobalState) -> Command[Literal["consultas", "sql_planner", "__end__"]]:
    # 1) Refresca la pregunta del usuario para ESTE turno y limpia ruido del turno anterior
    last_human = _last_human_text(state)
    local_state = dict(state)  # no mutamos el original
    if last_human:
        local_state.update({
            "human_query": last_human,
            # limpiar efímeros para no “contaminar” el siguiente turno
            "exec_error": "",
            "rows": [],
            "sql_executed": "",
            # opcional:
            # "sql_query": "",
            # "final_answer": "",
        })

    # 2) Construye el prompt del supervisor con el GlobalState ACTUALIZADO
    messages = apply_prompt_template("supervisor", local_state)

    # 3) Decide la ruta
    llm = get_llm_by_type(AGENT_LLM_MAP["supervisor"])
    decision = llm.with_structured_output(Router).invoke(messages)
    goto = decision["next"]

    # 4) Heurística: si la pregunta menciona entidades/tablas del schema, fuerza sql_planner
    q = (local_state.get("human_query") or "").lower()
    schema_lc = (local_state.get("schema_txt") or "").lower()
    if goto != "sql_planner" and q and schema_lc:
        for hint in ["pagos", "condominio", "venta", "clientes"]:
            if hint in q and hint in schema_lc:
                goto = "sql_planner"
                break

    if goto == "FINISH":
        return Command(goto=END)

    # 5) Propaga al grafo el refresh de human_query y la limpieza efímera
    return Command(goto=goto, update={
        "human_query": local_state["human_query"],
        "exec_error": local_state["exec_error"],
        "rows": local_state["rows"],
        "sql_executed": local_state["sql_executed"],
        # opcional:
        # "sql_query": local_state.get("sql_query",""),
        # "final_answer": local_state.get("final_answer",""),
    })
def retriever(state: GlobalState) -> Command[Literal["supervisor", "__end__"]]:
    # retriever_agent debe devolver SOLO mensajes nuevos en result["messages"]
    result = retriever_agent.invoke(state)
    return Command(
        goto="supervisor",
        update={
            "messages": result["messages"],
        },
    )


def sql_planner(state: GlobalState) -> Command[Literal["sql_execute", "__end__"]]:
    """
    Invoca al planner (Prompt 1) usando el GlobalState del grafo, parsea el JSON devuelto
    y actualiza el estado con: sql_query, tables_used, params, planning_reasoning.
    Luego enruta a sql_execute (o termina si falla).
    """
    # 1) Renderiza el prompt con TU GlobalState (sí incluye human_query, schema_txt, etc.)
    messages = apply_prompt_template("sql_planner", state)

    # 2) Llama al LLM directamente con esos messages
    llm = get_llm_by_type(AGENT_LLM_MAP["sql_planner_agent"])
    ai_msg: AIMessage = llm.invoke(messages)

    # 3) Parseo robusto del contenido del planner
    data = parse_planner_payload(ai_msg.content)

    # 4) Construye el update
    update = {
        # Sólo añadimos el nuevo mensaje del planner; add_messages en el state hará el merge
        "messages": [ai_msg],
        "sql_query": (data.get("sql_query") or "").strip(),
        "tables_used": data.get("tables_used") or [],
        "params": data.get("params") or {},
        "planning_reasoning": data.get("reasoning"),
    }

    # 5) Control de error si no hay SQL
    if not update["sql_query"]:
        update["exec_error"] = "El planner no devolvió 'sql_query'."
        return Command(goto=END, update=update)

    # 6) Enrutar a la ejecución SQL
    return Command(goto="sql_execute", update=update)

def sql_execute(state: GlobalState) -> Command[Literal["sql_answer", "__end__"]]:
    """
    Valida el SQL del planner, inyecta LIMIT, ejecuta y actualiza:
    rows / sql_executed / exec_error
    Luego enruta a sql_answer.
    """
    print("INGRESÓ AL SQL EXECUTE")
    sql_query: str = state.get("sql_query", "") or ""
    print("ESTA ES LA QUERY 1 ----> ", sql_query)
    params: Dict[str, Any] = state.get("params", {}) or {}
    allowed_prefixes = state.get("allowed_prefixes", ["vw_", "dim_", "fact_"])
    default_limit = int(state.get("default_limit", 200))
    dialect = (state.get("dialect") or "sqlite").lower()
    print("ESTA ES LA QUERY 2 ----> ", sql_query)

    if not sql_query:
        update = {
            "exec_error": "No se recibió 'sql_query' desde el planner.",
            "rows": [],
        }
        return Command(goto="sql_answer", update=update)

    schema_tables = get_schema_tables()

    """try:
        safe_sql = validate_and_rewrite_sql(
            sql_query,
            schema_tables=schema_tables,
            allowed_prefixes=allowed_prefixes,
            default_limit=default_limit,
            dialect=dialect,
        )
    except Exception as e:
        update = {
            "exec_error": f"SQL rechazado por validación: {e}",
            "rows": [],
            "sql_executed": "",
        }
        return Command(goto="sql_answer", update=update)"""
    print("ESTA ES LA QUERY 3 ----> ", sql_query)
    try:
        rows = run_query(sql_query, params=params)
    except Exception as e:
        update = {
            "exec_error": f"Error al ejecutar SQL: {e}",
            "rows": [],
            "sql_executed": sql_query,
        }
        return Command(goto="sql_answer", update=update)

    update = {
        "exec_error": "",
        "rows": rows,
        "sql_executed": sql_query,
    }
    print("ESTE ES EL UPDATE FINAL------------->", update)
    return Command(goto="sql_answer", update=update)


def answer(state: GlobalState) -> Command[Literal["__end__"]]:
    """
    Redacta la respuesta final (Prompt 2) usando el GlobalState del grafo.
    """
    print("INGRESÓ AL SQL ANSWER")
    print("DBG rows_len:", len(state.get("rows", [])))

    # 1) Renderiza el prompt del answer con TU GlobalState (incluye filas/preview)
    messages = apply_prompt_template("sql_answer", state)

    # (debug opcional) verifica que el prompt renderizado trae tus filas
    try:
        rendered = messages[0].content if hasattr(messages[0], "content") else str(messages[0])
        print("DBG prompt contiene 'id_pago':", "id_pago" in rendered)
    except Exception:
        pass

    # 2) Invoca al LLM directamente con esos messages
    llm = get_llm_by_type(AGENT_LLM_MAP["answer_agent"])
    ai = llm.invoke(messages)

    # 3) Normaliza salida a AIMessage
    ai_msg = ai if isinstance(ai, AIMessage) else AIMessage(content=str(ai))

    # 4) Actualiza estado y termina
    return Command(
        goto=END,
        update={
            "messages": [ai_msg],                 # add_messages hará el merge con historial
            "final_answer": ai_msg.content,       # opcional: útil para API
        },
    )
