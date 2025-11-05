from typing import Annotated
# database/__init__.py
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path
from fastapi import Depends

# Créer le dossier data/ s'il n'existe pas
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Remonte de src/database/ à la racine
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# Chemin vers la base de données
DB_PATH = DATA_DIR / "app_sportive.db"

# Crée un moteur de base de données SQLite
engine = create_engine(
    f"sqlite:///{DB_PATH}", 
    echo=True,
    connect_args={"check_same_thread": False}
)

# Définition de la classe de base (toutes les tables en hériteront)
Base = declarative_base()

# Création de sessions pour interagir avec la base
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

print(f" Base de données : {DB_PATH}")