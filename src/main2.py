
from database import engine, SessionLocal, Base
from business_objects.models import Utilisateur  # importe le modèle
from objects.dao.crud import create_user, get_all_users, update_user, delete_user

def init_db():
    """Crée physiquement les tables dans la base SQLite."""
    Base.metadata.create_all(bind=engine)
    print(" Tables créées / vérifiées.")

if __name__ == "__main__":
    init_db()

    # CREATE
    user = create_user("Dupont", "Alice", 26, "Alicia", "alice@example.com", "secret123")
    print(f"\n Utilisateur créé : {user.id} - {user.pseudo}")

    # READ
    print("\n👥 Liste des utilisateurs :")
    for u in get_all_users():
        print(f"- {u.id}: {u.nom} {u.prenom} ({u.pseudo})")

    # UPDATE
    updated = update_user(user.id, nom="Durand", pseudo="Alicia06")
    print(f"\n Utilisateur mis à jour : {updated.id} - {updated.nom} ({updated.pseudo})")

    # DELETE
    delete_user(user.id)
    print(f"\n Utilisateur {user.id} supprimé.")

    # READ again
    print("\n👥 Utilisateurs restants :")
    for u in get_all_users():
        print(f"- {u.id}: {u.nom} {u.prenom} ({u.pseudo})")

