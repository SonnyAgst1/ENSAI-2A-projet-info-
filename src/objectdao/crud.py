
from database import SessionLocal
from business_objects.models import Utilisateur

#CRUD pour utilisateur 
def create_user(nom, prenom, age, pseudo, mail, mdp):
    """CREATE : ajoute un utilisateur en base"""
    db = SessionLocal()
    try:
        user = Utilisateur(
            nom=nom,
            prenom=prenom,
            age=age,
            pseudo=pseudo,
            mail=mail,
            mdp=mdp
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


def get_all_users():
    """READ : retourne la liste des utilisateurs"""
    db = SessionLocal()
    try:
        return db.query(Utilisateur).all()
    finally:
        db.close()

def update_user(user_id, **kwargs):
    db = SessionLocal()
    try:
        user = db.query(Utilisateur).get(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.commit()
        return user
    finally:
        db.close()

def delete_user(user_id: int) -> bool:
    """DELETE : supprime un utilisateur de la base à partir de son ID.
    Retourne True si la suppression a réussi, False sinon.
    """
    db = SessionLocal()
    try:
        user = db.query(Utilisateur).get(user_id)
        if not user:
            print(f"Aucun utilisateur trouvé avec l'id {user_id}.")
            return False

        db.delete(user)
        db.commit()
        print(f"Utilisateur {user_id} supprimé avec succès.")
        return True

    except Exception as e:
        db.rollback()
        print(f"Erreur lors de la suppression : {e}")
        return False

    finally:
        db.close()