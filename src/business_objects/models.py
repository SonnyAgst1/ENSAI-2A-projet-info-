from sqlalchemy import (
    Column, Integer, String, Float,
    Date, Text, LargeBinary, ForeignKey, Table,
)
from sqlalchemy.orm import relationship
from src.database import Base

# --- Tables de Liaison (Many-to-Many) ---

follows = Table(
    'Follow', 
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('Utilisateur.id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('Utilisateur.id'), primary_key=True), 
    extend_existing=True
)

likes = Table(
    'Like', 
    Base.metadata,
    Column('utilisateur_id', Integer, ForeignKey('Utilisateur.id'), primary_key=True),
    Column('activite_id', Integer, ForeignKey('Activite.id'), primary_key=True), 
    extend_existing=True
)


# --- Classes ORM Principales ---

class Utilisateur(Base):
    __tablename__ = 'Utilisateur'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    age = Column(Integer)
    taille = Column(Float)
    pseudo = Column(String, unique=True, nullable=False)
    poids = Column(Float)
    photo_profil = Column(LargeBinary)
    mail = Column(String, unique=True, nullable=False)
    telephone = Column(String)
    mdp = Column(String, nullable=False)

    # Relations ORM - AVEC chemins complets
    followers = relationship(
        "business_objects.models.Utilisateur",  # <--- MODIFIÉ
        secondary=follows,
        primaryjoin=(follows.c.followed_id == id),
        secondaryjoin=(follows.c.follower_id == id),
        backref="following",
        lazy='dynamic'
    )
    activites = relationship("business_objects.models.Activite", back_populates="utilisateur") # <--- MODIFIÉ
    commentaires = relationship("business_objects.models.Commentaire", back_populates="auteur") # <--- MODIFIÉ
    liked_activites = relationship(
        "business_objects.models.Activite", # <--- MODIFIÉ
        secondary=likes,
        back_populates="likers"
    )

    def __repr__(self):
        return f"<Utilisateur(pseudo='{self.pseudo}')>"


class Activite(Base):
    __tablename__ = 'Activite'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nom = Column(String(255))
    type_sport = Column(String, nullable=False, default="unknow")
    date_activite = Column(Date, nullable=False)
    duree_activite = Column(Integer)
    description = Column(Text, nullable=True)
    gpx_path = Column(String(512))
    d_plus = Column(Integer, nullable=True)
    calories = Column(Integer, nullable=True)

    utilisateur_id = Column(Integer, ForeignKey('Utilisateur.id'), nullable=False)

    # Relations ORM
    utilisateur = relationship("business_objects.models.Utilisateur", back_populates="activites") # <--- MODIFIÉ
    commentaires = relationship(
        "business_objects.models.Commentaire", # <--- MODIFIÉ
        back_populates="activite", 
        cascade="all, delete-orphan"
    )
    likers = relationship(
        "business_objects.models.Utilisateur", # <--- MODIFIÉ
        secondary=likes,
        back_populates="liked_activites"
    )

    def __repr__(self):
        return f"<Activite(nom='{self.nom}', type='{self.type_sport}')>"


class Commentaire(Base):
    __tablename__ = 'Commentaire'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    contenu = Column(Text, nullable=False)

    activite_id = Column(Integer, ForeignKey('Activite.id'), nullable=False)
    auteur_id = Column(Integer, ForeignKey('Utilisateur.id'), nullable=False)

    # Relations ORM
    activite = relationship("business_objects.models.Activite", back_populates="commentaires") # <--- MODIFIÉ
    auteur = relationship("business_objects.models.Utilisateur", back_populates="commentaires") # <--- MODIFIÉ

    def __repr__(self):
        return f"<Commentaire(id={self.id}, activite_id={self.activite_id})>"