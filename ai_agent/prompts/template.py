import re
from pathlib import Path
from datetime import datetime, timezone
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage  # mejor que dicts role/content


def get_prompt_template(prompt_name: str) -> str:
    path = Path(__file__).with_name(f"{prompt_name}_prompt.md")
    try:
        template = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        template = path.read_text(encoding="latin-1")

    # 1) Escapa llaves literales
    template = template.replace("{", "{{").replace("}", "}}")
    # 2) Convierte <<VAR>> en {VAR} (placeholders reales)
    template = re.sub(r"<<([^>>]+)>>", r"{\1}", template)
    return template

def apply_prompt_template(prompt_name: str, state) -> list:
    template_str = get_prompt_template(prompt_name)
    pt = PromptTemplate.from_template(template_str)  # autodetecta variables

    # Contexto para el template (defaults seguros)
    ctx = {
        "CURRENT_TIME": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %z"),
        "human_query": state.get("human_query", ""),
        "schema_txt": state.get("schema_txt", ""),
        "dialect": state.get("dialect", "sqlite"),
        "default_limit": state.get("default_limit", 200),
        # según cómo lo espere tu prompt:
        "allowed_prefixes": ", ".join(state.get("allowed_prefixes", [])),
    }

    # Valida que no falte nada
    missing = [v for v in pt.input_variables if v not in ctx]
    if missing:
        # Si tu template tiene más variables, súmalas al ctx arriba
        raise KeyError(f"Faltan variables para el prompt '{prompt_name}': {missing}")

    system_prompt = pt.format(**ctx)

    # Devuelve LangChain Messages (no dicts estilo OpenAI)
    return [SystemMessage(content=system_prompt), *state["messages"]]
