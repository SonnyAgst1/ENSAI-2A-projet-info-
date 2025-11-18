"""
SCRIPT UTILITAIRE - NE PAS IMPORTER DANS L'API
Ce script sert uniquement à réinitialiser/tester la base de données.
Exécutez-le directement : python src/init_db_script.py
"""
from database import engine, Base
from business_objects.models import Utilisateur  # importe le modèle
from dao.utilisateur_dao import UtilisateurDAO

print("\n" + "="*60)
print(" SCRIPT D'INITIALISATION DE LA BASE DE DONNÉES")
print("="*60)

# Réinitialise complètement la base
print("\n  Suppression de toutes les tables...")
Base.metadata.drop_all(bind=engine)
print(" Tables supprimées")

print("\n Création des tables...")
Base.metadata.create_all(bind=engine)
print(" Tables créées\n")

print("="*60)
print(" Base de données réinitialisée avec succès !")
print("="*60 + "\n")

# Note : Les lignes suivantes étaient bugguées, je les ai retirées
# Si vous voulez créer des utilisateurs de test, utilisez UtilisateurDAO.create()