"""
Vue des statistiques utilisateur
"""
from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.statistiques_service import StatistiquesService


class StatistiquesVue(VueAbstraite):
    """Vue des statistiques"""
    
    def choisir_menu(self):
        from view.accueil_vue import AccueilVue
        
        utilisateur = Session().utilisateur
        if not utilisateur:
            return AccueilVue("❌ Vous devez être connecté")
        
        print("\n" + "=" * 50)
        print("📊 MES STATISTIQUES")
        print("=" * 50 + "\n")
        
        # Résumé global
        resume = StatistiquesService.obtenir_resume_global(utilisateur.id)
        
        print(f"📈 Résumé global :")
        print(f"   • {resume['nombre_total_activites']} activités")
        print(f"   • {resume['duree_totale_heures']:.1f} heures")
        print(f"   • {resume['calories_totales']} calories")
        print(f"   • Sports pratiqués : {', '.join(resume['sports_pratiques'])}")
        print()
        
        # Stats par sport
        stats_sport = StatistiquesService.obtenir_statistiques_par_sport(
            utilisateur.id, 12
        )
        
        if stats_sport:
            print("🏆 Par sport (12 dernières semaines) :")
            for sport, stats in stats_sport.items():
                print(f"\n   {sport.upper()} :")
                print(f"      • {stats['nombre_activites']} activités")
                print(f"      • {stats['duree_totale_heures']:.1f}h")
                print(f"      • {stats['calories_totales']} cal")
        
        print("\n" + "=" * 50 + "\n")
        
        choix = inquirer.select(
            message="Action :",
            choices=["Retour à l'accueil"]
        ).execute()
        
        return AccueilVue()