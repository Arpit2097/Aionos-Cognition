from typing import Any, Dict, List


def build_chart_payload(chart_type: str, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    labels = [r.get("label") for r in rows]
    values = [float(r.get("value") or 0) for r in rows]
    return {
        "type": chart_type,
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "label": "Sales",
                    "data": values,
                }
            ],
        },
        "options": {},
    }

