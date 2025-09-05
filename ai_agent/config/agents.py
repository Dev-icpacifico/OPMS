from typing import Literal

# Define available LLM types
LLMType = Literal["basic", "reasoning"]

# Define agent-LLM mapping
AGENT_LLM_MAP: dict[str, LLMType] = {
    "sarams": "basic",
    "supervisor": "basic",
    "consultas": "reasoning",
    "sql_planner_agent": "reasoning",      # nuevo agente especializado en queries SQL
    "answer_agent": "reasoning",
}
