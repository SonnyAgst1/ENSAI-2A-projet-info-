class FilDActivite:

    """
    Classe représentant un fil d'activité.

    Le fil d'activité permet :
      - d'ajouter de nouvelles activités,
      - de rafraîchir son contenu (par exemple, recharger les activités récentes).

    Pour simplifier, les activités sont stockées dans une liste interne.
    """

    def __init__(self):
        """
        Constructeur de la classe FilDActivite.

        Attributs :
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





# EXEMPLE D'UTILISATION
fil = FilDActivite()

# Ajout d’activités
fil.ajouterActivite("Course à pied - 5 km")
fil.ajouterActivite("Sortie vélo - 20 km")

# Rafraîchir le fil
fil.rafraichirFil()

































