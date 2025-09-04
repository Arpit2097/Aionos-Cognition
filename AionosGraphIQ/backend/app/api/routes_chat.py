from fastapi import APIRouter
from pydantic import BaseModel
from app.db.database import get_session
from app.services.query_engine import generate_sql_and_chart, execute_sql
from app.services.visualization import build_chart_payload
from app.services.insights import summarize_results


router = APIRouter()


class ChatRequest(BaseModel):
    query: str


@router.post("/chat")
def chat_query(payload: ChatRequest):
    plan = generate_sql_and_chart(payload.query)
    with get_session() as session:
        rows = execute_sql(session, plan["sql"])  # type: ignore[index]
    chart = build_chart_payload(plan["chart_type"], rows)  # type: ignore[index]
    summary = summarize_results(payload.query, rows)
    return {"chart": chart, "data": rows, "summary": summary, "sql": plan["sql"]}

