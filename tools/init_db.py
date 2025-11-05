# tools/init_db.py
from database.database import Base, engine
from dao.utilisateur_dao import Utilisateur
from dao.activite_dao import Activite
from dao.commentaire_dao import Commentaire

if __name__ == "__main__":
    print("📦 Création des tables dans la base SQLite...")
    Base.metadata.create_all(bind=engine)
    print("✅ Base initialisée avec succès !")
