import os
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from business_objects.models import Activite
from api.entree import ActiviteOut
from api.lien_dbapi import get_db

activites_router = APIRouter()


@activites_router.get("/activites")
def get_activites():
    return {"message": "Liste des activités"}


router = APIRouter(prefix="/activites", tags=["activites"])
UPLOAD_DIR = "uploads/gpx"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _safe_filename(s: str) -> str:
    return "".join(c if c.isalnum() or c in ("_", "-", ".", "@") else "_" for c in s)


@router.post("", response_model=ActiviteOut, status_code=201)
async def create_activite_with_gpx(
    utilisateur_id: int = Form(...),
    nom: str = Form(...),
    type_sport: str = Form(...),
    date_activite: date = Form(...),
    duree_activite: Optional[int] = Form(None),   # minutes
    description: Optional[str] = Form(None),
    d_plus: Optional[int] = Form(None),
    calories: Optional[int] = Form(None),
    gpx: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    # (Option) vérifier que l'utilisateur_id == user connecté ici

    gpx_path = None
    if gpx:
        # 1) Validations basiques
        if not gpx.filename.lower().endswith(".gpx"):
            raise HTTPException(status_code=400, detail="Le fichier doit être un .gpx")
        
        # 2) Nom de fichier unique & sûr
        fname = _safe_filename(f"{utilisateur_id}_{date_activite}_{gpx.filename}")
        fullpath = os.path.join(UPLOAD_DIR, fname)
        
        # 3) Sauvegarde du fichier sur le disque
        content = await gpx.read()
        with open(fullpath, "wb") as f:
            f.write(content)
        
        # 4) Stocker le chemin relatif (pas le chemin absolu complet)
        gpx_path = fullpath  # ou juste fname si vous préférez relatif

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
    db.add(a)
    db.commit()
    db.refresh(a)
    return a
