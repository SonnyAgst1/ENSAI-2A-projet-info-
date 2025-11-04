"""
Vue d'accueil de l'application sportive
"""
from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session


class AccueilVue(VueAbstraite):
    """Vue d'accueil de l'application"""
    
    def __init__(self, message=""):
        """
        Initialisation de la vue d'accueil
        
        Args:
            message: Message à afficher (optionnel)
        """
        super().__init__(message)
    
    def choisir_menu(self):
        """
        Choix du menu suivant
        
        Returns:
            VueAbstraite: Retourne la vue choisie par l'utilisateur
        """
        # Afficher le message s'il existe
        if self.message:
            print("\n" + "=" * 50)
            print(self.message)
            print("=" * 50)
        
        print("\n" + "-" * 50)
        print("🏃 BIENVENUE - APPLICATION SPORTIVE")
        print("-" * 50 + "\n")
        
        # Vérifier si un utilisateur est connecté
        utilisateur_connecte = Session().utilisateur
        
        if utilisateur_connecte:
            choices = [
                "Voir mon profil",
                "Mes activités",
                "Ajouter une activité",
                "Statistiques",
                "Se déconnecter",
                "Quitter",
            ]
        else:
            choices = [
                "Se connecter",
                "Créer un compte",
                "Quitter",
            ]
        
        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=choices,
        ).execute()
        
        # Gestion des choix
        match choix:
            case "Quitter":
                print("\n👋 Au revoir !\n")
                return None
            
            case "Se connecter":
                from view.connexion_vue import ConnexionVue
                return ConnexionVue()
            
            case "Créer un compte":
                from view.inscription_vue import InscriptionVue
                return InscriptionVue()
            
            case "Se déconnecter":
                Session().deconnexion()
                return AccueilVue("✅ Déconnexion réussie")
            
            case "Voir mon profil":
                from view.profil_vue import ProfilVue
                return ProfilVue()
            
            case "Mes activités":
                from view.liste_activites_vue import ListeActivitesVue
                return ListeActivitesVue()
            
            case "Ajouter une activité":
                from view.ajouter_activite_vue import AjouterActiviteVue
                return AjouterActiviteVue()
            
            case "Statistiques":
                from view.statistiques_vue import StatistiquesVue
                return StatistiquesVue()
            
            case _:
                return AccueilVue()