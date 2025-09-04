from fastapi import APIRouter
from pydantic import BaseModel
from app.db.database import get_session
from app.services.query_engine import execute_sql
from app.services.forecast import forecast_next_period


router = APIRouter()


class ForecastRequest(BaseModel):
    basis: str | None = None


@router.post("/forecast")
def forecast(payload: ForecastRequest):
    # Simple basis: monthly sales over all orders
    sql = (
        "SELECT strftime('%Y-%m', date(OrderDate)) AS label, "
        "ROUND(SUM((UnitPrice * Quantity) * (1 - Discount)), 2) AS value "
        "FROM Orders o JOIN OrderDetails od ON o.OrderID = od.OrderID "
        "GROUP BY strftime('%Y-%m', date(OrderDate)) ORDER BY label"
    )
    with get_session() as session:
        rows = execute_sql(session, sql)
    result = forecast_next_period(rows)
    return {"basis_points": rows, "projection": result}

