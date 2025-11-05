"""
DAO (Data Access Object) pour la table Utilisateur
Gère toutes les opérations de base de données pour les utilisateurs
"""
from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import SessionLocal
from business_objects.models import 


class UtilisateurDAO:
    """Classe DAO pour les opérations CRUD sur Utilisateur"""

    @staticmethod
    def create(
        nom: str,
        prenom: str,
        age: int,
        pseudo: str,
        mail: str,
        mdp: str,
        taille: Optional[float] = None,
        poids: Optional[float] = None,
        telephone: Optional[int] = None,
        photo_profil: Optional[bytes] = None
    ) -> Optional[Utilisateur]:
        """
        Crée un nouvel utilisateur en base de données

        Args:
            nom: Nom de l'utilisateur
            prenom: Prénom de l'utilisateur
            age: Âge de l'utilisateur
            pseudo: Pseudo unique
            mail: Email unique
            mdp: Mot de passe (à hasher en production)
            taille: Taille en cm (optionnel)
            poids: Poids en kg (optionnel)
            telephone: Numéro de téléphone (optionnel)
            photo_profil: Photo en bytes (optionnel)

        Returns:
            L'utilisateur créé ou None en cas d'erreur
        """
        db = SessionLocal()
        try:
            utilisateur = Utilisateur(
                nom=nom,
                prenom=prenom,
                age=age,
                pseudo=pseudo,
                mail=mail,
                mdp=mdp,
                taille=taille,
                poids=poids,
                telephone=telephone,
                photo_profil=photo_profil
            )

            db.add(utilisateur)
            db.commit()
            db.refresh(utilisateur)
            return utilisateur

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
    def get_by_id(user_id: int) -> Optional[Utilisateur]:
        """
        Récupère un utilisateur par son ID

        Args:
            user_id: ID de l'utilisateur

        Returns:
            L'utilisateur ou None si non trouvé
        """
        db = SessionLocal()
        try:
            return db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
        finally:
            db.close()

    @staticmethod
    def get_by_pseudo(pseudo: str) -> Optional[Utilisateur]:
        """
        Récupère un utilisateur par son pseudo

        Args:
            pseudo: Pseudo de l'utilisateur

        Returns:
            L'utilisateur ou None si non trouvé
        """
        db = SessionLocal()
        try:
            return db.query(Utilisateur).filter(Utilisateur.pseudo == pseudo).first()
        finally:
            db.close()

    @staticmethod
    def get_by_mail(mail: str) -> Optional[Utilisateur]:
        """
        Récupère un utilisateur par son email

        Args:
            mail: Email de l'utilisateur

        Returns:
            L'utilisateur ou None si non trouvé
        """
        db = SessionLocal()
        try:
            return db.query(Utilisateur).filter(Utilisateur.mail == mail).first()
        finally:
            db.close()

    @staticmethod
    def get_all() -> List[Utilisateur]:
        """
        Récupère tous les utilisateurs

        Returns:
            Liste de tous les utilisateurs
        """
        db = SessionLocal()
        try:
            return db.query(Utilisateur).all()
        finally:
            db.close()

    @staticmethod
    def update(user_id: int, **kwargs) -> Optional[Utilisateur]:
        """
        Met à jour un utilisateur

        Args:
            user_id: ID de l'utilisateur
            **kwargs: Champs à mettre à jour

        Returns:
            L'utilisateur mis à jour ou None si non trouvé
        """
        db = SessionLocal()
        try:
            utilisateur = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()

            if not utilisateur:
                return None

            for key, value in kwargs.items():
                if hasattr(utilisateur, key):
                    setattr(utilisateur, key, value)

            db.commit()
            db.refresh(utilisateur)
            return utilisateur

        except IntegrityError as e:
            db.rollback()
            print(f"Erreur d'intégrité : {e}")
            return None
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la mise à jour : {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def delete(user_id: int) -> bool:
        """
        Supprime un utilisateur

        Args:
            user_id: ID de l'utilisateur

        Returns:
            True si supprimé, False sinon
        """
        db = SessionLocal()
        try:
            utilisateur = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()

            if not utilisateur:
                return False

            db.delete(utilisateur)
            db.commit()
            return True

        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la suppression : {e}")
            return False
        finally:
            db.close()

    @staticmethod
    def exists_by_pseudo(pseudo: str) -> bool:
        """
        Vérifie si un pseudo existe déjà

        Args:
            pseudo: Pseudo à vérifier

        Returns:
            True si existe, False sinon
        """
        db = SessionLocal()
        try:
            return db.query(Utilisateur).filter(Utilisateur.pseudo == pseudo).first() is not None
        finally:
            db.close()

    @staticmethod
    def exists_by_mail(mail: str) -> bool:
        """
        Vérifie si un email existe déjà

        Args:
            mail: Email à vérifier

        Returns:
            True si existe, False sinon
        """
        db = SessionLocal()
        try:
            return db.query(Utilisateur).filter(Utilisateur.mail == mail).first() is not None
        finally:
            db.close()

    @staticmethod
    def search_by_pseudo(pattern: str, limit: int = 10) -> List[Utilisateur]:
        """
        Recherche des utilisateurs par pseudo (recherche partielle)

        Args:
            pattern: Motif de recherche
            limit: Nombre maximum de résultats

        Returns:
            Liste d'utilisateurs correspondants
        """
        db = SessionLocal()
        try:
            return db.query(Utilisateur).filter(
                Utilisateur.pseudo.ilike(f"%{pattern}%")
            ).limit(limit).all()
        finally:
            db.close()

    @staticmethod
    def count_all() -> int:
        """
        Compte le nombre total d'utilisateurs

        Returns:
            Nombre d'utilisateurs
        """
        db = SessionLocal()
        try:
            return db.query(Utilisateur).count()
        finally:
            db.close()
