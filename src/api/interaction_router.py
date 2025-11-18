"""
Router pour les interactions sociales - Likes et Commentaires (F3)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from api.schemas import (
    LikeResponse, CommentaireCreate, CommentaireOut, MessageResponse
)
from api.lien_dbapi import get_db
from service.activite_service import ActiviteService

router = APIRouter(prefix="/interactions", tags=["interactions"])


# ========== LIKES ==========

@router.post("/activites/{activite_id}/like/{user_id}", response_model=LikeResponse)
def liker_activite(
    activite_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Liker une activité (F3)
    
    **Paramètres:**
    - **activite_id**: ID de l'activité à liker
    - **user_id**: ID de l'utilisateur qui like
    
    **Retourne:**
    - success: Opération réussie
    - liked: État actuel (true si liké)
    - nb_likes: Nombre total de likes
    
    """
    # Vérifier que l'activité existe
    activite = ActiviteService.obtenir_activite_par_id(activite_id)
    if not activite:
        raise HTTPException(
            status_code=404,
            detail="Activité non trouvée"
        )
    
    # Liker
    resultat = ActiviteService.liker_activite(user_id, activite_id)
    
    if not resultat:
        raise HTTPException(
            status_code=400,
            detail="Vous avez déjà liké cette activité"
        )
    
    # Récupérer le nombre de likes
    nb_likes = ActiviteService.obtenir_nombre_likes(activite_id)
    
    return LikeResponse(
        success=True,
        liked=True,
        nb_likes=nb_likes
    )


@router.delete("/activites/{activite_id}/like/{user_id}", response_model=LikeResponse)
def unliker_activite(
    activite_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Retirer son like d'une activité (F3)
    
    **Paramètres:**
    - **activite_id**: ID de l'activité
    - **user_id**: ID de l'utilisateur
    
    """
    # Vérifier que l'activité existe
    activite = ActiviteService.obtenir_activite_par_id(activite_id)
    if not activite:
        raise HTTPException(
            status_code=404,
            detail="Activité non trouvée"
        )
    
    # Unliker
    resultat = ActiviteService.unliker_activite(user_id, activite_id)
    
    if not resultat:
        raise HTTPException(
            status_code=400,
            detail="Vous n'avez pas liké cette activité"
        )
    
    # Récupérer le nombre de likes
    nb_likes = ActiviteService.obtenir_nombre_likes(activite_id)
    
    return LikeResponse(
        success=True,
        liked=False,
        nb_likes=nb_likes
    )


@router.get("/activites/{activite_id}/likes")
def obtenir_likes_activite(
    activite_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtenir le nombre de likes et la liste des utilisateurs qui ont liké
    
    **Retourne:**
    ```json
    {
      "activite_id": 42,
      "nb_likes": 5,
      "utilisateurs": [...]
    }
    ```
    """
    from dao.like_dao import LikeDAO
    
    # Vérifier que l'activité existe
    activite = ActiviteService.obtenir_activite_par_id(activite_id)
    if not activite:
        raise HTTPException(
            status_code=404,
            detail="Activité non trouvée"
        )
    
    nb_likes = LikeDAO.count_by_activite(activite_id)
    utilisateurs = LikeDAO.get_users_who_liked(activite_id)
    
    return {
        "activite_id": activite_id,
        "nb_likes": nb_likes,
        "utilisateurs": [
            {
                "id": u.id,
                "pseudo": u.pseudo,
                "nom": f"{u.prenom} {u.nom}"
            }
            for u in utilisateurs
        ]
    }


@router.get("/activites/{activite_id}/like/{user_id}")
def verifier_like(
    activite_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Vérifier si un utilisateur a liké une activité
    
    ```
    """
    has_liked = ActiviteService.utilisateur_a_like(user_id, activite_id)
    
    return {
        "activite_id": activite_id,
        "user_id": user_id,
        "has_liked": has_liked
    }


# ========== COMMENTAIRES ==========

@router.post("/activites/{activite_id}/commentaires/{user_id}", 
             response_model=CommentaireOut, 
             status_code=201)
def ajouter_commentaire(
    activite_id: int,
    user_id: int,
    commentaire_data: CommentaireCreate,
    db: Session = Depends(get_db)
):
    """
    Ajouter un commentaire sur une activité (F3)
    
    **Paramètres:**
    - **activite_id**: ID de l'activité
    - **user_id**: ID de l'utilisateur qui commente
    - **contenu**: Contenu du commentaire (dans le body)
    
    """
    # Vérifier que l'activité existe
    activite = ActiviteService.obtenir_activite_par_id(activite_id)
    if not activite:
        raise HTTPException(
            status_code=404,
            detail="Activité non trouvée"
        )
    
    # Vérifier que le contenu n'est pas vide
    if not commentaire_data.contenu.strip():
        raise HTTPException(
            status_code=400,
            detail="Le contenu du commentaire ne peut pas être vide"
        )
    
    # Ajouter le commentaire
    commentaire = ActiviteService.ajouter_commentaire(
        utilisateur_id=user_id,
        activite_id=activite_id,
        contenu=commentaire_data.contenu
    )
    
    if not commentaire:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de l'ajout du commentaire"
        )
    
    return commentaire


@router.get("/activites/{activite_id}/commentaires", response_model=List[CommentaireOut])
def obtenir_commentaires(
    activite_id: int,
    limite: int = 50,
    db: Session = Depends(get_db)
):
    """
    Obtenir tous les commentaires d'une activité (F3)
    
    **Paramètres:**
    - **activite_id**: ID de l'activité
    - **limite**: Nombre maximum de commentaires (défaut: 50)

    """
    # Vérifier que l'activité existe
    activite = ActiviteService.obtenir_activite_par_id(activite_id)
    if not activite:
        raise HTTPException(
            status_code=404,
            detail="Activité non trouvée"
        )
    
    commentaires = ActiviteService.obtenir_commentaires_activite(activite_id)
    
    return commentaires[:limite]


@router.put("/commentaires/{commentaire_id}", response_model=CommentaireOut)
def modifier_commentaire(
    commentaire_id: int,
    commentaire_data: CommentaireCreate,
    db: Session = Depends(get_db)
):
    """
    Modifier un commentaire
    
    """
    # Vérifier que le contenu n'est pas vide
    if not commentaire_data.contenu.strip():
        raise HTTPException(
            status_code=400,
            detail="Le contenu du commentaire ne peut pas être vide"
        )
    
    commentaire = ActiviteService.modifier_commentaire(
        commentaire_id,
        commentaire_data.contenu
    )
    
    if not commentaire:
        raise HTTPException(
            status_code=404,
            detail="Commentaire non trouvé"
        )
    
    return commentaire


@router.delete("/commentaires/{commentaire_id}", response_model=MessageResponse)
def supprimer_commentaire(
    commentaire_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprimer un commentaire
     Seul l'auteur du commentaire devrait pouvoir le supprimer.
    
    """
    resultat = ActiviteService.supprimer_commentaire(commentaire_id)
    
    if not resultat:
        raise HTTPException(
            status_code=404,
            detail="Commentaire non trouvé"
        )
    
    return MessageResponse(
        message="Commentaire supprimé avec succès",
        success=True
    )


@router.get("/activites/{activite_id}/commentaires/count")
def compter_commentaires(
    activite_id: int,
    db: Session = Depends(get_db)
):
    """
    Compter le nombre de commentaires d'une activité
    
    """
    nb_commentaires = ActiviteService.obtenir_nombre_commentaires(activite_id)
    
    return {
        "activite_id": activite_id,
        "nb_commentaires": nb_commentaires
    }
    