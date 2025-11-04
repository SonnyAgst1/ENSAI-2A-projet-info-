# api/schemas.py
from datetime import date
from typing import Optional
from pydantic import BaseModel


class ActiviteOut(BaseModel):
    id: int
    nom: str
    type_sport: str
    date_activite: date
    duree_activite: Optional[int] = None
    description: Optional[str] = None
    d_plus: Optional[int] = None
    calories: Optional[int] = None
    utilisateur_id: int
    gpx_path: Optional[str] = None

    model_config = dict(from_attributes=True)  # Pydantic v2
