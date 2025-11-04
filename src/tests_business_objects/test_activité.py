import pytest
import datetime as dt
from activité import Activité


# Classes mock pour les tests
class MockUtilisateur:
    """Classe mock pour simuler un Utilisateur"""
    def __init__(self, id_utilisateur, pseudo):
        self._id_utilisateur = id_utilisateur
        self.pseudo = pseudo

    def __eq__(self, other):
        return isinstance(other, MockUtilisateur) and self._id_utilisateur == other._id_utilisateur

    def __hash__(self):
        return hash(self._id_utilisateur)


class MockCommentaire:
    """Classe mock pour simuler un Commentaire"""
    def __init__(self, id_commentaire, contenu):
        self.id_commentaire = id_commentaire
        self.contenu = contenu


class TestActivité:
    """Classe de tests pour la classe Activité"""

    # Fixtures
    @pytest.fixture
    def utilisateur1(self):
        """Fixture pour créer un utilisateur de test"""
        return MockUtilisateur(1, "RunnerPro")

    @pytest.fixture
    def utilisateur2(self):
        """Fixture pour créer un deuxième utilisateur"""
        return MockUtilisateur(2, "CyclisteAmatrice")

    @pytest.fixture
    def utilisateur3(self):
        """Fixture pour créer un troisième utilisateur"""
        return MockUtilisateur(3, "NageurOlympique")

    @pytest.fixture
    def commentaire1(self):
        """Fixture pour créer un commentaire de test"""
        return MockCommentaire(1, "Super activité !")

    @pytest.fixture
    def commentaire2(self):
        """Fixture pour créer un deuxième commentaire"""
        return MockCommentaire(2, "Bravo pour la performance")

    @pytest.fixture
    def activite_base(self, utilisateur1):
        """Fixture pour créer une activité de base"""
        return Activité(
            id_activite=1,
            utilisateur=utilisateur1,
            nom="Course matinale",
            type_sport="Course",
            dateActivite=dt.date(2024, 11, 1),
            dureeActivite=dt.time(1, 30, 0),
            description="Belle course dans le parc",
            fichiergpx="course.gpx",
            like=[],
            commentaire=[],
            denivelle=150,
            calories=900
        )

    @pytest.fixture
    def activite_natation(self, utilisateur1):
        """Fixture pour une activité de natation"""
        return Activité(
            id_activite=2,
            utilisateur=utilisateur1,
            nom="Séance piscine",
            type_sport="Natation",
            dateActivite=dt.date(2024, 11, 2),
            dureeActivite=dt.time(1, 0, 0),
            description="Entraînement technique",
            fichiergpx="natation.gpx",
            like=[],
            commentaire=[],
            denivelle=0,
            calories=500
        )

    @pytest.fixture
    def activite_velo(self, utilisateur2):
        """Fixture pour une activité de vélo"""
        return Activité(
            id_activite=3,
            utilisateur=utilisateur2,
            nom="Sortie vélo",
            type_sport="Vélo",
            dateActivite=dt.date(2024, 11, 3),
            dureeActivite=dt.time(2, 30, 0),
            description="Tour des cols",
            fichiergpx="velo.gpx",
            like=[],
            commentaire=[],
            denivelle=800,
            calories=1500
        )

    # Tests du constructeur
    def test_creation_activite_valide(self, utilisateur1):
        """Test la création d'une activité avec des paramètres valides"""
        activite = Activité(
            id_activite=1,
            utilisateur=utilisateur1,
            nom="Test Activity",
            type_sport="Course",
            dateActivite=dt.date(2024, 11, 1),
            dureeActivite=dt.time(1, 0, 0),
            description="Test description",
            fichiergpx="test.gpx",
            like=[],
            commentaire=[],
            denivelle=100,
            calories=600
        )

        assert activite.id == 1
        assert activite.utilisateur == utilisateur1
        assert activite.nom == "Test Activity"
        assert activite.type_sport == "Course"
        assert activite.dateActivite == dt.date(2024, 11, 1)
        assert activite.dureeActivite == dt.time(1, 0, 0)
        assert activite.description == "Test description"
        assert activite.fichiergpx == "test.gpx"
        assert activite.like == []
        assert activite.commentaire == []
        assert activite.denivelle == 100
        assert activite.calories == 600

    def test_creation_activite_avec_likes(self, utilisateur1, utilisateur2, utilisateur3):
        """Test la création d'une activité avec des likes"""
        likes = [utilisateur2._id_utilisateur, utilisateur3._id_utilisateur]
        activite = Activité(
            id_activite=1,
            utilisateur=utilisateur1,
            nom="Activité populaire",
            type_sport="Course",
            dateActivite=dt.date(2024, 11, 1),
            dureeActivite=dt.time(1, 0, 0),
            description="Très likée",
            fichiergpx="popular.gpx",
            like=likes,
            commentaire=[],
            denivelle=0,
            calories=500
        )

        assert len(activite.like) == 2
        assert utilisateur2._id_utilisateur in activite.like

    def test_creation_activite_avec_commentaires(self, utilisateur1, commentaire1, commentaire2):
        """Test la création d'une activité avec des commentaires"""
        commentaires = [commentaire1, commentaire2]
        activite = Activité(
            id_activite=1,
            utilisateur=utilisateur1,
            nom="Activité commentée",
            type_sport="Course",
            dateActivite=dt.date(2024, 11, 1),
            dureeActivite=dt.time(1, 0, 0),
            description="Beaucoup de retours",
            fichiergpx="commented.gpx",
            like=[],
            commentaire=commentaires,
            denivelle=0,
            calories=500
        )

        assert len(activite.commentaire) == 2
        assert commentaire1 in activite.commentaire

    # Tests des getters
    def test_getter_id(self, activite_base):
        """Test le getter de l'id"""
        assert activite_base.id == 1
        assert isinstance(activite_base.id, int)

    def test_getter_utilisateur(self, activite_base, utilisateur1):
        """Test le getter de l'utilisateur"""
        assert activite_base.utilisateur == utilisateur1
        assert activite_base.utilisateur.pseudo == "RunnerPro"

    def test_getter_nom(self, activite_base):
        """Test le getter du nom"""
        assert activite_base.nom == "Course matinale"
        assert isinstance(activite_base.nom, str)

    def test_getter_type_sport(self, activite_base):
        """Test le getter du type de sport"""
        assert activite_base.type_sport == "Course"
        assert isinstance(activite_base.type_sport, str)

    def test_getter_date_activite(self, activite_base):
        """Test le getter de la date"""
        assert activite_base.dateActivite == dt.date(2024, 11, 1)
        assert isinstance(activite_base.dateActivite, dt.date)

    def test_getter_duree_activite(self, activite_base):
        """Test le getter de la durée"""
        assert activite_base.dureeActivite == dt.time(1, 30, 0)
        assert isinstance(activite_base.dureeActivite, dt.time)

    def test_getter_description(self, activite_base):
        """Test le getter de la description"""
        assert activite_base.description == "Belle course dans le parc"
        assert isinstance(activite_base.description, str)

    def test_getter_fichier_gpx(self, activite_base):
        """Test le getter du fichier GPX"""
        assert activite_base.fichiergpx == "course.gpx"
        assert isinstance(activite_base.fichiergpx, str)

    def test_getter_like(self, activite_base):
        """Test le getter des likes"""
        assert activite_base.like == []
        assert isinstance(activite_base.like, list)

    def test_getter_commentaire(self, activite_base):
        """Test le getter des commentaires"""
        assert activite_base.commentaire == []
        assert isinstance(activite_base.commentaire, list)

    def test_getter_denivelle(self, activite_base):
        """Test le getter du dénivelé"""
        assert activite_base.denivelle == 150
        assert isinstance(activite_base.denivelle, int)

    def test_getter_calories(self, activite_base):
        """Test le getter des calories"""
        assert activite_base.calories == 900
        assert isinstance(activite_base.calories, int)

    # Tests des setters - nom
    def test_setter_nom_valide(self, activite_base):
        """Test la modification du nom avec une valeur valide"""
        activite_base.nom = "Course du soir"
        assert activite_base.nom == "Course du soir"

    def test_setter_nom_avec_espaces(self, activite_base):
        """Test la modification du nom avec des espaces autour"""
        activite_base.nom = "  Nouvelle course  "
        assert activite_base.nom == "  Nouvelle course  "

    def test_setter_nom_vide_leve_exception(self, activite_base):
        """Test que le setter refuse un nom vide"""
        with pytest.raises(ValueError, match="chaîne non vide"):
            activite_base.nom = ""

    def test_setter_nom_espaces_seuls_leve_exception(self, activite_base):
        """Test que le setter refuse un nom avec uniquement des espaces"""
        with pytest.raises(ValueError, match="chaîne non vide"):
            activite_base.nom = "   "

    def test_setter_nom_non_string_leve_exception(self, activite_base):
        """Test que le setter refuse un nom qui n'est pas une chaîne"""
        with pytest.raises(ValueError, match="chaîne non vide"):
            activite_base.nom = 123

    # Tests des setters - type_sport
    def test_setter_type_sport_valide(self, activite_base):
        """Test la modification du type de sport avec une valeur valide"""
        activite_base.type_sport = "Vélo"
        assert activite_base.type_sport == "Vélo"

    def test_setter_type_sport_vide_leve_exception(self, activite_base):
        """Test que le setter refuse un type de sport vide"""
        with pytest.raises(ValueError, match="chaîne non vide"):
            activite_base.type_sport = ""

    def test_setter_type_sport_non_string_leve_exception(self, activite_base):
        """Test que le setter refuse un type qui n'est pas une chaîne"""
        with pytest.raises(ValueError):
            activite_base.type_sport = None

    # Tests des setters - dateActivite
    def test_setter_date_valide(self, activite_base):
        """Test la modification de la date avec une valeur valide"""
        nouvelle_date = dt.date(2024, 12, 1)
        activite_base.dateActivite = nouvelle_date
        assert activite_base.dateActivite == nouvelle_date

    def test_setter_date_invalide_leve_exception(self, activite_base):
        """Test que le setter refuse une date invalide"""
        with pytest.raises(ValueError, match="doit être une date"):
            activite_base.dateActivite = "2024-11-01"

    def test_setter_date_none_leve_exception(self, activite_base):
        """Test que le setter refuse None comme date"""
        with pytest.raises(ValueError):
            activite_base.dateActivite = None

    # Tests des setters - dureeActivite
    def test_setter_duree_valide(self, activite_base):
        """Test la modification de la durée avec une valeur valide"""
        nouvelle_duree = dt.time(2, 0, 0)
        activite_base.dureeActivite = nouvelle_duree
        assert activite_base.dureeActivite == nouvelle_duree

    def test_setter_duree_invalide_leve_exception(self, activite_base):
        """Test que le setter refuse une durée invalide"""
        with pytest.raises(ValueError, match="doit être un temps"):
            activite_base.dureeActivite = "02:00:00"

    def test_setter_duree_entier_leve_exception(self, activite_base):
        """Test que le setter refuse un entier comme durée"""
        with pytest.raises(ValueError):
            activite_base.dureeActivite = 120

    # Tests des setters - description
    def test_setter_description_valide(self, activite_base):
        """Test la modification de la description avec une valeur valide"""
        nouvelle_desc = "Excellente séance d'entraînement"
        activite_base.description = nouvelle_desc
        assert activite_base.description == nouvelle_desc

    def test_setter_description_longue(self, activite_base):
        """Test la modification avec une description très longue"""
        description_longue = "x" * 1000
        activite_base.description = description_longue
        assert len(activite_base.description) == 1000

    def test_setter_description_vide_leve_exception(self, activite_base):
        """Test que le setter refuse une description vide"""
        with pytest.raises(ValueError, match="chaîne non vide"):
            activite_base.description = ""

    def test_setter_description_non_string_leve_exception(self, activite_base):
        """Test que le setter refuse une description non-string"""
        with pytest.raises(ValueError):
            activite_base.description = []

    # Tests des setters - fichiergpx
    def test_setter_fichier_gpx_valide(self, activite_base):
        """Test la modification du fichier GPX avec une valeur valide"""
        nouveau_gpx = "nouveau_parcours.gpx"
        activite_base.fichiergpx = nouveau_gpx
        assert activite_base.fichiergpx == nouveau_gpx

    def test_setter_fichier_gpx_vide_leve_exception(self, activite_base):
        """Test que le setter refuse un fichier GPX vide"""
        with pytest.raises(ValueError, match="chaîne non vide"):
            activite_base.fichiergpx = "   "

    # Tests des méthodes de comptage
    def test_compte_like_zero(self, activite_base):
        """Test compte_like avec aucun like"""
        assert activite_base.compte_like() == 0

    def test_compte_like_un(self, activite_base, utilisateur2):
        """Test compte_like avec un like"""
        activite_base._like = [utilisateur2._id_utilisateur]
        assert activite_base.compte_like() == 1

    def test_compte_like_plusieurs(self, activite_base):
        """Test compte_like avec plusieurs likes"""
        activite_base._like = [1, 2, 3, 4, 5]
        assert activite_base.compte_like() == 5

    def test_compte_commentaire_zero(self, activite_base):
        """Test compte_commentaire avec aucun commentaire"""
        assert activite_base.compte_commentaire() == 0

    def test_compte_commentaire_un(self, activite_base, commentaire1):
        """Test compte_commentaire avec un commentaire"""
        activite_base._commentaire = [commentaire1]
        assert activite_base.compte_commentaire() == 1

    def test_compte_commentaire_plusieurs(self, activite_base, commentaire1, commentaire2):
        """Test compte_commentaire avec plusieurs commentaires"""
        activite_base._commentaire = [commentaire1, commentaire2]
        assert activite_base.compte_commentaire() == 2

    def test_getNombreLike_coherent_avec_compte_like(self, activite_base):
        """Test que getNombreLike retourne la même valeur que compte_like"""
        activite_base._like = [1, 2, 3]
        assert activite_base.getNombreLike() == activite_base.compte_like()
        assert activite_base.getNombreLike() == 3

    def test_getNombreCommentaire_coherent_avec_compte_commentaire(
        self, activite_base, commentaire1
    ):
        """Test que getNombreCommentaire retourne la même valeur que compte_commentaire"""
        activite_base._commentaire = [commentaire1]
        assert activite_base.getNombreCommentaire() == activite_base.compte_commentaire()
        assert activite_base.getNombreCommentaire() == 1

    # Tests calculer_vitesse - Natation
    def test_calculer_vitesse_natation_2000m_60min(self, activite_natation):
        """Test calcul vitesse natation: 2000m en 60 minutes = 3 min/100m"""
        vitesse = activite_natation.calculer_vitesse(2000)
        assert vitesse == pytest.approx(3.0, rel=0.01)

    def test_calculer_vitesse_natation_1500m_45min(self, utilisateur1):
        """Test calcul vitesse natation: 1500m en 45 minutes = 3 min/100m"""
        activite = Activité(
            1, utilisateur1, "Natation", "Natation",
            dt.date.today(), dt.time(0, 45, 0),
            "Test", "test.gpx", [], [], 0, 0
        )
        vitesse = activite.calculer_vitesse(1500)
        assert vitesse == pytest.approx(3.0, rel=0.01)

    def test_calculer_vitesse_natation_majuscules(self, utilisateur1):
        """Test calcul vitesse natation avec majuscules"""
        activite = Activité(
            1, utilisateur1, "Test", "NATATION",
            dt.date.today(), dt.time(1, 0, 0),
            "Test", "test.gpx", [], [], 0, 0
        )
        vitesse = activite.calculer_vitesse(2000)
        assert vitesse == pytest.approx(3.0, rel=0.01)

    # Tests calculer_vitesse - Vélo
    def test_calculer_vitesse_velo_50km_2h(self, activite_velo):
        """Test calcul vitesse vélo: 50 km en 2h30 = 20 km/h"""
        vitesse = activite_velo.calculer_vitesse(50)
        assert vitesse == pytest.approx(20.0, rel=0.01)

    def test_calculer_vitesse_velo_sans_accent(self, utilisateur1):
        """Test calcul vitesse vélo sans accent"""
        activite = Activité(
            1, utilisateur1, "Vélo", "velo",
            dt.date.today(), dt.time(1, 0, 0),
            "Test", "test.gpx", [], [], 0, 0
        )
        vitesse = activite.calculer_vitesse(30)
        assert vitesse == pytest.approx(30.0, rel=0.01)

    def test_calculer_vitesse_velo_avec_accent(self, utilisateur1):
        """Test calcul vitesse vélo avec accent"""
        activite = Activité(
            1, utilisateur1, "Vélo", "vélo",
            dt.date.today(), dt.time(2, 0, 0),
            "Test", "test.gpx", [], [], 0, 0
        )
        vitesse = activite.calculer_vitesse(40)
        assert vitesse == pytest.approx(20.0, rel=0.01)

    # Tests calculer_vitesse - Marche
    def test_calculer_vitesse_marche_5km_60min(self, utilisateur1):
        """Test calcul vitesse marche: 5 km en 60 minutes = 12 min/km"""
        activite = Activité(
            1, utilisateur1, "Randonnée", "Marche",
            dt.date.today(), dt.time(1, 0, 0),
            "Test", "test.gpx", [], [], 0, 0
        )
        vitesse = activite.calculer_vitesse(5)
        assert vitesse == pytest.approx(12.0, rel=0.01)

    def test_calculer_vitesse_marche_10km_100min(self, utilisateur1):
        """Test calcul vitesse marche: 10 km en 100 minutes = 10 min/km"""
        activite = Activité(
            1, utilisateur1, "Marche", "marche",
            dt.date.today(), dt.time(1, 40, 0),
            "Test", "test.gpx", [], [], 0, 0
        )
        vitesse = activite.calculer_vitesse(10)
        assert vitesse == pytest.approx(10.0, rel=0.01)

    # Tests calculer_vitesse - Cas d'erreur
    def test_calculer_vitesse_duree_zero_leve_exception(self, utilisateur1):
        """Test calcul vitesse avec durée nulle"""
        activite = Activité(
            1, utilisateur1, "Course", "Course",
            dt.date.today(), dt.time(0, 0, 0),
            "Test", "test.gpx", [], [], 0, 0
        )
        with pytest.raises(ValueError, match="supérieure à 0"):
            activite.calculer_vitesse(10)

    def test_calculer_vitesse_avec_secondes(self, utilisateur1):
        """Test calcul vitesse avec des secondes dans la durée"""
        activite = Activité(
            1, utilisateur1, "Course", "Vélo",
            dt.date.today(), dt.time(1, 30, 30),
            "Test", "test.gpx", [], [], 0, 0
        )
        vitesse = activite.calculer_vitesse(45)
        # 1h 30min 30s = 90.5 minutes = 1.508333 heures
        # 45 km / 1.508333 h ≈ 29.83 km/h
        assert vitesse == pytest.approx(29.83, rel=0.01)

    # Tests calculer_calories (méthode statique)
    def test_calculer_calories_marche_2h_100m(self):
        """Test calcul calories marche: 2h avec 100m dénivelé"""
        calories = Activité.calculer_calories("marche", 2, 100)
        # 300 cal/h * 2h + 100m * 0.1 = 600 + 10 = 610
        assert calories == 610

    def test_calculer_calories_course_1h_50m(self):
        """Test calcul calories course: 1h avec 50m dénivelé"""
        calories = Activité.calculer_calories("course", 1, 50)
        # 600 cal/h * 1h + 50m * 0.1 = 600 + 5 = 605
        assert calories == 605

    def test_calculer_calories_velo_3h_500m(self):
        """Test calcul calories vélo: 3h avec 500m dénivelé"""
        calories = Activité.calculer_calories("vélo", 3, 500)
        # 500 cal/h * 3h + 500m * 0.1 = 1500 + 50 = 1550
        assert calories == 1550

    def test_calculer_calories_velo_sans_accent(self):
        """Test calcul calories vélo sans accent"""
        calories = Activité.calculer_calories("velo", 2, 200)
        # 500 cal/h * 2h + 200m * 0.1 = 1000 + 20 = 1020
        assert calories == 1020

    def test_calculer_calories_natation_1h30_0m(self):
        """Test calcul calories natation: 1h30 sans dénivelé"""
        calories = Activité.calculer_calories("natation", 1.5, 0)
        # 500 cal/h * 1.5h = 750
        assert calories == 750

    def test_calculer_calories_randonnee_4h_800m(self):
        """Test calcul calories randonnée: 4h avec 800m dénivelé"""
        calories = Activité.calculer_calories("randonnée", 4, 800)
        # 400 cal/h * 4h + 800m * 0.1 = 1600 + 80 = 1680
        assert calories == 1680

    def test_calculer_calories_randonnee_sans_accent(self):
        """Test calcul calories randonnée sans accent"""
        calories = Activité.calculer_calories("randonnee", 2, 300)
        # 400 cal/h * 2h + 300m * 0.1 = 800 + 30 = 830
        assert calories == 830

    def test_calculer_calories_sport_inconnu(self):
        """Test calcul calories pour un sport non référencé (valeur par défaut)"""
        calories = Activité.calculer_calories("escalade", 2, 200)
        # 400 cal/h (défaut) * 2h + 200m * 0.1 = 800 + 20 = 820
        assert calories == 820

    def test_calculer_calories_sans_denivelle(self):
        """Test calcul calories sans dénivelé"""
        calories = Activité.calculer_calories("marche", 1, 0)
        assert calories == 300

    def test_calculer_calories_duree_fractionnaire(self):
        """Test calcul calories avec durée fractionnaire"""
        calories = Activité.calculer_calories("course", 0.5, 25)
        # 600 cal/h * 0.5h + 25m * 0.1 = 300 + 2.5 = 302.5 → 302
        assert calories == 302

    def test_calculer_calories_majuscules(self):
        """Test calcul calories avec type sport en majuscules"""
        calories = Activité.calculer_calories("MARCHE", 1, 0)
        assert calories == 300


