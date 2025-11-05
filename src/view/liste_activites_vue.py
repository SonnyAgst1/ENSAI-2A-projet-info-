"""
Vue pour afficher la liste des activités de l'utilisateur
"""
from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.activite_service import ActiviteService


class ListeActivitesVue(VueAbstraite):
    """Vue de la liste des activités"""
    
    def choisir_menu(self):
        from view.accueil_vue import AccueilVue
        
        utilisateur = Session().utilisateur
        if not utilisateur:
            return AccueilVue("❌ Vous devez être connecté")
        
        # Récupérer les activités
        activites = ActiviteService.obtenir_activites_utilisateur(utilisateur.id)
        
        if not activites:
            print("\n📭 Vous n'avez pas encore d'activités")
            return AccueilVue()
        
        print("\n" + "=" * 50)
        print("📋 MES ACTIVITÉS")
        print("=" * 50 + "\n")
        
        for act in activites:
            print(f"🏃 {act.nom} - {act.type_sport}")
            print(f"   📅 {act.date_activite}")
            if act.duree_activite:
                heures = act.duree_activite // 3600
                minutes = (act.duree_activite % 3600) // 60
                print(f"   ⏱️  {heures}h{minutes:02d}min")
            if act.calories:
                print(f"   🔥 {act.calories} cal")
            print()
        
        choix = inquirer.select(
            message="Action :",
            choices=["Retour à l'accueil"]
        ).execute()
        
        return AccueilVue()