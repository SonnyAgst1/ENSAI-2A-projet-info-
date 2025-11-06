"""
Application FastAPI complète avec toutes les fonctionnalités
Version sans frontend
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from database import Base, engine # Imports essentiels pour l'initialisation de la DB
from business_objects import models # IMPÉRATIF: Importe les modèles pour que Base.metadata les connaisse
from dao.utilisateur_dao import UtilisateurDAO
from dao.activite_dao import ActiviteDAO

<<<<<<< HEAD
# =================================================================
# 1. CRÉATION DE L'APPLICATION (DOIT ÊTRE FAIT AVANT d'utiliser 'app')
# =================================================================
app = FastAPI(
    title="Application Sportive API",
    description="""
    API complète pour une application de suivi sportif.
    
    ## Fonctionnalités
    
    ### 👤 Utilisateurs
    * Créer un compte (inscription)
    * Se connecter
    * Modifier son profil
    * Supprimer son compte
    * Suivre/Ne plus suivre des utilisateurs
    * Voir ses abonnements et followers
    * Obtenir des suggestions d'utilisateurs
    
    ### 🏃 Activités (F1)
    * ✅ Créer une activité manuellement
    * ✅ Créer une activité depuis un fichier GPX
    * ✅ Consulter ses activités avec filtres (sport, date)
    * ✅ Modifier une activité
    * ✅ Supprimer une activité
    
    ### 📰 Fil d'actualité (F2)
    * ✅ Voir les activités des utilisateurs suivis
    * ✅ Filtrer par période (7, 30, 90 jours)
    * ✅ Rechercher des utilisateurs
    * ✅ Obtenir des suggestions d'utilisateurs à suivre
    * ✅ Statistiques du fil
    
    ### ❤️ Interactions (F3)
    * ✅ Liker/Unliker une activité
    * ✅ Commenter une activité
    * ✅ Voir les likes et commentaires
    * ✅ Modifier/Supprimer ses commentaires
    
    ### 📊 Statistiques (F4)
    * ✅ Nombre d'activités par semaine et par sport
    * ✅ Nombre de kilomètres parcourus par semaine
    * ✅ Nombre d'heures d'activité par semaine
    * ✅ Records personnels
    * ✅ Analyse de progression par sport
    * ✅ Tableau de bord complet
    
    ---
    
    ## 🚀 Démarrage rapide
    
    ### 1. Créer un compte
    ```bash
    POST /api/utilisateurs/inscription
    {
      "nom": "Dupont",
      "prenom": "Jean",
      "age": 30,
      "pseudo": "jdupont",
      "mail": "jean@example.com",
      "mdp": "password123"
    }
    ```
    
    ### 2. Se connecter
    ```bash
    POST /api/utilisateurs/connexion
    {
      "pseudo": "jdupont",
      "mdp": "password123"
    }
    ```
    
    ### 3. Créer une activité
    ```bash
    POST /api/activites
    {
      "utilisateur_id": 1,
      "nom": "Course matinale",
      "type_sport": "Course",
      "date_activite": "2024-11-06",
      "duree_activite": 3600
    }
    ```
    
    ### 4. Voir ses statistiques
    ```bash
    GET /api/statistiques/1/hebdomadaire
    ```
    
    ---
    
    ## 📚 Documentation
    
    * **Swagger UI** : [/docs](/docs) ← Interface interactive
    * **ReDoc** : [/redoc](/redoc) ← Documentation détaillée
    * **OpenAPI Schema** : [/openapi.json](/openapi.json)
    
    ---
    
    ## 🔗 Endpoints principaux
    
    | Catégorie | Endpoint | Description |
    |-----------|----------|-------------|
    | 👤 Utilisateurs | `/api/utilisateurs` | Gestion des comptes |
    | 🏃 Activités | `/api/activites` | CRUD activités + GPX |
    | 📰 Fil | `/api/fil` | Fil d'actualité |
    | ❤️ Interactions | `/api/interactions` | Likes & commentaires |
    | 📊 Stats | `/api/statistiques` | Statistiques détaillées |
    
    """,
    version="2.0.0",
    contact={
        "name": "Support",
        "email": "support@app-sportive.com"
    },
    license_info={
        "name": "MIT"
    }
)
# Importer les routers
from api.utilisateur_router import router as utilisateur_router
from api.activite_router import router as activite_router
from api.fil_router import router as fil_router
from api.interaction_router import router as interaction_router
from api.statistiques_router import router as statistiques_router
# =================================================================
# 2. LOGIQUE D'INITIALISATION DE LA BASE (Résout l'erreur SQLAlchemy)
# =================================================================
@app.on_event("startup")
def init_db_on_startup():
    """
    S'assure que les tables de la base de données sont créées
    une seule fois au démarrage du processus principal du serveur.
    Ceci résout l'erreur 'Multiple classes found' en mode --reload.
    """
    print("\n\n" + "="*60)
    print("🚀 Événement STARTUP : Initialisation de la Base de Données")
    print("="*60)
    
    # Créer les tables si elles n'existent pas
    Base.metadata.create_all(bind=engine) 
    
    print("✅ Création des tables terminée (si elles n'existaient pas).\n")

=======
# Créer les tables
Base.metadata.create_all(bind=engine)

# Créer l'application
app = FastAPI(docs_url="/docs", redoc_url=None, openapi_url="/openapi.json")
>>>>>>> 753f712abfb667f39fe7111f066dd9a6610e1f66

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production : spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Enregistrer les routers
app.include_router(utilisateur_router, prefix="/api")
app.include_router(activite_router, prefix="/api")
app.include_router(fil_router, prefix="/api")
app.include_router(interaction_router, prefix="/api")
app.include_router(statistiques_router, prefix="/api")


# ========== ROUTES RACINES ==========
@app.get("/", include_in_schema=False)
def redirect_docs():
    return RedirectResponse(url="docs")  # pas de slash initial


@app.get("/api", tags=["📋 Info"])
def api_info():
    """
    Informations générales sur l'API
    """
    return {
        "nom": "Application Sportive API",
        "version": "2.0.0",
        "status": "online",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "utilisateurs": {
                "base": "/api/utilisateurs",
                "inscription": "POST /api/utilisateurs/inscription",
                "connexion": "POST /api/utilisateurs/connexion",
                "profil": "GET /api/utilisateurs/{id}",
                "suivre": "POST /api/utilisateurs/{id}/follow/{followed_id}"
            },
            "activites": {
                "base": "/api/activites",
                "creer_manuel": "POST /api/activites",
                "creer_gpx": "POST /api/activites/gpx",
                "liste": "GET /api/activites/utilisateur/{id}",
                "modifier": "PUT /api/activites/{id}",
                "supprimer": "DELETE /api/activites/{id}"
            },
            "fil_actualite": {
                "base": "/api/fil",
                "obtenir": "GET /api/fil/{user_id}",
                "stats": "GET /api/fil/{user_id}/statistiques"
            },
            "interactions": {
                "base": "/api/interactions",
                "liker": "POST /api/interactions/activites/{id}/like/{user_id}",
                "commenter": "POST /api/interactions/activites/{id}/commentaires/{user_id}",
                "voir_commentaires": "GET /api/interactions/activites/{id}/commentaires"
            },
            "statistiques": {
                "base": "/api/statistiques",
                "resume": "GET /api/statistiques/{user_id}/resume",
                "hebdomadaire": "GET /api/statistiques/{user_id}/hebdomadaire",
                "par_sport": "GET /api/statistiques/{user_id}/par-sport",
                "tableau_bord": "GET /api/statistiques/{user_id}/tableau-bord"
            }
        },
        "fonctionnalites": {
            "F1": "✅ Gestion complète des activités (création, consultation, modification, suppression, upload GPX)",
            "F2": "✅ Fil d'actualité des utilisateurs suivis avec filtres temporels",
            "F3": "✅ Interactions sociales (likes et commentaires)",
            "F4": "✅ Statistiques détaillées (par semaine, par sport, progression, records)"
        }
    }


@app.get("/health", tags=["📋 Info"])
def health_check():
    """
    Vérification de santé de l'API
    """
    return {
        "status": "healthy",
        "database": "connected",
        "version": "2.0.0"
    }


@app.get("/stats/global", tags=["📋 Info"])
def stats_globales():
    """
    Statistiques globales de l'application
    """
    return {
        "utilisateurs": {
            "total": UtilisateurDAO.count_all()
        },
        "activites": {
            "total": len(ActiviteDAO.get_all())
        }
    }


# ========== GESTIONNAIRES D'ERREURS ==========

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Gestionnaire d'erreurs de validation personnalisé
    """
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({
            "champ": field,
            "erreur": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Erreur de validation des données",
            "erreurs": errors,
            "aide": "Vérifiez que tous les champs requis sont présents et ont le bon format"
        }
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Gestionnaire pour les routes non trouvées"""
    return JSONResponse(
        status_code=404,
        content={
            "message": "Endpoint non trouvé",
            "chemin": str(request.url.path),
            "aide": "Consultez la documentation sur /docs"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Gestionnaire pour les erreurs internes"""
    return JSONResponse(
        status_code=500,
        content={
            "message": "Erreur interne du serveur",
            "aide": "Contactez le support si le problème persiste"
        }
    )


# ========== POINT D'ENTRÉE ==========

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Configuration pour Onyxia
    port = int(os.getenv("PORT", 9000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print("\n" + "="*60)
    print("🏃 APPLICATION SPORTIVE API")
    print("="*60)
    print(f"\n🌐 Serveur : {host}:{port}")
    print("\n📚 Documentation disponible sur :")
    print(f"   → http://localhost:{port}/docs (Swagger UI)")
    print(f"   → http://localhost:{port}/redoc (ReDoc)")
    print("\n💡 Sur Onyxia, utilisez l'URL publique fournie par le service")
    print("   Format habituel : https://user-xxxxx.lab.sspcloud.fr/docs")
    print("\n🚀 Démarrage du serveur...")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )