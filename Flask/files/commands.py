import click
from .app import app,db
# from datetime import datetime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
# from sqlalchemy.exc import IntegrityError
import base64


@app.cli.command()
@click.argument('filename')

def loaddb(filename):
    '''
     Create all tables and populate them with data in filename
    '''
    login = 'debray'
    passwd = 'debray'
    serveur = 'servinfo-maria'
    bd = 'DBdebray'
    engine = create_engine(f'mysql+mysqldb://{login}:{passwd}@{serveur}/{bd}', echo=False)
    print("--- Suppression de toutes les tables de la BD ---")
    db.metadata.drop_all(bind=engine)

    print("--- Construction des tables de la BD ---")
    db.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # importation des données à partir de yaml
    import yaml
    data = yaml.safe_load(open(filename))
    from .models import Lieu, Instrument, Utilisateur, StyleMusical, GroupeConcert , Necessiter, TypeBillet , AcheterBillet ,StyleSimilaire, GroupeDeMusique, Artiste,Concert, ActiviteAnnexe, PreInscription, GroupesFavoris, Hebergement, OrganisationDunGroupe, Jouer


    for nomTable in data:
        if "Lieu" in nomTable:
            lieux = nomTable["Lieu"]
            for lieu_data in lieux:
                lieu = Lieu(lieuId=lieu_data["lieuId"], nomL=lieu_data["nomL"], capaciteL=lieu_data["capaciteL"], adresseL=lieu_data["adresseL"])
                session.add(lieu)
                session.commit()


        elif "Instrument" in nomTable:
            instruments = nomTable["Instrument"]
            for instrument_data in instruments:
                instrument = Instrument(instrumentId=instrument_data["instrumentId"], nomInstru=instrument_data["nomInstru"])
                session.add(instrument)

        elif "Utilisateur" in nomTable:
            utilisateur = nomTable["Utilisateur"]
            for utilisateur_data in utilisateur:
                from .models import Utilisateur
                from hashlib import sha256
                m = sha256()
                m.update(utilisateur_data["MDPUtilisateur"].encode())
                u =Utilisateur(utilisateurId=utilisateur_data["utilisateurId"], nomUtilisateur=utilisateur_data["nomUtilisateur"], emailUtilisateur=utilisateur_data["emailUtilisateur"], MDPUtilisateur= m.hexdigest(), DdN=utilisateur_data["DdN"],tel=utilisateur_data["tel"],role=utilisateur_data["role"])
                # neworg(engine,organisation_data["nomOrga"],organisation_data["motDePasse"],organisation_data["typeOrga"])
                # organisation = Organisation(nomOrga=organisation_data["nomOrga"], motDePasse=organisation_data["motDePasse"], typeOrga=organisation_data["typeOrga"])
                session.add(u)

        elif "StyleMusical" in nomTable:
            styles = nomTable["StyleMusical"]
            for style_data in styles:
                style = StyleMusical(styleId=style_data["styleId"], nomSM=style_data["nomSM"])
                session.add(style)

        # elif "Festival" in nomTable:
        #     festivals = nomTable["Festival"]
        #     for festival_data in festivals:
        #         festival = Festival(festivalId=festival_data["festivalId"], nomF=festival_data["nomF"], dateHeureDebutF=festival_data["dateHeureDebutF"], DateHeureFinF=festival_data["DateHeureFinF"])
        #         session.add(festival)
        
        elif "GroupeConcert" in nomTable:
            groupeConcerts = nomTable["GroupeConcert"]
            for groupeConcert_data in groupeConcerts:
                groupeConcert = GroupeConcert(groupeConcertId=groupeConcert_data["groupeConcertId"], nomGroupeConcert=groupeConcert_data["nomGroupeConcert"],descriptionGP=groupeConcert_data["descriptionGP"], dateHeureDebutGP=groupeConcert_data["dateHeureDebutGP"], dateHeureFinGP=groupeConcert_data["dateHeureFinGP"])
                session.add(groupeConcert)
        

        elif "StyleSimilaire" in nomTable:
            styles_similaires = nomTable["StyleSimilaire"]
            for style_sim_data in styles_similaires:
                style_sim = StyleSimilaire(styleId=style_sim_data["styleId"], styleSim=style_sim_data["styleSim"])
                session.add(style_sim)

        elif "GroupeDeMusique" in nomTable:
            groupes = nomTable["GroupeDeMusique"]
            for groupe_data in groupes:
                with open(groupe_data["photoGM"], 'rb') as image_file:
                    encoded_image = base64.b64encode(image_file.read())
                groupe = GroupeDeMusique(groupeId=groupe_data["groupeId"], nomGM=groupe_data["nomGM"], descriptionGM=groupe_data["descriptionGM"], lienGM=groupe_data["lienGM"], photoGM=encoded_image, styleId=groupe_data["styleId"])
                session.add(groupe)

        elif "Artiste" in nomTable:
            artistes = nomTable["Artiste"]
            for artiste_data in artistes:
                artiste = Artiste(artisteId=artiste_data["artisteId"], nomArt=artiste_data["nomArt"], groupeId=artiste_data["groupeId"])
                session.add(artiste)
                session.commit()

        elif "TypeBillet" in nomTable:
            typeBillet = nomTable["TypeBillet"]
            for typebillet_data in typeBillet:
                Typebillets = TypeBillet(typeBilletId=typebillet_data["typeBilletId"], nomTypeBillet=typebillet_data["nomTypeBillet"], prixB=typebillet_data["prixB"])
                session.add(Typebillets)

        elif "Concert" in nomTable:
            concerts = nomTable["Concert"]
            for concert_data in concerts:
                concert = Concert(concertId=concert_data["concertId"], dateHeureDebutConcert=concert_data["dateHeureDebutConcert"], dateHeureFinConcert=concert_data["dateHeureFinConcert"], lieuId=concert_data["lieuId"], groupeConcertId=concert_data["groupeConcertId"], groupeId=concert_data["groupeId"])
                session.add(concert)

        elif "Necessiter" in nomTable:
            necessiters = nomTable["Necessiter"]
            for necessiter_data in necessiters:
                necessiter = Necessiter(typeBilletId=necessiter_data["typeBilletId"], groupeConcertId=necessiter_data["groupeConcertId"])
                session.add(necessiter)
        
        elif "AcheterBillet" in nomTable:
            acheterbillets = nomTable["AcheterBillet"]
            for acheterbillet_data in acheterbillets:
                acheterbillet = AcheterBillet(billetId=acheterbillet_data["billetId"], utilisateurId=acheterbillet_data["utilisateurId"],typeBilletId=acheterbillet_data["typeBilletId"])
                session.add(acheterbillet)

        elif "ActiviteAnnexe" in nomTable:
            activites = nomTable["ActiviteAnnexe"]
            for activite_data in activites:
                activite = ActiviteAnnexe(activiteId=activite_data["activiteId"], descriptionACT=activite_data["descriptionACT"], dateHeureACT=activite_data["dateHeureACT"], lieuId=activite_data["lieuId"], groupeConcertId=activite_data["groupeConcertId"], VisibilitePubliqueACT=activite_data["VisibilitePubliqueACT"], GroupeDeMusiqueID=activite_data["GroupeDeMusiqueID"])
                session.add(activite)

        elif "PreInscription" in nomTable:
            pre_inscriptions = nomTable["PreInscription"]
            for pre_inscription_data in pre_inscriptions:
                pre_inscription = PreInscription(preinscriptionId=pre_inscription_data["preinscriptionId"], utilisateurId=pre_inscription_data["utilisateurId"], groupeConcertId=pre_inscription_data["groupeConcertId"], dateHeurePI=pre_inscription_data["dateHeurePI"])
                session.add(pre_inscription)

        elif "GroupesFavoris" in nomTable:
            groupes_favoris = nomTable["GroupesFavoris"]
            for groupes_favoris_data in groupes_favoris:
                groupes_favoris = GroupesFavoris(utilisateurId=groupes_favoris_data["utilisateurId"], groupeId=groupes_favoris_data["groupeId"])
                session.add(groupes_favoris)

        elif "Hebergement" in nomTable:
            hebergements = nomTable["Hebergement"]
            for hebergement_data in hebergements:
                hebergement = Hebergement(HebergementID=hebergement_data["HebergementID"], NomDeLHebergement=hebergement_data["NomDeLHebergement"], PlacesDisponiblesParJour=hebergement_data["PlacesDisponiblesParJour"])
                session.add(hebergement)

        elif "OrganisationDunGroupe" in nomTable:
            organisations_dun_groupe = nomTable["OrganisationDunGroupe"]
            for organisation_dun_groupe_data in organisations_dun_groupe:
                organisation_dun_groupe = OrganisationDunGroupe(OrgaID=organisation_dun_groupe_data["OrgaID"], concertId=organisation_dun_groupe_data["concertId"], JourArriveeODG=organisation_dun_groupe_data["JourArriveeODG"], HeureArriveeODG=organisation_dun_groupe_data["HeureArriveeODG"], JourDepartODG=organisation_dun_groupe_data["JourDepartODG"], HeureDepartODG=organisation_dun_groupe_data["HeureDepartODG"], TempsDeMontageODG=organisation_dun_groupe_data["TempsDeMontageODG"], TempsDeDemontageODG=organisation_dun_groupe_data["TempsDeDemontageODG"], HebergementID=organisation_dun_groupe_data["HebergementID"])
                session.add(organisation_dun_groupe)

                
        elif "Jouer" in nomTable:
            jouers = nomTable["Jouer"]
            for jouer_data in jouers:
                jouer = Jouer(instrumentId=jouer_data["instrumentId"], ArtisteId=jouer_data["ArtisteId"])
                session.add(jouer)

    session.commit()

