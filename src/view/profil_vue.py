"""
Vue du profil utilisateur
"""
from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.utilisateur_service import UtilisateurService


class ProfilVue(VueAbstraite):
    """Vue du profil utilisateur"""

    def __init__(self, message=""):
        super().__init__(message)

    def choisir_menu(self):
        """
        Affiche le profil de l'utilisateur connecté

        Returns:
            VueAbstraite: La prochaine vue à afficher
        """
        from view.accueil_vue import AccueilVue

        utilisateur = Session().utilisateur

        if not utilisateur:
            return AccueilVue("❌ Vous devez être connecté pour voir votre profil")

        print("\n" + "=" * 50)
        print("👤 MON PROFIL")
        print("=" * 50)
        print(f"\n📝 Pseudo : {utilisateur.pseudo}")
        print(f"👤 Nom : {utilisateur.prenom} {utilisateur.nom}")
        print(f"📧 Email : {utilisateur.mail}")
        print(f"🎂 Âge : {utilisateur.age} ans")

        if utilisateur.taille:
            print(f"📏 Taille : {utilisateur.taille} cm")
        if utilisateur.poids:
            print(f"⚖️  Poids : {utilisateur.poids} kg")
        if utilisateur.telephone:
            print(f"📱 Téléphone : {utilisateur.telephone}")

        # Statistiques
        nb_activites = UtilisateurService.obtenir_nombre_activites(utilisateur.id)
        nb_followers = UtilisateurService.obtenir_nombre_followers(utilisateur.id)
        nb_suivis = UtilisateurService.obtenir_nombre_suivis(utilisateur.id)

        print(f"\n📊 Statistiques :")
        print(f"   • {nb_activites} activité(s)")
        print(f"   • {nb_followers} follower(s)")
        print(f"   • {nb_suivis} abonnement(s)")
        print("=" * 50 + "\n")

        choix = inquirer.select(
            message="Que souhaitez-vous faire ?",
            choices=[
                "Modifier mon profil",
                "Retour à l'accueil"
            ]
        ).execute()

        match choix:
            case "Modifier mon profil":
                return self.modifier_profil()
            case "Retour à l'accueil":
                return AccueilVue()

    def modifier_profil(self):
        """Permet de modifier le profil utilisateur"""
        from view.accueil_vue import AccueilVue

        utilisateur = Session().utilisateur

        print("\n" + "-" * 50)
        print("✏️  MODIFIER MON PROFIL")
        print("-" * 50)
        print("(Appuyez sur Entrée pour conserver la valeur actuelle)\n")

        # Modifications possibles
        nouveau_pseudo = inquirer.text(
            message=f"Pseudo [{utilisateur.pseudo}] :",
            default=""
        ).execute()

        nouvelle_taille = inquirer.text(
            message=f"Taille [{utilisateur.taille or 'Non renseignée'}] :",
            default=""
        ).execute()

        nouveau_poids = inquirer.text(
            message=f"Poids [{utilisateur.poids or 'Non renseigné'}] :",
            default=""
        ).execute()

        nouveau_telephone = inquirer.text(
            message=f"Téléphone [{utilisateur.telephone or 'Non renseigné'}] :",
            default=""
        ).execute()

        # Préparer les modifications
        modifications = {}

        if nouveau_pseudo:
            modifications['pseudo'] = nouveau_pseudo
        if nouvelle_taille:
            modifications['taille'] = float(nouvelle_taille)
        if nouveau_poids:
            modifications['poids'] = float(nouveau_poids)
        if nouveau_telephone:
            modifications['telephone'] = int(nouveau_telephone)

        # Appliquer les modifications
        if modifications:
            utilisateur_modifie = UtilisateurService.modifier_utilisateur(
                utilisateur.id,
                **modifications
            )

            if utilisateur_modifie:
                Session().utilisateur = utilisateur_modifie
                return AccueilVue("✅ Profil modifié avec succès")
            else:
                return AccueilVue("❌ Erreur lors de la modification du profil")
        else:
            return AccueilVue("ℹ️  Aucune modification effectuée")
