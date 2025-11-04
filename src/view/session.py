"""
Gestion de la session utilisateur
"""


class Session:
    """Singleton pour gérer la session utilisateur"""
    
    _instance = None
    _utilisateur = None
    
    def __new__(cls):
        """Implémentation du pattern Singleton"""
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
        return cls._instance
    
    @property
    def utilisateur(self):
        """
        Retourne l'utilisateur connecté
        
        Returns:
            Utilisateur: L'utilisateur connecté ou None
        """
        return self._utilisateur
    
    @utilisateur.setter
    def utilisateur(self, user):
        """
        Définit l'utilisateur connecté
        
        Args:
            user: L'utilisateur à connecter
        """
        self._utilisateur = user
    
    def deconnexion(self):
        """Déconnecte l'utilisateur"""
        self._utilisateur = None
    
    def est_connecte(self):
        """
        Vérifie si un utilisateur est connecté
        
        Returns:
            bool: True si connecté, False sinon
        """
        return self._utilisateur is not None
    
    def afficher(self):
        """
        Affiche les informations de session
        
        Returns:
            str: Message formaté avec les infos de session
        """
        if self.est_connecte():
            return (
                f"📊 INFORMATIONS DE SESSION\n"
                f"{'=' * 50}\n"
                f"👤 Utilisateur : {self._utilisateur.pseudo}\n"
                f"📧 Email : {self._utilisateur.mail}\n"
                f"👥 Nom : {self._utilisateur.prenom} {self._utilisateur.nom}\n"
                f"🎂 Âge : {self._utilisateur.age} ans\n"
                f"{'=' * 50}"
            )
        else:
            return "❌ Aucun utilisateur connecté"