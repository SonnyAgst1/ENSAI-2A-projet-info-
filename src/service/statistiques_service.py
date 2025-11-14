"""
Service pour la gestion des statistiques utilisateur (F4)
"""
from typing import Dict, List
from datetime import date, datetime, timedelta
from collections import defaultdict
from sqlalchemy import func, and_

from database import SessionLocal
from business_objects.models import Activite


class StatistiquesService:
    """Service pour gérer les statistiques utilisateur"""

    @staticmethod
    def obtenir_activites_par_semaine(
        utilisateur_id: int,
        nombre_semaines: int = 12
    ) -> Dict[str, Dict[str, int]]:
        """
        Calcule le nombre d'activités par semaine et par sport

        Args:
            utilisateur_id: ID de l'utilisateur
            nombre_semaines: Nombre de semaines à analyser (par défaut 12)

        Returns:
            Dictionnaire {
                'semaine_2024-W01': {'course': 3, 'vélo': 2},
                'semaine_2024-W02': {'course': 4, 'natation': 1},
                ...
            }
        """
        db = SessionLocal()
        try:
            date_debut = date.today() - timedelta(weeks=nombre_semaines)

            activites = db.query(Activite).filter(
                and_(
                    Activite.utilisateur_id == utilisateur_id,
                    Activite.date_activite >= date_debut
                )
            ).all()

            # Organiser par semaine et par sport
            stats = defaultdict(lambda: defaultdict(int))

            for activite in activites:
                # Calculer le numéro de semaine ISO
                annee, semaine, _ = activite.date_activite.isocalendar()
                cle_semaine = f"{annee}-W{semaine:02d}"

                # Incrémenter le compteur pour ce sport
                stats[cle_semaine][activite.type_sport] += 1

            # Convertir en dictionnaire normal
            return {semaine: dict(sports) for semaine, sports in stats.items()}

        finally:
            db.close()

    @staticmethod
    def obtenir_kilometres_par_semaine(
        utilisateur_id: int,
        nombre_semaines: int = 12
    ) -> Dict[str, float]:
        """
        Calcule le nombre de kilomètres parcourus par semaine

        Args:
            utilisateur_id: ID de l'utilisateur
            nombre_semaines: Nombre de semaines à analyser

        Returns:
            Dictionnaire {'semaine_2024-W01': 42.5, 'semaine_2024-W02': 38.2, ...}
        """
        db = SessionLocal()
        try:
            date_debut = date.today() - timedelta(weeks=nombre_semaines)

            activites = db.query(Activite).filter(
                and_(
                    Activite.utilisateur_id == utilisateur_id,
                    Activite.date_activite >= date_debut,
                    Activite.distance.isnot(None)
                )
            ).all()

            # Organiser par semaine
            stats = defaultdict(float)

            for activite in activites:
                annee, semaine, _ = activite.date_activite.isocalendar()
                cle_semaine = f"{annee}-W{semaine:02d}"

                # d_plus représente le dénivelé, pas la distance
                # Pour avoir la distance, il faudrait l'extraire du fichier GPX
                # Ici on utilise d_plus comme proxy (à adapter selon vos besoins)
                if activite.distance:
                    stats[cle_semaine] += activite.distance / 1000.0  # Convertir en km

            return dict(stats)

        finally:
            db.close()

    @staticmethod
    def obtenir_heures_par_semaine(
        utilisateur_id: int,
        nombre_semaines: int = 12
    ) -> Dict[str, float]:
        """
        Calcule le nombre d'heures d'activité par semaine

        Args:
            utilisateur_id: ID de l'utilisateur
            nombre_semaines: Nombre de semaines à analyser

        Returns:
            Dictionnaire {'semaine_2024-W01': 8.5, 'semaine_2024-W02': 10.2, ...}
        """
        db = SessionLocal()
        try:
            date_debut = date.today() - timedelta(weeks=nombre_semaines)

            activites = db.query(Activite).filter(
                and_(
                    Activite.utilisateur_id == utilisateur_id,
                    Activite.date_activite >= date_debut,
                    Activite.duree_activite.isnot(None)
                )
            ).all()

            # Organiser par semaine
            stats = defaultdict(float)

            for activite in activites:
                annee, semaine, _ = activite.date_activite.isocalendar()
                cle_semaine = f"{annee}-W{semaine:02d}"

                # Convertir les secondes en heures
                if activite.duree_activite:
                    heures = activite.duree_activite / 3600.0
                    stats[cle_semaine] += heures

            return dict(stats)

        finally:
            db.close()

    @staticmethod
    def obtenir_statistiques_completes(
        utilisateur_id: int,
        nombre_semaines: int = 12
    ) -> Dict:
        """
        Récupère toutes les statistiques en une seule fois

        Args:
            utilisateur_id: ID de l'utilisateur
            nombre_semaines: Nombre de semaines à analyser

        Returns:
            Dictionnaire avec toutes les statistiques
        """
        return {
            'activites_par_semaine': StatistiquesService.obtenir_activites_par_semaine(
                utilisateur_id, nombre_semaines
            ),
            'kilometres_par_semaine': StatistiquesService.obtenir_kilometres_par_semaine(
                utilisateur_id, nombre_semaines
            ),
            'heures_par_semaine': StatistiquesService.obtenir_heures_par_semaine(
                utilisateur_id, nombre_semaines
            ),
            'periode_analyse': {
                'date_debut': (date.today() - timedelta(weeks=nombre_semaines)).isoformat(),
                'date_fin': date.today().isoformat(),
                'nombre_semaines': nombre_semaines
            }
        }

    @staticmethod
    def obtenir_statistiques_par_sport(
        utilisateur_id: int,
        nombre_semaines: int = 12
    ) -> Dict[str, Dict]:
        """
        Calcule les statistiques détaillées par type de sport

        Args:
            utilisateur_id: ID de l'utilisateur
            nombre_semaines: Nombre de semaines à analyser

        Returns:
            Dictionnaire {
                'course': {
                    'nombre_activites': 15,
                    'duree_totale_heures': 12.5,
                    'distance_totale_km': 85.3,
                    'calories_totales': 8500
                },
                'vélo': {...},
                ...
            }
        """
        db = SessionLocal()
        try:
            date_debut = date.today() - timedelta(weeks=nombre_semaines)

            activites = db.query(Activite).filter(
                and_(
                    Activite.utilisateur_id == utilisateur_id,
                    Activite.date_activite >= date_debut
                )
            ).all()

            # Organiser par sport
            stats = defaultdict(lambda: {
                'nombre_activites': 0,
                'duree_totale_heures': 0.0,
                'distance_totale_km': 0.0,
                'calories_totales': 0,
                'denivele_total': 0
            })

            for activite in activites:
                sport = activite.type_sport
                stats[sport]['nombre_activites'] += 1

                if activite.duree_activite:
                    stats[sport]['duree_totale_heures'] += activite.duree_activite / 3600.0

                if activite.distance:
                    stats[sport]['distance_totale_km'] += activite.distance / 1000.0
                    stats[sport]['denivele_total'] += activite.d_plus

                if activite.calories:
                    stats[sport]['calories_totales'] += activite.calories

            return dict(stats)

        finally:
            db.close()

    @staticmethod
    def obtenir_progression(
        utilisateur_id: int,
        type_sport: str,
        nombre_semaines: int = 12
    ) -> Dict:
        """
        Calcule la progression pour un sport spécifique

        Args:
            utilisateur_id: ID de l'utilisateur
            type_sport: Type de sport à analyser
            nombre_semaines: Nombre de semaines à analyser

        Returns:
            Dictionnaire avec les données de progression
        """
        db = SessionLocal()
        try:
            date_debut = date.today() - timedelta(weeks=nombre_semaines)

            activites = db.query(Activite).filter(
                and_(
                    Activite.utilisateur_id == utilisateur_id,
                    Activite.type_sport == type_sport,
                    Activite.date_activite >= date_debut
                )
            ).order_by(Activite.date_activite).all()

            if not activites:
                return {
                    'sport': type_sport,
                    'activites': [],
                    'progression': None
                }

            # Extraire les données pour chaque activité
            progression = []
            for activite in activites:
                progression.append({
                    'date': activite.date_activite.isoformat(),
                    'duree_minutes': activite.duree_activite / 60 if activite.duree_activite else 0,
                    'distance_km': activite.distance/ 1000 if activite.distance else 0,
                    'calories': activite.calories or 0
                })

            # Calculer les moyennes sur les 4 premières et 4 dernières semaines
            milieu = len(progression) // 2
            debut = progression[:milieu]
            fin = progression[milieu:]

            def moyenne(liste, cle):
                valeurs = [x[cle] for x in liste if x[cle] > 0]
                return sum(valeurs) / len(valeurs) if valeurs else 0

            return {
                'sport': type_sport,
                'nombre_activites': len(progression),
                'activites': progression,
                'moyennes': {
                    'debut_periode': {
                        'duree_minutes': moyenne(debut, 'duree_minutes'),
                        'distance_km': moyenne(debut, 'distance_km'),
                        'calories': moyenne(debut, 'calories')
                    },
                    'fin_periode': {
                        'duree_minutes': moyenne(fin, 'duree_minutes'),
                        'distance_km': moyenne(fin, 'distance_km'),
                        'calories': moyenne(fin, 'calories')
                    }
                }
            }

        finally:
            db.close()

    @staticmethod
    def obtenir_records_personnels(utilisateur_id: int) -> Dict:
        """
        Récupère les records personnels de l'utilisateur

        Args:
            utilisateur_id: ID de l'utilisateur

        Returns:
            Dictionnaire avec les records par type
        """
        db = SessionLocal()
        try:
            activites = db.query(Activite).filter(
                Activite.utilisateur_id == utilisateur_id
            ).all()

            if not activites:
                return {}

            records = {}

            # Organiser par sport
            par_sport = defaultdict(list)
            for activite in activites:
                par_sport[activite.type_sport].append(activite)

            # Trouver les records pour chaque sport
            for sport, activites_sport in par_sport.items():
                # Durée la plus longue
                activite_plus_longue = max(
                    activites_sport,
                    key=lambda a: a.duree_activite or 0
                )

                # Plus de dénivelé
                activite_plus_denivele = max(
                    activites_sport,
                    key=lambda a: a.d_plus or 0
                )

                # Plus de calories
                activite_plus_calories = max(
                    activites_sport,
                    key=lambda a: a.calories or 0
                )

                records[sport] = {
                    'duree_maximale': {
                        'valeur': (
                            activite_plus_longue.duree_activite / 3600
                            if activite_plus_longue.duree_activite
                            else 0
                        ),

                        'date': activite_plus_longue.date_activite.isoformat(),
                        'activite': activite_plus_longue.nom
                    },
                    'denivele_maximal': {
                        'valeur': activite_plus_denivele.d_plus or 0,
                        'date': activite_plus_denivele.date_activite.isoformat(),
                        'activite': activite_plus_denivele.nom
                    },
                    'calories_maximales': {
                        'valeur': activite_plus_calories.calories or 0,
                        'date': activite_plus_calories.date_activite.isoformat(),
                        'activite': activite_plus_calories.nom
                    }
                }

            return records

        finally:
            db.close()

    @staticmethod
    def obtenir_resume_global(utilisateur_id: int) -> Dict:
        """
        Récupère un résumé global de toutes les activités

        Args:
            utilisateur_id: ID de l'utilisateur

        Returns:
            Dictionnaire avec le résumé global
        """
        db = SessionLocal()
        try:
            activites = db.query(Activite).filter(
                Activite.utilisateur_id == utilisateur_id
            ).all()

            if not activites:
                return {
                    'nombre_total_activites': 0,
                    'duree_totale_heures': 0,
                    'distance_totale_km': 0,
                    'calories_totales': 0,
                    'sports_pratiques': []
                }

            duree_totale = sum(a.duree_activite or 0 for a in activites) / 3600
            distance_totale = sum(a.distance or 0 for a in activites) / 1000
            calories_totales = sum(a.calories or 0 for a in activites)
            sports_pratiques = list(set(a.type_sport for a in activites))

            # Date première et dernière activité
            dates = [a.date_activite for a in activites]
            date_premiere = min(dates)
            date_derniere = max(dates)

            return {
                'nombre_total_activites': len(activites),
                'duree_totale_heures': round(duree_totale, 2),
                'distance_totale_km': round(distance_totale, 2),
                'calories_totales': int(calories_totales),
                'sports_pratiques': sports_pratiques,
                'date_premiere_activite': date_premiere.isoformat(),
                'date_derniere_activite': date_derniere.isoformat(),
                'jours_actif': (date_derniere - date_premiere).days
            }

        finally:
            db.close()
