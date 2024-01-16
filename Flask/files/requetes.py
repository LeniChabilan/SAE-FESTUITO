from .models import *
from sqlalchemy import create_engine,asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import pymysql
from datetime import datetime
import os

from sqlalchemy.orm import joinedload

from .models import Utilisateur
from hashlib import sha256


from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64

Base = declarative_base()
from .app import db
from flask_login import UserMixin
from .app import login_manager

from .models import Utilisateur

def login():
    login='debray'
    passwd='debray'
    serveur='servinfo-maria'
    bd='DBdebray'
    engine=create_engine('mysql+mysqldb://'+login+':'+passwd+'@'+serveur+'/'+bd, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session




def create_user(nom,email,mdp,ddn,tel):
    session=login()
    id=session.query(func.max(Utilisateur.utilisateurId)).all()[0][0]+1
    print(id)
    role="Spectateur"
    m = sha256()
    m.update(mdp.encode())
    user=Utilisateur(id,nom,email,m.hexdigest(),ddn,tel,role)
    print(user.nomUtilisateur)
    print(user.emailUtilisateur)
    print(user.MDPUtilisateur)
    session.add(user)
    session.commit()

def get_info_utilisateur(id):

    session=login()
    return session.query(Utilisateur).filter(Utilisateur.utilisateurId==id).first()

def get_info_utilisateur():
    session=login()
    return session.query(Utilisateur).all()


def get_info_groupe():
    session=login()
    return session.query(GroupeDeMusique).options(joinedload(GroupeDeMusique.style)).all()

def get_info_un_groupe(id):
    session=login()
    return session.query(GroupeDeMusique).filter(GroupeDeMusique.groupeId==id).first()

def get_info_un_artiste(id):
    session=login()
    return session.query(Artiste).filter(Artiste.artisteId==id).first()

def get_info_artiste():
    session=login()
    return session.query(Artiste).options(joinedload(Artiste.groupe)).all()

def get_info_concert():
    session=login()
    return session.query(Concert).options(joinedload(Concert.groupe), joinedload(Concert.lieu)).all()

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
    


def get_max_id_concert():
    session = login()
    if session.query(func.max(Concert.concertId)).all()[0][0] is None:
        return 1
    return session.query(func.max(Concert.concertId)).all()[0][0] + 1


def ajouter_concert(dateHeureDebutConcert,dateHeureFinConcert, lieuId, festivalId,groupeId):
    session=login()
    conc=Concert(get_max_id_concert(),datetime.strptime(dateHeureDebutConcert,"%Y-%m-%d").date(),datetime.strptime(dateHeureFinConcert,"%Y-%m-%d").date(),lieuId,festivalId,groupeId)
    session.add(conc)
    session.commit()

def get_max_id_groupe():
    session = login()
    if session.query(func.max(GroupeDeMusique.groupeId)).all()[0][0] is None:
        return 1
    return session.query(func.max(GroupeDeMusique.groupeId)).all()[0][0] + 1

def ajouter_groupe(nom,description,lien,image,styleId):
    session = login()
    grp=GroupeDeMusique(get_max_id_groupe(),nom,description,lien,image,styleId)
    session.add(grp)
    session.commit()

def mod_concert(id,dateHeureDebutConcert,dateFin, lieuId, festivalId,groupeId):
    session = login()
    conc=get_info_un_concert(id)
    if conc:
        conc.dateHeureDebutConcert=dateHeureDebutConcert
        conc.dateHeureFinConcert=dateFin
        conc.lieuId=lieuId
        conc.festivalId=festivalId
        conc.groupeId=groupeId
        session.commit()
    else:
        print("le concert n'a pas été trouvé")
    

def mod_groupe(id,nom,description,lien,image,styleId):
    session=login()
    grp=get_info_un_groupe(id)
    if grp:
        grp.nom=nom
        grp.description=description
        grp.image=image
        grp.styleId=styleId
        grp.lien=lien
        session.commit()
    else:
        print("Le groupe n'a pas été trouvé")

def sup_concert(id):
    session=login()
    try:
        session.query(Lieu).filter_by(concertId=id).delete(synchronize_session=False)
        session.query(Festival).filter_by(concertId=id).delete(synchronize_session=False)
        session.query(GroupeDeMusique).filter_by(concertId=id).delete(synchronize_session=False)
        session.commit()
        return "Concert supprimé"
    except:
        session.rollback()
        return "Erreur"

def get_user_by_email(email):
    session=login()
    return session.query(Utilisateur).filter(Utilisateur.emailUtilisateur==email).first()


def get_user_by_id(id):
    session=login()
    return session.query(Utilisateur).filter(Utilisateur.utilisateurId==id).first()

def mod_artiste(id, nom, mail, mdp, ddn, tel):
    session=login()
    art=session.query(Utilisateur).filter(Utilisateur.utilisateurId==id).first()
    if art:
        print(art.nomUtilisateur, art.emailUtilisateur, art.MDPUtilisateur, art.DdN, art.tel)
        art.nomUtilisateur=nom
        art.emailUtilisateur=mail
        m = sha256()
        m.update(mdp.encode())
        art.MDPUtilisateur=m.hexdigest()
        art.DdN=ddn
        art.tel=tel
        print(art.nomUtilisateur, art.emailUtilisateur, art.MDPUtilisateur, art.DdN, art.tel)
        session.commit()
    else:
        print("L'artiste n'a pas été trouvé")



def get_prochain_concert():
    session = login()
    
    conc = (
        session.query(Concert)
        .options(joinedload(Concert.groupe))
        .filter(Concert.dateHeureDebutConcert >= datetime.now())
        .order_by(asc(Concert.dateHeureDebutConcert))
        .first()
    )

    return conc



def supprimer_concert(id):
    try:
        # Supprimez le concert et toutes les lignes liées dans d'autres tables
        db.session.query(OrganisationDunGroupe).filter_by(concertId=id).delete(synchronize_session=False)

        db.session.query(Concert).filter_by(concertId=id).delete(synchronize_session=False)

        db.session.commit()
        return "Concert et enregistrements liés supprimés avec succès."
    except pymysql.IntegrityError:
        # Si une contrainte de clé étrangère empêche la suppression, gérez l'erreur ici
        db.session.rollback()
        return "Erreur : Impossible de supprimer le concert et ses enregistrements liés en raison de contraintes de clé étrangère."


def supprimer_artiste(id):
    try:
        # Supprimez le concert et toutes les lignes liées dans d'autres tables
        db.session.query(Jouer).filter_by(ArtisteId=id).delete(synchronize_session=False)

        db.session.query(Artiste).filter_by(artisteId=id).delete(synchronize_session=False)

        db.session.commit()
        return "Artiste et enregistrements liés supprimés avec succès."
    except pymysql.IntegrityError:
        # Si une contrainte de clé étrangère empêche la suppression, gérez l'erreur ici
        db.session.rollback()
        return "Erreur : Impossible de supprimer l'artiste et ses enregistrements liés en raison de contraintes de clé étrangère."


def supprimer_groupe(id):
    try:
        session=login()
        conc=session.query(Concert).filter_by(groupeId=id).first()
        
        # Supprimez le concert et toutes les lignes liées dans d'autres tables
        session.query(Artiste).filter_by(groupeId=id).delete(synchronize_session=False)
        supprimer_concert(conc.concertId)
        session.query(ActiviteAnnexe).filter_by(GroupeDeMusiqueID=id).delete(synchronize_session=False)
        session.query(GroupesFavoris).filter_by(groupeId=id).delete(synchronize_session=False)

        session.query(GroupeDeMusique).filter_by(groupeId=id).delete(synchronize_session=False)

        session.commit()
        return "Groupe et enregistrements liés supprimés avec succès."
    except pymysql.IntegrityError:
        # Si une contrainte de clé étrangère empêche la suppression, gérez l'erreur ici
        db.session.rollback()
        return "Erreur : Impossible de supprimer le groupe et ses enregistrements liés en raison de contraintes de clé étrangère."



def supprimer_utilisateur(id):
    try:
        # Supprimez le concert et toutes les lignes liées dans d'autres tables
        db.session.query(PreInscription).filter_by(utilisateurId=id).delete(synchronize_session=False)
        db.session.query(GroupesFavoris).filter_by(utilisateurId=id).delete(synchronize_session=False)
        db.session.query(Billet).filter_by(utilisateurId=id).delete(synchronize_session=False)
        db.session.query(Utilisateur).filter_by(utilisateurId=id).delete(synchronize_session=False)

        db.session.commit()
        return "Utilisateur et enregistrements liés supprimés avec succès."
    except pymysql.IntegrityError:
        # Si une contrainte de clé étrangère empêche la suppression, gérez l'erreur ici
        db.session.rollback()
        return "Erreur : Impossible de supprimer l'utilisateur et ses enregistrements liés en raison de contraintes de clé étrangère."
