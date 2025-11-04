import pytest
from datetime import date, timedelta
from business_objects.utilisateur import Utilisateur


# Classes mock pour les tests
class MockActivite:
    """Classe mock pour simuler une Activite"""
    def __init__(self, id_activite, nom, distance=10, duree=60, calories=500, d_plus=100):
        self.id_activite = id_activite
        self.nom = nom
        self.d_plus = d_plus  # Distance en km
        self.duree_activite = duree  # Durée en minutes
        self.calories = calories
        self._likes = []
        self._commentaires = []

    def ajouter_like_utilisateur(self, utilisateur):
        if utilisateur not in self._likes:
            self._likes.append(utilisateur)

    def supprimer_like_utilisateur(self, utilisateur):
        if utilisateur in self._likes:
            self._likes.remove(utilisateur)

    def comptelike(self):
        return len(self._likes)

    def ajouter_commentaire(self, utilisateur, texte):
        self._commentaires.append({"utilisateur": utilisateur, "texte": texte})

    def supprimer_commentaire(self, commentaire):
        if commentaire in self._commentaires:
            self._commentaires.remove(commentaire)

    def comptecommentaire(self):
        return len(self._commentaires)


class MockService:
    """Classe mock pour simuler la classe Service qui gère les follows"""
    def __init__(self):
        self._follows = {}  # {follower_id: [followee_id1, followee_id2, ...]}

    def ajouter_follow(self, follower_id, followee_id):
        if follower_id not in self._follows:
            self._follows[follower_id] = []
        if followee_id not in self._follows[follower_id]:
            self._follows[follower_id].append(followee_id)
            return True
        return False

    def supprimer_follow(self, follower_id, followee_id):
        if follower_id in self._follows and followee_id in self._follows[follower_id]:
            self._follows[follower_id].remove(followee_id)
            return True
        return False

    def get_following(self, user_id):
        return self._follows.get(user_id, []).copy()

    def get_followers(self, user_id):
        followers = []
        for follower_id, followees in self._follows.items():
            if user_id in followees:
                followers.append(follower_id)
        return followers


@pytest.fixture
def date_naissance():
    """Fixture pour une date de naissance"""
    return date(1990, 5, 15)


@pytest.fixture
def utilisateur_base(date_naissance):
    """Fixture pour créer un utilisateur de test"""
    return Utilisateur(
        id_utilisateur=1,
        pseudo="RunnerPro",
        nom="Dupont",
        prenom="Jean",
        date_de_naissance=date_naissance,
        taille=175,
        poids=70,
        mail="jean.dupont@example.com",
        telephone=612345678,
        mdp="password123"
    )


@pytest.fixture
def utilisateur_avec_activites(date_naissance):
    """Fixture pour un utilisateur avec des activités"""
    activites = [
        MockActivite(1, "Course 1", 10, 60, 500, 100),
        MockActivite(2, "Vélo", 25, 90, 700, 150),
        MockActivite(3, "Course 2", 15, 75, 600, 120)
    ]
    return Utilisateur(
        id_utilisateur=2,
        pseudo="SportifMax",
        nom="Martin",
        prenom="Sophie",
        date_de_naissance=date_naissance,
        taille=165,
        poids=60,
        mail="sophie.martin@example.com",
        telephone=623456789,
        mdp="secure456",
        liste_activites=activites
    )


@pytest.fixture
def service():
    """Fixture pour créer une instance de MockService"""
    return MockService()


