import pytest
from sqlalchemy.exc import IntegrityError
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from business_objects.models import Commentaire
from dao.commentaire_dao import CommentaireDAO

# Mock de la session SQLAlchemy
@pytest.fixture
def mock_db_session(mocker):
    return mocker.patch("dao.commentaire_dao.SessionLocal")

# Mock du modèle Commentaire
@pytest.fixture
def mock_commentaire():
    commentaire = Commentaire(
        id=1,
        activite_id=1,
        auteur_id=1,
        contenu="Test commentaire"
    )
    return commentaire

# Test 1 : Création d'un commentaire
def test_create_commentaire(mock_db_session, mock_commentaire, mocker):
    # Mock de db.add, db.commit, db.refresh
    mock_db = mocker.MagicMock()
    mock_db_session.return_value = mock_db
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    # Appel de la méthode
    result = CommentaireDAO.create(
        activite_id=1,
        auteur_id=1,
        contenu="Test commentaire"
    )

    # Vérifications
    assert result is not None
    assert result.contenu == "Test commentaire"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

# Test 2 : Récupération d'un commentaire par ID
def test_get_by_id(mock_db_session, mock_commentaire, mocker):
    # Mock de db.query().filter().first()
    mock_db = mocker.MagicMock()
    mock_db_session.return_value = mock_db
    mock_db.query.return_value.filter.return_value.first.return_value = mock_commentaire

    # Appel de la méthode
    result = CommentaireDAO.get_by_id(1)

    # Vérifications
    assert result is not None
    assert result.id == 1
    mock_db.query.assert_called_once()

# Test 3 : Mise à jour d'un commentaire
def test_update_commentaire(mock_db_session, mock_commentaire, mocker):
    # Mock de db.query().filter().first()
    mock_db = mocker.MagicMock()
    mock_db_session.return_value = mock_db
    mock_db.query.return_value.filter.return_value.first.return_value = mock_commentaire
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    # Appel de la méthode
    result = CommentaireDAO.update(1, "Nouveau contenu")

    # Vérifications
    assert result is not None
    assert result.contenu == "Nouveau contenu"
    mock_db.commit.assert_called_once()

# Test 4 : Suppression d'un commentaire
def test_delete_commentaire(mock_db_session, mock_commentaire, mocker):
    # Mock de db.query().filter().first()
    mock_db = mocker.MagicMock()
    mock_db_session.return_value = mock_db
    mock_db.query.return_value.filter.return_value.first.return_value = mock_commentaire
    mock_db.delete.return_value = None
    mock_db.commit.return_value = None

    # Appel de la méthode
    result = CommentaireDAO.delete(1)

    # Vérifications
    assert result is True
    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()

# Test 5 : Récupération des commentaires d'une activité
def test_get_by_activite(mock_db_session, mocker):
    # Mock de db.query().filter().order_by().all()
    mock_db = mocker.MagicMock()
    mock_db_session.return_value = mock_db
    mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
        Commentaire(id=1, activite_id=1, auteur_id=1, contenu="Commentaire 1"),
        Commentaire(id=2, activite_id=1, auteur_id=2, contenu="Commentaire 2"),
    ]

    # Appel de la méthode
    result = CommentaireDAO.get_by_activite(1)

    # Vérifications
    assert len(result) == 2
    assert result[0].contenu == "Commentaire 1"
    assert result[1].contenu == "Commentaire 2"
    mock_db.query.assert_called_once()
