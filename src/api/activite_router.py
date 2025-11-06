"""
Router pour les activités (F1)
"""
import os
from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from sqlalchemy.orm import Session

from api.schemas import (
    ActiviteOut, ActiviteCreate, ActiviteUpdate, MessageResponse
)
from api.lien_dbapi import get_db
from service.activite_service import ActiviteService

router = APIRouter(prefix="/activites", tags=["activités"])

UPLOAD_DIR = "uploads/gpx"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _safe_filename(s: str) -> str:
    """Crée un nom de fichier sécurisé"""
    return "".join(c if c.isalnum() or c in ("_", "-", ".", "@") else "_" for c in s)


# ========== CRÉATION ==========

@router.post("/gpx", response_model=ActiviteOut, status_code=201)
async def creer_activite_gpx(
    utilisateur_id: int = Form(...),
    nom: str = Form(...),
    type_sport: str = Form(...),
    description: Optional[str] = Form(""),
    gpx: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Créer une activité à partir d'un fichier GPX (F1)
    
    Le fichier GPX est analysé pour extraire :
    - Date de l'activité
    - Durée
    - Dénivelé positif
    - Calories estimées
    
    **Paramètres:**
    - **utilisateur_id**: ID de l'utilisateur
    - **nom**: Nom de l'activité
    - **type_sport**: Type de sport (Course, Vélo, etc.)
    - **description**: Description optionnelle
    - **gpx**: Fichier GPX
    """
    # Validation du fichier
    if not gpx.filename.lower().endswith(".gpx"):
        raise HTTPException(
            status_code=400,
            detail="Le fichier doit être un .gpx"
        )
    
    # Nom de fichier unique et sûr
    fname = _safe_filename(f"{utilisateur_id}_{nom}_{gpx.filename}")
    fullpath = os.path.join(UPLOAD_DIR, fname)
    
    # Sauvegarde du fichier
    content = await gpx.read()
    with open(fullpath, "wb") as f:
        f.write(content)
    
    # Créer l'activité depuis le GPX
    activite = ActiviteService.creer_activite_depuis_gpx(
        fichier_gpx=fullpath,
        utilisateur_id=utilisateur_id,
        nom=nom,
        type_sport=type_sport,
        description=description
    )
    
    if not activite:
        # Supprimer le fichier en cas d'erreur
        if os.path.exists(fullpath):
            os.remove(fullpath)
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la création de l'activité depuis le GPX"
        )
    
    return activite


@router.post("", response_model=ActiviteOut, status_code=201)
def creer_activite_manuelle(
    activite_data: ActiviteCreate,
    db: Session = Depends(get_db)
):
    """
    Créer une activité manuellement (sans fichier GPX) (F1)
    
    **Paramètres:**
    - **utilisateur_id**: ID de l'utilisateur
    - **nom**: Nom de l'activité
    - **type_sport**: Type de sport
    - **date_activite**: Date (format YYYY-MM-DD)
    - **duree_activite**: Durée en secondes
    - **description**: Description (optionnel)
    - **d_plus**: Dénivelé positif en mètres (optionnel)
    - **calories**: Calories dépensées (optionnel)
    """
    activite = ActiviteService.creer_activite_manuelle(
        utilisateur_id=activite_data.utilisateur_id,
        nom=activite_data.nom,
        type_sport=activite_data.type_sport,
        date_activite=activite_data.date_activite,
        duree_activite=activite_data.duree_activite,
        description=activite_data.description or "",
        d_plus=activite_data.d_plus or 0,
        calories=activite_data.calories or 0
    )
    
    if not activite:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la création de l'activité"
        )
    
    return activite


# ========== CONSULTATION ==========

@router.get("/{activite_id}", response_model=ActiviteOut)
def obtenir_activite(activite_id: int, db: Session = Depends(get_db)):
    """
    Récupérer une activité par son ID
    """
    activite = ActiviteService.obtenir_activite_par_id(activite_id)
    
    if not activite:
        raise HTTPException(
            status_code=404,
            detail="Activité non trouvée"
        )
    
    return activite


@router.get("/utilisateur/{user_id}", response_model=List[ActiviteOut])
def lister_activites_utilisateur(
    user_id: int,
    type_sport: Optional[str] = Query(None, description="Filtrer par sport"),
    date_debut: Optional[date] = Query(None, description="Date de début (YYYY-MM-DD)"),
    date_fin: Optional[date] = Query(None, description="Date de fin (YYYY-MM-DD)"),
    limit: Optional[int] = Query(50, description="Nombre maximum d'activités"),
    db: Session = Depends(get_db)
):
    """
    Lister les activités d'un utilisateur avec filtres (F1)
    
    **Filtres possibles:**
    - **type_sport**: Filtrer par type de sport (Course, Vélo, etc.)
    - **date_debut**: Date de début de la période
    - **date_fin**: Date de fin de la période
    - **limit**: Nombre maximum d'activités à retourner
    
    **Exemples:**
    - `/activites/utilisateur/1` : Toutes les activités de l'utilisateur 1
    - `/activites/utilisateur/1?type_sport=Course` : Seulement les courses
    - `/activites/utilisateur/1?date_debut=2024-01-01&date_fin=2024-12-31` : Activités 2024
    """
    activites = ActiviteService.obtenir_activites_utilisateur(
        utilisateur_id=user_id,
        type_sport=type_sport,
        date_debut=date_debut,
        date_fin=date_fin,
        limit=limit
    )
    
    return activites


# ========== MODIFICATION ==========

@router.put("/{activite_id}", response_model=ActiviteOut)
def modifier_activite(
    activite_id: int,
    activite_data: ActiviteUpdate,
    db: Session = Depends(get_db)
):
    """
    Modifier une activité (F1)
    
    Seuls les champs fournis seront modifiés.
    
    **Champs modifiables:**
    - nom
    - type_sport
    - description
    """
    # Vérifier que l'activité existe
    activite_existante = ActiviteService.obtenir_activite_par_id(activite_id)
    if not activite_existante:
        raise HTTPException(
            status_code=404,
            detail="Activité non trouvée"
        )
    
    # Préparer les modifications
    modifications = activite_data.model_dump(exclude_none=True)
    
    if not modifications:
        raise HTTPException(
            status_code=400,
            detail="Aucune modification fournie"
        )
    
    # Appliquer les modifications
    activite = ActiviteService.modifier_activite(
        activite_id,
        **modifications
    )
    
    if not activite:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la modification"
        )
    
    return activite


# ========== SUPPRESSION ==========

@router.delete("/{activite_id}", response_model=MessageResponse)
def supprimer_activite(activite_id: int, db: Session = Depends(get_db)):
    """
    Supprimer une activité (F1)
    
    **Note:** Cette action est irréversible et supprimera aussi :
    - Tous les likes sur l'activité
    - Tous les commentaires sur l'activité
    """
    # Vérifier que l'activité existe
    activite = ActiviteService.obtenir_activite_par_id(activite_id)
    if not activite:
        raise HTTPException(
            status_code=404,
            detail="Activité non trouvée"
        )
    
    # Supprimer
    resultat = ActiviteService.supprimer_activite(activite_id)
    
    if not resultat:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la suppression"
        )
    
    return MessageResponse(
        message="Activité supprimée avec succès",
        success=True
    )


# ========== STATISTIQUES ==========

@router.get("/utilisateur/{user_id}/count")
def compter_activites(
    user_id: int,
    type_sport: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Compter les activités d'un utilisateur
    
    - **type_sport**: Filtrer par type de sport (optionnel)
    """
    from dao.activite_dao import ActiviteDAO
    
    if type_sport:
        count = ActiviteDAO.count_by_user_and_sport(user_id, type_sport)
    else:
        count = ActiviteDAO.count_by_user(user_id)
    
    return {"utilisateur_id": user_id, "nombre_activites": count}


@router.get("/utilisateur/{user_id}/sports")
def lister_sports_pratiques(user_id: int, db: Session = Depends(get_db)):
    """
    Lister les sports pratiqués par un utilisateur
    """
    from dao.activite_dao import ActiviteDAO
    
    sports = ActiviteDAO.get_sports_list(user_id)
    
    return {"utilisateur_id": user_id, "sports": sports}