class TestUtilisateur:
    """Classe de tests pour la classe Utilisateur"""

    # Tests du constructeur
    def test_creation_utilisateur_complet(self):
        """Test la création d'un utilisateur avec tous les paramètres"""
        user = Utilisateur(
            id_utilisateur=1,
            pseudo="TestUser",
            nom="Nom",
            prenom="Prenom",
            date_de_naissance=date(1995, 1, 1),
            taille=180,
            poids=75,
            mail="test@example.com",
            telephone=600000000,
            mdp="mdp123"
        )

        assert user.id_utilisateur == 1
        assert user.pseudo == "TestUser"
        assert user.nom == "Nom"
        assert user.prenom == "Prenom"
        assert user.taille == 180
        assert user.poids == 75
        assert user.mail == "test@example.com"
        assert user.telephone == 600000000
        assert user.liste_activites == []

    def test_creation_utilisateur_avec_activites(self):
        """Test la création d'un utilisateur avec une liste d'activités"""
        activites = [MockActivite(1, "Test", 5, 30, 200, 50)]
        user = Utilisateur(
            id_utilisateur=1,
            pseudo="TestUser",
            nom="Nom",
            prenom="Prenom",
            date_de_naissance=date(1995, 1, 1),
            taille=170,
            poids=65,
            mail="test@example.com",
            telephone=600000000,
            mdp="mdp123",
            liste_activites=activites
        )

        assert len(user.liste_activites) == 1
        assert user.liste_activites[0].nom == "Test"

    # Tests des getters
    def test_getter_id_utilisateur(self, utilisateur_base):
        """Test le getter de l'id"""
        assert utilisateur_base.id_utilisateur == 1
        assert isinstance(utilisateur_base.id_utilisateur, int)

    def test_getter_pseudo(self, utilisateur_base):
        """Test le getter du pseudo"""
        assert utilisateur_base.pseudo == "RunnerPro"

    def test_getter_nom(self, utilisateur_base):
        """Test le getter du nom"""
        assert utilisateur_base.nom == "Dupont"

    def test_getter_prenom(self, utilisateur_base):
        """Test le getter du prénom"""
        assert utilisateur_base.prenom == "Jean"

    def test_getter_age_calcul_correct(self):
        """Test le calcul de l'âge"""
        # Utilisateur né il y a exactement 30 ans
        date_naissance = date.today() - timedelta(days=365*30)
        user = Utilisateur(
            id_utilisateur=1,
            pseudo="Test",
            nom="Nom",
            prenom="Prenom",
            date_de_naissance=date_naissance,
            taille=170,
            poids=70,
            mail="test@example.com",
            telephone=600000000,
            mdp="mdp123"
        )

        assert user.age == 30 or user.age == 29  # Peut varier selon le jour exact

    def test_getter_taille(self, utilisateur_base):
        """Test le getter de la taille"""
        assert utilisateur_base.taille == 175

    def test_getter_poids(self, utilisateur_base):
        """Test le getter du poids"""
        assert utilisateur_base.poids == 70

    def test_getter_mail(self, utilisateur_base):
        """Test le getter du mail"""
        assert utilisateur_base.mail == "jean.dupont@example.com"

    def test_getter_telephone(self, utilisateur_base):
        """Test le getter du téléphone"""
        assert utilisateur_base.telephone == 612345678

    def test_getter_liste_activites_retourne_copie(self, utilisateur_avec_activites):
        """Test que le getter liste_activites retourne une copie"""
        liste = utilisateur_avec_activites.liste_activites
        liste.append(MockActivite(999, "Fake", 0, 0, 0, 0))

        assert len(utilisateur_avec_activites.liste_activites) == 3
        assert len(liste) == 4

    # Tests des setters
    def test_setter_pseudo_valide(self, utilisateur_base):
        """Test la modification du pseudo avec une valeur valide"""
        utilisateur_base.pseudo = "NewPseudo"
        assert utilisateur_base.pseudo == "NewPseudo"

    def test_setter_pseudo_vide_leve_exception(self, utilisateur_base):
        """Test que le setter refuse un pseudo vide"""
        with pytest.raises(ValueError, match="Le pseudo doit être une chaîne non vide"):
            utilisateur_base.pseudo = ""

    def test_setter_pseudo_espaces_leve_exception(self, utilisateur_base):
        """Test que le setter refuse un pseudo avec uniquement des espaces"""
        with pytest.raises(ValueError, match="Le pseudo doit être une chaîne non vide"):
            utilisateur_base.pseudo = "   "

    def test_setter_taille_valide(self, utilisateur_base):
        """Test la modification de la taille avec une valeur valide"""
        utilisateur_base.taille = 180.5
        assert utilisateur_base.taille == 180.5

    def test_setter_taille_negative_leve_exception(self, utilisateur_base):
        """Test que le setter refuse une taille négative"""
        with pytest.raises(ValueError, match="La taille doit être un nombre positif"):
            utilisateur_base.taille = -175

    def test_setter_taille_zero_leve_exception(self, utilisateur_base):
        """Test que le setter refuse une taille de zéro"""
        with pytest.raises(ValueError, match="La taille doit être un nombre positif"):
            utilisateur_base.taille = 0

    def test_setter_poids_valide(self, utilisateur_base):
        """Test la modification du poids avec une valeur valide"""
        utilisateur_base.poids = 75.5
        assert utilisateur_base.poids == 75.5

    def test_setter_poids_negatif_leve_exception(self, utilisateur_base):
        """Test que le setter refuse un poids négatif"""
        with pytest.raises(ValueError, match="Le poids doit être un nombre positif"):
            utilisateur_base.poids = -70

    def test_setter_mail_valide(self, utilisateur_base):
        """Test la modification du mail avec une valeur valide"""
        utilisateur_base.mail = "nouveau@example.com"
        assert utilisateur_base.mail == "nouveau@example.com"

    def test_setter_mail_sans_arobase_leve_exception(self, utilisateur_base):
        """Test que le setter refuse un mail sans @"""
        with pytest.raises(ValueError, match="Le mail doit être valide"):
            utilisateur_base.mail = "emailinvalide.com"

    def test_setter_telephone_int_valide(self, utilisateur_base):
        """Test la modification du téléphone avec un entier"""
        utilisateur_base.telephone = 699999999
        assert utilisateur_base.telephone == 699999999

    def test_setter_telephone_str_valide(self, utilisateur_base):
        """Test la modification du téléphone avec une chaîne"""
        utilisateur_base.telephone = "06 12 34 56 78"
        assert utilisateur_base.telephone == "06 12 34 56 78"

    # Tests de la méthode connexion
    def test_connexion_identifiants_corrects(self, utilisateur_base):
        """Test la connexion avec des identifiants corrects"""
        resultat = utilisateur_base.connexion("RunnerPro", "password123")
        assert resultat is True

    def test_connexion_mauvais_pseudo(self, utilisateur_base):
        """Test la connexion avec un mauvais pseudo"""
        resultat = utilisateur_base.connexion("WrongPseudo", "password123")
        assert resultat is False

    def test_connexion_mauvais_mdp(self, utilisateur_base):
        """Test la connexion avec un mauvais mot de passe"""
        resultat = utilisateur_base.connexion("RunnerPro", "wrongpassword")
        assert resultat is False

    def test_connexion_identifiants_vides(self, utilisateur_base):
        """Test la connexion avec des identifiants vides"""
        resultat = utilisateur_base.connexion("", "")
        assert resultat is False

    # Tests de la méthode deconnexion
    def test_deconnexion(self, utilisateur_base):
        """Test la déconnexion"""
        # La méthode ne fait rien pour l'instant mais ne doit pas lever d'exception
        utilisateur_base.deconnexion()
        assert True

    # Tests des méthodes de follow avec Service
    def test_follow_utilisateur_avec_service(self, utilisateur_base, service):
        """Test le follow d'un utilisateur via le service"""
        resultat = utilisateur_base.follow_utilisateur(2, service)

        assert resultat is True
        following = utilisateur_base.get_following(service)
        assert 2 in following

    def test_follow_utilisateur_doublon(self, utilisateur_base, service):
        """Test qu'on ne peut pas follow deux fois le même utilisateur"""
        utilisateur_base.follow_utilisateur(2, service)
        resultat = utilisateur_base.follow_utilisateur(2, service)

        assert resultat is False

    def test_follow_soi_meme_refuse(self, utilisateur_base, service):
        """Test qu'on ne peut pas se suivre soi-même"""
        resultat = utilisateur_base.follow_utilisateur(1, service)
        assert resultat is False

    def test_unfollow_utilisateur_avec_service(self, utilisateur_base, service):
        """Test l'unfollow d'un utilisateur via le service"""
        utilisateur_base.follow_utilisateur(2, service)
        resultat = utilisateur_base.unfollow_utilisateur(2, service)

        assert resultat is True
        following = utilisateur_base.get_following(service)
        assert 2 not in following

    def test_unfollow_utilisateur_non_suivi(self, utilisateur_base, service):
        """Test l'unfollow d'un utilisateur non suivi"""
        resultat = utilisateur_base.unfollow_utilisateur(2, service)
        assert resultat is False

    def test_get_following(self, utilisateur_base, service):
        """Test la récupération de la liste des utilisateurs suivis"""
        utilisateur_base.follow_utilisateur(2, service)
        utilisateur_base.follow_utilisateur(3, service)
        utilisateur_base.follow_utilisateur(4, service)

        following = utilisateur_base.get_following(service)

        assert len(following) == 3
        assert 2 in following
        assert 3 in following
        assert 4 in following

    def test_get_followers(self, utilisateur_base, service):
        """Test la récupération de la liste des followers"""
        # Créer d'autres utilisateurs qui suivent utilisateur_base
        user2 = Utilisateur(2, "User2", "Nom2", "Prenom2", date(1995, 1, 1),
                            170, 65, "user2@test.com", 600000002, "mdp2"
                            )
        user3 = Utilisateur(3, "User3", "Nom3", "Prenom3", date(1995, 1, 1),
                            170, 65, "user3@test.com", 600000003, "mdp3"
                            )

        user2.follow_utilisateur(1, service)
        user3.follow_utilisateur(1, service)

        followers = utilisateur_base.get_followers(service)

        assert len(followers) == 2
        assert 2 in followers
        assert 3 in followers

    # Tests des méthodes d'interaction avec les activités
    def test_ajouter_like_activite(self, utilisateur_base):
        """Test l'ajout d'un like sur une activité"""
        activite = MockActivite(1, "Course", 10, 60, 500, 100)
        utilisateur_base.ajouter_like(activite)

        assert activite.comptelike() == 1

    def test_supprimer_like_activite(self, utilisateur_base):
        """Test la suppression d'un like sur une activité"""
        activite = MockActivite(1, "Course", 10, 60, 500, 100)
        utilisateur_base.ajouter_like(activite)
        utilisateur_base.supprimer_like(activite)

        assert activite.comptelike() == 0

    def test_ajouter_commentaire_activite(self, utilisateur_base):
        """Test l'ajout d'un commentaire sur une activité"""
        activite = MockActivite(1, "Course", 10, 60, 500, 100)
        utilisateur_base.ajouter_commentaire(activite, "Super course !")

        assert activite.comptecommentaire() == 1

    def test_supprimer_activite(self, utilisateur_avec_activites):
        """Test la suppression d'une activité"""
        activite = utilisateur_avec_activites.liste_activites[0]
        resultat = utilisateur_avec_activites.supprimer_activite(activite)

        assert resultat is True
        assert len(utilisateur_avec_activites.liste_activites) == 2

    def test_supprimer_activite_inexistante(self, utilisateur_base):
        """Test la suppression d'une activité inexistante"""
        activite = MockActivite(999, "Fake", 0, 0, 0, 0)
        resultat = utilisateur_base.supprimer_activite(activite)

        assert resultat is False

    # Tests des méthodes de calcul
    def test_calculer_distance_totale_sans_activites(self, utilisateur_base):
        """Test le calcul de la distance avec aucune activité"""
        distance = utilisateur_base.calculer_distance_totale()
        assert distance == 0

    def test_calculer_duree_totale(self, utilisateur_avec_activites):
        """Test le calcul de la durée totale"""
        duree = utilisateur_avec_activites.calculer_duree_totale()
        assert duree == 225  # 60 + 90 + 75

    def test_calculer_calories_totales(self, utilisateur_avec_activites):
        """Test le calcul des calories totales"""
        calories = utilisateur_avec_activites.calculer_calories_totales()
        assert calories == 1800  # 500 + 700 + 600

    def test_calculer_d_plus_total(self, utilisateur_avec_activites):
        """Test le calcul du dénivelé positif total"""
        d_plus = utilisateur_avec_activites.calculer_d_plus_total()
        assert d_plus == 370  # 100 + 150 + 120

    def test_calculer_vitesse_moyenne_sans_activites(self, utilisateur_base):
        """Test le calcul de la vitesse avec aucune activité"""
        vitesse = utilisateur_base.calculer_vitesse_moyenne_globale()
        assert vitesse == 0.0

    def test_calculer_vitesse_moyenne_duree_nulle(self):
        """Test le calcul de la vitesse avec durée nulle"""
        activites = [MockActivite(1, "Test", 10, 0, 0, 0)]
        user = Utilisateur(1, "Test", "Nom", "Prenom", date(1990, 1, 1),
                           170, 70, "test@test.com", 600000000, "mdp",
                           liste_activites=activites
                           )

        vitesse = user.calculer_vitesse_moyenne_globale()
        assert vitesse == 0.0

    # Tests des méthodes de statistiques
    def test_get_nombre_like(self, utilisateur_avec_activites):
        """Test le comptage des likes reçus"""
        # Simuler des likes sur les activités
        for activite in utilisateur_avec_activites._liste_activites:
            activite.ajouter_like_utilisateur(Utilisateur(999, "Test", "T", "T",
                                                          date(1990, 1, 1), 170, 70,
                                                          "t@t.com", 600000000, "mdp"))

        total_likes = utilisateur_avec_activites.get_nombre_like()
        assert total_likes == 3

    def test_get_nombre_commentaire(self, utilisateur_avec_activites):
        """Test le comptage des commentaires reçus"""
        user_test = Utilisateur(999, "Test", "T", "T", date(1990, 1, 1),
                                170, 70, "t@t.com", 600000000, "mdp"
                                )

        # Simuler des commentaires sur les activités
        for activite in utilisateur_avec_activites._liste_activites:
            activite.ajouter_commentaire(user_test, "Commentaire test")

        total_commentaires = utilisateur_avec_activites.get_nombre_commentaire()
        assert total_commentaires == 3

    # Tests de la méthode s_inscrire
    def test_s_inscrire(self, utilisateur_base):
        """Test l'inscription avec de nouvelles données"""
        resultat = utilisateur_base.s_inscrire("new@email.com", "NewPseudo", "newpass")

        assert resultat is True
        assert utilisateur_base.mail == "new@email.com"
        assert utilisateur_base.pseudo == "NewPseudo"

    # Tests des méthodes spéciales
    def test_str_representation(self, utilisateur_avec_activites):
        """Test la représentation textuelle de l'utilisateur"""
        representation = str(utilisateur_avec_activites)

        assert "SportifMax" in representation
        assert "Sophie" in representation
        assert "Martin" in representation
        assert "3 activités" in representation

    def test_repr_representation(self, utilisateur_base):
        """Test la représentation technique de l'utilisateur"""
        representation = repr(utilisateur_base)

        assert "Utilisateur(id=1" in representation
        assert "pseudo=RunnerPro" in representation
        assert "activites=0" in representation

    def test_egalite_utilisateurs(self, date_naissance):
        """Test l'égalité entre deux utilisateurs"""
        user1 = Utilisateur(1, "User1", "Nom", "Prenom", date_naissance,
                            170, 70, "test@test.com", 600000000, "mdp"
                            )
        user2 = Utilisateur(1, "User2", "Autre", "Autre", date_naissance,
                            180, 80, "autre@test.com", 600000001, "mdp2"
                            )

        assert user1 == user2  # Même ID

    def test_inegalite_utilisateurs(self, date_naissance):
        """Test l'inégalité entre deux utilisateurs"""
        user1 = Utilisateur(1, "User1", "Nom", "Prenom", date_naissance,
                            170, 70, "test@test.com", 600000000, "mdp"
                            )
        user2 = Utilisateur(2, "User2", "Nom", "Prenom", date_naissance,
                            170, 70, "test@test.com", 600000000, "mdp"
                            )

        assert user1 != user2  # IDs différents

    def test_hash_utilisateur(self, utilisateur_base):
        """Test le hash de l'utilisateur"""
        hash_value = hash(utilisateur_base)
        assert isinstance(hash_value, int)
        assert hash_value == hash(1)  # Hash basé sur l'ID

    def test_utilisateur_dans_set(self, date_naissance):
        """Test qu'on peut utiliser un utilisateur dans un set"""
        user1 = Utilisateur(1, "User1", "Nom", "Prenom", date_naissance,
                            170, 70, "test@test.com", 600000000, "mdp"
                            )
        user2 = Utilisateur(2, "User2", "Nom", "Prenom", date_naissance,
                            170, 70, "test@test.com", 600000000, "mdp"
                            )

        users_set = {user1, user2}
        assert len(users_set) == 2
        assert user1 in users_set
        assert user2 in users_set


