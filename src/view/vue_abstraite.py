"""
Classe abstraite pour les vues de l'application
"""
from abc import ABC, abstractmethod


class VueAbstraite(ABC):
    """Classe abstraite pour les vues"""
    
    def __init__(self, message=""):
        """
        Initialisation de la vue
        
        Args:
            message: Message à afficher (optionnel)
        """
        self.message = message
    
    @abstractmethod
    def choisir_menu(self):
        """
        Méthode abstraite pour le choix du menu
        Doit être implémentée par toutes les classes filles
        
        Returns:
            VueAbstraite: La prochaine vue à afficher
        """
        pass
    
    def afficher(self):
        """
        Affiche le message de la vue
        """
        if self.message:
            print("\n" + "=" * 50)
            print(self.message)
            print("=" * 50 + "\n")