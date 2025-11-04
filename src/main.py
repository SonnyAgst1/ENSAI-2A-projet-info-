from __init__ import init_db
from objects.dao.crud import create_user, get_user_by_pseudo, create_activity
from datetime import date  # Pour utiliser le type Date

if __name__ == "__main__":

    print("--- Initialisation de l'application ---")

    # 1. Assurez-vous que la base de données et les tables existent
    init_db()

    # 2. Exemple d'utilisation du DAO (Couche Accès aux Données)

    # Création d'un utilisateur
    try:
        user_a = create_user("Dupont", "Marie", "MDU", "m.dupont@mail.com", "pass123")
        print(f"\n Utilisateur créé: {user_a.pseudo} (ID: {user_a.id})")
    except ValueError as e:
        print(f"\n Erreur de création utilisateur: {e}")
        user_a = get_user_by_pseudo("MDU")  # Si l'utilisateur existe déjà, on le récupère

    # Création d'une activité pour cet utilisateur
    if user_a:
        try:
            activity = create_activity(
                user_id=user_a.id,
                nom="Course 10k",
                type_sport="Course à pied",
                date_activite=date(2025, 10, 3),  # Utiliser le type 'date' de Python
                duree_activite=3600  # en secondes
            )
            print(f" Activité créée: '{activity.nom}' par {user_a.pseudo}")

            # Récupération et vérification
            activities = get_activities_for_user(user_a.id)
            print(f"Total activités de {user_a.pseudo}: {len(activities)}")

        except Exception as e:
            print(f"Erreur lors de la création d'activité: {e}")

    # 3. Le reste de la logique de l'application se déploie ici...
    print("\n--- Fin de l'application ---")
