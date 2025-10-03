# src/objects.dao/crud.py

from business_objects.models import Utilisateur, Activite, Commentaire
from __init__ import get_session 
from sqlalchemy.exc import IntegrityError # Pour gérer les erreurs de contraintes SQL (ex: pseudo déjà pris)

# --- Opérations Utilisateur ---

def create_user(nom, prenom, pseudo, mail, mdp):
    """Crée et sauvegarde un nouvel utilisateur."""
    session = get_session()
    try:
        new_user = Utilisateur(
            nom=nom, prenom=prenom, pseudo=pseudo, mail=mail, mdp=mdp
            # Les autres champs seront NULL par défaut si non fournis
        )
        session.add(new_user)
        session.commit()
        return new_user
    except IntegrityError:
        session.rollback()
        raise ValueError(f"Erreur: Le pseudo '{pseudo}' ou l'e-mail '{mail}' est déjà utilisé.")
    finally:
        session.close()

def get_user_by_pseudo(pseudo):
    """Récupère un utilisateur par son pseudo."""
    session = get_session()
    try:
        # Le .first() retourne l'objet Utilisateur ou None
        return session.query(Utilisateur).filter(Utilisateur.pseudo == pseudo).first()
    finally:
        session.close()

# --- Opérations Activité ---

def create_activity(user_id, nom, type_sport, date_activite, duree_activite):
    """Crée et sauvegarde une nouvelle activité liée à un utilisateur."""
    session = get_session()
    try:
        new_activity = Activite(
            utilisateur_id=user_id, 
            nom=nom, 
            type_sport=type_sport, 
            date_activite=date_activite, 
            duree_activite=duree_activite
        )
        session.add(new_activity)
        session.commit()
        return new_activity
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_activities_for_user(user_id):
    """Récupère toutes les activités d'un utilisateur."""
    session = get_session()
    try:
        # On peut requêter Activite et filtrer sur la clé étrangère
        return session.query(Activite).filter(Activite.utilisateur_id == user_id).all()
    finally:
        session.close()

# ... Ajouter ici les fonctions pour Follow, Commentaire, Like, etc. ...