import pytest
from business_objects.commentaire import Commentaire


# Classes mock pour les tests
class MockUtilisateur:
    """Classe mock pour simuler un Utilisateur"""
    def __init__(self, id_utilisateur, pseudo):
        self.id_utilisateur = id_utilisateur
        self.pseudo = pseudo

    def __eq__(self, other):
        return isinstance(other, MockUtilisateur) and self.id_utilisateur == other.id_utilisateur

    def __hash__(self):
        return hash(self.id_utilisateur)


class MockActivite:
    """Classe mock pour simuler une Activite"""
    def __init__(self, id_activite, nom):
        self.id_activite = id_activite
        self.nom = nom


class TestCommentaire:
    """Classe de tests pour la classe Commentaire"""

    @pytest.fixture
    def utilisateur1(self):
        """Fixture pour créer un utilisateur de test"""
        return MockUtilisateur(1, "SportifPro")

    @pytest.fixture
    def utilisateur2(self):
        """Fixture pour créer un deuxième utilisateur de test"""
        return MockUtilisateur(2, "RunnerFan")

    @pytest.fixture
    def utilisateur3(self):
        """Fixture pour créer un troisième utilisateur de test"""
        return MockUtilisateur(3, "FitnessLover")

    @pytest.fixture
    def activite(self):
        """Fixture pour créer une activité de test"""
        return MockActivite(1, "Course matinale")

    @pytest.fixture
    def commentaire(self, utilisateur1, activite):
        """Fixture pour créer un commentaire de test"""
        return Commentaire(1, utilisateur1, activite, "Super séance aujourd'hui !")

    # Tests du constructeur
    def test_creation_commentaire(self, utilisateur1, activite):
        """Test la création d'un commentaire avec des paramètres valides"""
        com = Commentaire(1, utilisateur1, activite, "Test contenu")

        assert com.id == 1
        assert com.auteur == utilisateur1
        assert com.activite == activite
        assert com.contenu == "Test contenu"
        assert com.like == []

    def test_creation_commentaire_avec_contenu_long(self, utilisateur1, activite):
        """Test la création d'un commentaire avec un contenu long"""
        contenu_long = "a" * 500
        com = Commentaire(1, utilisateur1, activite, contenu_long)

        assert len(com.contenu) == 500
        assert com.contenu == contenu_long

    # Tests des getters
    def test_getter_id(self, commentaire):
        """Test le getter de l'id"""
        assert commentaire.id == 1
        assert isinstance(commentaire.id, int)

    def test_getter_auteur(self, commentaire, utilisateur1):
        """Test le getter de l'auteur"""
        assert commentaire.auteur == utilisateur1
        assert commentaire.auteur.pseudo == "SportifPro"

    def test_getter_activite(self, commentaire, activite):
        """Test le getter de l'activité"""
        assert commentaire.activite == activite
        assert commentaire.activite.nom == "Course matinale"

    def test_getter_contenu(self, commentaire):
        """Test le getter du contenu"""
        assert commentaire.contenu == "Super séance aujourd'hui !"
        assert isinstance(commentaire.contenu, str)

    def test_getter_like_retourne_copie(self, commentaire, utilisateur2):
        """Test que le getter like retourne une copie de la liste"""
        commentaire.ajouter_like(utilisateur2)
        likes = commentaire.like
        likes.append(MockUtilisateur(999, "Fake"))

        # La liste originale ne doit pas être modifiée
        assert len(commentaire.like) == 1
        assert len(likes) == 2

    # Tests du setter contenu
    def test_setter_contenu_valide(self, commentaire):
        """Test la modification du contenu avec une valeur valide"""
        nouveau_contenu = "Contenu mis à jour"
        commentaire.contenu = nouveau_contenu

        assert commentaire.contenu == nouveau_contenu

    def test_setter_contenu_vide_leve_exception(self, commentaire):
        """Test que le setter refuse un contenu vide"""
        with pytest.raises(ValueError, match="Le contenu doit être une chaîne non vide"):
            commentaire.contenu = ""

    def test_setter_contenu_espaces_leve_exception(self, commentaire):
        """Test que le setter refuse un contenu avec uniquement des espaces"""
        with pytest.raises(ValueError, match="Le contenu doit être une chaîne non vide"):
            commentaire.contenu = "   "

    def test_setter_contenu_non_string_leve_exception(self, commentaire):
        """Test que le setter refuse un contenu qui n'est pas une chaîne"""
        with pytest.raises(ValueError, match="Le contenu doit être une chaîne non vide"):
            commentaire.contenu = 123

        with pytest.raises(ValueError, match="Le contenu doit être une chaîne non vide"):
            commentaire.contenu = None

    # Tests de la méthode ajouter_like
    def test_ajouter_like_premier_utilisateur(self, commentaire, utilisateur2):
        """Test l'ajout du premier like"""
        resultat = commentaire.ajouter_like(utilisateur2)

        assert resultat is True
        assert utilisateur2 in commentaire.like
        assert len(commentaire.like) == 1

    def test_ajouter_like_plusieurs_utilisateurs(self, commentaire, utilisateur2, utilisateur3):
        """Test l'ajout de plusieurs likes"""
        commentaire.ajouter_like(utilisateur2)
        commentaire.ajouter_like(utilisateur3)

        assert len(commentaire.like) == 2
        assert utilisateur2 in commentaire.like
        assert utilisateur3 in commentaire.like

    def test_ajouter_like_doublon(self, commentaire, utilisateur2):
        """Test qu'on ne peut pas liker deux fois"""
        commentaire.ajouter_like(utilisateur2)
        resultat = commentaire.ajouter_like(utilisateur2)

        assert resultat is False
        assert len(commentaire.like) == 1

    def test_auteur_peut_liker_son_commentaire(self, commentaire, utilisateur1):
        """Test que l'auteur peut liker son propre commentaire"""
        resultat = commentaire.ajouter_like(utilisateur1)

        assert resultat is True
        assert utilisateur1 in commentaire.like

    # Tests de la méthode supprimer_like
    def test_supprimer_like_existant(self, commentaire, utilisateur2):
        """Test la suppression d'un like existant"""
        commentaire.ajouter_like(utilisateur2)
        resultat = commentaire.supprimer_like(utilisateur2)

        assert resultat is True
        assert utilisateur2 not in commentaire.like
        assert len(commentaire.like) == 0

    def test_supprimer_like_inexistant(self, commentaire, utilisateur2):
        """Test la suppression d'un like qui n'existe pas"""
        resultat = commentaire.supprimer_like(utilisateur2)

        assert resultat is False
        assert len(commentaire.like) == 0

    def test_supprimer_like_parmi_plusieurs(self, commentaire, utilisateur2, utilisateur3):
        """Test la suppression d'un like quand il y en a plusieurs"""
        commentaire.ajouter_like(utilisateur2)
        commentaire.ajouter_like(utilisateur3)

        commentaire.supprimer_like(utilisateur2)

        assert utilisateur2 not in commentaire.like
        assert utilisateur3 in commentaire.like
        assert len(commentaire.like) == 1

    # Tests de la méthode comptelike
    def test_comptelike_aucun_like(self, commentaire):
        """Test le comptage quand il n'y a aucun like"""
        assert commentaire.comptelike() == 0

    def test_comptelike_un_like(self, commentaire, utilisateur2):
        """Test le comptage avec un like"""
        commentaire.ajouter_like(utilisateur2)
        assert commentaire.comptelike() == 1

    def test_comptelike_plusieurs_likes(
        self, commentaire, utilisateur1, utilisateur2, utilisateur3
    ):
        """Test le comptage avec plusieurs likes"""
        commentaire.ajouter_like(utilisateur1)
        commentaire.ajouter_like(utilisateur2)
        commentaire.ajouter_like(utilisateur3)

        assert commentaire.comptelike() == 3

    def test_comptelike_apres_suppression(self, commentaire, utilisateur2, utilisateur3):
        """Test le comptage après ajout et suppression de likes"""
        commentaire.ajouter_like(utilisateur2)
        commentaire.ajouter_like(utilisateur3)
        commentaire.supprimer_like(utilisateur2)

        assert commentaire.comptelike() == 1

    # Tests des méthodes spéciales
    def test_str_representation(self, commentaire):
        """Test la représentation textuelle du commentaire"""
        representation = str(commentaire)

        assert "Commentaire #1" in representation
        assert "SportifPro" in representation
        assert "Super séance aujourd'hui" in representation
        assert "0 likes" in representation

    def test_str_representation_avec_contenu_long(self, utilisateur1, activite):
        """Test la représentation textuelle avec un contenu long"""
        contenu_long = "a" * 100
        com = Commentaire(1, utilisateur1, activite, contenu_long)
        representation = str(com)

        # Vérifie que le contenu est tronqué à 50 caractères
        assert len(representation.split(":")[1].split("...")[0].strip()) <= 50

    def test_repr_representation(self, commentaire):
        """Test la représentation technique du commentaire"""
        representation = repr(commentaire)

        assert "Commentaire(id=1" in representation
        assert "auteur=SportifPro" in representation
        assert "likes=0" in representation

    # Tests d'intégration
    def test_scenario_complet_likes(self, commentaire, utilisateur1, utilisateur2, utilisateur3):
        """Test un scénario complet d'ajout et suppression de likes"""
        # État initial
        assert commentaire.comptelike() == 0

        # Ajout de likes
        commentaire.ajouter_like(utilisateur1)
        commentaire.ajouter_like(utilisateur2)
        commentaire.ajouter_like(utilisateur3)
        assert commentaire.comptelike() == 3

        # Tentative de doublon
        commentaire.ajouter_like(utilisateur1)
        assert commentaire.comptelike() == 3

        # Suppression d'un like
        commentaire.supprimer_like(utilisateur2)
        assert commentaire.comptelike() == 2

        # Vérification de la liste
        assert utilisateur1 in commentaire.like
        assert utilisateur2 not in commentaire.like
        assert utilisateur3 in commentaire.like

    def test_modification_contenu_preserve_likes(self, commentaire, utilisateur2):
        """Test que la modification du contenu préserve les likes"""
        commentaire.ajouter_like(utilisateur2)
        commentaire.contenu = "Nouveau contenu"

        assert commentaire.comptelike() == 1
        assert utilisateur2 in commentaire.like


