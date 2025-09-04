from fastapi import FastAPI
from .api.routes_health import router as health_router

app = FastAPI(title="AionosGraphIQ Backend", version="0.1.0")

app.include_router(health_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok", "service": "AionosGraphIQ"}
