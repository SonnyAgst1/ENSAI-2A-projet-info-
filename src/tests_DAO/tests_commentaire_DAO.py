import pytest
from datetime import date
from dao.commentaire_dao import CommentaireDAO
from dao.utilisateur_dao import UtilisateurDAO
from dao.activite_dao import ActiviteDAO
from database import SessionLocal, Base, engine

@pytest.fixture(scope="function")
def setup_database():
    """Crée les tables avant chaque test et les supprime après"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def utilisateur_test(setup_database):
    """Crée un utilisateur de test"""
    user = UtilisateurDAO.create(
        nom="Dupont",
        prenom="Jean",
        age=30,
        pseudo="jdupont_test",
        mail="jean.test@example.com",
        mdp="password123"
    )
    return user


@pytest.fixture
def activite_test(setup_database, utilisateur_test):
    """Crée une activité de test"""
    activite = ActiviteDAO.create(
        utilisateur_id=utilisateur_test.id,
        nom="Course test",
        type_sport="course",
        date_activite=date.today(),
        duree_activite=3600
    )
    return activite


class TestCommentaireDAO:
    """Tests pour le DAO Commentaire"""
    
    def test_create_commentaire(self, activite_test, utilisateur_test):
        """Test création d'un commentaire"""
        commentaire = CommentaireDAO.create(
            activite_id=activite_test.id,
            auteur_id=utilisateur_test.id,
            contenu="Super course !"
        )
        
        assert commentaire is not None
        assert commentaire.id is not None
        assert commentaire.contenu == "Super course !"
        assert commentaire.activite_id == activite_test.id
        assert commentaire.auteur_id == utilisateur_test.id
    
    def test_get_by_id(self, activite_test, utilisateur_test):
        """Test récupération d'un commentaire par ID"""
        # Créer
        commentaire = CommentaireDAO.create(
            activite_id=activite_test.id,
            auteur_id=utilisateur_test.id,
            contenu="Test commentaire"
        )
        
        # Récupérer
        commentaire_recupere = CommentaireDAO.get_by_id(commentaire.id)
        
        assert commentaire_recupere is not None
        assert commentaire_recupere.id == commentaire.id
        assert commentaire_recupere.contenu == "Test commentaire"
    
    def test_get_by_activite(self, activite_test, utilisateur_test):
        """Test récupération des commentaires d'une activité"""
        # Créer plusieurs commentaires
        CommentaireDAO.create(
            activite_id=activite_test.id,
            auteur_id=utilisateur_test.id,
            contenu="Commentaire 1"
        )
        CommentaireDAO.create(
            activite_id=activite_test.id,
            auteur_id=utilisateur_test.id,
            contenu="Commentaire 2"
        )
        
        # Récupérer
        commentaires = CommentaireDAO.get_by_activite(activite_test.id)
        
        assert len(commentaires) == 2
        assert commentaires[0].contenu in ["Commentaire 1", "Commentaire 2"]
    
    def test_update_commentaire(self, activite_test, utilisateur_test):
        """Test modification d'un commentaire"""
        # Créer
        commentaire = CommentaireDAO.create(
            activite_id=activite_test.id,
            auteur_id=utilisateur_test.id,
            contenu="Contenu initial"
        )
        
        # Modifier
        commentaire_modifie = CommentaireDAO.update(
            commentaire.id,
            "Contenu modifié"
        )
        
        assert commentaire_modifie is not None
        assert commentaire_modifie.contenu == "Contenu modifié"
    
    def test_delete_commentaire(self, activite_test, utilisateur_test):
        """Test suppression d'un commentaire"""
        # Créer
        commentaire = CommentaireDAO.create(
            activite_id=activite_test.id,
            auteur_id=utilisateur_test.id,
            contenu="À supprimer"
        )
        
        # Supprimer
        result = CommentaireDAO.delete(commentaire.id)
        
        assert result is True
        
        # Vérifier qu'il n'existe plus
        commentaire_supprime = CommentaireDAO.get_by_id(commentaire.id)
        assert commentaire_supprime is None
    
    def test_count_by_activite(self, activite_test, utilisateur_test):
        """Test comptage des commentaires d'une activité"""
        # Créer 3 commentaires
        for i in range(3):
            CommentaireDAO.create(
                activite_id=activite_test.id,
                auteur_id=utilisateur_test.id,
                contenu=f"Commentaire {i+1}"
            )
        
        # Compter
        count = CommentaireDAO.count_by_activite(activite_test.id)
        
        assert count == 3
    
    def test_is_author(self, activite_test, utilisateur_test):
        """Test vérification de l'auteur d'un commentaire"""
        # Créer
        commentaire = CommentaireDAO.create(
            activite_id=activite_test.id,
            auteur_id=utilisateur_test.id,
            contenu="Mon commentaire"
        )
        
        # Vérifier
        assert CommentaireDAO.is_author(commentaire.id, utilisateur_test.id) is True
        assert CommentaireDAO.is_author(commentaire.id, 999) is False
    
    def test_get_by_id_inexistant(self, setup_database):
        """Test récupération d'un commentaire inexistant"""
        commentaire = CommentaireDAO.get_by_id(9999)
        assert commentaire is None
    
    def test_delete_inexistant(self, setup_database):
        """Test suppression d'un commentaire inexistant"""
        result = CommentaireDAO.delete(9999)
        assert result is False