from datetime import date, datetime
import hashlib


class Utilisateur:
    """ Classe représentant un utilisateur
    """
    def __init__(
        self,
        id_utilisateur,
        pseudo,
        nom,
        prenom,
        date_de_naissance,
        taille,
        poids,
        mail,
        telephone,
        mdp,
        liste_activites
    ):
        """ Initialise un utilisateur

        Args:
        id_utilisateur (int) : Identifiant unique de l'utilisateur
        pseudo (str) : pseudo de l'utilisateur
        nom (str) : nom de l'utilisateur
        prenom (str) : prenom de l'utilisateur
        date_de_naissance (date) : date de naissance de l'utilisateur
        taille (int) : taille de l'utilisateur
        poids (int) : poids de l'utilisateur
        mail (str) : mail de l'utilisateur
        telephone (int) : telephone de l'utilisateur
        mdp (str) : mot de passe de l'utilisateur
        liste_activite (list<Activite>) : liste d'activités de l'utilisateur
        """
        self._id_utilisateur = id_utilisateur
        self._pseudo = pseudo
        self._nom = nom
        self._prenom = prenom
        self._date_de_naissance = date_de_naissance
        self._taille = taille
        self._poids = poids
        self._mail = mail
        self._telephone = telephone
        self._mdp = mdp
        self._liste_activites = liste_activites if liste_activites is not None else []

    # Getters
    @property
    def id_utilisateur(self):
        """Retourne l'identifiant de l'utilisateur"""
        return self._id_utilisateur

    @property
    def pseudo(self):
        """Retourne le pseudo de l'utilisateur"""
        return self._pseudo

    @property
    def nom(self):
        """Retourne le nom de l'utilisateur"""
        return self._nom

    @property
    def prenom(self):
        """Retourne le prénom de l'utilisateur"""
        return self._prenom

    @property
    def age(self):
        """Calcule et retourne l'âge de l'utilisateur"""
        today = date.today()
        age = today.year - self._date_de_naissance.year
        if (today.month, today.day) < (self._date_de_naissance.month, self._date_de_naissance.day):
            age -= 1
        return age

    @property
    def taille(self):
        """Retourne la taille de l'utilisateur"""
        return self._taille

    @property
    def poids(self):
        """Retourne le poids de l'utilisateur"""
        return self._poids

    @property
    def mail(self):
        """Retourne le mail de l'utilisateur"""
        return self._mail

    @property
    def telephone(self):
        """Retourne le téléphone de l'utilisateur"""
        return self._telephone

    @property
    def liste_activites(self):
        """Retourne une copie de la liste d'activités"""
        return self._liste_activites.copy()

    # Setters
    @pseudo.setter
    def pseudo(self, nouveau_pseudo):
        """Modifie le pseudo de l'utilisateur"""
        if isinstance(nouveau_pseudo, str) and nouveau_pseudo.strip():
            self._pseudo = nouveau_pseudo
        else:
            raise ValueError("Le pseudo doit être une chaîne non vide")

    @taille.setter
    def taille(self, nouvelle_taille):
        """Modifie la taille de l'utilisateur"""
        if isinstance(nouvelle_taille, (int, float)) and nouvelle_taille > 0:
            self._taille = nouvelle_taille
        else:
            raise ValueError("La taille doit être un nombre positif")

    @poids.setter
    def poids(self, nouveau_poids):
        """Modifie le poids de l'utilisateur"""
        if isinstance(nouveau_poids, (int, float)) and nouveau_poids > 0:
            self._poids = nouveau_poids
        else:
            raise ValueError("Le poids doit être un nombre positif")

    @mail.setter
    def mail(self, nouveau_mail):
        """Modifie le mail de l'utilisateur"""
        if isinstance(nouveau_mail, str) and '@' in nouveau_mail:
            self._mail = nouveau_mail
        else:
            raise ValueError("Le mail doit être valide")

    @telephone.setter
    def telephone(self, nouveau_telephone):
        """Modifie le téléphone de l'utilisateur"""
        if isinstance(nouveau_telephone, (int, str)):
            self._telephone = nouveau_telephone
        else:
            raise ValueError("Le téléphone doit être un nombre ou une chaîne")

    # Méthodes liées à l'authentification
    def connexion(self, pseudo, mdp):
        """
        Vérifie les identifiants de connexion

        Args:
            pseudo (str): Le pseudo de l'utilisateur
            mdp (str): Le mot de passe à vérifier

        Returns:
            bool: True si les identifiants sont corrects, False sinon
        """
        return self._pseudo == pseudo and self._mdp == mdp

    def deconnexion(self):
        """
        Déconnecte l'utilisateur

        Returns:
            None
        """
        # Dans une vraie application, cela supprimerait la session
        pass

    # Méthodes liées aux follows (utilisant la classe Service)
    def follow_utilisateur(self, id_utilisateur, service):
        """
        Suit un autre utilisateur via la classe Service

        Args:
            id_utilisateur (int): L'identifiant de l'utilisateur à suivre
            service (Service): Instance de la classe Service pour gérer les follows

        Returns:
            bool: True si l'utilisateur a été ajouté, False s'il était déjà suivi
        """
        if id_utilisateur != self._id_utilisateur and hasattr(service, 'ajouter_follow'):
            return service.ajouter_follow(self._id_utilisateur, id_utilisateur)
        return False

    def unfollow_utilisateur(self, id_utilisateur, service):
        """
        Arrête de suivre un utilisateur via la classe Service

        Args:
            id_utilisateur (int): L'identifiant de l'utilisateur à ne plus suivre
            service (Service): Instance de la classe Service pour gérer les follows

        Returns:
            bool: True si l'utilisateur a été retiré, False s'il n'était pas suivi
        """
        if hasattr(service, 'supprimer_follow'):
            return service.supprimer_follow(self._id_utilisateur, id_utilisateur)
        return False

    def get_following(self, service):
        """
        Récupère la liste des utilisateurs suivis via la classe Service

        Args:
            service (Service): Instance de la classe Service pour gérer les follows

        Returns:
            list: Liste des IDs des utilisateurs suivis
        """
        if hasattr(service, 'get_following'):
            return service.get_following(self._id_utilisateur)
        return []

    def get_followers(self, service):
        """
        Récupère la liste des followers via la classe Service

        Args:
            service (Service): Instance de la classe Service pour gérer les follows

        Returns:
            list: Liste des IDs des utilisateurs qui suivent cet utilisateur
        """
        if hasattr(service, 'get_followers'):
            return service.get_followers(self._id_utilisateur)
        return []

    # Méthodes liées aux activités
    def ajouter_like(self, activite):
        """
        Ajoute un like à une activité

        Args:
            activite (Activite): L'activité à liker

        Returns:
            None
        """
        if hasattr(activite, 'ajouter_like_utilisateur'):
            activite.ajouter_like_utilisateur(self)

    def supprimer_like(self, activite):
        """
        Retire le like d'une activité

        Args:
            activite (Activite): L'activité à unliker

        Returns:
            None
        """
        if hasattr(activite, 'supprimer_like_utilisateur'):
            activite.supprimer_like_utilisateur(self)

    def ajouter_commentaire(self, activite, commentaire_str):
        """
        Ajoute un commentaire sur une activité

        Args:
            activite (Activite): L'activité à commenter
            commentaire_str (str): Le contenu du commentaire

        Returns:
            None
        """
        if hasattr(activite, 'ajouter_commentaire'):
            activite.ajouter_commentaire(self, commentaire_str)

    def supprimer_commentaire(self, activite, commentaire):
        """
        Supprime un commentaire sur une activité

        Args:
            activite (Activite): L'activité concernée
            commentaire (Commentaire): Le commentaire à supprimer

        Returns:
            None
        """
        if hasattr(activite, 'supprimer_commentaire'):
            activite.supprimer_commentaire(commentaire)

    def modifier_activite(self, activite):
        """
        Modifie une activité de l'utilisateur

        Args:
            activite (Activite): L'activité à modifier

        Returns:
            None
        """
        if activite in self._liste_activites:
            # La modification se fait directement sur l'objet activité
            pass

    def supprimer_activite(self, activite):
        """
        Supprime une activité de la liste de l'utilisateur

        Args:
            activite (Activite): L'activité à supprimer

        Returns:
            bool: True si l'activité a été supprimée, False sinon
        """
        if activite in self._liste_activites:
            self._liste_activites.remove(activite)
            return True
        return False

    # Méthodes de vérification (depuis le diagramme UML)
    def s_inscrire(self, mail, pseudo, mdp):
        """
        Inscrit un nouvel utilisateur

        Args:
            mail (str): L'email de l'utilisateur
            pseudo (str): Le pseudo de l'utilisateur
            mdp (str): Le mot de passe de l'utilisateur

        Returns:
            bool: True si l'inscription a réussi
        """
        # Dans une vraie application, cela créerait un nouvel utilisateur en base
        self._mail = mail
        self._pseudo = pseudo
        self._mdp = mdp
        return True

    def rafraichir_fil(self):
        """
        Rafraîchit le fil d'actualité de l'utilisateur

        Returns:
            None
        """
        pass

    # Méthodes de calcul (basées sur le diagramme UML)
    def calculer_distance_totale(self, activites=None):
        """
        Calcule la distance totale parcourue

        Args:
            activites (list): Liste d'activités (utilise self._liste_activites si None)

        Returns:
            float: La distance totale en kilomètres
        """
        if activites is None:
            activites = self._liste_activites

        distance_totale = 0
        for activite in activites:
            if hasattr(activite, 'd_plus'):
                distance_totale += activite.d_plus
        return distance_totale

    def calculer_duree_totale(self, activites=None):
        """
        Calcule la durée totale des activités

        Args:
            activites (list): Liste d'activités (utilise self._liste_activites si None)

        Returns:
            int: La durée totale en minutes
        """
        if activites is None:
            activites = self._liste_activites

        duree_totale = 0
        for activite in activites:
            if hasattr(activite, 'duree_activite'):
                duree_totale += activite.duree_activite
        return duree_totale

    def calculer_calories_totales(self, activites=None):
        """
        Calcule le total de calories brûlées

        Args:
            activites (list): Liste d'activités (utilise self._liste_activites si None)

        Returns:
            int: Le nombre total de calories
        """
        if activites is None:
            activites = self._liste_activites

        calories_totales = 0
        for activite in activites:
            if hasattr(activite, 'calories'):
                calories_totales += activite.calories
        return calories_totales

    def calculer_d_plus_total(self, activites=None):
        """
        Calcule le dénivelé positif total

        Args:
            activites (list): Liste d'activités (utilise self._liste_activites si None)

        Returns:
            int: Le dénivelé positif total en mètres
        """
        if activites is None:
            activites = self._liste_activites

        d_plus_total = 0
        for activite in activites:
            if hasattr(activite, 'd_plus'):
                d_plus_total += activite.d_plus
        return d_plus_total

    def calculer_vitesse_moyenne_globale(self, activites=None):
        """
        Calcule la vitesse moyenne sur toutes les activités

        Args:
            activites (list): Liste d'activités (utilise self._liste_activites si None)

        Returns:
            float: La vitesse moyenne en km/h
        """
        if activites is None:
            activites = self._liste_activites

        if not activites:
            return 0.0

        distance_totale = self.calculer_distance_totale(activites)
        duree_totale = self.calculer_duree_totale(activites)

        if duree_totale == 0:
            return 0.0

        # Convertir la durée en heures et calculer la vitesse
        duree_heures = duree_totale / 60
        return distance_totale / duree_heures if duree_heures > 0 else 0.0

    # Méthodes pour obtenir des statistiques
    def get_nombre_like(self):
        """
        Retourne le nombre total de likes reçus sur toutes les activités

        Returns:
            int: Le nombre total de likes
        """
        total_likes = 0
        for activite in self._liste_activites:
            if hasattr(activite, 'comptelike'):
                total_likes += activite.comptelike()
        return total_likes

    def get_nombre_commentaire(self):
        """
        Retourne le nombre total de commentaires reçus sur toutes les activités

        Returns:
            int: Le nombre total de commentaires
        """
        total_commentaires = 0
        for activite in self._liste_activites:
            if hasattr(activite, 'comptecommentaire'):
                total_commentaires += activite.comptecommentaire()
        return total_commentaires

    # Méthodes spéciales
    def __str__(self):
        """Représentation textuelle de l'utilisateur"""
        return (
            f"{self._pseudo} ({self._prenom} {self._nom}) - "
            f"{len(self._liste_activites)} activités"
        )

    def __repr__(self):
        """Représentation technique de l'utilisateur"""
        return (
            f"Utilisateur(id={self._id_utilisateur}, "
            f"pseudo={self._pseudo}, "
            f"activites={len(self._liste_activites)})"
        )

    def __eq__(self, other):
        """Comparaison d'égalité entre utilisateurs"""
        if not isinstance(other, Utilisateur):
            return False
        return self._id_utilisateur == other._id_utilisateur

    def __hash__(self):
        """Hash de l'utilisateur basé sur son ID"""
        return hash(self._id_utilisateur)
