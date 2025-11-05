import os

from typing import BinaryIO

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from business_objects.models import Activite
from .entree import ActiviteOut
from .lien_dbapi import get_db
from database import SessionDep
import gpxpy

activites_router = APIRouter()


@router.post("", status_code=201)
async def create_activite_with_gpx(
    db:SessionDep,
    utilisateur_id: int = Form(...),
    nom: str = Form(...),
    gpx: UploadFile = File(...),
) -> str:
    print(f"Nom user:{nom}, nom de ficher {gpx.filename}, user_id:{utilisateur_id}")
    await save_gpx(gpx.file, filename=gpx.filename)
    #activity_duration = gpxpy.parse(gpx.read()).get_duration()

    a = Activite(nom=nom, gpx_path = gpx.filename, duree_activite=54.25)
    db.add(a)
    db.commit()
    db.refresh(a)
    
    # (Option) vérifier que l'utilisateur_id == user connecté ici

    """

    # 4) création DB
    a = Activite(
        utilisateur_id=utilisateur_id,
        nom=nom,
        type_sport=type_sport,
        date_activite=date_activite,
        duree_activite=duree_activite,
        description=description,
        d_plus=d_plus,
        calories=calories,
        gpx_path=gpx_path,
    )
    
    """
    return "ok"


@activites_router.get("/activites")
def get_activites():
    return {"message": "Liste des activités"}


router = APIRouter(prefix="/api/activites", tags=["activites"])
UPLOAD_DIR = "uploads/gpx"
os.makedirs(UPLOAD_DIR, exist_ok=True)

##def _safe_filename(s: str) -> str:
##    return "".join(c if c.isalnum() or c in ("_", "-", ".", "@") else "_" for c in s)

def parse_strava_gpx(content):
    gpx = gpxpy.parse(content)
    # Distance totale en 3D (mètres)
    distance_m = gpx.length_3d()

    # Durée totale (secondes)
    duration_s = gpx.get_duration()

    # Temps/distance/vitesse en mouvement
    moving = gpx.get_moving_data()

    return {
        "nom": gpx.tracks[0].name,
        "type": gpx.tracks[0].type,
        "distance totale": distance_m/1000,
        "durée totale": duration_s/60,
        "temps en mouvement": moving.moving_time/60,
        "distance en mouvement": moving.moving_distance/1000,
        "vitesse moyenne": moving.moving_distance/moving.moving_time*3.6,
        "vitesse max": moving.max_speed*3.6
    }


def is_file_correct(file:UploadFile) -> bool:
    gpx_path = None
    if gpx:
        # 1) Validations basiques
        if not gpx.filename.lower().endswith(".gpx"):
            raise HTTPException(status_code=400, detail="Le fichier doit être un .gpx")

        # 4) Stocker le chemin relatif (pas le chemin absolu complet)
        gpx_path = fullpath  # ou juste fname si vous préférez relatif

async def save_gpx(file:BinaryIO, filename:str):
    fullpath = os.path.join(UPLOAD_DIR, filename)
    with open(fullpath, "wb") as f:
        f.write(file.read())


@router.post("", status_code=201)
async def create_activite_with_gpx(
    db:SessionDep,
    utilisateur_id: int = Form(...),
    nom: str = Form(...),
    gpx: UploadFile = File(...),
) -> str:
    print(f"Nom user:{nom}, nom de ficher {gpx.filename}, user_id:{utilisateur_id}")
    await save_gpx(gpx.file, filename=gpx.filename)
    #activity_duration = gpxpy.parse(gpx.read()).get_duration()

    a = Activite(nom=nom, gpx_path = gpx.filename, duree_activite=54.25)
    db.add(a)
    db.commit()
    db.refresh(a)
    
    # (Option) vérifier que l'utilisateur_id == user connecté ici

    """

    # 4) création DB
    a = Activite(
        utilisateur_id=utilisateur_id,
        nom=nom,
        type_sport=type_sport,
        date_activite=date_activite,
        duree_activite=duree_activite,
        description=description,
        d_plus=d_plus,
        calories=calories,
        gpx_path=gpx_path,
    )
    
    """
    return "ok"
