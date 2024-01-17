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

def get_info_lieu():
    session=login()
    return session.query(Lieu).all()

def get_info_un_lieu(id):
    session=login()
    return session.query(Lieu).filter(Lieu.lieuId==id).first()

def get_info_activite_annexe(id):
    session=login()
    return session.query(ActiviteAnnexe).filter(ActiviteAnnexe.activiteId==id).first()

def get_info_toutes_activite():
    session=login()
    return session.query(ActiviteAnnexe).all()

def get_info_groupe_concert():
    session=login()
    return session.query(GroupeConcert).all()


def get_groupe_favori(idUtil):
    session=login()
    return session.query(GroupesFavoris).filter(GroupesFavoris.utilisateurId==idUtil).all()
    
def get_info_style():
    session=login()
    return session.query(StyleMusical).all()

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

def create_groupe(nom, description, lien, image, style):
    try:
        session = login()
        stl = session.query(StyleMusical).filter_by(nomSM=style).first()
        styleId = stl.styleId
        id = session.query(func.max(GroupeDeMusique.groupeId)).all()[0][0] + 1
        groupe = GroupeDeMusique(
            groupeId=id,
            nomGM=nom,
            descriptionGM=description,
            lienGM=lien,
            image=image,
            styleId=styleId
        )
        session.add(groupe)
        print(f"Groupe ajouté avec l'ID : {groupe.groupeId}")
        
        session.commit()
        return groupe.groupeId
    except Exception as e:
        print(f"Erreur lors de la création du groupe : {str(e)}")
        session.rollback()  # Annule la transaction en cas d'erreur
    finally:
        session.close()


def create_artiste(nom, groupeId):
    session = login()
    id = session.query(func.max(Artiste.artisteId)).all()[0][0] + 1
    artiste = Artiste(id, nom, groupeId)
    session.add(artiste)
    session.commit()

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


def get_info_un_utilisateur(id):
    session=login()
    return session.query(Utilisateur).filter(Utilisateur.utilisateurId==id).first()

def get_user_by_id(id):
    session=login()
    return session.query(Utilisateur).filter(Utilisateur.utilisateurId==id).first()

def mod_utilisateur(id, nom, mail, mdp, ddn, tel):
    session=login()
    util=session.query(Utilisateur).filter(Utilisateur.utilisateurId==id).first()
    if util:
        print(util.nomUtilisateur, util.emailUtilisateur, util.MDPUtilisateur, util.DdN, util.tel)
        util.nomUtilisateur=nom
        util.emailUtilisateur=mail
        m = sha256()
        m.update(mdp.encode())
        util.MDPUtilisateur=m.hexdigest()
        util.DdN=ddn
        util.tel=tel
        print(util.nomUtilisateur, util.emailUtilisateur, util.MDPUtilisateur, util.DdN, util.tel)
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
        if conc is not None : 
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
        db.session.query(AcheterBillet).filter_by(utilisateurId=id).delete(synchronize_session=False)
        db.session.query(Utilisateur).filter_by(utilisateurId=id).delete(synchronize_session=False)

        db.session.commit()
        return "Utilisateur et enregistrements liés supprimés avec succès."
    except pymysql.IntegrityError:
        # Si une contrainte de clé étrangère empêche la suppression, gérez l'erreur ici
        db.session.rollback()
        return "Erreur : Impossible de supprimer l'utilisateur et ses enregistrements liés en raison de contraintes de clé étrangère."


def mod_artiste(id,nom, grp):
   
    session = login()
    art = session.query(Artiste).filter_by(artisteId = id).first()

    groupe=session.query(GroupeDeMusique).filter_by(nomGM = grp).first()
    grpId=groupe.groupeId
    if art:
        art.nomArt = nom
        
        art.groupeId = grpId
        art.groupe=groupe
        session.commit()
    else:
        print("L'artiste n'a pas été trouvé.")


def mod_groupe(id,nom, description,lien,style):
   
    session = login()
    groupe = session.query(GroupeDeMusique).filter_by(groupeId = id).first()

    stl=session.query(StyleMusical).filter_by(nomSM = style).first()
    styleID=stl.styleId
    if groupe:
        groupe.nomGM = nom
        
        groupe.descriptionGM = description
        groupe.lienGM=lien
        groupe.style=stl
        groupe.styleId = styleID
        session.commit()
    else:
        print("Le groupe n'a pas été trouvé.")


def mod_concert(id, dateD,dateF,lieu,grp,grpC):
   
    session = login()
    conc = session.query(Concert).filter_by(concertId = id).first()

    lieuC=session.query(Lieu).filter_by(nomL = lieu).first()
    lieuId=lieuC.lieuId
    groupe=session.query(GroupeDeMusique).filter_by(nomGM = grp).first()
    groupeId=groupe.groupeId
    groupeC=session.query(GroupeConcert).filter_by(nomGroupeConcert = grpC).first()
    groupeCId=groupeC.groupeConcertId
    
    if conc:
        conc.dateHeureDebutConcert = dateD
        
        conc.dateHeureFinConcert = dateF
        conc.lieuId=lieuId
        conc.lieu=lieuC
        conc.groupe=groupe
        conc.groupeC=groupeC
        conc.groupeConcertId=groupeCId
        conc.groupeId=groupeId
        session.commit()
    else:
        print("Le concert n'a pas été trouvé.")


def creer_conc(dateD, dateF, lieu, grp, grpC):
    session = login()

    lieuC = session.query(Lieu).filter_by(nomL=lieu).first()
    lieuId = lieuC.lieuId
    groupe = session.query(GroupeDeMusique).filter_by(nomGM=grp).first()
    groupeId = groupe.groupeId
    groupeC = session.query(GroupeConcert).filter_by(nomGroupeConcert=grpC).first()
    groupeCId = groupeC.groupeConcertId

    concert = Concert(
        dateHeureDebutConcert=datetime.strptime(dateD, "%Y-%m-%dT%H:%M"),
        dateHeureFinConcert=datetime.strptime(dateF, "%Y-%m-%dT%H:%M"),
        lieuId=lieuId,
        groupeConcertId=groupeCId,
        groupeId=groupeId
    )
    session.add(concert)
    session.commit()
