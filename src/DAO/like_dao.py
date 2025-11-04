"""
DAO (Data Access Object) pour la table de liaison Like
Gère toutes les opérations de base de données pour les likes
"""
from typing import List
from sqlalchemy import and_

from database import SessionLocal
from business_objects.models import Utilisateur, Activite, likes


class LikeDAO:
    """Classe DAO pour les opérations sur la table Like"""
    
    @staticmethod
    def create(utilisateur_id: int, activite_id: int) -> bool:
        """
        Crée un like sur une activité
        
        Args:
            utilisateur_id: ID de l'utilisateur qui like
            activite_id: ID de l'activité likée
            
        Returns:
            True si créé, False sinon
        """
        db = SessionLocal()
        try:
            # Vérifier si le like existe déjà
            existing = db.execute(
                likes.select().where(
                    and_(
                        likes.c.utilisateur_id == utilisateur_id,
                        likes.c.activite_id == activite_id
                    )
                )
            ).first()
            
            if existing:
                print("Le like existe déjà")
                return False
            
            # Créer le like
            db.execute(
                likes.insert().values(
                    utilisateur_id=utilisateur_id,
                    activite_id=activite_id
                )
            )
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la création du like : {e}")
            return False
        finally:
            db.close()
    
    @staticmethod
    def delete(utilisateur_id: int, activite_id: int) -> bool:
        """
        Supprime un like (unlike)
        
        Args:
            utilisateur_id: ID de l'utilisateur
            activite_id: ID de l'activité
            
        Returns:
            True si supprimé, False sinon
        """
        db = SessionLocal()
        try:
            result = db.execute(
                likes.delete().where(
                    and_(
                        likes.c.utilisateur_id == utilisateur_id,
                        likes.c.activite_id == activite_id
                    )
                )
            )
            db.commit()
            return result.rowcount > 0
            
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la suppression du like : {e}")
            return False
        finally:
            db.close()
    
    @staticmethod
    def exists(utilisateur_id: int, activite_id: int) -> bool:
        """
        Vérifie si un like existe
        
        Args:
            utilisateur_id: ID de l'utilisateur
            activite_id: ID de l'activité
            
        Returns:
            True si le like existe, False sinon
        """
        db = SessionLocal()
        try:
            result = db.execute(
                likes.select().where(
                    and_(
                        likes.c.utilisateur_id == utilisateur_id,
                        likes.c.activite_id == activite_id
                    )
                )
            ).first()
            
            return result is not None
        finally:
            db.close()
    
    @staticmethod
    def get_users_who_liked(activite_id: int) -> List[Utilisateur]:
        """
        Récupère la liste des utilisateurs qui ont liké une activité
        
        Args:
            activite_id: ID de l'activité
            
        Returns:
            Liste des utilisateurs qui ont liké
        """
        db = SessionLocal()
        try:
            activite = db.query(Activite).filter(Activite.id == activite_id).first()
            
            if not activite:
                return []
            
            return list(activite.likers)
        finally:
            db.close()
    
    @staticmethod
    def get_users_who_liked_ids(activite_id: int) -> List[int]:
        """
        Récupère la liste des IDs des utilisateurs qui ont liké
        
        Args:
            activite_id: ID de l'activité
            
        Returns:
            Liste des IDs des utilisateurs
        """
        db = SessionLocal()
        try:
            result = db.execute(
                likes.select().where(likes.c.activite_id == activite_id)
            ).fetchall()
            
            return [row.utilisateur_id for row in result]
        finally:
            db.close()
    
    @staticmethod
    def get_liked_activites_by_user(utilisateur_id: int) -> List[Activite]:
        """
        Récupère la liste des activités likées par un utilisateur
        
        Args:
            utilisateur_id: ID de l'utilisateur
            
        Returns:
            Liste des activités likées
        """
        db = SessionLocal()
        try:
            utilisateur = db.query(Utilisateur).filter(
                Utilisateur.id == utilisateur_id
            ).first()
            
            if not utilisateur:
                return []
            
            return list(utilisateur.liked_activites)
        finally:
            db.close()
    
    @staticmethod
    def get_liked_activites_ids_by_user(utilisateur_id: int) -> List[int]:
        """
        Récupère la liste des IDs des activités likées par un utilisateur
        
        Args:
            utilisateur_id: ID de l'utilisateur
            
        Returns:
            Liste des IDs des activités
        """
        db = SessionLocal()
        try:
            result = db.execute(
                likes.select().where(likes.c.utilisateur_id == utilisateur_id)
            ).fetchall()
            
            return [row.activite_id for row in result]
        finally:
            db.close()
    
    @staticmethod
    def count_by_activite(activite_id: int) -> int:
        """
        Compte le nombre de likes d'une activité
        
        Args:
            activite_id: ID de l'activité
            
        Returns:
            Nombre de likes
        """
        db = SessionLocal()
        try:
            result = db.execute(
                likes.select().where(likes.c.activite_id == activite_id)
            ).fetchall()
            
            return len(result)
        finally:
            db.close()
    
    @staticmethod
    def count_by_user(utilisateur_id: int) -> int:
        """
        Compte le nombre d'activités likées par un utilisateur
        
        Args:
            utilisateur_id: ID de l'utilisateur
            
        Returns:
            Nombre d'activités likées
        """
        db = SessionLocal()
        try:
            result = db.execute(
                likes.select().where(likes.c.utilisateur_id == utilisateur_id)
            ).fetchall()
            
            return len(result)
        finally:
            db.close()
    
    @staticmethod
    def delete_all_by_activite(activite_id: int) -> int:
        """
        Supprime tous les likes d'une activité
        (à utiliser lors de la suppression d'une activité)
        
        Args:
            activite_id: ID de l'activité
            
        Returns:
            Nombre de likes supprimés
        """
        db = SessionLocal()
        try:
            result = db.execute(
                likes.delete().where(likes.c.activite_id == activite_id)
            )
            db.commit()
            return result.rowcount
            
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la suppression : {e}")
            return 0
        finally:
            db.close()
    
    @staticmethod
    def delete_all_by_user(utilisateur_id: int) -> int:
        """
        Supprime tous les likes d'un utilisateur
        (à utiliser lors de la suppression d'un utilisateur)
        
        Args:
            utilisateur_id: ID de l'utilisateur
            
        Returns:
            Nombre de likes supprimés
        """
        db = SessionLocal()
        try:
            result = db.execute(
                likes.delete().where(likes.c.utilisateur_id == utilisateur_id)
            )
            db.commit()
            return result.rowcount
            
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la suppression : {e}")
            return 0
        finally:
            db.close()
    
    @staticmethod
    def toggle(utilisateur_id: int, activite_id: int) -> bool:
        """
        Toggle un like (like si pas liké, unlike si déjà liké)
        
        Args:
            utilisateur_id: ID de l'utilisateur
            activite_id: ID de l'activité
            
        Returns:
            True si maintenant liké, False si maintenant pas liké
        """
        if LikeDAO.exists(utilisateur_id, activite_id):
            LikeDAO.delete(utilisateur_id, activite_id)
            return False
        else:
            LikeDAO.create(utilisateur_id, activite_id)
            return True
    
    @staticmethod
    def user_has_liked(utilisateur_id: int, activite_id: int) -> bool:
        """
        Vérifie si un utilisateur a liké une activité
        (Alias de exists pour plus de clarté)
        
        Args:
            utilisateur_id: ID de l'utilisateur
            activite_id: ID de l'activité
            
        Returns:
            True si l'utilisateur a liké, False sinon
        """
        return LikeDAO.exists(utilisateur_id, activite_id)
    
    @staticmethod
    def get_most_liked_activites(limit: int = 10) -> List[tuple]:
        """
        Récupère les activités les plus likées
        
        Args:
            limit: Nombre maximum d'activités à retourner
            
        Returns:
            Liste de tuples (activite_id, nombre_likes)
        """
        db = SessionLocal()
        try:
            from sqlalchemy import func
            
            result = db.query(
                likes.c.activite_id,
                func.count(likes.c.utilisateur_id).label('nb_likes')
            ).group_by(
                likes.c.activite_id
            ).order_by(
                func.count(likes.c.utilisateur_id).desc()
            ).limit(limit).all()
            
            return [(row.activite_id, row.nb_likes) for row in result]
        finally:
            db.close()