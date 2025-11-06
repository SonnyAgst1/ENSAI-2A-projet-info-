#A renommé schema ( schema Pydantic )
# Schema Pydantic sont des modèles de Validation de donnée, permettent de ne validé automatique les données
#sans passé par des if. 

"""
Schémas Pydantic pour l'API
"""
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, EmailStr


# ========== UTILISATEUR ==========

class UtilisateurCreate(BaseModel):
    """Schéma pour créer un utilisateur"""
    nom: str
    prenom: str
    age: int
    pseudo: str
    mail: EmailStr
    mdp: str
    taille: Optional[float] = None
    poids: Optional[float] = None
    telephone: Optional[int] = None


class UtilisateurLogin(BaseModel):
    """Schéma pour la connexion"""
    pseudo: str
    mdp: str


class UtilisateurOut(BaseModel):
    """Schéma de sortie pour un utilisateur"""
    id: int
    nom: str
    prenom: str
    age: int
    pseudo: str
    mail: str
    taille: Optional[float] = None
    poids: Optional[float] = None
    telephone: Optional[int] = None

    model_config = dict(from_attributes=True)


class UtilisateurUpdate(BaseModel):
    """Schéma pour modifier un utilisateur"""
    nom: Optional[str] = None
    prenom: Optional[str] = None
    age: Optional[int] = None
    pseudo: Optional[str] = None
    taille: Optional[float] = None
    poids: Optional[float] = None
    telephone: Optional[int] = None


# ========== ACTIVITÉ ==========

class ActiviteCreate(BaseModel):
    """Schéma pour créer une activité manuelle"""
    utilisateur_id: int
    nom: str
    type_sport: str
    date_activite: date
    duree_activite: int  # en secondes
    description: Optional[str] = None
    d_plus: Optional[int] = None
    calories: Optional[int] = None


class ActiviteOut(BaseModel):
    """Schéma de sortie pour une activité"""
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

    model_config = dict(from_attributes=True)


class ActiviteWithUser(ActiviteOut):
    """Activité avec infos utilisateur (pour le fil)"""
    utilisateur: UtilisateurOut
    nb_likes: int
    nb_commentaires: int

    model_config = dict(from_attributes=True)


class ActiviteUpdate(BaseModel):
    """Schéma pour modifier une activité"""
    nom: Optional[str] = None
    type_sport: Optional[str] = None
    description: Optional[str] = None


# ========== COMMENTAIRE ==========

class CommentaireCreate(BaseModel):
    """Schéma pour créer un commentaire"""
    contenu: str


class CommentaireOut(BaseModel):
    """Schéma de sortie pour un commentaire"""
    id: int
    contenu: str
    activite_id: int
    auteur_id: int
    auteur: UtilisateurOut

    model_config = dict(from_attributes=True)


# ========== LIKE ==========

class LikeResponse(BaseModel):
    """Réponse après un like/unlike"""
    success: bool
    liked: bool
    nb_likes: int


# ========== FOLLOW ==========

class FollowResponse(BaseModel):
    """Réponse après un follow/unfollow"""
    success: bool
    following: bool
    nb_followers: int
    nb_following: int


# ========== STATISTIQUES ==========

class StatistiquesResume(BaseModel):
    """Résumé global des statistiques"""
    nombre_total_activites: int
    duree_totale_heures: float
    distance_totale_km: float
    calories_totales: int
    sports_pratiques: List[str]
    date_premiere_activite: Optional[str] = None
    date_derniere_activite: Optional[str] = None
    jours_actif: int


class StatistiquesSport(BaseModel):
    """Statistiques pour un sport"""
    nombre_activites: int
    duree_totale_heures: float
    distance_totale_km: float
    calories_totales: int
    denivele_total: int


class StatistiquesHebdo(BaseModel):
    """Statistiques hebdomadaires"""
    semaine: str
    nb_activites: int
    heures: float
    kilometres: float


# ========== FIL D'ACTUALITÉ ==========

class FilActualiteItem(BaseModel):
    """Item du fil d'actualité"""
    activite: ActiviteOut
    utilisateur: UtilisateurOut
    nb_likes: int
    nb_commentaires: int
    user_has_liked: bool


# ========== MESSAGES ==========

class MessageResponse(BaseModel):
    """Message de réponse générique"""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Message d'erreur"""
    detail: str

