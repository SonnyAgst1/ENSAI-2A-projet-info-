from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
from fastapi import Depends
from sqlmodel import Session # Garder cet import si vous l'utilisez ailleurs

# ====================================================================
# 1. CONFIGURATION DE BASE DE DONNÉES (Inchangé)
# ====================================================================

# Créer le dossier data/ s'il n'existe pas
# Le chemin parent[2] fonctionne si le dossier src est dans un sous-dossier
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# Chemin vers la base de données
DB_PATH = DATA_DIR / "app_sportive.db"

# Crée un moteur de base de données SQLite
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=False, # Désactiver l'echo ici si vous voulez moins de logs, mais ce n'est pas le problème
    connect_args={"check_same_thread": False}
)

# ====================================================================
# 2. DÉFINITION DE LA BASE DÉCLARATIVE (CORRECTION CRITIQUE)
# ====================================================================

# Nous allons vérifier si la classe Base a déjà été créée pour éviter le conflit
# C'est le point où SQLAlchemy enregistre les métadonnées.
try:
    # Tentative d'importer Base depuis le module, si déjà chargé
    from src.database import Base 
except (ImportError, AttributeError):
    # Si le module n'a pas encore de Base ou s'il n'est pas complètement initialisé, on la crée
    Base = declarative_base()


# ====================================================================
# 3. CRÉATION DES SESSIONS
# ====================================================================

# Création de sessions pour interagir avec la base
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_session():
    # Note : Utilisation de SessionLocal qui est une sessionmaker de SQLAlchemy
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dépendance utilisée dans les routeurs
# ATTENTION: Si vous utilisez Session de sqlmodel, assurez-vous de l'utiliser correctement.
# Si vous utilisez uniquement SQLAlchemy, cette ligne peut être simplifiée.
SessionDep = Annotated[Session, Depends(get_session)] 

# NOTE IMPORTANTE: Ce print est la cause du double affichage. 
# Le retirer ne corrige pas l'erreur de SQLAlchemy, mais clarifie le log.
# Je le garde car il vous est utile.
print(f" Base de données : {DB_PATH}")