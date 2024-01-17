from .app import *
from flask import render_template, flash, redirect, url_for, request
from .app import app, db
from flask import render_template, url_for, redirect,jsonify
from flask_login import login_user , current_user, logout_user, login_required
from hashlib import sha256
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField
from .requetes import *
from .models import Utilisateur
import base64




@app.route("/")
def home():
    return render_template("home.html", title="Home", lesConcerts=get_info_concert(),prochain=get_prochain_concert())


@app.route("/billeterie")
def billeterie():
    return render_template("billeterie.html") 

@app.route("/programmation")
def programmation():
    return render_template("programmation.html", lesConcerts=get_info_concert()) 


@app.route("/creer_compte", methods=["GET", "POST"])
def creer_compte():
    try:
        nom = request.form['nomUtilisateur']
        email = request.form['emailUtilisateur']
        mdp = request.form['MDPUtilisateur']
        ddn = request.form['DdN']
        tel = request.form['tel'] 
        if mdp == request.form['confirmMDPUtilisateur']:
            create_user(nom, email, mdp, ddn, tel)
            return render_template("home.html")
        else:
            return render_template("inscription.html")
    except Exception as e:
        print(f"Error in creer_compte: {str(e)}")
        return "Internal Server Error", 500



@app.route("/connexion")
def connexion1():
    return render_template("connexion.html")

@app.route("/inscription")
def inscription():
    return render_template("inscription.html")



@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/administrer_artistes")
def administrer_artistes():
    return render_template("administrer_artistes.html")

@app.route("/administrer_concert")
def administrer_concert():
    return render_template("administrer_concert.html")


@app.route("/sup-concert/<int:id>")
def sup_concert(id):
    supprimer_concert(id)
    return render_template("consulter_les_concert.html",concerts=get_info_concert())


@app.route("/sup-artiste/<int:id>")
def sup_artiste(id):
    supprimer_artiste(id)
    return render_template("consulter_les_artistes.html",artistes=get_info_artiste())

@app.route("/sup-groupe/<int:id>")
def sup_groupe(id):
    supprimer_groupe(id)
    return render_template("consulter_les_groupes.html",groupes=get_info_groupe())

@app.route("/sup-utilisateur/<int:id>")
def sup_utilisateur(id):
    supprimer_utilisateur(id)
    return render_template("administrer_utilisateur.html",utilisateurs=get_info_utilisateur())



@app.route("/administrer_utilisateur")
def administrer_utilisateur():
    return render_template("administrer_utilisateur.html", utilisateurs=get_info_utilisateur())


@app.route("/consulter_les_artistes")
def consulter_les_artistes():
    return render_template("consulter_les_artistes.html",artistes=get_info_artiste())

@app.route("/consulter_les_concert")
def consulter_les_concert():
    return render_template("consulter_les_concert.html",concerts=get_info_concert())

@app.route("/consulter_les_groupes")
def consulter_les_groupes():
    return render_template("consulter_les_groupes.html",groupes=get_info_groupe())
   

@app.route("/modifier_artiste/<int:id>")
def modifier_artiste(id):
    return render_template("modifier_artiste.html",artiste=get_info_un_artiste(id),liste_groupes=get_info_groupe(),art=get_info_un_artiste(id))


@app.route("/modif_artiste/<int:id>", methods =["POST"])
def modif_artiste(id):
    nom=request.form.get("nom")
    grp=request.form.get("groupe")

    mod_artiste(id,nom,grp)
    return render_template("consulter_les_artistes.html",artistes=get_info_artiste())



@app.route("/modifier_groupe/<int:id>")
def modifier_groupe(id):
    return render_template("modifier_groupe.html",groupe=get_info_un_groupe(id),liste_groupes=get_info_groupe(),listeStyle=get_info_style())


@app.route("/modif_groupe/<int:id>", methods =["POST"])
def modif_groupe(id):
    nom=request.form.get("nom")
    desc=request.form.get("description")
    link=request.form.get("lien")
    stl=request.form.get("style")
    mod_groupe(id,nom,desc,link,stl)
    return render_template("consulter_les_groupes.html",groupes=get_info_groupe())

@app.route("/creation_concert")
def creation_concert():
    return render_template("creation_concert.html",liste_groupes=get_info_groupe(),liste_lieu=get_info_lieu(), liste_grp_conc=get_info_groupe_concert())


