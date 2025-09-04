from typing import Any, Dict, List


def summarize_results(user_query: str, rows: List[Dict[str, Any]]) -> str:
    if not rows:
        return "No results found."
    total = sum(float(r.get("value") or 0) for r in rows)
    top = rows[0]
    pct = 0.0
    if total > 0:
        pct = (float(top.get("value") or 0) / total) * 100
    return (
        f"For query '{user_query}', total is {total:.2f}. "
        f"Top segment '{top.get('label')}' contributes {pct:.1f}%"
    )

