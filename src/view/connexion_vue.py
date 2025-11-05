"""
Vue de connexion utilisateur
"""
from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.utilisateur_service import UtilisateurService


class ConnexionVue(VueAbstraite):
    """Vue de connexion à l'application"""

    def __init__(self, message=""):
        """
        Initialisation de la vue de connexion

        Args:
            message: Message à afficher (optionnel)
        """
        super().__init__(message)

    def choisir_menu(self):
        """
        Affiche le formulaire de connexion et gère l'authentification

        Returns:
            VueAbstraite: La prochaine vue à afficher
        """
        from view.accueil_vue import AccueilVue

        print("\n" + "-" * 50)
        print("🔐 CONNEXION")
        print("-" * 50 + "\n")

        # Demander le pseudo
        pseudo = inquirer.text(
            message="Pseudo :",
            validate=lambda x: len(x) > 0 or "Le pseudo ne peut pas être vide"
        ).execute()

        # Demander le mot de passe
        mot_de_passe = inquirer.secret(
            message="Mot de passe :",
            validate=lambda x: len(x) > 0 or "Le mot de passe ne peut pas être vide"
        ).execute()

        # Tentative de connexion
        utilisateur = UtilisateurService.connexion(pseudo, mot_de_passe)

        if utilisateur:
            # Connexion réussie
            Session().utilisateur = utilisateur
            return AccueilVue(f"✅ Connexion réussie ! Bienvenue {utilisateur.pseudo}")
        else:
            # Échec de connexion
            print("\n❌ Identifiants incorrects\n")

            choix = inquirer.select(
                message="Que souhaitez-vous faire ?",
                choices=[
                    "Réessayer",
                    "Créer un compte",
                    "Retour à l'accueil"
                ]
            ).execute()

            match choix:
                case "Réessayer":
                    return ConnexionVue()
                case "Créer un compte":
                    from view.inscription_vue import InscriptionVue
                    return InscriptionVue()
                case "Retour à l'accueil":
                    return AccueilVue()
