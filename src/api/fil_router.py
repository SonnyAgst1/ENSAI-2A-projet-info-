"""
Router pour le fil d'actualité (F2)
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from api.schemas import FilActualiteItem, ActiviteOut, UtilisateurOut
from api.lien_dbapi import get_db
from service.fil_actualite_service import FilActualiteService
from service.activite_service import ActiviteService

router = APIRouter(prefix="/fil", tags=["fil d'actualité"])


@router.get("/{user_id}", response_model=List[FilActualiteItem])
def obtenir_fil_actualite(
    user_id: int,
    nb_jours: int = Query(7, description="Nombre de jours à remonter"),
    limite: int = Query(50, description="Nombre maximum d'activités"),
    db: Session = Depends(get_db)
):
    """
    Obtenir le fil d'actualité d'un utilisateur (F2)
    
    Retourne les activités des utilisateurs suivis par l'utilisateur.
    
    **Paramètres:**
    - **user_id**: ID de l'utilisateur
    - **nb_jours**: Nombre de jours à remonter (défaut: 7)
    - **limite**: Nombre maximum d'activités (défaut: 50)
    
    **Exemple:**
    ```
    GET /fil/1?nb_jours=30&limite=100
    ```
    
    **Réponse:**
    ```json
    [
      {
        "activite": {...},
        "utilisateur": {...},
        "nb_likes": 5,
        "nb_commentaires": 3,
        "user_has_liked": true
      }
    ]
    ```
    """
    fil_data = FilActualiteService.obtenir_fil_actualite(
        utilisateur_id=user_id,
        nb_jours=nb_jours,
        limite=limite
    )
    
    # Formater la réponse avec le statut de like
    fil_response = []
    for item in fil_data:
        user_has_liked = ActiviteService.utilisateur_a_like(
            user_id,
            item['activite'].id
        )
        
        fil_response.append(
            FilActualiteItem(
                activite=item['activite'],
                utilisateur=item['utilisateur'],
                nb_likes=item['nb_likes'],
                nb_commentaires=item['nb_commentaires'],
                user_has_liked=user_has_liked
            )
        )
    
    return fil_response


@router.get("/{user_id}/recentes")
def obtenir_activites_recentes_suivis(
    user_id: int,
    limite: int = Query(20, description="Nombre d'activités"),
    db: Session = Depends(get_db)
):
    """
    Obtenir les activités les plus récentes des utilisateurs suivis
    
    Version simplifiée du fil d'actualité, sans pagination.
    
    **Paramètres:**
    - **user_id**: ID de l'utilisateur
    - **limite**: Nombre maximum d'activités (défaut: 20)
    """
    fil = FilActualiteService.obtenir_fil_actualite(
        utilisateur_id=user_id,
        nb_jours=7,
        limite=limite
    )
    
    return {
        "utilisateur_id": user_id,
        "nombre_activites": len(fil),
        "activites": [
            {
                "activite_id": item['activite'].id,
                "nom": item['activite'].nom,
                "type_sport": item['activite'].type_sport,
                "date": item['activite'].date_activite,
                "auteur_pseudo": item['utilisateur'].pseudo,
                "nb_likes": item['nb_likes'],
                "nb_commentaires": item['nb_commentaires']
            }
            for item in fil
        ]
    }


@router.get("/{user_id}/statistiques")
def obtenir_statistiques_fil(
    user_id: int,
    nb_jours: int = Query(7),
    db: Session = Depends(get_db)
):
    """
    Obtenir des statistiques sur le fil d'actualité
    
    **Retourne:**
    - Nombre total d'activités dans le fil
    - Nombre d'utilisateurs actifs
    - Répartition par sport
    - Total de likes et commentaires
    """
    fil = FilActualiteService.obtenir_fil_actualite(
        utilisateur_id=user_id,
        nb_jours=nb_jours,
        limite=1000
    )
    
    if not fil:
        return {
            "message": "Fil vide",
            "nb_activites": 0
        }
    
    # Calculer les stats
    utilisateurs_actifs = set()
    sports = {}
    total_likes = 0
    total_commentaires = 0
    
    for item in fil:
        utilisateurs_actifs.add(item['utilisateur'].id)
        sport = item['activite'].type_sport
        sports[sport] = sports.get(sport, 0) + 1
        total_likes += item['nb_likes']
        total_commentaires += item['nb_commentaires']
    
    return {
        "periode_jours": nb_jours,
        "nb_activites": len(fil),
        "nb_utilisateurs_actifs": len(utilisateurs_actifs),
        "repartition_sports": sports,
        "total_likes": total_likes,
        "total_commentaires": total_commentaires,
        "moyenne_likes_par_activite": round(total_likes / len(fil), 2) if fil else 0,
        "moyenne_commentaires_par_activite": round(total_commentaires / len(fil), 2) if fil else 0
    }