from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importe la Base déclarative pour que `create_all` puisse trouver toutes les classes
from business_objects.models import Base 

DB_FILE = 'strava_clone_sqlalchemy.db'

# 1. Création du moteur (connexion à la BDD)
engine = create_engine(f"sqlite:///{DB_FILE}")

# 2. Fabrique de sessions
# SessionLocal est la "recette" pour créer une session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Crée toutes les tables dans la base de données si elles n'existent pas."""
    # Base.metadata sait de quelles tables il a besoin grâce aux classes dans models.py
    Base.metadata.create_all(bind=engine)
    print(f"Base de données '{DB_FILE}' initialisée (tables créées).")

def get_session():
    """Fournit une nouvelle session de base de données à utiliser par le DAO."""
    session = SessionLocal()
    try:
        return session
    finally:
        # NOTE: La fermeture de la session doit être gérée par la fonction appelante
        # Pour des raisons de simplicité ici, nous la retournons. 
        # Dans un environnement web (ex: FastAPI), on utilise un 'yield' pour la fermeture.
        pass