import datetime as dt
import gpxpy
from typing import List

from business_objects.utilisateur import Utilisateur
from business_objects.commentaire import Commentaire


class Activité:
    """
    Classe représentant une activité
    """

    def __init__(
        self,
        id_activite: int,
        utilisateur: Utilisateur,
        nom: str,
        type_sport: str,
        dateActivite: dt.date,
        dureeActivite: dt.time,
        description: str,
        fichiergpx: str,
        like: list,
        commentaire: list,
        denivelle: int,
        calories: int
    ):
        """
        Initialise une activité

        Args:
            id_activite (int): Identifiant unique de l'activité
            utilisateur (Utilisateur): L'utilisateur qui fait l'activité
            nom (str): Le nom de l'activité
            type_sport (str): Le type de sport qu'est l'activité
            dateActivite (date): La date à laquelle a été réalisée l'activité
            dureeActivite (time): Combien de temps a duré l'activité
            description (str): La description de l'activité
            fichiergpx (str): Le fichier gpx de l'activité
            like (set <id_utilisateur>): Quels utilisateurs ont mis un like à l'activité
            commentaire (str): Les commentaires sous l'activité
            denivelle (int): le dénivellé réalisé lors de l'activité
            calories (int): le nombre de calories dépensées lors de l'activité
        """
        self._id_activite = id_activite
        self._utilisateur = utilisateur
        self._nom = nom
        self._type_sport = type_sport
        self._dateActivite = dateActivite
        self._dureeActivite = dureeActivite
        self._description = description
        self._fichiergpx = fichiergpx
        self._like = like
        self._commentaire = commentaire
        self._denivelle = denivelle
        self._calories = calories

    # Getters
    @property
    def id(self):
        """Retourne l'identifiant de l'activité"""
        return self._id_activite

    @property
    def utilisateur(self):
        """Retourne l'utilisateur qui a fait l'activité"""
        return self._utilisateur

    @property
    def nom(self):
        """Retourne le nom de l'activité"""
        return self._nom

    @property
    def type_sport(self):
        """Retourne le type du sport de l'activité"""
        return self._type_sport

    @property
    def dateActivite(self):
        """Retourne la date de l'activité"""
        return self._dateActivite

    @property
    def dureeActivite(self):
        """Retourne la durée de l'activité"""
        return self._dureeActivite

    @property
    def description(self):
        """Retourne la description de l'activité"""
        return self._description

    @property
    def fichiergpx(self):
        """Retourne le fichier gpx de l'activité"""
        return self._fichiergpx

    @property
    def like(self):
        """Retourne les likes de l'activité"""
        return self._like

    @property
    def commentaire(self):
        """Retourne les commentaires de l'activité"""
        return self._commentaire

    @property
    def denivelle(self):
        """Retourne le dénivellé réalisé lors de l'ctivité"""
        return self._denivelle

    @property
    def calories(self):
        """Retourne les calories dépensées lors de l'activité"""
        return self._calories

    # Setters
    @nom.setter
    def nom(self, nouveau_nom):
        """Modifie le nom de l'activité"""
        if isinstance(nouveau_nom, str) and nouveau_nom.strip():
            self._nom = nouveau_nom
        else:
            raise ValueError("Le nom de l'activité doit être une chaîne non vide")

    @type_sport.setter
    def type_sport(self, nouveau_type):
        """Modifie le type de sport de l'activité"""
        if isinstance(nouveau_type, str) and nouveau_type.strip():
            self._type_sport = nouveau_type
        else:
            raise ValueError("Le type de sport de l'activité doit être une chaîne non vide")

    @dateActivite.setter
    def dateActivite(self, nouvelle_date):
        """Modifie la date de l'activité"""
        if isinstance(nouvelle_date, dt.date):
            self._dateActivite = nouvelle_date
        else:
            raise ValueError("La date de l'activité doit être une date")

    @dureeActivite.setter
    def dureeActivite(self, nouvelle_duree):
        """Modifie la durée de l'activité"""
        if isinstance(nouvelle_duree, dt.time):
            self._dureeActivite = nouvelle_duree
        else:
            raise ValueError("La durée de l'activité doit être un temps")

    @description.setter
    def description(self, nouvelle_description):
        """Modifie la description de l'activité"""
        if isinstance(nouvelle_description, str) and nouvelle_description.strip():
            self._description = nouvelle_description
        else:
            raise ValueError("La description de l'activité doit être une chaîne non vide")

    @fichiergpx.setter
    def fichiergpx(self, nouveau_gpx):
        """Modifie le fichier gpx"""
        if isinstance(nouveau_gpx, str) and nouveau_gpx.strip():
            self._fichiergpx = nouveau_gpx
        else:
            raise ValueError("Le fichier gpx doit être une chaîne non vide")

    @denivelle.setter
    def denivelle(self, nouveau_denivelle):
        """Modifie le denivellé"""
        if isinstance(nouveau_denivelle, int) and nouveau_denivelle >= 0:
            self._denivelle = nouveau_denivelle
        else:
            raise ValueError("Le denivellé doit être un entier")

    @calories.setter
    def calories(self, nouvelle_calorie):
        """Modifie le nombre de calories dépensées"""
        if isinstance(nouvelle_calorie, int) and nouvelle_calorie.strip():
            self._calories = nouvelle_calorie
        else:
            raise ValueError("Le nombre de calories dépensées doit être un entier")

    # Méthodes métier
    def compte_like(self) -> int:
        """
        Compte le nombre de likes d'une activité

        Returns:
        int: Le nombre de likes
        """
        return len(self._like)

    def compte_commentaire(self) -> int:
        """
        Compte le nombre de commentaires d'une activité

        Returns:
        int: Le nombre de commentaires
        """
        return len(self._commentaire)

    def getNombreLike(self) -> int:
        """
        Retourne le nombre de likes de l'activité

        Returns:
        int: Le nombre de likes
        """
        return len(self._like)

    def getNombreCommentaire(self) -> int:
        """
        Retourne le nombre de commentaires de l'activité

        Returns:
        int: Le nombre de commentaires
        """
        return len(self._commentaire)

    def calculer_vitesse(self, distance: float) -> float:
        """
        Calcule la vitesse selon le type de sport

        Args:
            distance (float): La distance parcourue (en km pour vélo et marche, en m pour natation)

        Returns:
            float: La vitesse calculée selon le type de sport
                - Natation: min/100m
                - Vélo: km/h
                - Marche: min/km
        """
        duree_minutes = (
            self._dureeActivite.hour * 60
            + self._dureeActivite.minute
            + self._dureeActivite.second / 60
        )
        if duree_minutes == 0:
            raise ValueError("La durée de l'activité doit être supérieure à 0")
        type_sport_lower = self._type_sport.lower()
        if type_sport_lower == "natation":
            return (duree_minutes/distance)*100
        elif type_sport_lower == "vélo" or type_sport_lower == "velo":
            duree_heures = duree_minutes/60
            return distance/duree_heures
        elif type_sport_lower == "marche":
            return duree_minutes/distance

    @staticmethod
    def calculer_calories(type_sport: str, duree_heures: float, denivelle: int) -> int:
        """
        Calcule approximativement les calories dépensées

        Args:
            type_sport (str): Type de sport
            duree_heures (float): Durée en heures
            denivelle (int): Dénivelé positif en mètres

        Returns:
            int: Estimation des calories dépensées
        """
        # Calories de base par heure selon le sport (valeurs moyennes)
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

        # Calories totales = calories de base + bonus pour le dénivelé
        calories_totales = cal_base*duree_heures + (denivelle*0.1)

        return int(calories_totales)

    @classmethod
    def creerActivite(
        cls,
        fichier_gpx: str,
        id_activite: int,
        utilisateur: Utilisateur,
        nom: str,
        type_sport: str,
        description: str = ""
    ):
        """
        Crée une activité à partir d'un fichier GPX

        Args:
            fichier_gpx (str): Chemin vers le fichier GPX
            id_activite (int): Identifiant unique de l'activité
            utilisateur (Utilisateur): L'utilisateur qui a réalisé l'activité
            nom (str): Nom de l'activité
            type_sport (str): Type de sport (natation, vélo, marche, etc.)
            description (str): Description optionnelle de l'activité

        Returns:
            Activité: Une nouvelle instance d'Activité avec les données extraites du GPX
        """

        try:
            with open(fichier_gpx, 'r') as gpx_file:
                gpx = gpxpy.parse(gpx_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Le fichier GPX '{fichier_gpx}' n'existe pas")
        except Exception as e:
            raise ValueError(f"Erreur lors de la lecture du fichier GPX: {e}")

        # Vérifier qu'il y a des données dans le GPX
        if not gpx.tracks or not gpx.tracks[0].segments or not gpx.tracks[0].segments[0].points:
            raise ValueError("Le fichier GPX ne contient pas de données de trace valides")

        # Extraire les points de trace
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                points.extend(segment.points)

        if len(points) < 2:
            raise ValueError("Le fichier GPX doit contenir au moins 2 points")

        # Calculer la date de l'activité (premier point)
        date_activite = points[0].time.date() if points[0].time else dt.date.today()

        # Calculer la durée de l'activité
        if points[0].time and points[-1].time:
            duree_totale = points[-1].time - points[0].time
            heures = duree_totale.seconds // 3600
            minutes = (duree_totale.seconds % 3600) // 60
            secondes = duree_totale.seconds % 60
            duree_activite = dt.time(heures, minutes, secondes)
        else:
            duree_activite = dt.time(0, 0, 0)

        # Calculer le dénivelé positif
        denivelle = 0
        for i in range(1, len(points)):
            if points[i].elevation and points[i-1].elevation:
                diff = points[i].elevation - points[i-1].elevation
                if diff > 0:
                    denivelle += diff
        denivelle = int(denivelle)

        # Calculer les calories
        duree_heures = duree_totale.seconds / 3600 if points[0].time and points[-1].time else 0
        calories = cls.calculer_calories(type_sport, duree_heures, denivelle)

        # Créer l'activité avec cls au lieu de Activité
        return cls(
            id_activite=id_activite,
            utilisateur=utilisateur,
            nom=nom,
            type_sport=type_sport,
            dateActivite=date_activite,
            dureeActivite=duree_activite,
            description=description,
            fichiergpx=fichier_gpx,
            like=[],
            commentaire=[],
            denivelle=denivelle,
            calories=calories
        )
