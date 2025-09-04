import os
from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "AionosGraphIQ Backend"
    environment: str = os.getenv("ENVIRONMENT", "local")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:////workspace/AionosGraphIQ/database/northwind.sqlite")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")

settings = Settings()
