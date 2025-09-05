from langgraph.graph import START, END, StateGraph

from ai_agent.graph.nodes import (
    sarams,
    supervisor,
    retriever,
    sql_planner,
    sql_execute,
    answer,
)
from ai_agent.graph.schema import GlobalState
from ai_agent.persistence.checkpointer_sqlite import checkpointer

builder = StateGraph(GlobalState)

# --- Nodes ---

# --- Entry ---

builder.add_edge(START, "sara")
builder.add_node("sara", sarams)
builder.add_node("supervisor", supervisor)
builder.add_node("consultas", retriever)
builder.add_node("sql_planner", sql_planner)
builder.add_node("sql_execute", sql_execute)
builder.add_node("sql_answer", answer)

# --- Edges desde 'sql_planner' ---

builder.add_edge("sql_planner", "sql_execute")

# --- Edges desde 'sql_execute' ---

builder.add_edge("sql_execute", "sql_answer")

# --- Edges desde 'sql_answer' ---

builder.add_edge("sql_answer", "supervisor")
graph = builder.compile(checkpointer=checkpointer)

with open("assets/graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())
