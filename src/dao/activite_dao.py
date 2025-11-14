"""
DAO pour la table Activite
Gère toutes les opérations de base de données pour les activités
"""
from typing import Optional, List
from datetime import date
from sqlalchemy import and_, or_, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import SessionLocal
from business_objects.models import Activite


class ActiviteDAO:
    """Classe DAO pour les opérations CRUD sur Activite"""

    @staticmethod
    def create(
        utilisateur_id: int,
        nom: str,
        type_sport: str,
        date_activite: date,
        duree_activite: int,  # En SECONDES (déjà correct)
        description: str = "",
        gpx_path: Optional[str] = None,  # AJOUTER ce paramètre
        fichier_gpx: Optional[bytes] = None,  # Garder celui-ci
        d_plus: int = 0,
        calories: int = 0,
        distance: float = 0 
    ) -> Optional[Activite]:
        """
        Crée une nouvelle activité en base de données

        Args:
            utilisateur_id: ID de l'utilisateur
            nom: Nom de l'activité
            type_sport: Type de sport
            date_activite: Date de l'activité
            duree_activite: Durée en secondes
            description: Description (optionnel)
            fichier_gpx: Fichier GPX en bytes (optionnel)
            d_plus: Dénivelé positif (optionnel)
            calories: Calories dépensées (optionnel)

        Returns:
            L'activité créée ou None en cas d'erreur
        """
        db = SessionLocal()
        try:
            activite = Activite(
                utilisateur_id=utilisateur_id,
                nom=nom,
                type_sport=type_sport,
                date_activite=date_activite,
                duree_activite=duree_activite,
                description=description,
                fichier_gpx=fichier_gpx,
                d_plus=d_plus,
                calories=calories,
                distance=distance
            )

            db.add(activite)
            db.commit()
            db.refresh(activite)
            return activite

        except IntegrityError as e:
            db.rollback()
            print(f"Erreur d'intégrité : {e}")
            return None
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la création : {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def get_by_id(activite_id: int) -> Optional[Activite]:
        """
        Récupère une activité par son ID

        Args:
            activite_id: ID de l'activité

        Returns:
            L'activité ou None si non trouvée
        """
        db = SessionLocal()
        try:
            return db.query(Activite).filter(Activite.id == activite_id).first()
        finally:
            db.close()

    @staticmethod
    def get_all() -> List[Activite]:
        """
        Récupère toutes les activités

        Returns:
            Liste de toutes les activités
        """
        db = SessionLocal()
        try:
            return db.query(Activite).order_by(desc(Activite.date_activite)).all()
        finally:
            db.close()

    @staticmethod
    def get_by_user(
        utilisateur_id: int,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Activite]:
        """
        Récupère toutes les activités d'un utilisateur

        Args:
            utilisateur_id: ID de l'utilisateur
            limit: Nombre maximum d'activités (optionnel)
            offset: Décalage pour pagination (optionnel)

        Returns:
            Liste des activités de l'utilisateur
        """
        db = SessionLocal()
        try:
            query = db.query(Activite).filter(
                Activite.utilisateur_id == utilisateur_id
            ).order_by(desc(Activite.date_activite))

            if limit:
                query = query.limit(limit).offset(offset)

            return query.all()
        finally:
            db.close()

    @staticmethod
    def get_by_user_and_sport(
        utilisateur_id: int,
        type_sport: str,
        limit: Optional[int] = None
    ) -> List[Activite]:
        """
        Récupère les activités d'un utilisateur pour un sport spécifique

        Args:
            utilisateur_id: ID de l'utilisateur
            type_sport: Type de sport
            limit: Nombre maximum d'activités (optionnel)

        Returns:
            Liste des activités filtrées
        """
        db = SessionLocal()
        try:
            query = db.query(Activite).filter(
                and_(
                    Activite.utilisateur_id == utilisateur_id,
                    Activite.type_sport == type_sport
                )
            ).order_by(desc(Activite.date_activite))

            if limit:
                query = query.limit(limit)

            return query.all()
        finally:
            db.close()

    @staticmethod
    def get_by_date_range(
        utilisateur_id: int,
        date_debut: date,
        date_fin: date
    ) -> List[Activite]:
        """
        Récupère les activités d'un utilisateur dans une période

        Args:
            utilisateur_id: ID de l'utilisateur
            date_debut: Date de début
            date_fin: Date de fin

        Returns:
            Liste des activités dans la période
        """
        db = SessionLocal()
        try:
            return db.query(Activite).filter(
                and_(
                    Activite.utilisateur_id == utilisateur_id,
                    Activite.date_activite >= date_debut,
                    Activite.date_activite <= date_fin
                )
            ).order_by(desc(Activite.date_activite)).all()
        finally:
            db.close()

    @staticmethod
    def get_by_filters(
        utilisateur_id: int,
        type_sport: Optional[str] = None,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Activite]:
        """
        Récupère les activités avec filtres multiples

        Args:
            utilisateur_id: ID de l'utilisateur
            type_sport: Type de sport (optionnel)
            date_debut: Date de début (optionnel)
            date_fin: Date de fin (optionnel)
            limit: Nombre maximum d'activités (optionnel)
            offset: Décalage pour pagination (optionnel)

        Returns:
            Liste des activités filtrées
        """
        db = SessionLocal()
        try:
            query = db.query(Activite).filter(Activite.utilisateur_id == utilisateur_id)

            if type_sport:
                query = query.filter(Activite.type_sport == type_sport)

            if date_debut:
                query = query.filter(Activite.date_activite >= date_debut)

            if date_fin:
                query = query.filter(Activite.date_activite <= date_fin)

            query = query.order_by(desc(Activite.date_activite))

            if limit:
                query = query.limit(limit).offset(offset)

            return query.all()
        finally:
            db.close()

    @staticmethod
    def update(activite_id: int, **kwargs) -> Optional[Activite]:
        """
        Met à jour une activité

        Args:
            activite_id: ID de l'activité
            **kwargs: Champs à mettre à jour

        Returns:
            L'activité mise à jour ou None si non trouvée
        """
        db = SessionLocal()
        try:
            activite = db.query(Activite).filter(Activite.id == activite_id).first()

            if not activite:
                return None

            for key, value in kwargs.items():
                if hasattr(activite, key):
                    setattr(activite, key, value)

            db.commit()
            db.refresh(activite)
            return activite

        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la mise à jour : {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def delete(activite_id: int) -> bool:
        """
        Supprime une activité

        Args:
            activite_id: ID de l'activité

        Returns:
            True si supprimée, False sinon
        """
        db = SessionLocal()
        try:
            activite = db.query(Activite).filter(Activite.id == activite_id).first()

            if not activite:
                return False

            db.delete(activite)
            db.commit()
            return True

        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la suppression : {e}")
            return False
        finally:
            db.close()

    @staticmethod
    def count_by_user(utilisateur_id: int) -> int:
        """
        Compte le nombre d'activités d'un utilisateur

        Args:
            utilisateur_id: ID de l'utilisateur

        Returns:
            Nombre d'activités
        """
        db = SessionLocal()
        try:
            return db.query(Activite).filter(
                Activite.utilisateur_id == utilisateur_id
            ).count()
        finally:
            db.close()

    @staticmethod
    def count_by_user_and_sport(utilisateur_id: int, type_sport: str) -> int:
        """
        Compte le nombre d'activités d'un utilisateur pour un sport

        Args:
            utilisateur_id: ID de l'utilisateur
            type_sport: Type de sport

        Returns:
            Nombre d'activités
        """
        db = SessionLocal()
        try:
            return db.query(Activite).filter(
                and_(
                    Activite.utilisateur_id == utilisateur_id,
                    Activite.type_sport == type_sport
                )
            ).count()
        finally:
            db.close()

    @staticmethod
    def get_sports_list(utilisateur_id: int) -> List[str]:
        """
        Récupère la liste des sports pratiqués par un utilisateur

        Args:
            utilisateur_id: ID de l'utilisateur

        Returns:
            Liste des types de sport
        """
        db = SessionLocal()
        try:
            sports = db.query(Activite.type_sport).filter(
                Activite.utilisateur_id == utilisateur_id
            ).distinct().all()

            return [sport[0] for sport in sports]
        finally:
            db.close()

    @staticmethod
    def get_recent_by_user(
        utilisateur_id: int,
        nb_jours: int = 7,
        limit: int = 10
    ) -> List[Activite]:
        """
        Récupère les activités récentes d'un utilisateur

        Args:
            utilisateur_id: ID de l'utilisateur
            nb_jours: Nombre de jours à remonter
            limit: Nombre maximum d'activités

        Returns:
            Liste des activités récentes
        """
        from datetime import timedelta
        db = SessionLocal()
        try:
            date_limite = date.today() - timedelta(days=nb_jours)

            return db.query(Activite).filter(
                and_(
                    Activite.utilisateur_id == utilisateur_id,
                    Activite.date_activite >= date_limite
                )
            ).order_by(desc(Activite.date_activite)).limit(limit).all()
        finally:
            db.close()
