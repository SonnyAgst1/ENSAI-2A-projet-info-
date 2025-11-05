from typing import Optional, List
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError
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
        """
        Crée un nouveau utilisateur

        Args:
            nom: Nom de l'utilisateur
            prenom: Prénom de l'utilisateur
            age: Âge de l'utilisateur
            pseudo: Pseudo unique
            mail: Email unique
            mdp: Mot de passe (devrait être hashé en production)
            taille: Taille en cm (optionnel)
            poids: Poids en kg (optionnel)
            telephone: Numéro de téléphone (optionnel)
            photo_profil: Photo de profil en bytes (optionnel)

        Returns:
            L'utilisateur créé ou None en cas d'erreur
        """
        db = SessionLocal()
        try:
            # TODO: En production, hasher le mot de passe avec bcrypt
            # from bcrypt import hashpw, gensalt
            # mdp_hash = hashpw(mdp.encode('utf-8'), gensalt())

            utilisateur = Utilisateur(
                nom=nom,
                prenom=prenom,
                age=age,
                pseudo=pseudo,
                mail=mail,
                mdp=mdp,  # En prod: mdp_hash
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
            return db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
        finally:
            db.close()

    @staticmethod
    def obtenir_utilisateur_par_pseudo(pseudo: str) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son pseudo"""
        db = SessionLocal()
        try:
            return db.query(Utilisateur).filter(Utilisateur.pseudo == pseudo).first()
        finally:
            db.close()

    @staticmethod
    def obtenir_utilisateur_par_email(email: str) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son email"""
        db = SessionLocal()
        try:
            return db.query(Utilisateur).filter(Utilisateur.mail == email).first()
        finally:
            db.close()

    @staticmethod
    def obtenir_tous_utilisateurs() -> List[Utilisateur]:
        """Récupère tous les utilisateurs"""
        db = SessionLocal()
        try:
            return db.query(Utilisateur).all()
        finally:
            db.close()

    @staticmethod
    def modifier_utilisateur(
        user_id: int,
        **kwargs
    ) -> Optional[Utilisateur]:
        """
        Modifie les informations d'un utilisateur

        Args:
            user_id: ID de l'utilisateur
            **kwargs: Champs à modifier (nom, prenom, age, taille, poids, etc.)

        Returns:
            L'utilisateur modifié ou None si non trouvé
        """
        db = SessionLocal()
        try:
            utilisateur = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()

            if not utilisateur:
                return None

            # Mise à jour des champs fournis
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
        """
        Supprime un utilisateur

        Args:
            user_id: ID de l'utilisateur à supprimer

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
    def connexion(pseudo: str, mdp: str) -> Optional[Utilisateur]:
        """
        Authentifie un utilisateur

        Args:
            pseudo: Pseudo de l'utilisateur
            mdp: Mot de passe

        Returns:
            L'utilisateur si authentifié, None sinon
        """
        db = SessionLocal()
        try:
            utilisateur = db.query(Utilisateur).filter(
                Utilisateur.pseudo == pseudo
            ).first()

            if not utilisateur:
                return None

            # TODO: En production, vérifier avec bcrypt
            # from bcrypt import checkpw
            # if checkpw(mdp.encode('utf-8'), utilisateur.mdp):
            #     return utilisateur

            if utilisateur.mdp == mdp:
                return utilisateur

            return None

        finally:
            db.close()

    # ========== GESTION DES FOLLOWS ==========

    @staticmethod
    def suivre_utilisateur(follower_id: int, followed_id: int) -> bool:
        """
        Fait suivre un utilisateur par un autre

        Args:
            follower_id: ID de l'utilisateur qui suit
            followed_id: ID de l'utilisateur suivi

        Returns:
            True si le follow est créé, False sinon
        """
        if follower_id == followed_id:
            print("Un utilisateur ne peut pas se suivre lui-même")
            return False

        db = SessionLocal()
        try:
            follower = db.query(Utilisateur).filter(Utilisateur.id == follower_id).first()
            followed = db.query(Utilisateur).filter(Utilisateur.id == followed_id).first()

            if not follower or not followed:
                print("Utilisateur non trouvé")
                return False

            # Vérifier si le follow existe déjà
            existing = db.execute(
                follows.select().where(
                    follows.c.follower_id == follower_id,
                    follows.c.followed_id == followed_id
                )
            ).first()

            if existing:
                print("Le follow existe déjà")
                return False

            # Créer le follow
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
        """
        Arrête de suivre un utilisateur

        Args:
            follower_id: ID de l'utilisateur qui suit
            followed_id: ID de l'utilisateur suivi

        Returns:
            True si le unfollow est effectué, False sinon
        """
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
        """
        Récupère la liste des utilisateurs suivis par un utilisateur

        Args:
            user_id: ID de l'utilisateur

        Returns:
            Liste des utilisateurs suivis
        """
        db = SessionLocal()
        try:
            utilisateur = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
            if not utilisateur:
                return []

            return list(utilisateur.following)

        finally:
            db.close()

    @staticmethod
    def obtenir_followers(user_id: int) -> List[Utilisateur]:
        """
        Récupère la liste des followers d'un utilisateur

        Args:
            user_id: ID de l'utilisateur

        Returns:
            Liste des followers
        """
        db = SessionLocal()
        try:
            utilisateur = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
            if not utilisateur:
                return []

            return list(utilisateur.followers)

        finally:
            db.close()

    @staticmethod
    def est_suivi_par(user_id: int, follower_id: int) -> bool:
        """
        Vérifie si un utilisateur est suivi par un autre

        Args:
            user_id: ID de l'utilisateur potentiellement suivi
            follower_id: ID du follower potentiel

        Returns:
            True si user_id est suivi par follower_id
        """
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
            return db.query(Activite).filter(Activite.utilisateur_id == user_id).count()
        finally:
            db.close()

    @staticmethod
    def obtenir_nombre_followers(user_id: int) -> int:
        """Retourne le nombre de followers d'un utilisateur"""
        db = SessionLocal()
        try:
            result = db.execute(
                follows.select().where(follows.c.followed_id == user_id)
            ).fetchall()
            return len(result)
        finally:
            db.close()

    @staticmethod
    def obtenir_nombre_suivis(user_id: int) -> int:
        """Retourne le nombre d'utilisateurs suivis"""
        db = SessionLocal()
        try:
            result = db.execute(
                follows.select().where(follows.c.follower_id == user_id)
            ).fetchall()
            return len(result)
        finally:
            db.close()
