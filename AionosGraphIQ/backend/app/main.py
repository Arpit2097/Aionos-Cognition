from fastapi import FastAPI
from .api.routes_health import router as health_router
from .api.routes_chat import router as chat_router
from .api.routes_forecast import router as forecast_router
from .db.database import initialize_database
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    initialize_database()
    yield
    # Shutdown

app = FastAPI(title="AionosGraphIQ Backend", version="0.1.0", lifespan=lifespan)

app.include_router(health_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(forecast_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok", "service": "AionosGraphIQ"}
