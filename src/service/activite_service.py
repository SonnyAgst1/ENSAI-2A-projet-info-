from typing import Optional, List, Dict
from datetime import date, datetime, time, timedelta
from sqlalchemy import and_, or_, func
from sqlalchemy.exc import IntegrityError
import gpxpy
import gpxpy.gpx

from database import SessionLocal
from business_objects.models import Utilisateur, Activite, Commentaire, likes


class ActiviteService:
    """Service pour gérer toutes les opérations liées aux activités"""

    @staticmethod
    def creer_activite_depuis_gpx(
        fichier_gpx: str,
        utilisateur_id: int,
        nom: str,
        type_sport: str,
        description: str = ""
    ) -> Optional[Activite]:
        """
        Crée une activité à partir d'un fichier GPX

        Args:
            fichier_gpx: Chemin vers le fichier GPX
            utilisateur_id: ID de l'utilisateur
            nom: Nom de l'activité
            type_sport: Type de sport (course, vélo, natation, etc.)
            description: Description optionnelle

        Returns:
            L'activité créée ou None en cas d'erreur
        """
        try:
            # Parser le fichier GPX
            with open(fichier_gpx, 'r') as gpx_file:
                gpx = gpxpy.parse(gpx_file)
        except FileNotFoundError:
            print(f"Le fichier GPX '{fichier_gpx}' n'existe pas")
            return None
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier GPX: {e}")
            return None

        # Vérifier qu'il y a des données
        if not gpx.tracks or not gpx.tracks[0].segments or not gpx.tracks[0].segments[0].points:
            print("Le fichier GPX ne contient pas de données de trace valides")
            return None

        # Extraire les points
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                points.extend(segment.points)

        if len(points) < 2:
            print("Le fichier GPX doit contenir au moins 2 points")
            return None

        # Calculer la date de l'activité
        date_activite = points[0].time.date() if points[0].time else date.today()

        # Calculer la durée
        if points[0].time and points[-1].time:
            duree_totale = points[-1].time - points[0].time
            duree_secondes = int(duree_totale.total_seconds())
        else:
            duree_secondes = 0

        # Calculer le dénivelé positif
        d_plus = 0
        for i in range(1, len(points)):
            if points[i].elevation and points[i-1].elevation:
                diff = points[i].elevation - points[i-1].elevation
                if diff > 0:
                    d_plus += diff
        d_plus = int(d_plus)

        # Calculer les calories
        duree_heures = duree_secondes / 3600 if duree_secondes > 0 else 0
        calories = ActiviteService._calculer_calories(type_sport, duree_heures, d_plus)

        # Lire le contenu du fichier GPX en bytes pour le stocker
        with open(fichier_gpx, 'rb') as f:
            fichier_gpx_bytes = f.read()

        # Créer l'activité en base
        db = SessionLocal()
        try:
            activite = Activite(
                nom=nom,
                type_sport=type_sport,
                date_activite=date_activite,
                duree_activite=duree_secondes,
                description=description,
                fichier_gpx=fichier_gpx_bytes,
                d_plus=d_plus,
                calories=calories,
                utilisateur_id=utilisateur_id
            )

            db.add(activite)
            db.commit()
            db.refresh(activite)
            return activite

        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la création de l'activité : {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def creer_activite_manuelle(
        utilisateur_id: int,
        nom: str,
        type_sport: str,
        date_activite: date,
        duree_activite: int,  # en secondes
        description: str = "",
        d_plus: int = 0,
        calories: int = 0
    ) -> Optional[Activite]:
        """
        Crée une activité manuellement (sans fichier GPX)

        Args:
            utilisateur_id: ID de l'utilisateur
            nom: Nom de l'activité
            type_sport: Type de sport
            date_activite: Date de l'activité
            duree_activite: Durée en secondes
            description: Description optionnelle
            d_plus: Dénivelé positif
            calories: Calories dépensées

        Returns:
            L'activité créée ou None en cas d'erreur
        """
        db = SessionLocal()
        try:
            activite = Activite(
                nom=nom,
                type_sport=type_sport,
                date_activite=date_activite,
                duree_activite=duree_activite,
                description=description,
                d_plus=d_plus,
                calories=calories,
                utilisateur_id=utilisateur_id
            )

            db.add(activite)
            db.commit()
            db.refresh(activite)
            return activite

        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la création de l'activité : {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def _calculer_calories(type_sport: str, duree_heures: float, denivelle: int) -> int:
        """
        Calcule approximativement les calories dépensées

        Args:
            type_sport: Type de sport
            duree_heures: Durée en heures
            denivelle: Dénivelé positif en mètres

        Returns:
            Estimation des calories dépensées
        """
        calories_par_heure = {
            "marche": 300,
            "course": 600,
            "vélo": 500,
            "velo": 500,
            "natation": 500,
            "randonnée": 400,
            "randonnee": 400
        }

        type_sport_lower = type_sport.lower()
        cal_base = calories_par_heure.get(type_sport_lower, 400)

        calories_totales = cal_base * duree_heures + (denivelle * 0.1)

        return int(calories_totales)

    @staticmethod
    def obtenir_activite_par_id(activite_id: int) -> Optional[Activite]:
        """Récupère une activité par son ID"""
        db = SessionLocal()
        try:
            return db.query(Activite).filter(Activite.id == activite_id).first()
        finally:
            db.close()

    @staticmethod
    def obtenir_activites_utilisateur(
        utilisateur_id: int,
        type_sport: Optional[str] = None,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None,
        limit: Optional[int] = None
    ) -> List[Activite]:
        """
        Récupère les activités d'un utilisateur avec filtres optionnels

        Args:
            utilisateur_id: ID de l'utilisateur
            type_sport: Filtrer par type de sport (optionnel)
            date_debut: Date de début (optionnel)
            date_fin: Date de fin (optionnel)
            limit: Nombre maximum d'activités à retourner (optionnel)

        Returns:
            Liste des activités correspondantes
        """
        db = SessionLocal()
        try:
            query = db.query(Activite).filter(Activite.utilisateur_id == utilisateur_id)

            # Appliquer les filtres
            if type_sport:
                query = query.filter(Activite.type_sport == type_sport)

            if date_debut:
                query = query.filter(Activite.date_activite >= date_debut)

            if date_fin:
                query = query.filter(Activite.date_activite <= date_fin)

            # Trier par date décroissante
            query = query.order_by(Activite.date_activite.desc())

            if limit:
                query = query.limit(limit)

            return query.all()

        finally:
            db.close()

    @staticmethod
    def modifier_activite(
        activite_id: int,
        **kwargs
    ) -> Optional[Activite]:
        """
        Modifie une activité

        Args:
            activite_id: ID de l'activité
            **kwargs: Champs à modifier

        Returns:
            L'activité modifiée ou None si non trouvée
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
            print(f"Erreur lors de la modification : {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def supprimer_activite(activite_id: int) -> bool:
        """
        Supprime une activité

        Args:
            activite_id: ID de l'activité à supprimer

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

