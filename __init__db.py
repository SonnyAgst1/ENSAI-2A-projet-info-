"""
Script d'initialisation de la base de données
Crée toutes les tables définies dans les modèles SQLAlchemy
"""
from src.database import engine, Base
from src.business_objects.models import Utilisateur, Activite, Commentaire, follows

def init_database():
    """
    Crée toutes les tables dans la base de données
    """
    print("Création des tables...")
    
    # Créer toutes les tables définies dans Base.metadata
    Base.metadata.create_all(bind=engine)
    
    print("✓ Tables créées avec succès!")
    print("\nTables créées:")
    print("  - Utilisateur")
    print("  - Activite")
    print("  - Commentaire")
    print("  - follows (table de liaison)")

if __name__ == "__main__":
    init_database()