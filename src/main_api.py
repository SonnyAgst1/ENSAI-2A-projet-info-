"""
Application FastAPI complète avec toutes les fonctionnalités
Version sans frontend
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from database import Base, engine
import logging 
from business_objects import models

# Créer les tables
Base.metadata.create_all(bind=engine)

# Créer l'application
app = FastAPI(debug=True, docs_url="/docs", redoc_url=None, openapi_url="/openapi.json")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production : spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importer les routers
from api.utilisateur_router import router as utilisateur_router
from api.activite_router import router as activite_router
from api.fil_router import router as fil_router
from api.interaction_router import router as interaction_router
from api.statistiques_router import router as statistiques_router

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
    
    Retourne :
    - Version de l'API
    - Liste des endpoints disponibles
    - Résumé des fonctionnalités
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
    
    Utilisé pour le monitoring et les checks de disponibilité.
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
    
    Retourne le nombre total d'utilisateurs, d'activités, etc.
    """
    from dao.utilisateur_dao import UtilisateurDAO
    from dao.activite_dao import ActiviteDAO
    
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
    
    Retourne des messages d'erreur plus clairs pour les problèmes de validation
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


# Logger Uvicorn (écrit la trace complète dans la console)
logger = logging.getLogger("uvicorn.error")

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.exception("Internal server error")  # <-- imprime la traceback complète
    return JSONResponse(
        status_code=500,
        content={
            "message": "Erreur interne du serveur",
            "aide": "Une erreur est survenue. Regarde la console pour la trace complète."
        }
    )


# ========== POINT D'ENTRÉE ==========

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Configuration pour Onyxia
    # Par défaut port 9000 (standard Onyxia)
    port = int(os.getenv("PORT", 9000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print("\n" + "="*60)
    print("🏃 APPLICATION SPORTIVE API")
    print("="*60)
    print(f"\n🌐 Serveur : {host}:{port}")
    print("\n📚 Documentation disponible sur :")
    print(f"   → http://localhost:{port}/docs (Swagger UI)")
    print(f"   → http://localhost:{port}/redoc (ReDoc)")
    print("\n💡 Sur Onyxia, utilisez l'URL publique fournie par le service")
    print("   Format habituel : https://user-xxxxx.lab.sspcloud.fr/docs")
    print("\n🚀 Démarrage du serveur...")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )