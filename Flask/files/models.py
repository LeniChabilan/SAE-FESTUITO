from sqlalchemy import Column, Integer, String, Boolean, Date,DateTime, Float, Text, ForeignKey , Time 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
from .app import db
# from flask_login import UserMixin
# from .app import login_manager

# @login_manager.user_loader
# def load_user(nomOrga):
#     return Organisation.query.get(nomOrga)

class Lieu(db.Model):
    __tablename__ = 'Lieu'
    lieuId = Column(Integer, primary_key=True)
    nomL = Column(String(255))
    capaciteL = Column(Integer)
    adresseL = Column(String(255))

class Instrument(db.Model):
    __tablename__ = 'Instrument'
    instrumentId = Column(Integer, primary_key=True)
    nomInstru = Column(String(255))

class Spectateur(db.Model):
    __tablename__ = 'Spectateur'
    spectateurId = Column(Integer, primary_key=True)
    nomSpec = Column(String(255))
    emailSpec = Column(String(255))
    MDPSpec = Column(String(255))

class StyleMusical(db.Model):
    __tablename__ = 'StyleMusical'
    styleId = Column(Integer, primary_key=True)
    nomSM = Column(String(255))

class Festival(db.Model):
    __tablename__ = 'Festival'
    festivalId = Column(Integer, primary_key=True)
    nomF = Column(String(255))
    dateDebutF = Column(Date)
    DateHeureFinF = Column(DateTime, nullable=False)

# class StyleSimilaire(db.Model):
#     __tablename__ = 'StyleSimilaire'
#     styleId = Column(Integer, primary_key=True)
#     styleSim = Column(Integer, ForeignKey('StyleMusical.styleId'))
#     style = relationship(StyleMusical, foreign_keys=[styleId])
#     styleSimilaire = relationship(StyleMusical, foreign_keys=[styleSim])


class StyleSimilaire(db.Model):
    __tablename__ = 'StyleSimilaire'
    styleId = Column(Integer, ForeignKey('StyleMusical.styleId'), primary_key=True)
    styleSim = Column(Integer, ForeignKey('StyleMusical.styleId'))
    style = relationship('StyleMusical', foreign_keys=[styleId], backref='style_similar')
    styleSimilaire = relationship('StyleMusical', foreign_keys=[styleSim])


class GroupeDeMusique(db.Model):
    __tablename__ = 'GroupeDeMusique'
    groupeId = Column(Integer, primary_key=True)
    nomGM = Column(String(255))
    descriptionGM = Column(Text)
    lienGM = Column(String(255))
    styleId = Column(Integer, ForeignKey('StyleMusical.styleId'))
    style = relationship(StyleMusical)

class Artiste(db.Model):
    __tablename__ = 'Artiste'
    artisteId = Column(Integer, primary_key=True)
    nomArt = Column(String(255))
    groupeId = Column(Integer, ForeignKey('GroupeDeMusique.groupeId'))
    groupe = relationship(GroupeDeMusique)

class Billet(db.Model):
    __tablename__ = 'Billet'
    billetId = Column(Integer, primary_key=True)
    typeB = Column(String(255))
    prixB = Column(Float)
    spectateurId = Column(Integer, ForeignKey('Spectateur.spectateurId'))
    festivalId = Column(Integer, ForeignKey('Festival.festivalId'))
    spectateur = relationship(Spectateur)
    festival = relationship(Festival)

class Concert(db.Model):
    __tablename__ = 'Concert'
    concertId = Column(Integer, primary_key=True)
    dateHeureDebutConcert = Column(DateTime)
    dureeConcert = Column(Integer)
    lieuId = Column(Integer, ForeignKey('Lieu.lieuId'))
    festivalId = Column(Integer, ForeignKey('Festival.festivalId'))
    groupeId = Column(Integer, ForeignKey('GroupeDeMusique.groupeId'))
    lieu = relationship(Lieu)
    festival = relationship(Festival)
    groupe = relationship(GroupeDeMusique)

class ActiviteAnnexe(db.Model):
    __tablename__ = 'ActiviteAnnexe'
    activiteId = Column(Integer, primary_key=True)
    descriptionACT = Column(Text)
    dateHeureACT = Column(DateTime)
    lieuId = Column(Integer, ForeignKey('Lieu.lieuId'))
    festivalId = Column(Integer, ForeignKey('Festival.festivalId'))
    VisibilitePubliqueACT = Column(Boolean)
    GroupeDeMusiqueID = Column(Integer, ForeignKey('GroupeDeMusique.groupeId'))
    lieu = relationship(Lieu)
    festival = relationship(Festival)
    groupe = relationship(GroupeDeMusique)

class PreInscription(db.Model):
    __tablename__ = 'PreInscription'
    preinscriptionId = Column(Integer, primary_key=True)
    spectateurId = Column(Integer, ForeignKey('Spectateur.spectateurId'))
    festivalId = Column(Integer, ForeignKey('Festival.festivalId'))
    dateHeurePI = Column(DateTime)
    spectateur = relationship(Spectateur)
    festival = relationship(Festival)

class GroupesFavoris(db.Model):
    __tablename__ = 'GroupesFavoris'
    spectateurId = Column(Integer, ForeignKey('Spectateur.spectateurId'), primary_key=True)
    groupeId = Column(Integer, ForeignKey('GroupeDeMusique.groupeId'), primary_key=True)
    spectateur = relationship(Spectateur)
    groupe = relationship(GroupeDeMusique)

class Hebergement(db.Model):
    __tablename__ = 'Hebergement'
    HebergementID = Column(Integer, primary_key=True, autoincrement=True)
    NomDeLHebergement = Column(String(255), nullable=False)
    PlacesDisponiblesParJour = Column(Integer, nullable=False)

class OrganisationDunGroupe(db.Model):
    __tablename__ = 'OrganisationDunGroupe'
    OrgaID = Column(Integer, primary_key=True, autoincrement=True)
    concertId = Column(Integer, ForeignKey('Concert.concertId'))
    JourArriveeODG = Column(Date)
    HeureArriveeODG = Column(Time)
    JourDepartODG = Column(Date)
    HeureDepartODG = Column(Time)
    TempsDeMontageODG = Column(Time)
    TempsDeDemontageODG = Column(Time)
    HebergementID = Column(Integer, ForeignKey('Hebergement.HebergementID'))
    concert = relationship(Concert)
    hebergement = relationship(Hebergement)

class Jouer(db.Model):
    __tablename__ = 'Jouer'
    instrumentId = Column(Integer, ForeignKey('Instrument.instrumentId'), primary_key=True)
    ArtisteId = Column(Integer, ForeignKey('Artiste.artisteId'), primary_key=True)
    instrument = relationship(Instrument)
    artiste = relationship(Artiste)
