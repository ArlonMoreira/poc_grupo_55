"""
Python tools used by the agent pipeline:
  - execute_sql          : runs a query against PostgreSQL and returns raw results
  - analyze_data         : computes descriptive statistics on the returned rows (pandas)
  - generate_visualization: renders a chart or table image from query results
"""
import os
import time

import matplotlib
matplotlib.use("Agg")  # non-interactive backend — must be set before pyplot import
import matplotlib.pyplot as plt
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


# ---------------------------------------------------------------------------
# Visualization tool
# ---------------------------------------------------------------------------

_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def generate_visualization(columns: list, rows: list, viz_decision: dict) -> str | None:
    """Render a chart or table as a PNG image and return its absolute file path.

    Args:
        columns:      Column names from the SQL result.
        rows:         Row data from the SQL result.
        viz_decision: Dict produced by steps.decide_visualization with keys:
                        type        – "bar" | "horizontal_bar" | "line" | "pie" | "table" | "none"
                        x_column    – category / X-axis column name
                        y_column    – numeric / Y-axis column name
                        title       – chart title

    Returns:
        Absolute path to the generated PNG, or None when type is "none" or on error.
    """
    viz_type = viz_decision.get("type", "none")
    if viz_type == "none" or not rows:
        return None

    df = pd.DataFrame(rows, columns=columns)
    x_col = viz_decision.get("x_column")
    y_col = viz_decision.get("y_column")
    title = viz_decision.get("title", "Análise SIH/SUS")

    try:
        if viz_type == "table":
            _draw_cols = columns[:10]  # cap columns for readability
            _draw_df = df[_draw_cols].head(20)
            fig, ax = plt.subplots(figsize=(max(10, len(_draw_cols) * 1.8), min(2 + len(_draw_df) * 0.55, 14)))
            ax.axis("off")
            tbl = ax.table(
                cellText=_draw_df.astype(str).values,
                colLabels=_draw_cols,
                loc="center",
                cellLoc="center",
            )
            tbl.auto_set_font_size(False)
            tbl.set_fontsize(9)
            tbl.scale(1.1, 1.6)
            ax.set_title(title, fontsize=13, pad=12, fontweight="bold")

        else:
            if x_col not in df.columns or y_col not in df.columns:
                return None

            df = df.head(20)
            df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
            x_vals = df[x_col].astype(str)
            y_vals = df[y_col]

            plt.style.use("seaborn-v0_8-whitegrid")

            if viz_type == "bar":
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.bar(x_vals, y_vals, color="#2196F3", edgecolor="white")
                ax.set_xlabel(x_col, fontsize=11)
                ax.set_ylabel(y_col, fontsize=11)
                plt.xticks(rotation=40, ha="right", fontsize=9)

            elif viz_type == "horizontal_bar":
                fig, ax = plt.subplots(figsize=(12, max(5, len(df) * 0.45)))
                ax.barh(x_vals, y_vals, color="#2196F3", edgecolor="white")
                ax.set_xlabel(y_col, fontsize=11)
                ax.set_ylabel(x_col, fontsize=11)
                ax.invert_yaxis()

            elif viz_type == "line":
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(x_vals, y_vals, marker="o", linewidth=2, color="#2196F3")
                ax.set_xlabel(x_col, fontsize=11)
                ax.set_ylabel(y_col, fontsize=11)
                plt.xticks(rotation=40, ha="right", fontsize=9)

            elif viz_type == "pie":
                fig, ax = plt.subplots(figsize=(9, 9))
                ax.pie(y_vals, labels=x_vals, autopct="%1.1f%%", startangle=140)
                ax.axis("equal")

            else:
                return None

            ax.set_title(title, fontsize=13, pad=12, fontweight="bold")

        plt.tight_layout()
        os.makedirs(_OUTPUT_DIR, exist_ok=True)
        filepath = os.path.join(_OUTPUT_DIR, f"viz_{int(time.time())}.png")
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        return os.path.abspath(filepath)

    except Exception:
        return None
    finally:
        plt.close("all")
