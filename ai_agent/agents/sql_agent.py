from langgraph.prebuilt import create_react_agent

from ai_agent.config.agents import AGENT_LLM_MAP
from ai_agent.prompts.template import apply_prompt_template
from .llm import get_llm_by_type

sql_planner_agent = create_react_agent(
    get_llm_by_type(AGENT_LLM_MAP["sql_planner_agent"]),
    tools=[],
    # Prompt específico para SQL: incluye reglas (solo SELECT, LIMIT, allowlist, etc.)
    prompt=lambda state: apply_prompt_template("sql_planner", state),
)

answer_agent = create_react_agent(
    get_llm_by_type(AGENT_LLM_MAP["answer_agent"]),
    tools=[],
    # Prompt específico para SQL: incluye reglas (solo SELECT, LIMIT, allowlist, etc.)
    prompt=lambda state: apply_prompt_template("sql_answer", state),
)