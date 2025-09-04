from typing import Dict, Any, List
import pandas as pd


def forecast_next_period(monthly_points: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not monthly_points:
        return {"projection": 0.0, "trend": "flat"}
    df = pd.DataFrame(monthly_points)
    df = df.sort_values("label")
    df["value"] = df["value"].astype(float)
    # Simple last-3 moving average
    window = min(3, len(df))
    projection = df["value"].tail(window).mean()
    trend = "up" if df["value"].iloc[-1] < projection else ("down" if df["value"].iloc[-1] > projection else "flat")
    return {"projection": float(projection), "trend": trend}