# Tests paramétrés
class TestActivitéParamétré:
    """Tests paramétrés pour la classe Activité"""

    @pytest.mark.parametrize("nom_invalide", [
        "",
        "   ",
        "\n",
        "\t",
        123,
        None,
        [],
    ])
    def test_setter_nom_valeurs_invalides(self, nom_invalide):
        """Test le setter nom avec différentes valeurs invalides"""
        utilisateur = MockUtilisateur(1, "Test")
        activite = Activité(
            1, utilisateur, "Nom initial", "Course",
            dt.date.today(), dt.time(1, 0, 0),
            "Description", "test.gpx", [], [], 0, 0
        )

        with pytest.raises(ValueError):
            activite.nom = nom_invalide

    @pytest.mark.parametrize("type_sport,duree,distance,vitesse_attendue", [
        ("Natation", dt.time(1, 0, 0), 2000, 3.0),      # 60 min / 2000m * 100 = 3 min/100m
        ("natation", dt.time(0, 30, 0), 1000, 3.0),     # 30 min / 1000m * 100 = 3 min/100m
        ("Vélo", dt.time(2, 0, 0), 50, 25.0),          # 50 km / 2h = 25 km/h
        ("velo", dt.time(1, 0, 0), 30, 30.0),          # 30 km / 1h = 30 km/h
        ("Marche", dt.time(1, 0, 0), 5, 12.0),         # 60 min / 5 km = 12 min/km
        ("marche", dt.time(1, 30, 0), 9, 10.0),        # 90 min / 9 km = 10 min/km
    ])
    def test_calculer_vitesse_differents_sports(
        self, type_sport, duree, distance, vitesse_attendue
    ):
        """Test calcul vitesse pour différents sports et configurations"""
        utilisateur = MockUtilisateur(1, "Test")
        activite = Activité(
            1, utilisateur, "Test", type_sport,
            dt.date.today(), duree,
            "Test", "test.gpx", [], [], 0, 0
        )

        vitesse = activite.calculer_vitesse(distance)
        assert vitesse == pytest.approx(vitesse_attendue, rel=0.01)
