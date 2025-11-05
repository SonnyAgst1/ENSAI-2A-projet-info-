# src/database/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
import os
from pathlib import Path

Base = declarative_base()

# --- config SQLite ---
DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "data" / "app.db"
DEFAULT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DB_MODE = os.getenv("DB_MODE", "dev")

if DB_MODE == "test":
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
else:
    engine = create_engine(
        f"sqlite:///{DEFAULT_DB_PATH}",
        connect_args={"check_same_thread": False},
        future=True,
    )

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
