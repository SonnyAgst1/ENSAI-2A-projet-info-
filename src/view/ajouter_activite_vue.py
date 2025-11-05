"""
Vue pour ajouter une nouvelle activité
"""
from InquirerPy import inquirer
from datetime import date
from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.activite_service import ActiviteService


class AjouterActiviteVue(VueAbstraite):
    """Vue d'ajout d'activité"""

    def choisir_menu(self):
        from view.accueil_vue import AccueilVue

        utilisateur = Session().utilisateur
        if not utilisateur:
            return AccueilVue("❌ Vous devez être connecté")

        print("\n" + "=" * 50)
        print("➕ AJOUTER UNE ACTIVITÉ")
        print("=" * 50 + "\n")

        # Formulaire
        nom = inquirer.text(
            message="Nom de l'activité :",
            validate=lambda x: len(x) > 0
        ).execute()

        type_sport = inquirer.select(
            message="Type de sport :",
            choices=["Course", "Vélo", "Natation", "Marche", "Randonnée", "Autre"]
        ).execute()

        date_str = inquirer.text(
            message="Date (YYYY-MM-DD) :",
            default=str(date.today())
        ).execute()

        duree_minutes = inquirer.number(
            message="Durée (minutes) :",
            min_allowed=1
        ).execute()

        description = inquirer.text(
            message="Description (optionnel) :",
            default=""
        ).execute()

        d_plus = inquirer.number(
            message="Dénivelé positif (m, optionnel) :",
            default=0
        ).execute()

        calories = inquirer.number(
            message="Calories (optionnel) :",
            default=0
        ).execute()

        # Créer l'activité
        activite = ActiviteService.creer_activite_manuelle(
            utilisateur_id=utilisateur.id,
            nom=nom,
            type_sport=type_sport,
            date_activite=date.fromisoformat(date_str),
            duree_activite=int(duree_minutes) * 60,
            description=description,
            d_plus=int(d_plus),
            calories=int(calories)
        )

        if activite:
            return AccueilVue("✅ Activité ajoutée avec succès !")
        else:
            return AccueilVue("❌ Erreur lors de l'ajout de l'activité")
