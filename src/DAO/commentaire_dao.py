"""
DAO (Data Access Object) pour la table Commentaire
Gère toutes les opérations de base de données pour les commentaires
"""
from typing import Optional, List
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from database import SessionLocal
from business_objects.models import Commentaire


class CommentaireDAO:
    """Classe DAO pour les opérations CRUD sur Commentaire"""

    @staticmethod
    def create(
        activite_id: int,
        auteur_id: int,
        contenu: str
    ) -> Optional[Commentaire]:
        """
        Crée un nouveau commentaire en base de données

        Args:
            activite_id: ID de l'activité commentée
            auteur_id: ID de l'auteur du commentaire
            contenu: Contenu du commentaire

        Returns:
            Le commentaire créé ou None en cas d'erreur
        """
        db = SessionLocal()
        try:
            commentaire = Commentaire(
                activite_id=activite_id,
                auteur_id=auteur_id,
                contenu=contenu
            )

            db.add(commentaire)
            db.commit()
            db.refresh(commentaire)
            return commentaire

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
    def get_by_id(commentaire_id: int) -> Optional[Commentaire]:
        """
        Récupère un commentaire par son ID

        Args:
            commentaire_id: ID du commentaire

        Returns:
            Le commentaire ou None si non trouvé
        """
        db = SessionLocal()
        try:
            return db.query(Commentaire).filter(Commentaire.id == commentaire_id).first()
        finally:
            db.close()

    @staticmethod
    def get_all() -> List[Commentaire]:
        """
        Récupère tous les commentaires

        Returns:
            Liste de tous les commentaires
        """
        db = SessionLocal()
        try:
            return db.query(Commentaire).all()
        finally:
            db.close()

    @staticmethod
    def get_by_activite(activite_id: int, limit: Optional[int] = None) -> List[Commentaire]:
        """
        Récupère tous les commentaires d'une activité

        Args:
            activite_id: ID de l'activité
            limit: Nombre maximum de commentaires (optionnel)

        Returns:
            Liste des commentaires de l'activité
        """
        db = SessionLocal()
        try:
            query = db.query(Commentaire).filter(
                Commentaire.activite_id == activite_id
            ).order_by(desc(Commentaire.id))

            if limit:
                query = query.limit(limit)

            return query.all()
        finally:
            db.close()

    @staticmethod
    def get_by_auteur(auteur_id: int, limit: Optional[int] = None) -> List[Commentaire]:
        """
        Récupère tous les commentaires d'un auteur

        Args:
            auteur_id: ID de l'auteur
            limit: Nombre maximum de commentaires (optionnel)

        Returns:
            Liste des commentaires de l'auteur
        """
        db = SessionLocal()
        try:
            query = db.query(Commentaire).filter(
                Commentaire.auteur_id == auteur_id
            ).order_by(desc(Commentaire.id))

            if limit:
                query = query.limit(limit)

            return query.all()
        finally:
            db.close()

    @staticmethod
    def update(commentaire_id: int, nouveau_contenu: str) -> Optional[Commentaire]:
        """
        Met à jour le contenu d'un commentaire

        Args:
            commentaire_id: ID du commentaire
            nouveau_contenu: Nouveau contenu

        Returns:
            Le commentaire mis à jour ou None si non trouvé
        """
        db = SessionLocal()
        try:
            commentaire = db.query(Commentaire).filter(
                Commentaire.id == commentaire_id
            ).first()

            if not commentaire:
                return None

            commentaire.contenu = nouveau_contenu
            db.commit()
            db.refresh(commentaire)
            return commentaire

        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la mise à jour : {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def delete(commentaire_id: int) -> bool:
        """
        Supprime un commentaire

        Args:
            commentaire_id: ID du commentaire

        Returns:
            True si supprimé, False sinon
        """
        db = SessionLocal()
        try:
            commentaire = db.query(Commentaire).filter(
                Commentaire.id == commentaire_id
            ).first()

            if not commentaire:
                return False

            db.delete(commentaire)
            db.commit()
            return True

        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la suppression : {e}")
            return False
        finally:
            db.close()

    @staticmethod
    def delete_by_activite(activite_id: int) -> int:
        """
        Supprime tous les commentaires d'une activité

        Args:
            activite_id: ID de l'activité

        Returns:
            Nombre de commentaires supprimés
        """
        db = SessionLocal()
        try:
            commentaires = db.query(Commentaire).filter(
                Commentaire.activite_id == activite_id
            ).all()

            count = len(commentaires)

            for commentaire in commentaires:
                db.delete(commentaire)

            db.commit()
            return count

        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la suppression : {e}")
            return 0
        finally:
            db.close()

    @staticmethod
    def count_by_activite(activite_id: int) -> int:
        """
        Compte le nombre de commentaires d'une activité

        Args:
            activite_id: ID de l'activité

        Returns:
            Nombre de commentaires
        """
        db = SessionLocal()
        try:
            return db.query(Commentaire).filter(
                Commentaire.activite_id == activite_id
            ).count()
        finally:
            db.close()

    @staticmethod
    def count_by_auteur(auteur_id: int) -> int:
        """
        Compte le nombre de commentaires d'un auteur

        Args:
            auteur_id: ID de l'auteur

        Returns:
            Nombre de commentaires
        """
        db = SessionLocal()
        try:
            return db.query(Commentaire).filter(
                Commentaire.auteur_id == auteur_id
            ).count()
        finally:
            db.close()

    @staticmethod
    def get_recent_by_activite(activite_id: int, limit: int = 5) -> List[Commentaire]:
        """
        Récupère les commentaires les plus récents d'une activité

        Args:
            activite_id: ID de l'activité
            limit: Nombre de commentaires à retourner

        Returns:
            Liste des commentaires récents
        """
        db = SessionLocal()
        try:
            return db.query(Commentaire).filter(
                Commentaire.activite_id == activite_id
            ).order_by(desc(Commentaire.id)).limit(limit).all()
        finally:
            db.close()

    @staticmethod
    def is_author(commentaire_id: int, utilisateur_id: int) -> bool:
        """
        Vérifie si un utilisateur est l'auteur d'un commentaire

        Args:
            commentaire_id: ID du commentaire
            utilisateur_id: ID de l'utilisateur

        Returns:
            True si l'utilisateur est l'auteur, False sinon
        """
        db = SessionLocal()
        try:
            commentaire = db.query(Commentaire).filter(
                Commentaire.id == commentaire_id
            ).first()

            if not commentaire:
                return False

            return commentaire.auteur_id == utilisateur_id
        finally:
            db.close()
