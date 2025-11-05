"""
Vue d'inscription utilisateur
"""
from InquirerPy import inquirer
from datetime import datetime
from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.utilisateur_service import UtilisateurService


class InscriptionVue(VueAbstraite):
    """Vue d'inscription à l'application"""

    def __init__(self, message=""):
        """
        Initialisation de la vue d'inscription

        Args:
            message: Message à afficher (optionnel)
        """
        super().__init__(message)

    def choisir_menu(self):
        """
        Affiche le formulaire d'inscription et crée le compte

        Returns:
            VueAbstraite: La prochaine vue à afficher
        """
        from view.accueil_vue import AccueilVue

        print("\n" + "-" * 50)
        print("✍️  CRÉATION DE COMPTE")
        print("-" * 50 + "\n")

        # Collecte des informations
        pseudo = inquirer.text(
            message="Pseudo :",
            validate=lambda x: len(x) >= 3 or "Le pseudo doit contenir au moins 3 caractères"
        ).execute()

        # Vérifier si le pseudo existe déjà
        if UtilisateurService.obtenir_utilisateur_par_pseudo(pseudo):
            print(f"\n❌ Le pseudo '{pseudo}' est déjà utilisé\n")
            return InscriptionVue()

        nom = inquirer.text(
            message="Nom :",
            validate=lambda x: len(x) > 0 or "Le nom ne peut pas être vide"
        ).execute()

        prenom = inquirer.text(
            message="Prénom :",
            validate=lambda x: len(x) > 0 or "Le prénom ne peut pas être vide"
        ).execute()

        age = inquirer.number(
            message="Âge :",
            default=None,
        ).execute()

        mail = inquirer.text(
            message="Email :",
            validate=lambda x: "@" in x and "." in x.split("@")[1] or "Email invalide"
        ).execute()

        # Vérifier si l'email existe déjà
        if UtilisateurService.obtenir_utilisateur_par_email(mail):
            print(f"\n❌ L'email '{mail}' est déjà utilisé\n")
            return InscriptionVue()

        mot_de_passe = inquirer.secret(
            message="Mot de passe :",
            validate=lambda x: len(x) >= 6 or "Le mot de passe doit contenir au moins 6 caractères"
        ).execute()

        mot_de_passe_confirmation = inquirer.secret(
            message="Confirmer le mot de passe :"
        ).execute()

        if mot_de_passe != mot_de_passe_confirmation:
            print("\n❌ Les mots de passe ne correspondent pas\n")
            return InscriptionVue()

        # Informations optionnelles
        print("\n📋 Informations optionnelles (appuyez sur Entrée pour passer)\n")

        taille = inquirer.text(
            message="Taille (cm) [optionnel] :",
            default=""
        ).execute()

        poids = inquirer.text(
            message="Poids (kg) [optionnel] :",
            default=""
        ).execute()

        telephone = inquirer.text(
            message="Téléphone [optionnel] :",
            default=""
        ).execute()

        # Convertir les valeurs optionnelles
        taille = float(taille) if taille else None
        poids = float(poids) if poids else None
        telephone = int(telephone) if telephone else None

        # Créer l'utilisateur
        utilisateur = UtilisateurService.creer_utilisateur(
            nom=nom,
            prenom=prenom,
            age=int(age),
            pseudo=pseudo,
            mail=mail,
            mdp=mot_de_passe,
            taille=taille,
            poids=poids,
            telephone=telephone
        )

        if utilisateur:
            # Inscription réussie - connexion automatique
            Session().utilisateur = utilisateur
            return AccueilVue(
                f"✅ Compte créé avec succès !\n"
                f"Bienvenue {utilisateur.pseudo} 🎉"
            )
        else:
            print("\n❌ Erreur lors de la création du compte\n")

            choix = inquirer.select(
                message="Que souhaitez-vous faire ?",
                choices=[
                    "Réessayer",
                    "Retour à l'accueil"
                ]
            ).execute()

            match choix:
                case "Réessayer":
                    return InscriptionVue()
                case "Retour à l'accueil":
                    return AccueilVue()
