from sqlalchemy import (
    create_engine, Column, Integer, String, Float,
    Date, Text, LargeBinary, ForeignKey, Table
)
from sqlalchemy.orm import declarative_base, relationship
from database import Base

# --- Tables de Liaison (Many-to-Many) ---

# Table de liaison pour les followers (Follow)
follows = Table('Follow', Base.metadata,
                Column('follower_id', Integer, ForeignKey('Utilisateur.id'), primary_key=True),
                Column('followed_id', Integer, ForeignKey('Utilisateur.id'), primary_key=True)
                )

# Table de liaison pour les Likes sur les activités
likes = Table('Like', Base.metadata,
              Column('utilisateur_id', Integer, ForeignKey('Utilisateur.id'), primary_key=True),
              Column('activite_id', Integer, ForeignKey('Activite.id'), primary_key=True)
              )


# --- Classes ORM Principales ---

class Utilisateur(Base):
    __tablename__ = 'Utilisateur'

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    age = Column(Integer)
    taille = Column(Float)
    pseudo = Column(String, unique=True, nullable=False)
    poids = Column(Float)
    photo_profil = Column(LargeBinary)
    mail = Column(String, unique=True, nullable=False)
    telephone = Column(String, nullage = True)
    mdp = Column(String, nullable=False)

    # Relations ORM
    followers = relationship(
        "Utilisateur",
        secondary=follows,
        primaryjoin=(follows.c.followed_id == id),
        secondaryjoin=(follows.c.follower_id == id),
        backref="following",
        lazy='dynamic'
    )
    activites = relationship("Activite", back_populates="utilisateur")
    commentaires = relationship("Commentaire", back_populates="auteur")
    liked_activites = relationship(
        "Activite",
        secondary=likes,
        back_populates="likers"
    )

    def __repr__(self):
        return f"<Utilisateur(pseudo='{self.pseudo}')>"


class Activite(Base):
    __tablename__ = 'Activite'

    id = Column(Integer, primary_key=True)
    nom = Column(String(255))
    type_sport = Column(String, nullable=False, default="unknow")
    date_activite = Column(Date, nullable=False, default="unknow")
    duree_activite = Column(Integer)
    description = Column(Text, nullable=True)
    gpx_path = Column(String(512))
    d_plus = Column(Integer, nullable=True)
    calories = Column(Integer, nullable=True)

    utilisateur_id = Column(Integer, ForeignKey('Utilisateur.id'), nullable=False)

    # Relations ORM
    utilisateur = relationship("Utilisateur", back_populates="activites")
    commentaires = relationship(
        "Commentaire", back_populates="activite", cascade="all, delete-orphan"
        )
    likers = relationship(
        "Utilisateur",
        secondary=likes,
        back_populates="liked_activites"
    )

    def __repr__(self):
        return f"<Activite(nom='{self.nom}', type='{self.type_sport}')>"


class Commentaire(Base):
    __tablename__ = 'Commentaire'

    id = Column(Integer, primary_key=True)
    contenu = Column(Text, nullable=False)

    activite_id = Column(Integer, ForeignKey('Activite.id'), nullable=False)
    auteur_id = Column(Integer, ForeignKey('Utilisateur.id'), nullable=False)

    # Relations ORM
    activite = relationship("Activite", back_populates="commentaires")
    auteur = relationship("Utilisateur", back_populates="commentaires")

    def __repr__(self):
        return f"<Commentaire(id={self.id}, activite_id={self.activite_id})>"
