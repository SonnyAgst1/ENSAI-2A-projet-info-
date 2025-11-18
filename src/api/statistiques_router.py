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


@router.get("/{user_id}/complet")
def obtenir_statistiques_completes(
    user_id: int,
    nb_semaines: int = Query(12, description="Nombre de semaines à analyser"),
    sections: str = Query(
        "resume,hebdo,sports,records,progression,tableau_bord",
        description="Sections à inclure (séparées par virgules): resume,hebdo,sports,records,progression,tableau_bord"
    ),
    sports: str = Query(
        None,
        description="Sports pour la progression (séparés par virgules). Si non spécifié, analyse tous les sports"
    ),
    db: Session = Depends(get_db)
):
    """
    Obtenir toutes les statistiques en une seule requête avec sections sélectives
    
    Sections disponibles:
    - resume: Résumé global (activités totales, durée, distance, calories, etc.)
    - hebdo: Statistiques hebdomadaires (activités, heures, km par semaine)
    - sports: Statistiques détaillées par sport
    - records: Records personnels par sport
    - progression: Analyse de progression (nécessite paramètre sports)
    -*tableau_bord: KPIs simplifiés (7j, 30j, totaux)
    

    """
    sections_list = [s.strip() for s in sections.split(',')]
    result = {}
    
    # Résumé global
    if 'resume' in sections_list:
        result['resume_global'] = StatistiquesService.obtenir_resume_global(user_id)
    
    # Statistiques hebdomadaires
    if 'hebdo' in sections_list:
        stats_activites = StatistiquesService.obtenir_activites_par_semaine(
            user_id, nb_semaines
        )
        stats_heures = StatistiquesService.obtenir_heures_par_semaine(
            user_id, nb_semaines
        )
        stats_km = StatistiquesService.obtenir_kilometres_par_semaine(
            user_id, nb_semaines
        )
        
        total_activites = sum(sum(v.values()) for v in stats_activites.values())
        total_heures = sum(stats_heures.values())
        total_km = sum(stats_km.values())
        
        result['hebdomadaire'] = {
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
    
    # Statistiques par sport
    if 'sports' in sections_list:
        stats = StatistiquesService.obtenir_statistiques_par_sport(
            user_id, nb_semaines
        )
        result['par_sport'] = {
            "periode_semaines": nb_semaines,
            "statistiques": stats
        }
    
    # Records personnels
    if 'records' in sections_list:
        result['records'] = StatistiquesService.obtenir_records_personnels(user_id)
    
    # Progression par sport
    if 'progression' in sections_list:
        progressions = {}
        
        if sports:
            # Sports spécifiés
            sports_list = [s.strip() for s in sports.split(',')]
        else:
            # Tous les sports de l'utilisateur
            stats_sports = StatistiquesService.obtenir_statistiques_par_sport(
                user_id, nb_semaines
            )
            sports_list = list(stats_sports.keys()) if stats_sports else []
        
        for sport in sports_list:
            progression = StatistiquesService.obtenir_progression(
                user_id, sport, nb_semaines
            )
            
            if progression['nombre_activites'] >= 2:
                debut = progression['moyennes']['debut_periode']
                fin = progression['moyennes']['fin_periode']
                
                progression['progression'] = {
                    "duree": f"{((fin['duree_minutes'] - debut['duree_minutes']) / debut['duree_minutes'] * 100) if debut['duree_minutes'] > 0 else 0:+.1f}%",
                    "distance": f"{((fin['distance_km'] - debut['distance_km']) / debut['distance_km'] * 100) if debut['distance_km'] > 0 else 0:+.1f}%",
                    "calories": f"{((fin['calories'] - debut['calories']) / debut['calories'] * 100) if debut['calories'] > 0 else 0:+.1f}%"
                }
            
            if progression['nombre_activites'] > 0:
                progressions[sport] = progression
        
        result['progressions'] = progressions
    
    # Tableau de bord
    if 'tableau_bord' in sections_list:
        stats_7j = StatistiquesService.obtenir_statistiques_completes(user_id, 1)
        stats_30j = StatistiquesService.obtenir_statistiques_completes(user_id, 4)
        resume = StatistiquesService.obtenir_resume_global(user_id)
        stats_sports = StatistiquesService.obtenir_statistiques_par_sport(user_id, 12)
        
        sport_favori = None
        if stats_sports:
            sport_favori = max(
                stats_sports.items(),
                key=lambda x: x[1]['nombre_activites']
            )[0]
        
        result['tableau_bord'] = {
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
    
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Aucune section valide spécifiée"
        )
    
    return result


