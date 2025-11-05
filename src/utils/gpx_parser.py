import gpxpy
import gpxpy.gpx
from datetime import timedelta, datetime
import os

def analyser_gpx(chemin_fichier):
    """Analyse un fichier GPX et retourne la durée, la distance et le dénivelé."""
    try:
        with open(chemin_fichier, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
    except Exception as e:
        print(f"❌ Erreur de lecture GPX : {e}")
        return None

    # Calcul de la distance
    distance_2d = gpx.length_2d() # Distance en mètres
    distance_km = distance_2d / 1000

    # Calcul de la durée
    duree = gpx.get_duration() # Durée en secondes

    # Calcul du dénivelé positif
    up, down = gpx.get_elevation_extremes() # Dénivelé n'est pas toujours fiable/simple

    # Méthode plus robuste pour le dénivelé positif (somme des montées)
    denivele_positif = gpx.get_uphill_downhill().uphill

    # Point de départ (date et heure)
    start_time = gpx.get_time_bounds().start_time

    return {
        'distance': distance_km,
        'duree_secondes': duree,
        'denivele_positif': denivele_positif,
        'date_debut': start_time
    }