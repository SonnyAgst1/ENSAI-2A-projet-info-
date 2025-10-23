
from database import SessionLocal
from business_objects.models import Utilisateur

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
    """UPDATE : modifie un utilisateur en base"""
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


def delete_user(user_id):
    """DELETE : supprime un utilisateur en base"""
    db = SessionLocal()
    try:
        user = db.query(Utilisateur).get(user_id)
        if not user:
            return False

        db.delete(user)
        db.commit()
        return True
    finally:
        db.close()