# Tests paramétrés
class TestCommentaireParametre:
    """Tests paramétrés pour la classe Commentaire"""

    @pytest.mark.parametrize("id_com,pseudo,contenu", [
        (1, "User1", "Commentaire 1"),
        (999, "UserMax", "Un autre commentaire"),
        (42, "TestUser", "x" * 1000),  # Contenu très long
    ])
    def test_creation_avec_differents_parametres(self, id_com, pseudo, contenu):
        """Test la création avec différents paramètres"""
        utilisateur = MockUtilisateur(id_com, pseudo)
        activite = MockActivite(1, "Test Activity")
        com = Commentaire(id_com, utilisateur, activite, contenu)

        assert com.id == id_com
        assert com.auteur.pseudo == pseudo
        assert com.contenu == contenu

    @pytest.mark.parametrize("contenu_invalide", [
        "",
        "   ",
        "\n",
        "\t",
        123,
        None,
        [],
        {},
    ])
    def test_setter_contenu_invalides(self, contenu_invalide):
        """Test le setter avec différentes valeurs invalides"""
        utilisateur = MockUtilisateur(1, "Test")
        activite = MockActivite(1, "Test")
        com = Commentaire(1, utilisateur, activite, "Contenu initial")

        with pytest.raises(ValueError):
            com.contenu = contenu_invalide
