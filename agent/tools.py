"""
Python tools used by the agent pipeline:
  - execute_sql : runs a query against PostgreSQL and returns raw results
  - analyze_data: computes descriptive statistics on the returned rows (pandas)
"""
import pandas as pd
import psycopg2

from agent.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

MAX_ROWS = 2000


def execute_sql(query: str) -> dict:
    """Execute a SQL query against the PostgreSQL database.

    Returns a dict with keys:
        success   (bool)
        columns   (list[str])
        rows      (list[list])
        row_count (int)
        truncated (bool)  -- True when result was capped at MAX_ROWS
        error     (str | None)
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=int(DB_PORT),
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
        )
        cur = conn.cursor()
        cur.execute(query)
        columns = [desc[0] for desc in cur.description] if cur.description else []
        rows = cur.fetchmany(MAX_ROWS)
        cur.close()
        conn.close()
        return {
            "success": True,
            "columns": columns,
            "rows": [list(r) for r in rows],
            "row_count": len(rows),
            "truncated": len(rows) == MAX_ROWS,
            "error": None,
        }
    except Exception as exc:
        return {
            "success": False,
            "columns": [],
            "rows": [],
            "row_count": 0,
            "truncated": False,
            "error": str(exc),
        }


def analyze_data(columns: list, rows: list) -> dict:
    """Compute descriptive statistics on query result rows.

    Returns a dict with:
        row_count   (int)
        numeric     (dict)  -- per-column min/max/mean/sum
        categorical (dict)  -- per-column unique count + top-10 values
    """
    if not rows:
        return {"row_count": 0, "numeric": {}, "categorical": {}}

    df = pd.DataFrame(rows, columns=columns)
    summary: dict = {"row_count": len(df), "numeric": {}, "categorical": {}}

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            s = df[col].dropna()
            summary["numeric"][col] = {
                "min": float(s.min()) if len(s) else None,
                "max": float(s.max()) if len(s) else None,
                "mean": round(float(s.mean()), 4) if len(s) else None,
                "sum": float(s.sum()) if len(s) else None,
            }
        else:
            top = df[col].value_counts().head(10).to_dict()
            summary["categorical"][col] = {
                "unique": int(df[col].nunique()),
                "top": {str(k): int(v) for k, v in top.items()},
            }

    return summary
