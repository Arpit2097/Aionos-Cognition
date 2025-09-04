from typing import Any, Dict, List, Tuple
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.config import settings


def _heuristic_intent_to_sql(user_query: str) -> Tuple[str, str]:
    """Very simple heuristic NL->SQL and chart type mapping for POC.
    Returns (sql, chart_type).
    """
    q = user_query.lower()

    if "pie" in q and ("region" in q or "by region" in q):
        sql = (
            "SELECT COALESCE(ShipRegion, 'Unknown') AS label, "
            "ROUND(SUM((UnitPrice * Quantity) * (1 - Discount)), 2) AS value "
            "FROM Orders o JOIN OrderDetails od ON o.OrderID = od.OrderID "
            "GROUP BY ShipRegion ORDER BY value DESC"
        )
        return sql, "pie"

    if ("sales" in q and "category" in q) or ("category" in q and ("best" in q or "highest" in q)):
        sql = (
            "SELECT c.CategoryName AS label, "
            "ROUND(SUM((od.UnitPrice * od.Quantity) * (1 - od.Discount)), 2) AS value "
            "FROM Categories c "
            "JOIN Products p ON p.CategoryID = c.CategoryID "
            "JOIN OrderDetails od ON od.ProductID = p.ProductID "
            "GROUP BY c.CategoryName ORDER BY value DESC"
        )
        return sql, "bar"

    if "total sales" in q and ("last month" in q or "previous month" in q):
        sql = (
            "SELECT strftime('%Y-%m', date(OrderDate)) AS label, "
            "ROUND(SUM((UnitPrice * Quantity) * (1 - Discount)), 2) AS value "
            "FROM Orders o JOIN OrderDetails od ON o.OrderID = od.OrderID "
            "WHERE date(OrderDate) >= date('now','start of month','-1 month') "
            "AND date(OrderDate) < date('now','start of month') "
            "GROUP BY strftime('%Y-%m', date(OrderDate))"
        )
        return sql, "line"

    if "sales by" in q and "month" in q:
        sql = (
            "SELECT strftime('%Y-%m', date(OrderDate)) AS label, "
            "ROUND(SUM((UnitPrice * Quantity) * (1 - Discount)), 2) AS value "
            "FROM Orders o JOIN OrderDetails od ON o.OrderID = od.OrderID "
            "GROUP BY strftime('%Y-%m', date(OrderDate)) ORDER BY label"
        )
        return sql, "line"

    # Fallback: top products by sales
    sql = (
        "SELECT p.ProductName AS label, "
        "ROUND(SUM((od.UnitPrice * od.Quantity) * (1 - od.Discount)), 2) AS value "
        "FROM Products p JOIN OrderDetails od ON od.ProductID = p.ProductID "
        "GROUP BY p.ProductName ORDER BY value DESC LIMIT 10"
    )
    return sql, "bar"


def generate_sql_and_chart(user_query: str) -> Dict[str, Any]:
    # Placeholder for real LangGraph orchestration; use heuristics for POC
    sql, chart_type = _heuristic_intent_to_sql(user_query)
    return {"sql": sql, "chart_type": chart_type}


def execute_sql(session: Session, sql: str) -> List[Dict[str, Any]]:
    result = session.execute(text(sql))
    rows = []
    for row in result.mappings():
        rows.append({"label": row.get("label"), "value": row.get("value")})
    return rows