@app.route("/modifier_concert/<int:id>")
def modifier_concert(id):
    return render_template("modif_concert.html",concert=get_info_un_concert(id),liste_groupes=get_info_groupe(),liste_lieu=get_info_lieu(), liste_grp_conc=get_info_groupe_concert())

@app.route("/creer_concert", methods=["GET", "POST"])
def creer_concert():
    dateD = request.form.get("Datedebut")
    dateF = request.form.get("dateF")
    lieu = request.form.get("Lieu")
    grp = request.form.get("groupe")
    grpC = request.form.get("groupeConcert")
   
    creer_conc( dateD,dateF,lieu,grp,grpC)
    return render_template("administrer_concert.html")


@app.route("/modif_concert/<int:id>", methods=["GET", "POST"])
def modif_concert(id):
    dateD = request.form.get("Datedebut")
    dateF = request.form.get("dateF")
    lieu = request.form.get("Lieu")
    grp = request.form.get("groupe")
    grpC = request.form.get("groupeConcert")
   
    mod_concert(id, dateD,dateF,lieu,grp,grpC)
    return render_template("consulter_les_concert.html",concerts=get_info_concert())



@app.route("/modifier_utilisateur/<int:id>")
def modifier_utilisateur(id):
    return render_template("modifier_utilisateur.html",utilisateur=get_info_un_utilisateur(id))

@app.route("/modif_utilisateur/<int:id>", methods=["GET", "POST"])
def modif_utilisateur(id):
    nom = request.form.get("nom")
    mail = request.form.get("email")
    mdp = request.form.get("mdp")
    ddn = request.form.get("dateDN")
    tel = request.form.get("numero")
   
    mod_utilisateur(id, nom, mail, mdp, ddn, tel)
    return redirect(url_for('administrer_utilisateur',utilisateurs=get_info_utilisateur()))




@app.route("/creation_groupe")
def creation_groupe():
    return render_template("creation_groupe.html", list_style=get_info_style())

@app.route("/creation_artiste/<int:id>")
def creation_artiste(id):
    return render_template("creation_artiste.html",id=id)

class LoginForm(FlaskForm):
    emailUtilisateur = StringField('Username')
    motDePasse = PasswordField('Password')
    next = HiddenField()
    def get_authenticated_user(self):
        user = get_user_by_email(self.emailUtilisateur.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.motDePasse.data.encode())
        passwd = m.hexdigest()
        print(passwd, user.MDPUtilisateur)
        return user if passwd == user.MDPUtilisateur else print("Mot de passe incorrect")

@app.route("/connexion/", methods =("GET","POST",))
def connexion():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            if user.role == "Spectateur":
                login_user(user)
                return redirect(url_for("home"))
            else:
                login_user(user)
                return redirect(url_for("admin"))
    return render_template("connexion.html", form=f)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/profil/<int:user>")
def profil(user):
    return render_template("profil.html", user=get_user_by_id(user))


@app.route("/modifier_profil/<int:user>", methods=["GET", "POST"])
def modifier_profil(user):
   return render_template("modifier_profil.html", user=get_user_by_id(user))

@app.route("/modif_artiste_art/<int:id>", methods=["GET", "POST"])
def modif_artiste_art(id):
    nom = request.form.get("nom")
    mail = request.form.get("emailUtilisateur")
    mdp = request.form.get("MDPUtilisateur")
    ddn = request.form.get("DdN")
    tel = request.form.get("tel")
    mod_utilisateur(id, nom, mail, mdp, ddn, tel)
    return redirect(url_for('profil', user=id))

@app.route("/creation_groupe_gr", methods=["POST"])
def creation_groupe_gr():
    try:
        upload_file = request.files['avatar']
            
        # Lire le contenu du fichier
        file_content = upload_file.read()
        
        # Encoder en base64
        base64_encoded = base64.b64encode(file_content)
        nom = request.form.get("nom")
        desc = request.form.get("description")
        lien = request.form.get("lien")
        image = base64_encoded
        style = request.form.get("style")
        if nom is None or desc is None or lien is None or image is None or style is None:
            raise Exception("Missing fields")
        id=create_groupe(nom, desc, lien, image, style)
        print("Groupe ajouté")
        return redirect(url_for('creation_artiste',id=id))
    except:
        return render_template("creation_groupe.html",list_style=get_info_style())
    
@app.route("/creation_artiste_art/<int:id>", methods=["POST"])
def creation_artiste_art(id):
    nom = request.form.get("pseudo")
    create_artiste(nom,id)
    return redirect(url_for('creation_artiste',id=id))

