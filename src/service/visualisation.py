from typing import Dict, Optional
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import calendar
import numpy as np


class VisualisationService:
    """Service pour créer des visualisations des statistiques"""

    @staticmethod
    def creer_barplot_activites_par_semaine(
        stats: Dict[str, Dict[str, int]],
        titre: str = "Nombre d'activités par semaine et par sport",
        fichier_sortie: Optional[str] = None
    ):
        """
        Crée un barplot empilé du nombre d'activités par semaine et par sport

        Args:
            stats: Dictionnaire retourné par obtenir_activites_par_semaine()
            titre: Titre du graphique
            fichier_sortie: Chemin pour sauvegarder (None = affichage)
        """
        if not stats:
            print("Pas de données à visualiser")
            return

        # Préparer les données
        semaines = sorted(stats.keys())
        sports = set()
        for sports_semaine in stats.values():
            sports.update(sports_semaine.keys())
        sports = sorted(list(sports))

        # Créer la matrice de données
        data = {sport: [] for sport in sports}
        for semaine in semaines:
            for sport in sports:
                data[sport].append(stats[semaine].get(sport, 0))

        # Créer le graphique
        fig, ax = plt.subplots(figsize=(14, 7))

        # Barres empilées
        bottom = np.zeros(len(semaines))
        colors = sns.color_palette("husl", len(sports))

        for i, sport in enumerate(sports):
            ax.bar(semaines, data[sport], bottom=bottom, label=sport, color=colors[i])
            bottom += np.array(data[sport])

        ax.set_xlabel('Semaine', fontsize=12)
        ax.set_ylabel('Nombre d\'activités', fontsize=12)
        ax.set_title(titre, fontsize=14, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(axis='y', alpha=0.3)

        # Rotation des labels
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        if fichier_sortie:
            plt.savefig(fichier_sortie, dpi=300, bbox_inches='tight')
            print(f"Graphique sauvegardé dans {fichier_sortie}")
        else:
            plt.show()

        plt.close()

    @staticmethod
    def creer_lineplot_heures_par_semaine(
        stats: Dict[str, float],
        titre: str = "Heures d'activité par semaine",
        fichier_sortie: Optional[str] = None
    ):
        """
        Crée un graphique en ligne des heures par semaine

        Args:
            stats: Dictionnaire retourné par obtenir_heures_par_semaine()
            titre: Titre du graphique
            fichier_sortie: Chemin pour sauvegarder (None = affichage)
        """
        if not stats:
            print("Pas de données à visualiser")
            return

        semaines = sorted(stats.keys())
        heures = [stats[s] for s in semaines]

        fig, ax = plt.subplots(figsize=(14, 7))

        ax.plot(semaines, heures, marker='o', linewidth=2, markersize=8,
                color='#2E86AB', markerfacecolor='#A23B72')
        ax.fill_between(range(len(semaines)), heures, alpha=0.3, color='#2E86AB')

        ax.set_xlabel('Semaine', fontsize=12)
        ax.set_ylabel('Heures d\'activité', fontsize=12)
        ax.set_title(titre, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        # Ajouter la moyenne
        moyenne = sum(heures) / len(heures)
        ax.axhline(y=moyenne, color='red', linestyle='--',
                   label=f'Moyenne: {moyenne:.1f}h', linewidth=2)
        ax.legend()

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        if fichier_sortie:
            plt.savefig(fichier_sortie, dpi=300, bbox_inches='tight')
            print(f"Graphique sauvegardé dans {fichier_sortie}")
        else:
            plt.show()

        plt.close()

    @staticmethod
    def creer_calendar_heatmap(
        stats: Dict[str, float],
        annee: int,
        titre: str = "Activité annuelle",
        fichier_sortie: Optional[str] = None
    ):
        """
        Crée une heatmap calendaire (comme GitHub)

        Args:
            stats: Dictionnaire avec dates et valeurs
            annee: Année à visualiser
            titre: Titre du graphique
            fichier_sortie: Chemin pour sauvegarder (None = affichage)
        """
        # Créer une matrice pour tous les jours de l'année
        premier_jour = datetime(annee, 1, 1).date()
        dernier_jour = datetime(annee, 12, 31).date()

        # Préparer les données
        dates = []
        valeurs = []

        jour_courant = premier_jour
        while jour_courant <= dernier_jour:
            dates.append(jour_courant)

            # Chercher la valeur pour cette date dans stats (semaine)
            annee_iso, semaine_iso, _ = jour_courant.isocalendar()
            cle_semaine = f"{annee_iso}-W{semaine_iso:02d}"
            valeurs.append(stats.get(cle_semaine, 0))

            jour_courant += timedelta(days=1)

        # Organiser en semaines
        semaines = []
        semaine_courante = []

        for i, (date, valeur) in enumerate(zip(dates, valeurs)):
            semaine_courante.append(valeur)
            if date.weekday() == 6:  # Dimanche
                if len(semaine_courante) < 7:
                    # Compléter avec des 0 au début
                    semaine_courante = [0] * (7 - len(semaine_courante)) + semaine_courante
                semaines.append(semaine_courante)
                semaine_courante = []

        # Ajouter la dernière semaine
        if semaine_courante:
            semaine_courante += [0] * (7 - len(semaine_courante))
            semaines.append(semaine_courante)

        # Créer la heatmap
        data = np.array(semaines).T

        fig, ax = plt.subplots(figsize=(16, 4))

        cmap = sns.color_palette("YlGnBu", as_cmap=True)
        sns.heatmap(data, cmap=cmap, linewidths=2, linecolor='white',
                    square=True, cbar_kws={'label': 'Heures'}, ax=ax)

        ax.set_xlabel('Semaines', fontsize=12)
        ax.set_ylabel('Jours', fontsize=12)
        ax.set_yticklabels(['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'])
        ax.set_title(titre, fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()

        if fichier_sortie:
            plt.savefig(fichier_sortie, dpi=300, bbox_inches='tight')
            print(f"Graphique sauvegardé dans {fichier_sortie}")
        else:
            plt.show()

        plt.close()

    @staticmethod
    def creer_pieplot_repartition_sports(
        stats_par_sport: Dict[str, Dict],
        titre: str = "Répartition par sport",
        fichier_sortie: Optional[str] = None
    ):
        """
        Crée un diagramme circulaire de la répartition par sport

        Args:
            stats_par_sport: Dictionnaire retourné par obtenir_statistiques_par_sport()
            titre: Titre du graphique
            fichier_sortie: Chemin pour sauvegarder (None = affichage)
        """
        if not stats_par_sport:
            print("Pas de données à visualiser")
            return

        sports = list(stats_par_sport.keys())
        valeurs = [stats_par_sport[s]['nombre_activites'] for s in sports]

        fig, ax = plt.subplots(figsize=(10, 8))

        colors = sns.color_palette("Set2", len(sports))
        explode = [0.05] * len(sports)  # Légère séparation

        wedges, texts, autotexts = ax.pie(
            valeurs,
            labels=sports,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            explode=explode,
            textprops={'fontsize': 11}
        )

        # Améliorer l'apparence
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title(titre, fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()

        if fichier_sortie:
            plt.savefig(fichier_sortie, dpi=300, bbox_inches='tight')
            print(f"Graphique sauvegardé dans {fichier_sortie}")
        else:
            plt.show()

        plt.close()

    @staticmethod
    def creer_graphique_interactif_plotly(
        stats: Dict[str, Dict[str, int]],
        titre: str = "Activités par semaine (interactif)"
    ) -> str:
        """
        Crée un graphique interactif avec Plotly

        Args:
            stats: Dictionnaire retourné par obtenir_activites_par_semaine()
            titre: Titre du graphique

        Returns:
            HTML du graphique interactif
        """
        if not stats:
            return "<p>Pas de données à visualiser</p>"

        # Préparer les données
        semaines = sorted(stats.keys())
        sports = set()
        for sports_semaine in stats.values():
            sports.update(sports_semaine.keys())
        sports = sorted(list(sports))

        fig = go.Figure()

        for sport in sports:
            valeurs = [stats[semaine].get(sport, 0) for semaine in semaines]
            fig.add_trace(go.Bar(
                name=sport,
                x=semaines,
                y=valeurs,
                hovertemplate='<b>%{x}</b><br>' +
                              f'{sport}: %{{y}} activités<br>' +
                              '<extra></extra>'
            ))

        fig.update_layout(
            title=titre,
            xaxis_title='Semaine',
            yaxis_title='Nombre d\'activités',
            barmode='stack',
            hovermode='x unified',
            template='plotly_white',
            height=500
        )

        return fig.to_html(include_plotlyjs='cdn')

    @staticmethod
    def creer_dashboard_complet(
        stats_completes: Dict,
        stats_par_sport: Dict,
        fichier_sortie: str = "dashboard.png"
    ):
        """
        Crée un dashboard complet avec plusieurs graphiques

        Args:
            stats_completes: Retour de obtenir_statistiques_completes()
            stats_par_sport: Retour de obtenir_statistiques_par_sport()
            fichier_sortie: Nom du fichier de sortie
        """
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

        # 1. Activités par semaine (barplot)
        ax1 = fig.add_subplot(gs[0, :])
        stats_activites = stats_completes['activites_par_semaine']
        if stats_activites:
            semaines = sorted(stats_activites.keys())
            sports = set()
            for sports_semaine in stats_activites.values():
                sports.update(sports_semaine.keys())
            sports = sorted(list(sports))

            data = {sport: [] for sport in sports}
            for semaine in semaines:
                for sport in sports:
                    data[sport].append(stats_activites[semaine].get(sport, 0))

            bottom = np.zeros(len(semaines))
            colors = sns.color_palette("husl", len(sports))

            for i, sport in enumerate(sports):
                ax1.bar(semaines, data[sport], bottom=bottom, label=sport, color=colors[i])
                bottom += np.array(data[sport])

            ax1.set_title('Activités par semaine', fontsize=12, fontweight='bold')
            ax1.legend(loc='upper left', ncol=len(sports))
            ax1.tick_params(axis='x', rotation=45)

        # 2. Heures par semaine (lineplot)
        ax2 = fig.add_subplot(gs[1, 0])
        stats_heures = stats_completes['heures_par_semaine']
        if stats_heures:
            semaines = sorted(stats_heures.keys())
            heures = [stats_heures[s] for s in semaines]
            ax2.plot(semaines, heures, marker='o', linewidth=2, color='#2E86AB')
            ax2.fill_between(range(len(semaines)), heures, alpha=0.3, color='#2E86AB')
            ax2.set_title('Heures par semaine', fontsize=12, fontweight='bold')
            ax2.tick_params(axis='x', rotation=45)
            ax2.grid(True, alpha=0.3)

        # 3. Kilomètres par semaine
        ax3 = fig.add_subplot(gs[1, 1])
        stats_km = stats_completes['kilometres_par_semaine']
        if stats_km:
            semaines = sorted(stats_km.keys())
            km = [stats_km[s] for s in semaines]
            ax3.plot(semaines, km, marker='s', linewidth=2, color='#A23B72')
            ax3.fill_between(range(len(semaines)), km, alpha=0.3, color='#A23B72')
            ax3.set_title('Kilomètres par semaine', fontsize=12, fontweight='bold')
            ax3.tick_params(axis='x', rotation=45)
            ax3.grid(True, alpha=0.3)

        # 4. Répartition par sport (pie)
        ax4 = fig.add_subplot(gs[2, 0])
        if stats_par_sport:
            sports = list(stats_par_sport.keys())
            valeurs = [stats_par_sport[s]['nombre_activites'] for s in sports]
            colors = sns.color_palette("Set2", len(sports))
            ax4.pie(valeurs, labels=sports, autopct='%1.1f%%', colors=colors)
            ax4.set_title('Répartition par sport', fontsize=12, fontweight='bold')

        # 5. Statistiques textuelles
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.axis('off')

        if stats_par_sport:
            texte = "STATISTIQUES GLOBALES\n" + "="*30 + "\n\n"
            total_activites = sum(s['nombre_activites'] for s in stats_par_sport.values())
            total_heures = sum(s['duree_totale_heures'] for s in stats_par_sport.values())
            total_calories = sum(s['calories_totales'] for s in stats_par_sport.values())

            texte += f"Total activités: {total_activites}\n"
            texte += f"Total heures: {total_heures:.1f}h\n"
            texte += f"Total calories: {total_calories:,}\n\n"

            texte += "PAR SPORT:\n" + "-"*30 + "\n"
            for sport, stats in stats_par_sport.items():
                texte += f"\n{sport.upper()}:\n"
                texte += f"  • {stats['nombre_activites']} activités\n"
                texte += f"  • {stats['duree_totale_heures']:.1f}h\n"
                texte += f"  • {stats['calories_totales']:,} cal\n"

            ax5.text(0.1, 0.9, texte, fontsize=10, verticalalignment='top',
                     fontfamily='monospace', bbox=dict(boxstyle='round',
                                                       facecolor='wheat', alpha=0.3)
                     )

        plt.suptitle('TABLEAU DE BORD SPORTIF', fontsize=16, fontweight='bold', y=0.98)

        plt.savefig(fichier_sortie, dpi=300, bbox_inches='tight')
        print(f"Dashboard sauvegardé dans {fichier_sortie}")
        plt.close()
