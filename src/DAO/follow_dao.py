"""
DAO (Data Access Object) pour la table de liaison Follow
Gère toutes les opérations de base de données pour les relations de suivi
"""
from typing import List
from sqlalchemy import and_

from database import SessionLocal
from business_objects.models import Utilisateur, follows


class FollowDAO:
    """Classe DAO pour les opérations sur la table Follow"""
    
    @staticmethod
    def create(follower_id: int, followed_id: int) -> bool:
        """
        Crée une relation de suivi (follow)
        
        Args:
            follower_id: ID de l'utilisateur qui suit
            followed_id: ID de l'utilisateur suivi
            
        Returns:
            True si créé, False sinon
        """
        if follower_id == followed_id:
            print("Un utilisateur ne peut pas se suivre lui-même")
            return False
        
        db = SessionLocal()
        try:
            # Vérifier si la relation existe déjà
            existing = db.execute(
                follows.select().where(
                    and_(
                        follows.c.follower_id == follower_id,
                        follows.c.followed_id == followed_id
                    )
                )
            ).first()
            
            if existing:
                print("La relation de suivi existe déjà")
                return False
            
            # Créer la relation
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
            print(f"Erreur lors de la création du follow : {e}")
            return False
        finally:
            db.close()
    
    @staticmethod
    def delete(follower_id: int, followed_id: int) -> bool:
        """
        Supprime une relation de suivi (unfollow)
        
        Args:
            follower_id: ID de l'utilisateur qui suit
            followed_id: ID de l'utilisateur suivi
            
        Returns:
            True si supprimé, False sinon
        """
        db = SessionLocal()
        try:
            result = db.execute(
                follows.delete().where(
                    and_(
                        follows.c.follower_id == follower_id,
                        follows.c.followed_id == followed_id
                    )
                )
            )
            db.commit()
            return result.rowcount > 0
            
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la suppression du follow : {e}")
            return False
        finally:
            db.close()
    
    @staticmethod
    def exists(follower_id: int, followed_id: int) -> bool:
        """
        Vérifie si une relation de suivi existe
        
        Args:
            follower_id: ID de l'utilisateur qui suit
            followed_id: ID de l'utilisateur suivi
            
        Returns:
            True si la relation existe, False sinon
        """
        db = SessionLocal()
        try:
            result = db.execute(
                follows.select().where(
                    and_(
                        follows.c.follower_id == follower_id,
                        follows.c.followed_id == followed_id
                    )
                )
            ).first()
            
            return result is not None
        finally:
            db.close()
    
    @staticmethod
    def get_following(user_id: int) -> List[Utilisateur]:
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
    def get_following_ids(user_id: int) -> List[int]:
        """
        Récupère la liste des IDs des utilisateurs suivis
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Liste des IDs des utilisateurs suivis
        """
        db = SessionLocal()
        try:
            result = db.execute(
                follows.select().where(follows.c.follower_id == user_id)
            ).fetchall()
            
            return [row.followed_id for row in result]
        finally:
            db.close()
    
    @staticmethod
    def get_followers(user_id: int) -> List[Utilisateur]:
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
    def get_followers_ids(user_id: int) -> List[int]:
        """
        Récupère la liste des IDs des followers
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Liste des IDs des followers
        """
        db = SessionLocal()
        try:
            result = db.execute(
                follows.select().where(follows.c.followed_id == user_id)
            ).fetchall()
            
            return [row.follower_id for row in result]
        finally:
            db.close()
    
    @staticmethod
    def count_following(user_id: int) -> int:
        """
        Compte le nombre d'utilisateurs suivis
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Nombre d'utilisateurs suivis
        """
        db = SessionLocal()
        try:
            result = db.execute(
                follows.select().where(follows.c.follower_id == user_id)
            ).fetchall()
            
            return len(result)
        finally:
            db.close()
    
    @staticmethod
    def count_followers(user_id: int) -> int:
        """
        Compte le nombre de followers
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Nombre de followers
        """
        db = SessionLocal()
        try:
            result = db.execute(
                follows.select().where(follows.c.followed_id == user_id)
            ).fetchall()
            
            return len(result)
        finally:
            db.close()
    
    @staticmethod
    def delete_all_by_user(user_id: int) -> int:
        """
        Supprime toutes les relations de suivi impliquant un utilisateur
        (à utiliser lors de la suppression d'un utilisateur)
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Nombre de relations supprimées
        """
        db = SessionLocal()
        try:
            # Supprimer où l'utilisateur est follower
            result1 = db.execute(
                follows.delete().where(follows.c.follower_id == user_id)
            )
            
            # Supprimer où l'utilisateur est suivi
            result2 = db.execute(
                follows.delete().where(follows.c.followed_id == user_id)
            )
            
            db.commit()
            return result1.rowcount + result2.rowcount
            
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la suppression : {e}")
            return 0
        finally:
            db.close()
    
    @staticmethod
    def get_mutual_follows(user_id: int) -> List[Utilisateur]:
        """
        Récupère les utilisateurs avec lesquels il y a un suivi mutuel
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Liste des utilisateurs avec suivi mutuel
        """
        db = SessionLocal()
        try:
            # Récupérer les IDs suivis
            following_ids = FollowDAO.get_following_ids(user_id)
            
            # Parmi ceux-ci, lesquels suivent aussi l'utilisateur
            mutual_ids = []
            for followed_id in following_ids:
                if FollowDAO.exists(followed_id, user_id):
                    mutual_ids.append(followed_id)
            
            # Récupérer les objets Utilisateur
            if not mutual_ids:
                return []
            
            return db.query(Utilisateur).filter(
                Utilisateur.id.in_(mutual_ids)
            ).all()
        finally:
            db.close()
    
    @staticmethod
    def is_following(follower_id: int, followed_id: int) -> bool:
        """
        Vérifie si follower_id suit followed_id
        (Alias de exists pour plus de clarté)
        
        Args:
            follower_id: ID de l'utilisateur qui suit
            followed_id: ID de l'utilisateur potentiellement suivi
            
        Returns:
            True si la relation existe, False sinon
        """
        return FollowDAO.exists(follower_id, followed_id)