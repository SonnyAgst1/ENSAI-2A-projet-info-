
from database.py import engine, SessionLocal
from models import Base, Utilisateur


#  Crée physiquement les tables
Base.metadata.create_all(engine)
print("✅ Base SQLite créée avec succès !")

# Ouvre une session
db = SessionLocal()

#  Ajoute des utilisateurs
u1 = Utilisateur(
    nom="Dupont", prenom="Alice", age=25, taille=1.68,
    pseudo="Alicia", poids=60.0, mail="alice@example.com",
    telephone=123456789, mdp="secret123"
)
u2 = Utilisateur(
    nom="Martin", prenom="Bob", age=30, taille=1.80,
    pseudo="Bobby", poids=75.0, mail="bob@example.com",
    telephone=987654321, mdp="azerty"
)

db.add_all([u1, u2])
db.commit()
print(" Utilisateurs ajoutés !")

#  Vérifie
for u in db.query(Utilisateur).all():
    print(f"{u.id}: {u.nom} {u.prenom} ({u.pseudo})")

db.close()
