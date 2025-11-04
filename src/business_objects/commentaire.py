class Commentaire:
    """
    Classe représentant un commentaire sur une activité
    """

    def __init__(self, id_commentaire, auteur, activite, contenu):
        """
        Initialise un commentaire

        Args:
            id_commentaire (int): Identifiant unique du commentaire
            auteur (Utilisateur): L'utilisateur qui a écrit le commentaire
            activite (Activite): L'activité commentée
            contenu (str): Le contenu textuel du commentaire
        """
        self._id = id_commentaire
        self._auteur = auteur
        self._activite = activite
        self._contenu = contenu
        self._like = []  # Liste des utilisateurs qui ont liké

    # Getters
    @property
    def id(self):
        """Retourne l'identifiant du commentaire"""
        return self._id

    @property
    def auteur(self):
        """Retourne l'auteur du commentaire"""
        return self._auteur

    @property
    def activite(self):
        """Retourne l'activité associée"""
        return self._activite

    @property
    def contenu(self):
        """Retourne le contenu du commentaire"""
        return self._contenu

    @property
    def like(self):
        """Retourne la liste des utilisateurs qui ont liké"""
        return self._like.copy()

    # Setters
    @contenu.setter
    def contenu(self, nouveau_contenu):
        """Modifie le contenu du commentaire"""
        if isinstance(nouveau_contenu, str) and nouveau_contenu.strip():
            self._contenu = nouveau_contenu
        else:
            raise ValueError("Le contenu doit être une chaîne non vide")

    # Méthodes métier
    def ajouter_like(self, utilisateur):
        """
        Ajoute un like d'un utilisateur au commentaire

        Args:
            utilisateur (Utilisateur): L'utilisateur qui like le commentaire

        Returns:
            bool: True si le like a été ajouté, False si l'utilisateur avait déjà liké
        """
        if utilisateur not in self._like:
            self._like.append(utilisateur)
            return True
        return False

    def supprimer_like(self, utilisateur):
        """
        Retire le like d'un utilisateur du commentaire

        Args:
            utilisateur (Utilisateur): L'utilisateur qui retire son like

        Returns:
            bool: True si le like a été retiré, False si l'utilisateur n'avait pas liké
        """
        if utilisateur in self._like:
            self._like.remove(utilisateur)
            return True
        return False

    def comptelike(self):
        """
        Compte le nombre de likes sur le commentaire

        Returns:
            int: Le nombre de likes
        """
        return len(self._like)

    # Méthode spéciale pour l'affichage
    def __str__(self):
        """Représentation textuelle du commentaire"""
        return (
            f"Commentaire #{self._id} par {self._auteur.pseudo}: "
            f"{self._contenu[:50]}... ({self.comptelike()} likes)"
        )

    def __repr__(self):
        """Représentation technique du commentaire"""
        return (
            f"Commentaire(id={self._id}, "
            f"auteur={self._auteur.pseudo}, "
            f"likes={self.comptelike()})"
        )


# Exemple d'utilisation (nécessite les classes Utilisateur et Activite)
if __name__ == "__main__":
    # Simulation avec des objets simplifiés
    class UtilisateurSimple:
        def __init__(self, id_u, pseudo):
            self.id_utilisateur = id_u
            self.pseudo = pseudo

    class ActiviteSimple:
        def __init__(self, id_a, nom):
            self.id_activite = id_a
            self.nom = nom

    # Création d'objets de test
    user1 = UtilisateurSimple(1, "SportifPro")
    user2 = UtilisateurSimple(2, "RunnerFan")
    user3 = UtilisateurSimple(3, "FitnessLover")

    activite1 = ActiviteSimple(1, "Course matinale")

    # Création d'un commentaire
    com1 = Commentaire(
        1, user1, activite1, "Super séance aujourd'hui ! J'ai battu mon record personnel."
        )

    print(com1)
    print(f"Nombre de likes: {com1.comptelike()}")

    # Ajout de likes
    com1.ajouter_like(user2)
    com1.ajouter_like(user3)
    print(f"Après ajout de likes: {com1.comptelike()}")

    # Tentative d'ajout d'un like déjà existant
    resultat = com1.ajouter_like(user2)
    print(f"Tentative de re-like: {resultat}")
    print(f"Nombre de likes: {com1.comptelike()}")

    # Suppression d'un like
    com1.supprimer_like(user2)
    print(f"Après suppression d'un like: {com1.comptelike()}")

    # Modification du contenu
    com1.contenu = "Contenu mis à jour avec de nouvelles informations !"
    print(f"Contenu modifié: {com1.contenu}")
