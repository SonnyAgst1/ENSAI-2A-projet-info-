# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Crée un moteur de base de données SQLite (fichier local)
engine = create_engine("sqlite:///app_sportive.db", echo=True)
# "app_sportive.db" sera le fichier SQLite créé automatiquement

# Définition de la classe de base (toutes les tables en hériteront)
Base = declarative_base()

# Création de sessions pour interagir avec la base
SessionLocal = sessionmaker(bind=engine)