# Tests paramétrés
class TestUtilisateurParametre:
    """Tests paramétrés pour la classe Utilisateur"""

    @pytest.mark.parametrize("taille,poids", [
        (150, 50),
        (175.5, 70.5),
        (200, 100),
        (160, 55),
    ])
    def test_creation_differentes_tailles_poids(self, taille, poids):
        """Test la création avec différentes tailles et poids"""
        user = Utilisateur(
            id_utilisateur=1,
            pseudo="Test",
            nom="Nom",
            prenom="Prenom",
            date_de_naissance=date(1990, 1, 1),
            taille=taille,
            poids=poids,
            mail="test@example.com",
            telephone=600000000,
            mdp="mdp123"
        )

        assert user.taille == taille
        assert user.poids == poids

    @pytest.mark.parametrize("valeur_invalide", [
        -1,
        0,
        -175,
        "abc",
    ])
    def test_setter_taille_valeurs_invalides(self, utilisateur_base, valeur_invalide):
        """Test le setter taille avec différentes valeurs invalides"""
        with pytest.raises(ValueError):
            utilisateur_base.taille = valeur_invalide

    @pytest.mark.parametrize("mail_invalide", [
        "emailsansarobase",
        "email.com",
        "",
        123,
    ])
    def test_setter_mail_valeurs_invalides(self, utilisateur_base, mail_invalide):
        """Test le setter mail avec différentes valeurs invalides"""
        with pytest.raises(ValueError):
            utilisateur_base.mail = mail_invalide
