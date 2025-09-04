from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from pathlib import Path
from app.db import models

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Session dependency
from contextlib import contextmanager

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def initialize_database() -> None:
    """Create tables and seed initial data if available."""
    # Ensure tables exist
    models.Base.metadata.create_all(bind=engine)

    # Optionally seed from init_db.sql if present
    potential_paths = [
        Path("/workspace/AionosGraphIQ/database/init_db.sql"),
        Path(__file__).resolve().parents[3] / "database" / "init_db.sql",
        Path("./database/init_db.sql").resolve(),
    ]

    init_sql_path = next((p for p in potential_paths if p.exists()), None)
    if init_sql_path and settings.database_url.startswith("sqlite"):
        with engine.connect() as connection:
            sql_script = init_sql_path.read_text()
            for statement in filter(None, (s.strip() for s in sql_script.split(";\n"))):
                connection.execute(text(statement))
            connection.commit()
