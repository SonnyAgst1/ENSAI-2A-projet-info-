from typing import Optional, List
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError
from database import SessionLocal
from business_objects.models import Utilisateur, Activite, Commentaire, follows


class UtilisateurService:
    """Service pour gérer toutes les opérations liées aux utilisateurs"""