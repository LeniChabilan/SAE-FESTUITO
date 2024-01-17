from sqlalchemy import Column, Integer, String, Boolean, Date,DateTime, Float, Text, ForeignKey , Time , LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .app import login_manager

Base = declarative_base()
from .app import db
from flask_login import UserMixin
from .app import login_manager

@login_manager.user_loader
def load_user(utilisateurId):
    return Utilisateur.query.get(utilisateurId)

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

class Utilisateur(db.Model,UserMixin):
    __tablename__ = 'Utilisateur'
    utilisateurId = Column(Integer, primary_key=True)
    nomUtilisateur = Column(String(255))
    emailUtilisateur = Column(String(255))
    MDPUtilisateur = Column(String(255))
    DdN= Column(Date)
    tel= Column(String(10))
    role = Column(String(255))

    def get_id(self):
        return self.utilisateurId
    
    def __init__(self, utilisateurId, nomUtilisateur, emailUtilisateur, MDPUtilisateur, DdN, tel, role):
        self.utilisateurId = utilisateurId
        self.nomUtilisateur = nomUtilisateur
        self.emailUtilisateur = emailUtilisateur
        self.MDPUtilisateur = MDPUtilisateur
        self.DdN = DdN 
        self.tel = tel
        self.role = role
        

    

class StyleMusical(db.Model):
    __tablename__ = 'StyleMusical'
    styleId = Column(Integer, primary_key=True)
    nomSM = Column(String(255))

class GroupeConcert(db.Model):
    __tablename__ = 'GroupeConcert'
    groupeConcertId = Column(Integer, primary_key=True)
    nomGroupeConcert = Column(String(255))
    descriptionGP = Column(Text)
    dateHeureDebutGP = Column(DateTime)
    dateHeureFinGP = Column(DateTime)

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
    photoGM = Column(String, nullable=True)
    styleId = Column(Integer, ForeignKey('StyleMusical.styleId'))
    style = relationship(StyleMusical)

    def __init__(self, groupeId, nomGM, descriptionGM, lienGM,image, styleId):
        self.groupeId = groupeId
        self.nomGM = nomGM
        self.descriptionGM = descriptionGM
        self.lienGM = lienGM
        self.photoGM=image
        self.styleId = styleId


class Artiste(db.Model):
    __tablename__ = 'Artiste'
    artisteId = Column(Integer, primary_key=True)
    nomArt = Column(String(255))
    groupeId = Column(Integer, ForeignKey('GroupeDeMusique.groupeId'))
    groupe = relationship(GroupeDeMusique)

    def __init__(self, artisteId, nomArt, groupeId):
        self.artisteId = artisteId
        self.nomArt = nomArt
        self.groupeId = groupeId

class Billet(db.Model):
    __tablename__ = 'Billet'
    billetId = Column(Integer, primary_key=True)
    typeB = Column(String(255))
    prixB = Column(Float)
    utilisateurId = Column(Integer, ForeignKey('Utilisateur.utilisateurId'))
    groupeConcertId = Column(Integer, ForeignKey('GroupeConcert.groupeConcertId'))
    utilisateur = relationship(Utilisateur)
    groupeC = relationship(GroupeConcert)

class Concert(db.Model):
    __tablename__ = 'Concert'
    concertId = Column(Integer, primary_key=True)
    dateHeureDebutConcert = Column(DateTime)
    dateHeureFinConcert = Column(DateTime)
    lieuId = Column(Integer, ForeignKey('Lieu.lieuId'))
    groupeConcertId = Column(Integer, ForeignKey('GroupeConcert.groupeConcertId'))
    groupeId = Column(Integer, ForeignKey('GroupeDeMusique.groupeId'))
    lieu = relationship(Lieu)
    groupeC = relationship(GroupeConcert)
    groupe = relationship(GroupeDeMusique)

class ActiviteAnnexe(db.Model):
    __tablename__ = 'ActiviteAnnexe'
    activiteId = Column(Integer, primary_key=True)
    descriptionACT = Column(Text)
    dateHeureACT = Column(DateTime)
    lieuId = Column(Integer, ForeignKey('Lieu.lieuId'))
    groupeConcertId = Column(Integer, ForeignKey('GroupeConcert.groupeConcertId'))
    VisibilitePubliqueACT = Column(Boolean)
    GroupeDeMusiqueID = Column(Integer, ForeignKey('GroupeDeMusique.groupeId'))
    lieu = relationship(Lieu)
    groupeC = relationship(GroupeConcert)
    groupe = relationship(GroupeDeMusique)

class PreInscription(db.Model):
    __tablename__ = 'PreInscription'
    preinscriptionId = Column(Integer, primary_key=True)
    utilisateurId = Column(Integer, ForeignKey('Utilisateur.utilisateurId'))
    groupeConcertId = Column(Integer, ForeignKey('GroupeConcert.groupeConcertId'))
    dateHeurePI = Column(DateTime)
    utilisateur = relationship(Utilisateur)
    groupeC = relationship(GroupeConcert)

class GroupesFavoris(db.Model):
    __tablename__ = 'GroupesFavoris'
    utilisateurId = Column(Integer, ForeignKey('Utilisateur.utilisateurId'), primary_key=True)
    groupeId = Column(Integer, ForeignKey('GroupeDeMusique.groupeId'), primary_key=True)
    utilisateur = relationship(Utilisateur)
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
