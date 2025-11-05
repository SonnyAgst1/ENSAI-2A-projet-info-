"""
Tests pour CommentaireDAO
"""
import pytest
from datetime import date
import sys
from pathlib import Path

# Ajouter src au chemin
sys.path.insert(0, str(Path(__file__).parent.parent))

from dao.commentaire_dao import CommentaireDAO
from dao.utilisateur_dao import UtilisateurDAO
from dao.activite_dao import ActiviteDAO
from database import Base, engine


@pytest.fixture(scope="function")
def setup_database():
    """Crée les tables avant chaque test et les supprime après"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def utilisateur_test(setup_database):
    """Crée et retourne un utilisateur de test"""
    return UtilisateurDAO.create(
        nom="Dupont",
        prenom="Jean",
        age=30,
        pseudo="jdupont_test",
        mail="jean.test@example.com",
        mdp="password123"
    )


@pytest.fixture
def activite_test(setup_database, utilisateur_test):
    """Crée et retourne une activité de test liée à l'utilisateur"""
    return ActiviteDAO.create(
        utilisateur_id=utilisateur_test.id,
        nom="Course test",
        type_sport="course",
        date_activite=date.today(),
        duree_activite=3600
    )


class TestCommentaireDAO:
    """Tests pour le DAO Commentaire"""

    def test_create_commentaire(self, activite_test, utilisateur_test):
        """Teste la création d'un commentaire"""
        contenu = "Super course !"
        commentaire = CommentaireDAO.create(
            activite_id=activite_test.id,
            auteur_id=utilisateur_test.id,
            contenu=contenu
        )
        assert commentaire is not None
        assert commentaire.contenu == contenu
        assert commentaire.activite_id == activite_test.id
        assert commentaire.auteur_id == utilisateur_test.id

    def test_get_by_id(self, activite_test, utilisateur_test):
        """Teste la récupération d'un commentaire par son ID"""
        contenu = "Test commentaire"
        commentaire = CommentaireDAO.create(
            activite_id=activite_test.id,
            auteur_id=utilisateur_test.id,
            contenu=contenu
        )
        commentaire_recupere = CommentaireDAO.get_by_id(commentaire.id)
        assert commentaire_recupere is not None
        assert commentaire_recupere.contenu == contenu
        assert commentaire_recupere.id == commentaire.id

    def test_get_by_activite(self, activite_test, utilisateur_test):
        """Teste la récupération des commentaires d'une activité"""
        commentaires_attendus = [
            "Commentaire 1",
            "Commentaire 2"
        ]
        for contenu in commentaires_attendus:
            CommentaireDAO.create(
                activite_id=activite_test.id,
                auteur_id=utilisateur_test.id,
                contenu=contenu
            )
        commentaires = CommentaireDAO.get_by_activite(activite_test.id)
        assert len(commentaires) == len(commentaires_attendus)
        contenus = [c.contenu for c in commentaires]
        for contenu in commentaires_attendus:
            assert contenu in contenus

    def test_delete_commentaire(self, activite_test, utilisateur_test):
        """Teste la suppression d'un commentaire"""
        contenu = "À supprimer"
        commentaire = CommentaireDAO.create(
            activite_id=activite_test.id,
            auteur_id=utilisateur_test.id,
            contenu=contenu
        )
        assert CommentaireDAO.delete(commentaire.id) is True
        assert CommentaireDAO.get_by_id(commentaire.id) is None

    def test_count_by_activite(self, activite_test, utilisateur_test):
        """Teste le comptage des commentaires d'une activité"""
        nb_commentaires = 3
        for i in range(nb_commentaires):
            CommentaireDAO.create(
                activite_id=activite_test.id,
                auteur_id=utilisateur_test.id,
                contenu=f"Commentaire {i+1}"
            )
        count = CommentaireDAO.count_by_activite(activite_test.id)
        assert count == nb_commentaires

    def test_is_author(self, activite_test, utilisateur_test):
        """Teste la vérification de l'auteur d'un commentaire"""
        contenu = "Mon commentaire"
        commentaire = CommentaireDAO.create(
            activite_id=activite_test.id,
            auteur_id=utilisateur_test.id,
            contenu=contenu
        )
        assert CommentaireDAO.is_author(commentaire.id, utilisateur_test.id) is True
        assert CommentaireDAO.is_author(commentaire.id, 999) is False
