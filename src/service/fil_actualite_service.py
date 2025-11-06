"""
Service pour gérer le fil d'actualité (F2)
Placez ce fichier dans src/service/fil_actualite_service.py
"""
from typing import List
from datetime import date, timedelta
from sqlalchemy import desc
from database import SessionLocal
from business_objects.models import Activite, Utilisateur, follows


class FilActualiteService:
    """Service pour le fil d'actualité"""

    @staticmethod
    def obtenir_fil_actualite(
        utilisateur_id: int,
        nb_jours: int = 7,
        limite: int = 50
    ) -> List[dict]:
        """
        Récupère le fil d'actualité d'un utilisateur
        (activités des utilisateurs qu'il suit)

        Args:
            utilisateur_id: ID de l'utilisateur
            nb_jours: Nombre de jours à remonter (par défaut 7)
            limite: Nombre maximum d'activités (par défaut 50)

        Returns:
            Liste de dictionnaires contenant les activités et infos utilisateur
        """
        db = SessionLocal()
        try:
            # Récupérer les IDs des utilisateurs suivis
            suivis = db.execute(
                follows.select().where(follows.c.follower_id == utilisateur_id)
            ).fetchall()
            
            ids_suivis = [row.followed_id for row in suivis]
            
            if not ids_suivis:
                return []

            # Date limite
            date_limite = date.today() - timedelta(days=nb_jours)

            # Récupérer les activités des utilisateurs suivis
            activites = db.query(Activite).filter(
                Activite.utilisateur_id.in_(ids_suivis),
                Activite.date_activite >= date_limite
            ).order_by(desc(Activite.date_activite)).limit(limite).all()

            # Formater les résultats avec les infos utilisateur
            fil = []
            for activite in activites:
                utilisateur = db.query(Utilisateur).filter(
                    Utilisateur.id == activite.utilisateur_id
                ).first()
                
                # Compter likes et commentaires
                nb_likes = len(activite.likers)
                nb_commentaires = len(activite.commentaires)
                
                fil.append({
                    'activite': activite,
                    'utilisateur': utilisateur,
                    'nb_likes': nb_likes,
                    'nb_commentaires': nb_commentaires
                })

            return fil

        finally:
            db.close()

    @staticmethod
    def rechercher_utilisateurs(
        pattern: str,
        limite: int = 10
    ) -> List[Utilisateur]:
        """
        Recherche des utilisateurs par pseudo

        Args:
            pattern: Motif de recherche
            limite: Nombre maximum de résultats

        Returns:
            Liste des utilisateurs trouvés
        """
        db = SessionLocal()
        try:
            return db.query(Utilisateur).filter(
                Utilisateur.pseudo.ilike(f"%{pattern}%")
            ).limit(limite).all()
        finally:
            db.close()

    @staticmethod
    def obtenir_suggestions_utilisateurs(
        utilisateur_id: int,
        limite: int = 10
    ) -> List[Utilisateur]:
        """
        Suggère des utilisateurs à suivre
        (utilisateurs non suivis qui ont des activités)

        Args:
            utilisateur_id: ID de l'utilisateur
            limite: Nombre de suggestions

        Returns:
            Liste d'utilisateurs suggérés
        """
        db = SessionLocal()
        try:
            # IDs déjà suivis
            suivis = db.execute(
                follows.select().where(follows.c.follower_id == utilisateur_id)
            ).fetchall()
            ids_suivis = [row.followed_id for row in suivis]
            ids_suivis.append(utilisateur_id)  # Exclure soi-même

            # Utilisateurs ayant des activités récentes
            from sqlalchemy import func
            
            utilisateurs_actifs = db.query(
                Activite.utilisateur_id,
                func.count(Activite.id).label('nb_activites')
            ).group_by(
                Activite.utilisateur_id
            ).order_by(
                desc('nb_activites')
            ).limit(limite * 2).all()

            # Filtrer ceux déjà suivis
            suggestions = []
            for user_id, _ in utilisateurs_actifs:
                if user_id not in ids_suivis:
                    user = db.query(Utilisateur).filter(
                        Utilisateur.id == user_id
                    ).first()
                    if user:
                        suggestions.append(user)
                        if len(suggestions) >= limite:
                            break

            return suggestions

        finally:
            db.close()