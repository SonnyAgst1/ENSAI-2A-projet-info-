from typing import Optional, List
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select # Ajout pour l'API moderne
from database import SessionLocal
from business_objects.models import Utilisateur, Activite, Commentaire, follows


class UtilisateurService:
    """Service pour gérer toutes les opérations liées aux utilisateurs"""

    @staticmethod
    def creer_utilisateur(
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
        # ... (Logique de création)
        db = SessionLocal()
        try:
            utilisateur = Utilisateur(
                nom=nom, prenom=prenom, age=age, pseudo=pseudo, mail=mail, mdp=mdp,
                taille=taille, poids=poids, telephone=telephone, photo_profil=photo_profil
            )
            db.add(utilisateur)
            db.commit()
            db.refresh(utilisateur)
            return utilisateur
        except IntegrityError as e:
            db.rollback()
            print(f"Erreur : pseudo ou email déjà existant - {e}")
            return None
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la création de l'utilisateur : {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def obtenir_utilisateur_par_id(user_id: int) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son ID"""
        db = SessionLocal()
        try:
            statement = select(Utilisateur).where(Utilisateur.id == user_id)
            return db.execute(statement).scalars().first()
        finally:
            db.close()

    @staticmethod
    def obtenir_utilisateur_par_pseudo(pseudo: str) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son pseudo"""
        db = SessionLocal()
        try:
            statement = select(Utilisateur).where(Utilisateur.pseudo == pseudo)
            return db.execute(statement).scalars().first()
        finally:
            db.close()

    @staticmethod
    def obtenir_utilisateur_par_email(email: str) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son email"""
        db = SessionLocal()
        try:
            statement = select(Utilisateur).where(Utilisateur.mail == email)
            return db.execute(statement).scalars().first()
        finally:
            db.close()

    @staticmethod
    def obtenir_tous_utilisateurs() -> List[Utilisateur]:
        """Récupère tous les utilisateurs"""
        db = SessionLocal()
        try:
            statement = select(Utilisateur)
            return db.execute(statement).scalars().all()
        finally:
            db.close()

    @staticmethod
    def modifier_utilisateur(user_id: int, **kwargs) -> Optional[Utilisateur]:
        """Modifie les informations d'un utilisateur"""
        db = SessionLocal()
        try:
            statement = select(Utilisateur).where(Utilisateur.id == user_id)
            utilisateur = db.execute(statement).scalars().first()

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
            print(f"Erreur : contrainte d'unicité violée - {e}")
            return None
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la modification : {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def supprimer_utilisateur(user_id: int) -> bool:
        """Supprime un utilisateur"""
        db = SessionLocal()
        try:
            statement = select(Utilisateur).where(Utilisateur.id == user_id)
            utilisateur = db.execute(statement).scalars().first()

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
    def connexion(pseudo: str, mdp: str) -> Optional[Utilisateur]:
        """Authentifie un utilisateur"""
        db = SessionLocal()
        try:
            statement = select(Utilisateur).where(Utilisateur.pseudo == pseudo)
            utilisateur = db.execute(statement).scalars().first()

            if not utilisateur:
                return None

            if utilisateur.mdp == mdp:
                return utilisateur

            return None
        finally:
            db.close()

    # ========== GESTION DES FOLLOWS ==========

    @staticmethod
    def suivre_utilisateur(follower_id: int, followed_id: int) -> bool:
        """Fait suivre un utilisateur par un autre"""
        if follower_id == followed_id:
            print("Un utilisateur ne peut pas se suivre lui-même")
            return False

        db = SessionLocal()
        try:
            follower_stmt = select(Utilisateur).where(Utilisateur.id == follower_id)
            followed_stmt = select(Utilisateur).where(Utilisateur.id == followed_id)

            follower = db.execute(follower_stmt).scalars().first()
            followed = db.execute(followed_stmt).scalars().first()

            if not follower or not followed:
                print("Utilisateur non trouvé")
                return False

            existing = db.execute(
                follows.select().where(
                    follows.c.follower_id == follower_id,
                    follows.c.followed_id == followed_id
                )
            ).first()

            if existing:
                print("Le follow existe déjà")
                return False

            db.execute(
                follows.insert().values(
                    follower_id=follower_id,
                    followed_id=followed_id
                )
            )
            db.commit()
            return True

        except Exception as e:
            db.rollback()
            print(f"Erreur lors du follow : {e}")
            return False
        finally:
            db.close()

    @staticmethod
    def ne_plus_suivre_utilisateur(follower_id: int, followed_id: int) -> bool:
        """Arrête de suivre un utilisateur"""
        db = SessionLocal()
        try:
            result = db.execute(
                follows.delete().where(
                    follows.c.follower_id == follower_id,
                    follows.c.followed_id == followed_id
                )
            )
            db.commit()
            return result.rowcount > 0

        except Exception as e:
            db.rollback()
            print(f"Erreur lors du unfollow : {e}")
            return False
        finally:
            db.close()

    @staticmethod
    def obtenir_utilisateurs_suivis(user_id: int) -> List[Utilisateur]:
        """Récupère la liste des utilisateurs suivis par un utilisateur"""
        db = SessionLocal()
        try:
            statement = select(Utilisateur).where(Utilisateur.id == user_id)
            utilisateur = db.execute(statement).scalars().first()
            
            if not utilisateur:
                return []

            return list(utilisateur.following)

        finally:
            db.close()

    @staticmethod
    def obtenir_followers(user_id: int) -> List[Utilisateur]:
        """Récupère la liste des followers d'un utilisateur"""
        db = SessionLocal()
        try:
            statement = select(Utilisateur).where(Utilisateur.id == user_id)
            utilisateur = db.execute(statement).scalars().first()
            
            if not utilisateur:
                return []

            return list(utilisateur.followers)

        finally:
            db.close()

    @staticmethod
    def est_suivi_par(user_id: int, follower_id: int) -> bool:
        """Vérifie si un utilisateur est suivi par un autre"""
        db = SessionLocal()
        try:
            result = db.execute(
                follows.select().where(
                    follows.c.follower_id == follower_id,
                    follows.c.followed_id == user_id
                )
            ).first()

            return result is not None

        finally:
            db.close()

    # ========== STATISTIQUES UTILISATEUR ==========

    @staticmethod
    def obtenir_nombre_activites(user_id: int) -> int:
        """Retourne le nombre total d'activités d'un utilisateur"""
        db = SessionLocal()
        try:
            # Utilisation de la fonction count() pour compter
            from sqlalchemy.sql import func
            count_stmt = select(func.count(Activite.id)).where(Activite.utilisateur_id == user_id)
            return db.execute(count_stmt).scalar_one()
        finally:
            db.close()

    @staticmethod
    def obtenir_nombre_followers(user_id: int) -> int:
        """Retourne le nombre de followers d'un utilisateur"""
        db = SessionLocal()
        try:
            from sqlalchemy.sql import func
            count_stmt = select(func.count()).select_from(follows).where(follows.c.followed_id == user_id)
            return db.execute(count_stmt).scalar_one()
        finally:
            db.close()

    @staticmethod
    def obtenir_nombre_suivis(user_id: int) -> int:
        """Retourne le nombre d'utilisateurs suivis"""
        db = SessionLocal()
        try:
            from sqlalchemy.sql import func
            count_stmt = select(func.count()).select_from(follows).where(follows.c.follower_id == user_id)
            return db.execute(count_stmt).scalar_one()
        finally:
            db.close()