# apps/agents/utils_sql.py
import json, re
from typing import Any, Dict

_JSON_BLOCK = re.compile(r"```json\s*(\{[\s\S]*?\})\s*```", re.I)
_FIRST_OBJECT = re.compile(r"(\{[\s\S]*\})")

_DEF_SCHEMA = {
    "sql_query": "",
    "tables_used": [],
    "params": {},
    "reasoning": None,
}

def parse_planner_payload(text: str) -> Dict[str, Any]:
    t = (text or "").strip()
    # 1) bloque ```json
    m = _JSON_BLOCK.search(t)
    if m:
        t = m.group(1)
    else:
        # 2) primer objeto entre llaves
        m2 = _FIRST_OBJECT.search(t)
        if m2:
            t = m2.group(1)
    # 3) intento JSON
    try:
        data = json.loads(t)
    except Exception:
        # fallback: comillas simples -> comillas dobles
        t2 = re.sub(r"'", '"', t)
        try:
            data = json.loads(t2)
        except Exception:
            return _DEF_SCHEMA.copy()
    # Normalización
    out = _DEF_SCHEMA.copy()
    out.update({
        "sql_query": (data.get("sql_query") or "").strip(),
        "tables_used": data.get("tables_used") or [],
        "params": data.get("params") or {},
        "reasoning": data.get("reasoning"),
    })
    return out
