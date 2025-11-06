"""
Router pour les statistiques utilisateur (F4)
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, List

from api.schemas import StatistiquesResume, StatistiquesSport, StatistiquesHebdo
from api.lien_dbapi import get_db
from service.statistiques_service import StatistiquesService

router = APIRouter(prefix="/statistiques", tags=["statistiques"])


@router.get("/{user_id}/resume", response_model=StatistiquesResume)
def obtenir_resume_global(user_id: int, db: Session = Depends(get_db)):
    """
    Obtenir le résumé global des statistiques d'un utilisateur
    
    **Retourne:**
    - Nombre total d'activités
    - Durée totale en heures
    - Distance totale en km
    - Calories totales
    - Sports pratiqués
    - Dates première/dernière activité
    - Nombre de jours actifs
    
    **Exemple:**
    ```
    GET /statistiques/1/resume
    ```
    """
    resume = StatistiquesService.obtenir_resume_global(user_id)
    
    if resume['nombre_total_activites'] == 0:
        raise HTTPException(
            status_code=404,
            detail="Aucune activité trouvée pour cet utilisateur"
        )
    
    return resume


@router.get("/{user_id}/hebdomadaire")
def obtenir_statistiques_hebdomadaires(
    user_id: int,
    nb_semaines: int = Query(12, description="Nombre de semaines à analyser"),
    db: Session = Depends(get_db)
):
    """
    Obtenir les statistiques hebdomadaires (F4)
    
    **Retourne pour chaque semaine:**
    - Nombre d'activités par sport
    - Nombre d'heures d'activité
    - Nombre de kilomètres parcourus
    
    **Paramètres:**
    - **user_id**: ID de l'utilisateur
    - **nb_semaines**: Nombre de semaines (défaut: 12)
    
    **Exemple:**
    ```
    GET /statistiques/1/hebdomadaire?nb_semaines=8
    ```
    
    **Réponse:**
    ```json
    {
      "periode_semaines": 12,
      "activites_par_semaine": {
        "2024-W01": {"course": 3, "vélo": 2},
        "2024-W02": {"course": 4}
      },
      "heures_par_semaine": {
        "2024-W01": 5.5,
        "2024-W02": 6.2
      },
      "kilometres_par_semaine": {
        "2024-W01": 42.5,
        "2024-W02": 38.0
      }
    }
    ```
    """
    stats_activites = StatistiquesService.obtenir_activites_par_semaine(
        user_id, nb_semaines
    )
    stats_heures = StatistiquesService.obtenir_heures_par_semaine(
        user_id, nb_semaines
    )
    stats_km = StatistiquesService.obtenir_kilometres_par_semaine(
        user_id, nb_semaines
    )
    
    # Calculer les totaux
    total_activites = sum(sum(v.values()) for v in stats_activites.values())
    total_heures = sum(stats_heures.values())
    total_km = sum(stats_km.values())
    
    return {
        "periode_semaines": nb_semaines,
        "activites_par_semaine": stats_activites,
        "heures_par_semaine": stats_heures,
        "kilometres_par_semaine": stats_km,
        "totaux": {
            "total_activites": total_activites,
            "total_heures": round(total_heures, 1),
            "total_kilometres": round(total_km, 1),
            "moyenne_activites_semaine": round(total_activites / nb_semaines, 1) if nb_semaines > 0 else 0,
            "moyenne_heures_semaine": round(total_heures / nb_semaines, 1) if nb_semaines > 0 else 0,
            "moyenne_km_semaine": round(total_km / nb_semaines, 1) if nb_semaines > 0 else 0
        }
    }


@router.get("/{user_id}/par-sport")
def obtenir_statistiques_par_sport(
    user_id: int,
    nb_semaines: int = Query(12, description="Nombre de semaines à analyser"),
    db: Session = Depends(get_db)
):
    """
    Obtenir les statistiques détaillées par sport
    
    **Retourne pour chaque sport:**
    - Nombre d'activités
    - Durée totale en heures
    - Distance totale en km
    - Dénivelé total
    - Calories totales
    
    **Exemple:**
    ```
    GET /statistiques/1/par-sport?nb_semaines=12
    ```
    
    **Réponse:**
    ```json
    {
      "periode_semaines": 12,
      "statistiques": {
        "course": {
          "nombre_activites": 15,
          "duree_totale_heures": 12.5,
          "distance_totale_km": 85.3,
          "denivele_total": 1250,
          "calories_totales": 8500
        },
        "vélo": {...}
      }
    }
    ```
    """
    stats = StatistiquesService.obtenir_statistiques_par_sport(
        user_id, nb_semaines
    )
    
    if not stats:
        raise HTTPException(
            status_code=404,
            detail="Aucune activité trouvée pour cet utilisateur"
        )
    
    return {
        "periode_semaines": nb_semaines,
        "statistiques": stats
    }


@router.get("/{user_id}/progression/{sport}")
def obtenir_progression(
    user_id: int,
    sport: str,
    nb_semaines: int = Query(12, description="Nombre de semaines à analyser"),
    db: Session = Depends(get_db)
):
    """
    Analyser la progression pour un sport spécifique
    
    Compare les performances entre le début et la fin de la période.
    
    **Paramètres:**
    - **user_id**: ID de l'utilisateur
    - **sport**: Type de sport (Course, Vélo, etc.)
    - **nb_semaines**: Période d'analyse (défaut: 12)
    
    **Exemple:**
    ```
    GET /statistiques/1/progression/Course?nb_semaines=12
    ```
    
    **Réponse:**
    ```json
    {
      "sport": "Course",
      "nombre_activites": 24,
      "moyennes": {
        "debut_periode": {
          "duree_minutes": 45,
          "distance_km": 8.5,
          "calories": 550
        },
        "fin_periode": {
          "duree_minutes": 52,
          "distance_km": 10.2,
          "calories": 650
        }
      },
      "progression": {
        "duree": "+15.6%",
        "distance": "+20.0%",
        "calories": "+18.2%"
      }
    }
    ```
    """
    progression = StatistiquesService.obtenir_progression(
        user_id, sport, nb_semaines
    )
    
    if progression['nombre_activites'] == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Aucune activité de type '{sport}' trouvée"
        )
    
    # Calculer les pourcentages de progression
    if progression['nombre_activites'] >= 2:
        debut = progression['moyennes']['debut_periode']
        fin = progression['moyennes']['fin_periode']
        
        progression['progression'] = {
            "duree": f"{((fin['duree_minutes'] - debut['duree_minutes']) / debut['duree_minutes'] * 100) if debut['duree_minutes'] > 0 else 0:+.1f}%",
            "distance": f"{((fin['distance_km'] - debut['distance_km']) / debut['distance_km'] * 100) if debut['distance_km'] > 0 else 0:+.1f}%",
            "calories": f"{((fin['calories'] - debut['calories']) / debut['calories'] * 100) if debut['calories'] > 0 else 0:+.1f}%"
        }
    
    return progression


@router.get("/{user_id}/records")
def obtenir_records(user_id: int, db: Session = Depends(get_db)):
    """
    Obtenir les records personnels de l'utilisateur
    
    **Retourne pour chaque sport:**
    - Record de durée (activité la plus longue)
    - Record de dénivelé (dénivelé maximal)
    - Record de calories (maximum de calories brûlées)
    
    **Exemple:**
    ```
    GET /statistiques/1/records
    ```
    
    **Réponse:**
    ```json
    {
      "course": {
        "duree_maximale": {
          "valeur": 2.5,
          "activite": "Marathon",
          "date": "2024-10-15"
        },
        "denivele_maximal": {...},
        "calories_maximales": {...}
      }
    }
    ```
    """
    records = StatistiquesService.obtenir_records_personnels(user_id)
    
    if not records:
        raise HTTPException(
            status_code=404,
            detail="Aucun record trouvé pour cet utilisateur"
        )
    
    return records


@router.get("/{user_id}/complet")
def obtenir_statistiques_completes(
    user_id: int,
    nb_semaines: int = Query(12, description="Nombre de semaines à analyser"),
    db: Session = Depends(get_db)
):
    """
    Obtenir toutes les statistiques en une seule requête
    
    Combine :
    - Résumé global
    - Statistiques hebdomadaires
    - Statistiques par sport
    - Records personnels
    
    **Exemple:**
    ```
    GET /statistiques/1/complet?nb_semaines=12
    ```
    """
    stats = StatistiquesService.obtenir_statistiques_completes(
        user_id, nb_semaines
    )
    
    # Ajouter les records
    stats['records'] = StatistiquesService.obtenir_records_personnels(user_id)
    
    # Ajouter le résumé global
    stats['resume_global'] = StatistiquesService.obtenir_resume_global(user_id)
    
    return stats


@router.get("/{user_id}/tableau-bord")
def obtenir_tableau_bord(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtenir un tableau de bord simplifié avec les KPIs principaux
    
    **Retourne:**
    - Nombre d'activités (7 derniers jours, 30 derniers jours, total)
    - Heures d'activité (semaine en cours, mois en cours)
    - Km parcourus (semaine, mois)
    - Sport le plus pratiqué
    - Dernière activité
    
    **Exemple:**
    ```
    GET /statistiques/1/tableau-bord
    ```
    """
    # Stats 7 jours
    stats_7j = StatistiquesService.obtenir_statistiques_completes(user_id, 1)
    stats_30j = StatistiquesService.obtenir_statistiques_completes(user_id, 4)
    resume = StatistiquesService.obtenir_resume_global(user_id)
    stats_sports = StatistiquesService.obtenir_statistiques_par_sport(user_id, 12)
    
    # Sport le plus pratiqué
    sport_favori = None
    if stats_sports:
        sport_favori = max(
            stats_sports.items(),
            key=lambda x: x[1]['nombre_activites']
        )[0]
    
    return {
        "activites": {
            "7_derniers_jours": sum(
                sum(v.values()) 
                for v in stats_7j.get('activites_par_semaine', {}).values()
            ),
            "30_derniers_jours": sum(
                sum(v.values()) 
                for v in stats_30j.get('activites_par_semaine', {}).values()
            ),
            "total": resume.get('nombre_total_activites', 0)
        },
        "heures": {
            "semaine_en_cours": sum(stats_7j.get('heures_par_semaine', {}).values()),
            "mois_en_cours": sum(stats_30j.get('heures_par_semaine', {}).values()),
            "total": resume.get('duree_totale_heures', 0)
        },
        "kilometres": {
            "semaine": sum(stats_7j.get('kilometres_par_semaine', {}).values()),
            "mois": sum(stats_30j.get('kilometres_par_semaine', {}).values()),
            "total": resume.get('distance_totale_km', 0)
        },
        "sport_favori": sport_favori,
        "derniere_activite": resume.get('date_derniere_activite'),
        "jours_actif": resume.get('jours_actif', 0)
    }