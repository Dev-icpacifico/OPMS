from __future__ import annotations

import json
from typing import Literal, Dict, Any

from cffi.cffi_opcode import PRIM_INT
from langchain_core.messages import AIMessage
from langgraph.graph import END
from langgraph.types import Command

from ai_agent.agents.sql_agent import sql_planner_agent, answer_agent
from ai_agent.agents.retriever_agent import retriever_agent
from ai_agent.agents.llm import get_llm_by_type
from ai_agent.config.agents import AGENT_LLM_MAP
from ai_agent.graph.schema import GlobalState, Router
from ai_agent.prompts.template import apply_prompt_template

from ai_agent.utils.sql_runner import run_query, get_schema_tables
from ai_agent.utils.sql_validator import validate_and_rewrite_sql
from ai_agent.utils.utils_sql import parse_planner_payload


def sarams(state: GlobalState) -> Command[Literal["supervisor", "__end__"]]:
    print("Este es el mensaje que recibe SaraMS: \n")
    print(state["messages"])
    messages = apply_prompt_template("sarams", state)
    response = get_llm_by_type(AGENT_LLM_MAP["sarams"]).invoke(messages)
    try:
        data = json.loads(response.content)
        goto = data["next"]
        if goto == "FINISH":
            print("🟢 SaraMS FINALIZA EL FLUJO")
            # Solo mensajes nuevos
            return Command(
                goto=END,
                update={
                    "messages": [AIMessage(content=data.get("response", ""))],
                    "task_completed": True,
                },
            )
        print(f"🔁 SaraMS DERIVA A: {goto}")
        # No escribir 'next' en el estado
        return Command(goto=goto)
    except Exception as e:
        print("❌ ERROR en JSON de SaraMS:", e)
        return Command(
            goto=END,
            update={
                "messages": [AIMessage(content="Disculpa, no pude procesar tu solicitud.")],
                "task_completed": True,
            },
        )


def supervisor(state: GlobalState) -> Command[Literal["consultas", "sql_planner", "__end__"]]:
    print("Mensaje recibido por el supervisor: \n", state.get("messages"))
    # Si ya está completado, termina.
    if state.get("task_completed") is True:
        return Command(goto=END)
    print("PASÓ EL IF ")
    messages = apply_prompt_template("supervisor", state)
    print("ESTE ES EL MENSAJE:--->: ", messages)
    try:
        print("Entra ak try")
        llm = get_llm_by_type(AGENT_LLM_MAP["supervisor"])
        print("Obtiene el LLM")
        decision = llm.with_structured_output(Router).invoke(messages)
        goto = decision["next"]
        print("Supervisor dirige a:", goto)
        if goto == "FINISH":
            return Command(goto=END)
        # Solo enruta; no escribir 'next'
        return Command(goto=goto)
    except Exception as e:
        print("Error en la decisión del supervisor:", e)
        return Command(
            goto=END,
            update={
                "messages": [AIMessage(content="No pude decidir a quién derivar tu solicitud.")],
                "task_completed": True,
            },
        )

def retriever(state: GlobalState) -> Command[Literal["supervisor", "__end__"]]:
    # retriever_agent debe devolver SOLO mensajes nuevos en result["messages"]
    result = retriever_agent.invoke(state)
    return Command(
        goto="supervisor",
        update={
            "messages": result["messages"],
        },
    )


def sql_planner(state: GlobalState) -> Command[Literal["sql_execute"]]:
    print("Mensaje recibido por el planner: \n", state.get("messages"))
    """
    Invoca al planner (Prompt 1) y PARSEA el JSON devuelto para poblar el estado:
    - sql_query
    - tables_used
    - params
    - planning_reasoning
    Luego enruta a sql_execute (o a sql_answer si falla).
    """
    print("ESTE ES EL STATE----->: ", state)
    print("ESTE ES EL PLANNER AGENT---> ", sql_planner_agent)
    result = sql_planner_agent.invoke(state)
    print("ESTE ES EL RESULT:--->: ", result)

    try:
        last_ai = None
        # Busca el último AIMessage del planner
        print("Entra al try")
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage):
                print("SI HAY MSG AIMESSAGES")
                last_ai = msg
                print("ESTE ES EL LAST AI --->", last_ai)
                break
        print("----------CONTINUACIÓN DEL FOR ------")
        if last_ai is None:
            raise ValueError("No se encontró AIMessage del planner.")


        print("ESTE ES EL JSON---->", parse_planner_payload(last_ai.content))
        data = parse_planner_payload(last_ai.content)
        print("ESTA ES LA DATA----->", data)

        next_step = "sql_execute"


        update = {
            # SOLO lo que vino nuevo del agent
            "messages": result["messages"],
            "sql_query": data.get("sql_query", "").strip(),
            "tables_used": data.get("tables_used", []) or [],
            "params": data.get("params", {}) or {},
            "planning_reasoning": data.get("reasoning", None),
        }
        print("ESTE ES EL UPDATE------>", update)

        if not update["sql_query"]:
            # Falla temprana: no hay SQL.
            update["exec_error"] = "El planner no devolvió 'sql_query'."
            next_step = END

        return Command(goto=next_step, update=update)

    except Exception as e:
        # No se pudo parsear JSON del planner
        return Command(
            goto=END,
            update={
                "messages": [AIMessage(content=f"No pude interpretar el plan SQL: {e}")],
                # "exec_error": f"No pude interpretar el plan SQL: {e}",
                "sql_query": "",
                "params": {},
                "tables_used": [],
            },
        )


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
    Redacta la respuesta final (Prompt 2)
    """
    print("INGRESÓ AL SQL ANSWER")
    print("ESTE ES EL STATE----->", state)

    result = answer_agent.invoke(state)

    #payload = build_ctx_from_state(state)  # arma HUMAN_QUERY, SQL_QUERY, SQL_ROWS_JSON
    #result = answer_agent.invoke(payload)  # el prompt template rellenará variables

    print("ESTE ES EL RESULT------> ", result)
    # Devolvemos solo los nuevos mensajes del agent
    return Command(goto=END, update={"messages": result["messages"]})
    # Si quieres terminar aquí:
    # return Command(goto=END, update={"messages": result["messages"], "task_completed": True})
