from database import engine, SessionLocal, Base
from business_objects.models import Utilisateur  # importe le modèle
from dao.utilisateur_dao import UtilisateurDAO

# Permet de reinitialisé la base de donnée pour relancer le fichier main sans soucis
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Base réinitialisée")


def init_db():
    """Crée physiquement les tables dans la base SQLite."""
    Base.metadata.create_all(bind=engine)
    print(" Tables créées")


if __name__ == "__main__":
    init_db()

    # Creation d'utilisateur
    create("Dupont", "Alice", 26, "Alicia", "alice@example.com", "secret123")
    create("Martin", "Lucas", 30, "Lulu", "lucas.martin@example.com", "mdp123")
    create("Durand", "Emma", 24, "Emmou", "emma.durand@example.com", "pass456")
    create("Petit", "Nina", 28, "Ninou", "nina.petit@example.com", "azerty789")

    # Visionnage liste des utilisateurs :

    print("\n Liste des utilisateurs en base :")
users = get_all_users()       # Appel de ta fonction CRUD
for u in users:
    print(f"- {u.id}: {u.nom} {u.prenom} ({u.pseudo})")

    # Renvoie bien la liste d'utilisateur


