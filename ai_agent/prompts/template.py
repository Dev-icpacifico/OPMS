import json
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

import json

def apply_prompt_template(prompt_name: str, state) -> list:
    print("[apply_prompt_template] llamado con:", prompt_name)
    print("[apply_prompt_template] keys:", list(state.keys()))
    template_str = get_prompt_template(prompt_name)
    pt = PromptTemplate.from_template(template_str)

    rows = state.get("rows", [])
    print("[apply_prompt_template] rows_len:", len(rows))

    # Contexto base (lo que ya tenías)
    ctx = {
        "CURRENT_TIME": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %z"),
        "human_query": state.get("human_query", ""),
        "schema_txt": state.get("schema_txt", ""),
        "dialect": state.get("dialect", "sqlite"),
        "default_limit": state.get("default_limit", 200),
        "allowed_prefixes": ", ".join(state.get("allowed_prefixes", [])),
    }

    # 🔑 Añade las variables que usa el prompt del ANSWER
    ctx.update({
        "HUMAN_QUERY": state.get("human_query") or state.get("original_query") or state.get("input", ""),
        "SQL_QUERY": state.get("sql_executed", state.get("sql_query", "")) or "",
        "SQL_ROWS_JSON": json.dumps(rows[:20], ensure_ascii=False),  # preview para no explotar tokens
    })

    # Compatibilidad si el .md tiene placeholders con \_ (p.ej. <<SQL\_ROWS\_JSON>>)
    for var in pt.input_variables:
        if var not in ctx:
            alt = var.replace("\\_", "_")
            if alt in ctx:
                ctx[var] = ctx[alt]

    # (debug útil)
    print("[APT] input_vars:", pt.input_variables)
    print("[APT] ctx tiene SQL_ROWS_JSON:", "SQL_ROWS_JSON" in ctx, " / SQL\\_ROWS\\_JSON:", "SQL\\_ROWS\\_JSON" in ctx)

    # Validación final
    missing = [v for v in pt.input_variables if v not in ctx]
    if missing:
        raise KeyError(f"Faltan variables para el prompt '{prompt_name}': {missing}")

    system_prompt = pt.format(**ctx)
    print("[APT] prompt contiene 'id_pago':", "id_pago" in system_prompt)

    return [SystemMessage(content=system_prompt), *state.get("messages", [])]
