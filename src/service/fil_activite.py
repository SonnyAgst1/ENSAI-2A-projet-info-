class FilDActivite:

    def __init__(self):
        """
        Constructeur de la classe FilDActivite.
        ----------
        activites : list
            Liste des activités actuellement présentes dans le fil.
        """
        self.activites = []

    def rafraichirFil(self):
        """
        Rafraîchit le fil d'activité.

        """
        print("Le fil d'activité a été rafraîchi.")
        print(f"Il contient actuellement {len(self.activites)} activité(s).")

    def ajouterActivite(self, activite):
        """
        Ajoute une nouvelle activité au fil.

        Paramètres :
        -----------
        activite : str
            Représente une activité sous forme de texte (ex. : 'Course de 5 km').

        Effets :
        --------
        - L'activité est ajoutée à la liste interne des activités.
        - Un message de confirmation est affiché.
        """
        self.activites.append(activite)
        print(f"Activité ajoutée : {activite}")


