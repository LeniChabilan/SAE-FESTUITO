from .models import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import pymysql
from datetime import datetime
import os

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64

Base = declarative_base()
from .app import db
from flask_login import UserMixin
from .app import login_manager

def login():
    login='chabilan'
    passwd='chabilan'
    serveur='servinfo-maria'
    bd='DBchabilan'
    engine=create_engine('mysql+mysqldb://'+login+':'+passwd+'@'+serveur+'/'+bd, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def get_info_utilisateur(id):
    session=login()
    return session.query(Utilisateur).filter(Utilisateur.utilisateurId==id).first()


def get_info_groupe(id):
    session=login()
    return session.query(Groupe).filter(Groupe.groupeId==id).first()

def get_info_artiste(id):
    session=login()
    return session.query(Artiste).filter(Artiste.artisteId==id).first()

def get_info_tous_concert():
    session=login()
    return session.query(Concert).all()

def get_info_un_concert(id):
    session=login()
    return session.query(Concert).filter(Concert.concertId==id).first()

def get_info_billet(id):
    session=login()
    return session.query(Billet).filter(Billet.billetId==id).first()

def get_info_lieu(id):
    session=login()
    return session.query(Lieu).filter(Lieu.lieuId==id).first()

def get_info_activite_annexe(id):
    session=login()
    return session.query(ActiviteAnnexe).filter(ActiviteAnnexe.activiteId==id).first()

def get_info_toutes_activite():
    session=login()
    return session.query(ActiviteAnnexe).all()

def get_groupe_favori(idUtil):
    session=login()
    return session.query(GroupesFavoris).filter(GroupesFavoris.utilisateurId==idUtil).all()
    