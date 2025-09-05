from __future__ import annotations
import os
from typing import Any, Dict, List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy import inspect

# --------- Descubrir la URL de la BD ----------
def _discover_sqlite_url() -> str:
    """
    Intenta leer la ruta de la BD de Django; si no, cae a env; si no, a sqlite:///db.sqlite3
    """
    # 1) Si se puede importar settings de Django:
    try:
        from django.conf import settings as dj_settings  # type: ignore
        name = dj_settings.DATABASES_SQLITE["default"]["NAME"]
        if name:
            # Ruta absoluta -> sqlite:////abs/path.db ; relativa -> sqlite:///relative.db
            if os.path.isabs(name):
                return f"sqlite:///{name}"
            else:
                # relativa al cwd
                return f"sqlite:///{os.path.abspath(name)}"
    except Exception:
        pass

    # 2) Variable de entorno:
    env_url = os.getenv("OPMS_DB_URL")
    if env_url:
        return env_url

    # 3) Default local:
    default_path = os.path.abspath("db.sqlite3")
    return f"sqlite:///{default_path}"

_ENGINE: Optional[Engine] = None

def get_engine() -> Engine:
    global _ENGINE
    if _ENGINE is None:
        db_url = _discover_sqlite_url()
        _ENGINE = create_engine(
            db_url,
            pool_pre_ping=True,
            future=True,
        )
    return _ENGINE

# --------- Introspección de esquema ----------
def get_schema_tables() -> List[str]:
    """
    Retorna lista de nombres de tablas reales en la BD (SQLite).
    """
    eng = get_engine()
    insp = inspect(eng)
    return insp.get_table_names()

# --------- Ejecución segura ----------
def run_query(sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Ejecuta SQL (ya validado) y retorna filas como lista de dicts.
    Nota: SQLite no soporta timeout a nivel servidor. Mantén LIMIT bajo.
    """
    eng = get_engine()
    with eng.connect() as conn:
        result = conn.execute(text(sql), params or {})
        rows = [dict(r._mapping) for r in result.fetchall()]
    return rows
