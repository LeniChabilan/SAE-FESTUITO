import click
from .app import app,db
# from datetime import datetime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
# from sqlalchemy.exc import IntegrityError


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
    from .models import Lieu, Instrument, Spectateur, StyleMusical, Festival, StyleSimilaire, GroupeDeMusique, Artiste, Billet, Concert, ActiviteAnnexe, PreInscription, GroupesFavoris, Hebergement, OrganisationDunGroupe, Jouer


    for nomTable in data:
        if "Lieu" in nomTable:
            lieux = nomTable["Lieu"]
            for lieu_data in lieux:
                lieu = Lieu(lieuId=lieu_data["lieuId"], nomL=lieu_data["nomL"], capaciteL=lieu_data["capaciteL"], adresseL=lieu_data["adresseL"])
                session.add(lieu)

        elif "Instrument" in nomTable:
            instruments = nomTable["Instrument"]
            for instrument_data in instruments:
                instrument = Instrument(instrumentId=instrument_data["instrumentId"], nomInstru=instrument_data["nomInstru"])
                session.add(instrument)

        elif "Spectateur" in nomTable:
            spectateurs = nomTable["Spectateur"]
            for spectateur_data in spectateurs:
                spectateur = Spectateur(spectateurId=spectateur_data["spectateurId"], nomSpec=spectateur_data["nomSpec"], emailSpec=spectateur_data["emailSpec"], MDPSpec=spectateur_data["MDPSpec"])
                session.add(spectateur)

        elif "StyleMusical" in nomTable:
            styles = nomTable["StyleMusical"]
            for style_data in styles:
                style = StyleMusical(styleId=style_data["styleId"], nomSM=style_data["nomSM"])
                session.add(style)

        elif "Festival" in nomTable:
            festivals = nomTable["Festival"]
            for festival_data in festivals:
                festival = Festival(festivalId=festival_data["festivalId"], nomF=festival_data["nomF"], dateDebutF=festival_data["dateDebutF"], DateHeureFinF=festival_data["DateHeureFinF"])
                session.add(festival)

        elif "StyleSimilaire" in nomTable:
            styles_similaires = nomTable["StyleSimilaire"]
            for style_sim_data in styles_similaires:
                style_sim = StyleSimilaire(styleId=style_sim_data["styleId"], styleSim=style_sim_data["styleSim"])
                session.add(style_sim)

        elif "GroupeDeMusique" in nomTable:
            groupes = nomTable["GroupeDeMusique"]
            for groupe_data in groupes:
                groupe = GroupeDeMusique(groupeId=groupe_data["groupeId"], nomGM=groupe_data["nomGM"], descriptionGM=groupe_data["descriptionGM"], lienGM=groupe_data["lienGM"], styleId=groupe_data["styleId"])
                session.add(groupe)

        elif "Artiste" in nomTable:
            artistes = nomTable["Artiste"]
            for artiste_data in artistes:
                artiste = Artiste(artisteId=artiste_data["artisteId"], nomArt=artiste_data["nomArt"], groupeId=artiste_data["groupeId"])
                session.add(artiste)

        elif "Billet" in nomTable:
            billets = nomTable["Billet"]
            for billet_data in billets:
                billet = Billet(billetId=billet_data["billetId"], typeB=billet_data["typeB"], prixB=billet_data["prixB"], spectateurId=billet_data["spectateurId"], festivalId=billet_data["festivalId"])
                session.add(billet)

        elif "Concert" in nomTable:
            concerts = nomTable["Concert"]
            for concert_data in concerts:
                concert = Concert(concertId=concert_data["concertId"], dateHeureDebutConcert=concert_data["dateHeureDebutConcert"], dureeConcert=concert_data["dureeConcert"], lieuId=concert_data["lieuId"], festivalId=concert_data["festivalId"], groupeId=concert_data["groupeId"])
                session.add(concert)

        elif "ActiviteAnnexe" in nomTable:
            activites = nomTable["ActiviteAnnexe"]
            for activite_data in activites:
                activite = ActiviteAnnexe(activiteId=activite_data["activiteId"], descriptionACT=activite_data["descriptionACT"], dateHeureACT=activite_data["dateHeureACT"], lieuId=activite_data["lieuId"], festivalId=activite_data["festivalId"], VisibilitePubliqueACT=activite_data["VisibilitePubliqueACT"], GroupeDeMusiqueID=activite_data["GroupeDeMusiqueID"])
                session.add(activite)

        elif "PreInscription" in nomTable:
            pre_inscriptions = nomTable["PreInscription"]
            for pre_inscription_data in pre_inscriptions:
                pre_inscription = PreInscription(preinscriptionId=pre_inscription_data["preinscriptionId"], spectateurId=pre_inscription_data["spectateurId"], festivalId=pre_inscription_data["festivalId"], dateHeurePI=pre_inscription_data["dateHeurePI"])
                session.add(pre_inscription)

        elif "GroupesFavoris" in nomTable:
            groupes_favoris = nomTable["GroupesFavoris"]
            for groupes_favoris_data in groupes_favoris:
                groupes_favoris = GroupesFavoris(spectateurId=groupes_favoris_data["spectateurId"], groupeId=groupes_favoris_data["groupeId"])
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



# @app.cli.command()
# def syncdb():
#     '''Creates all missing tables.'''
#     db.create_all()

# # @app.cli.command()
# # @click.argument('nomorga')
# # @click.argument('motDePasse')
# # @click.argument('typeorga')
# def neworg(engine,nomorga, motdepasse,typeorga):
#     print(nomorga)
#     from .models import Organisation
#     from hashlib import sha256
#     login='chabilan'
#     passwd='chabilan'
#     serveur='servinfo-maria'
#     bd='DBchabilan'
#     engine=create_engine('mysql+mysqldb://'+login+':'+passwd+'@'+serveur+'/'+bd, echo=False)
#     m = sha256()
#     print(m)
#     m.update(motdepasse.encode())
#     print(m)
#     u = Organisation(nomOrga=nomorga, motDePasse= m.hexdigest(), typeOrga=typeorga)
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     session.add(u)
#     # db.session.commit()
if __name__ == '__main__':
    login='debray'
    passwd='debray'
    serveur='servinfo-maria'
    bd='DBdebray'
    engine=create_engine('mysql+mysqldb://'+login+':'+passwd+'@'+serveur+'/'+bd, echo=False)

    Session = sessionmaker(bind=engine)
    session = Session()