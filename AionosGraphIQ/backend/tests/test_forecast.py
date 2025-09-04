from app.services.forecast import forecast_next_period


def test_forecast_next_period():
    points = [
        {"label": "1996-06", "value": 100.0},
        {"label": "1996-07", "value": 200.0},
        {"label": "1996-08", "value": 300.0},
    ]
    result = forecast_next_period(points)
    assert "projection" in result
    assert result["projection"] > 0

