"""
Router pour les utilisateurs
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import traceback

from api.schemas import (
    UtilisateurCreate, UtilisateurLogin, UtilisateurOut, 
    UtilisateurUpdate, MessageResponse, FollowResponse
)
from api.lien_dbapi import get_db
from service.utilisateur_service import UtilisateurService

router = APIRouter(prefix="/utilisateurs", tags=["utilisateurs"])


@router.post("/inscription", response_model=UtilisateurOut, status_code=201)
def creer_utilisateur(user_data: UtilisateurCreate, db: Session = Depends(get_db)):
    """
    Créer un nouveau compte utilisateur
    
    - **nom**: Nom de famille
    - **prenom**: Prénom
    - **age**: Âge
    - **pseudo**: Pseudo unique
    - **mail**: Email unique
    - **mdp**: Mot de passe
    """
    try:
        # Vérifier si le pseudo existe
        if UtilisateurService.obtenir_utilisateur_par_pseudo(user_data.pseudo):
            raise HTTPException(
                status_code=400,
                detail="Ce pseudo est déjà utilisé"
            )
        
        # Vérifier si l'email existe
        if UtilisateurService.obtenir_utilisateur_par_email(user_data.mail):
            raise HTTPException(
                status_code=400,
                detail="Cet email est déjà utilisé"
            )
        
        # Créer l'utilisateur
        utilisateur = UtilisateurService.creer_utilisateur(
            nom=user_data.nom,
            prenom=user_data.prenom,
            age=user_data.age,
            pseudo=user_data.pseudo,
            mail=user_data.mail,
            mdp=user_data.mdp,
            taille=user_data.taille,
            poids=user_data.poids,
            telephone=user_data.telephone
        )
        
        if not utilisateur:
            raise HTTPException(
                status_code=500,
                detail="Erreur lors de la création du compte"
            )
        
        return utilisateur
    
    except HTTPException:
        # Re-lever les HTTPException
        raise
    except Exception as e:
        # Logger l'erreur complète pour déboguer
        print(f"Erreur inattendue lors de l'inscription: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne: {str(e)}"
        )


@router.post("/connexion", response_model=UtilisateurOut)
def connexion(login_data: UtilisateurLogin, db: Session = Depends(get_db)):
    """
    Se connecter avec pseudo et mot de passe
    
    - **pseudo**: Pseudo de l'utilisateur
    - **mdp**: Mot de passe
    """
    utilisateur = UtilisateurService.connexion(
        login_data.pseudo,
        login_data.mdp
    )
    
    if not utilisateur:
        raise HTTPException(
            status_code=401,
            detail="Identifiants incorrects"
        )
    
    return utilisateur


@router.get("/{user_id}", response_model=UtilisateurOut)
def obtenir_utilisateur(user_id: int, db: Session = Depends(get_db)):
    """Récupérer un utilisateur par son ID"""
    utilisateur = UtilisateurService.obtenir_utilisateur_par_id(user_id)
    
    if not utilisateur:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur non trouvé"
        )
    
    return utilisateur


@router.get("/pseudo/{pseudo}", response_model=UtilisateurOut)
def obtenir_utilisateur_par_pseudo(pseudo: str, db: Session = Depends(get_db)):
    """Rechercher un utilisateur par son pseudo"""
    utilisateur = UtilisateurService.obtenir_utilisateur_par_pseudo(pseudo)
    
    if not utilisateur:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur non trouvé"
        )
    
    return utilisateur


@router.get("", response_model=List[UtilisateurOut])
def lister_utilisateurs(
    recherche: str = None,
    limite: int = 50,
    db: Session = Depends(get_db)
):
    """
    Lister tous les utilisateurs ou rechercher par pseudo
    
    - **recherche**: Filtre de recherche sur le pseudo (optionnel)
    - **limite**: Nombre maximum de résultats (défaut: 50)
    """
    if recherche:
        from service.fil_actualite_service import FilActualiteService
        return FilActualiteService.rechercher_utilisateurs(recherche, limite)
    else:
        return UtilisateurService.obtenir_tous_utilisateurs()[:limite]


@router.put("/{user_id}", response_model=UtilisateurOut)
def modifier_utilisateur(
    user_id: int,
    user_data: UtilisateurUpdate,
    db: Session = Depends(get_db)
):
    """
    Modifier les informations d'un utilisateur
    
    Seuls les champs fournis seront modifiés
    """
    # Préparer les modifications (exclure les valeurs None)
    modifications = user_data.model_dump(exclude_none=True)
    
    if not modifications:
        raise HTTPException(
            status_code=400,
            detail="Aucune modification fournie"
        )
    
    utilisateur = UtilisateurService.modifier_utilisateur(
        user_id,
        **modifications
    )
    
    if not utilisateur:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur non trouvé"
        )
    
    return utilisateur


@router.delete("/{user_id}", response_model=MessageResponse)
def supprimer_utilisateur(user_id: int, db: Session = Depends(get_db)):
    """Supprimer un utilisateur"""
    resultat = UtilisateurService.supprimer_utilisateur(user_id)
    
    if not resultat:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur non trouvé"
        )
    
    return MessageResponse(message="Utilisateur supprimé avec succès")


# ========== FOLLOWS ==========

@router.post("/{user_id}/follow/{followed_id}", response_model=FollowResponse)
def suivre_utilisateur(
    user_id: int,
    followed_id: int,
    db: Session = Depends(get_db)
):
    """
    Suivre un utilisateur
    
    - **user_id**: ID de l'utilisateur qui suit
    - **followed_id**: ID de l'utilisateur à suivre
    """
    if user_id == followed_id:
        raise HTTPException(
            status_code=400,
            detail="Vous ne pouvez pas vous suivre vous-même"
        )
    
    resultat = UtilisateurService.suivre_utilisateur(user_id, followed_id)
    
    if not resultat:
        raise HTTPException(
            status_code=400,
            detail="Vous suivez déjà cet utilisateur"
        )
    
    return FollowResponse(
        success=True,
        following=True,
        nb_followers=UtilisateurService.obtenir_nombre_followers(followed_id),
        nb_following=UtilisateurService.obtenir_nombre_suivis(user_id)
    )


@router.delete("/{user_id}/follow/{followed_id}", response_model=FollowResponse)
def ne_plus_suivre_utilisateur(
    user_id: int,
    followed_id: int,
    db: Session = Depends(get_db)
):
    """
    Ne plus suivre un utilisateur
    
    - **user_id**: ID de l'utilisateur qui suit
    - **followed_id**: ID de l'utilisateur à ne plus suivre
    """
    resultat = UtilisateurService.ne_plus_suivre_utilisateur(user_id, followed_id)
    
    if not resultat:
        raise HTTPException(
            status_code=400,
            detail="Vous ne suivez pas cet utilisateur"
        )
    
    return FollowResponse(
        success=True,
        following=False,
        nb_followers=UtilisateurService.obtenir_nombre_followers(followed_id),
        nb_following=UtilisateurService.obtenir_nombre_suivis(user_id)
    )


@router.get("/{user_id}/following", response_model=List[UtilisateurOut])
def obtenir_utilisateurs_suivis(user_id: int, db: Session = Depends(get_db)):
    """Récupérer la liste des utilisateurs suivis"""
    return UtilisateurService.obtenir_utilisateurs_suivis(user_id)


@router.get("/{user_id}/followers", response_model=List[UtilisateurOut])
def obtenir_followers(user_id: int, db: Session = Depends(get_db)):
    """Récupérer la liste des followers"""
    return UtilisateurService.obtenir_followers(user_id)


@router.get("/{user_id}/suggestions", response_model=List[UtilisateurOut])
def obtenir_suggestions(
    user_id: int,
    limite: int = 10,
    db: Session = Depends(get_db)
):
    """
    Obtenir des suggestions d'utilisateurs à suivre
    
    - **limite**: Nombre de suggestions (défaut: 10)
    """
    from service.fil_actualite_service import FilActualiteService
    return FilActualiteService.obtenir_suggestions_utilisateurs(user_id, limite)