from app.services.query_engine import generate_sql_and_chart


def test_generate_sql_and_chart_basic():
    plan = generate_sql_and_chart("Show me sales by region in a pie chart")
    assert plan["chart_type"] == "pie"
    assert "GROUP BY ShipRegion" in plan["sql"]

