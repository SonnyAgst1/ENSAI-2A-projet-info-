import datetime as dt

from utilisateur import Utilisateur
from commentaire import Commentaire


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
        like: set <id_utilisateur>,
        commentaire: list(Commentaire),
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
        self._id_activite = id_activite,
        self._utilisateur = utilisateur,
        self._nom = nom,
        self._type_sport = type_sport,
        self._dateActivite = dateActivite,
        self._dureeActivite = dureeActivite,
        self._description = description,
        self._fihiergpx = fichiergpx,
        self._like = like,
        self._commentaire = commentaire,
        self._denivelle = denivelle,
        self._calories = calories,

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
    def nom(self, nouveau_type):
        """Modifie le type de sport de l'activité"""
        if isinstance(nouveau_type, str) and nouveau_type.strip():
            self._type_sport = nouveau_type
        else:
            raise ValueError("Le type de sport de l'activité doit être une chaîne non vide")

    @dateActivite.setter
    def nom(self, nouvelle_date):
        """Modifie la date de l'activité"""
        if isinstance(nouvelle_date, dt.date) and nouvelle_date.strip():
            self._dateActivite = nouvelle_date
        else:
            raise ValueError("La dte de l'activité doit être une date")

    @dureeActivite.setter
    def nom(self, nouvelle_duree):
        """Modifie la durée de l'activité"""
        if isinstance(nouvelle_duree, dt.time) and nouvelle_duree.strip():
            self._dureeActivite = nouvelle_duree
        else:
            raise ValueError("La durée de l'activité doit être un temps")

    @description.setter
    def nom(self, nouvelle_description):
        """Modifie la description de l'activité"""
        if isinstance(nouvelle_description, str) and nouvelle_description.strip():
            self._description = nouvelle_description
        else:
            raise ValueError("La description de l'activité doit être une chaîne non vide")

    @fichiergpx.setter
    def nom(self, nouveau_gpx):
        """Modifie le fichier gpx"""
        if isinstance(nouveau_gpx, str) and nouveau_gpx.strip():
            self._fichiergpx = nouveau_gpx
        else:
            raise ValueError("Le fichier gpx doit être une chaîne non vide")

    @denivelle.setter
    def nom(self, nouveau_denivelle):
        """Modifie le denivellé"""
        if isinstance(nouveau_denivelle, int) and nouveau_denivelle.strip():
            self._denivelle = nouveau_denivelle
        else:
            raise ValueError("Le denivellé doit être un entier")

    @calories.setter
    def nom(self, nouvelle_calorie):
        """Modifie le nombre de calories dépensées"""
        if isinstance(nouvelle_calorie, int) and nouvelle_calorie.strip():
            self._calories = nouvelle_calorie
        else:
            raise ValueError("Le nombre de calories dépensées doit être un entier")

    # Méthodes métier
    def compte_like(self, like) -> int:
        """
        Compte le nombre de like d'une activité

        Args:
            like (set <id_utilisateur>): L'ensemble des utilisateurs qui ont like

        Returns:
            int: Le nombre de likes
        """
        nb_likes = len(self._like)
        return nb_likes

    def compte_commentaire(self, commentaire: str) -> int:
        """
        Compte le nombre de commentaires d'une activité

        Args:
            commentaire (str): un commentaire

        Returns:
            int: Le nombre de likes
        """
        nb_com = len(self._commentaire)
        return nb_com

    def getNombreLikes
