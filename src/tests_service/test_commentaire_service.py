"""
Tests pour la partie commentaires du ActiviteService
"""
import pytest
from datetime import date
from service.activite_service import ActiviteService
from service.utilisateur_service import UtilisateurService
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
    user = UtilisateurService.creer_utilisateur(
        nom="Martin",
        prenom="Sophie",
        age=28,
        pseudo="smartin_test",
        mail="sophie.test@example.com",
        mdp="securepass"
    )
    return user


@pytest.fixture
def activite_test(setup_database, utilisateur_test):
    """Crée une activité de test"""
    activite = ActiviteService.creer_activite_manuelle(
        utilisateur_id=utilisateur_test.id,
        nom="Sortie vélo",
        type_sport="vélo",
        date_activite=date.today(),
        duree_activite=7200,
        description="Belle sortie"
    )
    return activite


class TestActiviteServiceCommentaires:
    """Tests pour les fonctionnalités de commentaires"""
    
    def test_ajouter_commentaire(self, activite_test, utilisateur_test):
        """Test ajout d'un commentaire sur une activité"""
        commentaire = ActiviteService.ajouter_commentaire(
            utilisateur_id=utilisateur_test.id,
            activite_id=activite_test.id,
            contenu="Excellente sortie !"
        )
        
        assert commentaire is not None
        assert commentaire.contenu == "Excellente sortie !"
        assert commentaire.auteur_id == utilisateur_test.id
        assert commentaire.activite_id == activite_test.id
    
    def test_ajouter_commentaire_activite_inexistante(self, utilisateur_test, setup_database):
        """Test ajout commentaire sur activité inexistante"""
        commentaire = ActiviteService.ajouter_commentaire(
            utilisateur_id=utilisateur_test.id,
            activite_id=9999,
            contenu="Test"
        )
        
        assert commentaire is None
    
    def test_obtenir_commentaires_activite(self, activite_test, utilisateur_test):
        """Test récupération des commentaires d'une activité"""
        # Ajouter plusieurs commentaires
        ActiviteService.ajouter_commentaire(
            utilisateur_test.id,
            activite_test.id,
            "Premier commentaire"
        )
        ActiviteService.ajouter_commentaire(
            utilisateur_test.id,
            activite_test.id,
            "Deuxième commentaire"
        )
        
        # Récupérer
        commentaires = ActiviteService.obtenir_commentaires_activite(activite_test.id)
        
        assert len(commentaires) == 2
        assert any(c.contenu == "Premier commentaire" for c in commentaires)
        assert any(c.contenu == "Deuxième commentaire" for c in commentaires)
    
    def test_modifier_commentaire(self, activite_test, utilisateur_test):
        """Test modification d'un commentaire"""
        # Créer
        commentaire = ActiviteService.ajouter_commentaire(
            utilisateur_test.id,
            activite_test.id,
            "Commentaire original"
        )
        
        # Modifier
        commentaire_modifie = ActiviteService.modifier_commentaire(
            commentaire.id,
            "Commentaire modifié"
        )
        
        assert commentaire_modifie is not None
        assert commentaire_modifie.contenu == "Commentaire modifié"
    
    def test_supprimer_commentaire(self, activite_test, utilisateur_test):
        """Test suppression d'un commentaire"""
        # Créer
        commentaire = ActiviteService.ajouter_commentaire(
            utilisateur_test.id,
            activite_test.id,
            "À supprimer"
        )
        
        # Supprimer
        result = ActiviteService.supprimer_commentaire(commentaire.id)
        
        assert result is True
        
        # Vérifier
        commentaires = ActiviteService.obtenir_commentaires_activite(activite_test.id)
        assert len(commentaires) == 0
    
    def test_obtenir_nombre_commentaires(self, activite_test, utilisateur_test):
        """Test comptage des commentaires"""
        # Ajouter 3 commentaires
        for i in range(3):
            ActiviteService.ajouter_commentaire(
                utilisateur_test.id,
                activite_test.id,
                f"Commentaire {i+1}"
            )
        
        # Compter
        nb_commentaires = ActiviteService.obtenir_nombre_commentaires(activite_test.id)
        
        assert nb_commentaires == 3
    
    def test_commentaires_vides(self, activite_test):
        """Test récupération commentaires sur activité sans commentaires"""
        commentaires = ActiviteService.obtenir_commentaires_activite(activite_test.id)
        assert len(commentaires) == 0
        
        nb_commentaires = ActiviteService.obtenir_nombre_commentaires(activite_test.id)
        assert nb_commentaires == 0
    
    def test_commentaire_contenu_vide(self, activite_test, utilisateur_test):
        """Test ajout commentaire avec contenu vide (devrait réussir en base)"""
        commentaire = ActiviteService.ajouter_commentaire(
            utilisateur_test.id,
            activite_test.id,
            ""
        )
        # Le service ne valide pas le contenu vide, c'est OK
        assert commentaire is not None
    
    def test_multiple_utilisateurs_commentent(self, activite_test, setup_database):
        """Test plusieurs utilisateurs commentent la même activité"""
        # Créer un deuxième utilisateur
        user2 = UtilisateurService.creer_utilisateur(
            nom="Durand",
            prenom="Pierre",
            age=35,
            pseudo="pdurand_test",
            mail="pierre.test@example.com",
            mdp="pass123"
        )
        
        # Les deux commentent
        com1 = ActiviteService.ajouter_commentaire(
            activite_test.utilisateur_id,
            activite_test.id,
            "Commentaire auteur"
        )
        com2 = ActiviteService.ajouter_commentaire(
            user2.id,
            activite_test.id,
            "Commentaire autre"
        )
        
        # Vérifier
        commentaires = ActiviteService.obtenir_commentaires_activite(activite_test.id)
        assert len(commentaires) == 2
        assert com1.auteur_id != com2.auteur_id