from __future__ import annotations
from typing import Iterable, Set
import sqlglot
from sqlglot import exp

DEFAULT_BAD_EXPRESSIONS = (
    exp.Insert, exp.Update, exp.Delete, exp.Create, exp.Drop,
    exp.Alter, exp.Command, exp.Transaction, exp.Grant,
)

DEFAULT_BAD_FUNCTIONS = {"sleep", "load_file", "xp_cmdshell", "pg_read_file"}

def _collect_tables(expr: exp.Expression) -> Set[str]:
    tables: Set[str] = set()
    for t in expr.find_all(exp.Table):
        # t.name puede ser None si es subquery con alias; cuidamos Name
        if getattr(t, "name", None):
            tables.add(t.name)
    return tables

def _has_bad_nodes(expr: exp.Expression) -> bool:
    for node in expr.walk():
        if isinstance(node, DEFAULT_BAD_EXPRESSIONS):
            return True
    return False

def _has_bad_functions(expr: exp.Expression) -> bool:
    for func in expr.find_all(exp.Func):
        name = (func.name or "").lower()
        if name in DEFAULT_BAD_FUNCTIONS:
            return True
    return False

def _ensure_limit(sql: str, default_limit: int) -> str:
    expr = sqlglot.parse_one(sql, read="sqlite", error_level="RAISE")
    has_limit = any(isinstance(n, exp.Limit) for n in expr.find_all(exp.Limit))
    if not has_limit:
        return sql.rstrip().rstrip(";") + f" LIMIT {default_limit};"
    return sql

def validate_and_rewrite_sql(
    sql_query: str,
    *,
    schema_tables: Iterable[str],
    allowed_prefixes: Iterable[str],
    default_limit: int = 200,
    dialect: str = "sqlite",
) -> str:
    """
    Valida y devuelve un SQL seguro (sólo SELECT) con LIMIT garantizado.
    - dialect se usa para parseo; para SQLite usa 'sqlite'
    - schema_tables: nombres de tablas reales disponibles
    - allowed_prefixes: prefijos permitidos (p.ej. ["vw_", "dim_", "fact_"])
    """
    schema_tables = set(schema_tables or [])
    allowed_prefixes = list(allowed_prefixes or [])

    # Parse con sqlglot
    expr = sqlglot.parse_one(sql_query, read=dialect or "sqlite", error_level="RAISE")

    # Sólo SELECT:
    if expr.key != "SELECT":
        raise ValueError("Sólo se permiten consultas SELECT.")

    # Bloques peligrosos
    if _has_bad_nodes(expr):
        raise ValueError("Se detectaron comandos no permitidos en la consulta.")
    if _has_bad_functions(expr):
        raise ValueError("Se detectaron funciones no permitidas en la consulta.")

    # Tablas usadas y allowlist
    used = _collect_tables(expr)
    if not used:
        # permitimos SELECT sin FROM (p.ej. SELECT 1) si quieres, pero en BI normalmente queremos FROM
        # aquí lo bloqueamos para transparencia:
        raise ValueError("No se detectaron tablas en la consulta.")

    unknown = {t for t in used if t not in schema_tables}
    if unknown:
        raise ValueError(f"Tablas inexistentes en el esquema: {sorted(unknown)}")

    if allowed_prefixes:
        bad_prefix = {t for t in used if not any(t.startswith(p) for p in allowed_prefixes)}
        if bad_prefix:
            raise ValueError(f"Tablas fuera de prefijos permitidos: {sorted(bad_prefix)}")

    # LIMIT obligatorio
    safe_sql = _ensure_limit(sql_query, default_limit)
    return safe_sql
