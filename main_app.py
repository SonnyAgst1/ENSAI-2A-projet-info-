"""
Script principal de l'application sportive
"""
import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import Base, engine
from view.accueil_vue import AccueilVue


def initialiser_base_donnees():
    """Initialise la base de données si elle n'existe pas"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Base de données initialisée")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation de la base de données : {e}")
        sys.exit(1)


def main():
    """Point d'entrée principal de l'application"""
    print("\n" + "=" * 50)
    print("🏃 APPLICATION DE SUIVI SPORTIF")
    print("=" * 50)
    
    # Initialiser la base de données
    initialiser_base_donnees()
    
    # Boucle principale de l'application
    vue_courante = AccueilVue()
    
    while vue_courante is not None:
        try:
            # Afficher le message de la vue si présent
            if hasattr(vue_courante, 'message') and vue_courante.message:
                print(f"\n{vue_courante.message}")
            
            # Obtenir la prochaine vue
            vue_courante = vue_courante.choisir_menu()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interruption détectée")
            print("👋 Au revoir !\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Erreur inattendue : {e}")
            print("Retour à l'accueil...\n")
            vue_courante = AccueilVue()
    
    print("\n👋 Merci d'avoir utilisé l'application !\n")


if __name__ == "__main__":
    main()