# GESTION DES LIKES

    @staticmethod
    def liker_activite(utilisateur_id: int, activite_id: int) -> bool:
        """
        Like une activité

        Args:
            utilisateur_id: ID de l'utilisateur qui like
            activite_id: ID de l'activité

        Returns:
            True si le like est créé, False sinon
        """
        db = SessionLocal()
        try:
            # Vérifier que l'activité existe
            activite = db.query(Activite).filter(Activite.id == activite_id).first()
            if not activite:
                print("Activité non trouvée")
                return False

            # Vérifier que l'utilisateur existe
            utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
            if not utilisateur:
                print("Utilisateur non trouvé")
                return False

            # Vérifier si le like existe déjà
            existing = db.execute(
                likes.select().where(
                    likes.c.utilisateur_id == utilisateur_id,
                    likes.c.activite_id == activite_id
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
            print(f"Erreur lors du like : {e}")
            return False
        finally:
            db.close()

    @staticmethod
    def unliker_activite(utilisateur_id: int, activite_id: int) -> bool:
        """
        Retire le like d'une activité

        Args:
            utilisateur_id: ID de l'utilisateur
            activite_id: ID de l'activité

        Returns:
            True si le like est retiré, False sinon
        """
        db = SessionLocal()
        try:
            result = db.execute(
                likes.delete().where(
                    likes.c.utilisateur_id == utilisateur_id,
                    likes.c.activite_id == activite_id
                )
            )
            db.commit()
            return result.rowcount > 0

        except Exception as e:
            db.rollback()
            print(f"Erreur lors du unlike : {e}")
            return False
        finally:
            db.close()

    @staticmethod
    def obtenir_nombre_likes(activite_id: int) -> int:
        """Retourne le nombre de likes d'une activité"""
        db = SessionLocal()
        try:
            result = db.execute(
                likes.select().where(likes.c.activite_id == activite_id)
            ).fetchall()
            return len(result)
        finally:
            db.close()

    @staticmethod
    def utilisateur_a_like(utilisateur_id: int, activite_id: int) -> bool:
        """Vérifie si un utilisateur a liké une activité"""
        db = SessionLocal()
        try:
            result = db.execute(
                likes.select().where(
                    likes.c.utilisateur_id == utilisateur_id,
                    likes.c.activite_id == activite_id
                )
            ).first()
            return result is not None
        finally:
            db.close()

# GESTION DES COMMENTAIRES

    @staticmethod
    def ajouter_commentaire(
        utilisateur_id: int,
        activite_id: int,
        contenu: str
    ) -> Optional[Commentaire]:
        """
        Ajoute un commentaire sur une activité

        Args:
            utilisateur_id: ID de l'utilisateur qui commente
            activite_id: ID de l'activité
            contenu: Contenu du commentaire

        Returns:
            Le commentaire créé ou None en cas d'erreur
        """
        db = SessionLocal()
        try:
            # Vérifier que l'activité existe
            activite = db.query(Activite).filter(Activite.id == activite_id).first()
            if not activite:
                print("Activité non trouvée")
                return None

            # Vérifier que l'utilisateur existe
            utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
            if not utilisateur:
                print("Utilisateur non trouvé")
                return None

            commentaire = Commentaire(
                contenu=contenu,
                activite_id=activite_id,
                auteur_id=utilisateur_id
            )

            db.add(commentaire)
            db.commit()
            db.refresh(commentaire)
            return commentaire

        except Exception as e:
            db.rollback()
            print(f"Erreur lors de l'ajout du commentaire : {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def modifier_commentaire(commentaire_id: int, nouveau_contenu: str) -> Optional[Commentaire]:
        """
        Modifie un commentaire

        Args:
            commentaire_id: ID du commentaire
            nouveau_contenu: Nouveau contenu

        Returns:
            Le commentaire modifié ou None si non trouvé
        """
        db = SessionLocal()
        try:
            commentaire = db.query(Commentaire).filter(Commentaire.id == commentaire_id).first()

            if not commentaire:
                return None

            commentaire.contenu = nouveau_contenu
            db.commit()
            db.refresh(commentaire)
            return commentaire

        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la modification : {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def supprimer_commentaire(commentaire_id: int) -> bool:
        """
        Supprime un commentaire

        Args:
            commentaire_id: ID du commentaire

        Returns:
            True si supprimé, False sinon
        """
        db = SessionLocal()
        try:
            commentaire = db.query(Commentaire).filter(Commentaire.id == commentaire_id).first()

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
    def obtenir_commentaires_activite(activite_id: int) -> List[Commentaire]:
        """Récupère tous les commentaires d'une activité"""
        db = SessionLocal()
        try:
            return db.query(Commentaire).filter(
                Commentaire.activite_id == activite_id
            ).order_by(Commentaire.id.desc()).all()
        finally:
            db.close()

    @staticmethod
    def obtenir_nombre_commentaires(activite_id: int) -> int:
        """Retourne le nombre de commentaires d'une activité"""
        db = SessionLocal()
        try:
            return db.query(Commentaire).filter(Commentaire.activite_id == activite_id).count()
        finally:
            db.close()
