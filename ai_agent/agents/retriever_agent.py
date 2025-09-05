from ai_agent.agents.llm import *
from langgraph.prebuilt import create_react_agent
from ai_agent.tools.retriever_tool import retriever_tool
from .llm import get_llm_by_type
from ai_agent.config.agents import AGENT_LLM_MAP
from ai_agent.prompts.template import apply_prompt_template


retriever_agent = create_react_agent(
    get_llm_by_type(AGENT_LLM_MAP["consultas"]),
    tools=[retriever_tool],
    # prompt=prompt_retriever
    prompt = lambda state:apply_prompt_template("consultas", state),
)