@app.cli.command()
def dropBD():
    '''
     Create all tables and populate them with data in filename
    '''
    login = 'debray'
    passwd = 'debray'
    serveur = 'servinfo-maria'
    bd = 'DBdebray'
    engine = create_engine(f'mysql+mysqldb://{login}:{passwd}@{serveur}/{bd}', echo=False)
    print("--- Suppression de toutes les tables de la BD ---")
    db.metadata.drop_all(bind=engine)

    print("--- Construction des tables de la BD ---")
    db.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.commit()

@app.cli.command()
def syncdb():
    '''Creates all missing tables.'''
    db.create_all()

# @app.cli.command()
# @click.argument('nomorga')
# @click.argument('motDePasse')
# @click.argument('typeorga')
def neworg(engine,nomorga, motdepasse,typeorga):
    print(nomorga)
    from .models import Organisation
    from hashlib import sha256
    login='chabilan'
    passwd='chabilan'
    serveur='servinfo-maria'
    bd='DBchabilan'
    engine=create_engine('mysql+mysqldb://'+login+':'+passwd+'@'+serveur+'/'+bd, echo=False)
    m = sha256()
    print(m)
    m.update(motdepasse.encode())
    print(m)
    u = Organisation(nomOrga=nomorga, motDePasse= m.hexdigest(), typeOrga=typeorga)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(u)
#     # db.session.commit()
if __name__ == '__main__':
    login='debray'
    passwd='debray'
    serveur='servinfo-maria'
    bd='DBdebray'
    engine=create_engine('mysql+mysqldb://'+login+':'+passwd+'@'+serveur+'/'+bd, echo=False)

    Session = sessionmaker(bind=engine)
    session = Session()