import unittest
from unittest.mock import patch
from service.fil_activite import FilDActivite

class MockPrinter:
    """
    Mock très simple pour remplacer print().
    Il stocke tous les messages dans self.logs (liste de str).
    """
    def __init__(self):
        self.logs = []

    def print(self, *args, **kwargs):
        # Reproduit le comportement de print en joignant les args par des espaces
        msg = " ".join(str(a) for a in args)
        self.logs.append(msg)


# =========================
# Tests
# =========================
class TestFilDActiviteAvecMock(unittest.TestCase):
    """
    Tests unitaires de FilDActivite qui utilisent une classe mock (MockPrinter)
    pour vérifier les sorties sans rien afficher à l'écran.
    """

    def setUp(self):
        # Un FilDActivite neuf avant chaque test
        self.fil = FilDActivite()
        # Notre mock de console
        self.console = MockPrinter()

    def test_ajouterActivite(self):
        """
        TEST de ajouterActivite():
          - Doit ajouter l'activité dans la liste interne
          - Doit afficher le bon message via print()
        """
        with patch("builtins.print", self.console.print):
            self.fil.ajouterActivite("Course à pied - 5 km")

        # 1) État interne
        self.assertEqual(self.fil.activites, ["Course à pied - 5 km"])

        # 2) Sorties
        self.assertEqual(len(self.console.logs), 1)
        self.assertEqual(self.console.logs[0], "Activité ajoutée : Course à pied - 5 km")

    def test_rafraichirFil(self):
        """
        TEST de rafraichirFil():
          - Doit afficher 2 lignes :
              1) 'Le fil d'activité a été rafraîchi.'
              2) 'Il contient actuellement X activité(s).'
          - X doit être la longueur de la liste activites.
        """
        # On prépare des données
        self.fil.activites.extend(["A1", "A2", "A3"])

        with patch("builtins.print", self.console.print):
            self.fil.rafraichirFil()

        # Vérifie les 2 lignes
        self.assertEqual(self.console.logs, [
            "Le fil d'activité a été rafraîchi.",
            "Il contient actuellement 3 activité(s)."
        ])


if __name__ == "__main__":
    unittest.main(verbosity=2)
