from .app import *
from flask import render_template, flash, redirect, url_for, request
from .app import app, db
from flask import render_template, url_for, redirect
from flask_login import login_user , current_user, logout_user, login_required
from hashlib import sha256
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField
from .requetes import *
from .models import Utilisateur



@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/billeterie")
def billeterie():
    return render_template("billeterie.html") 

@app.route("/programmation")
def programmation():
    return render_template("programmation.html") 


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




@app.route("/administrer_utilisateur")
def administrer_utilisateur():
    return render_template("administrer_utilisateur.html")


@app.route("/consulter_les_artistes")
def consulter_les_artistes():
    return render_template("consulter_les_artistes.html")

@app.route("/consulter_les_concert")
def consulter_les_concert():
    return render_template("consulter_les_concert.html")

@app.route("/consulter_les_groupes")
def consulter_les_groupes():
    return render_template("consulter_les_groupes.html")
   

@app.route("/modifier_artiste")
def modifier_artiste():
    return render_template("modifier_artiste.html")

@app.route("/modifier_groupe")
def modifier_groupe():
    return render_template("modifier_groupe.html")

@app.route("/modifier_utilisateur")
def modifier_utilisateur():
    return render_template("modifier_utilisateur.html")


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
   
    mod_artiste(id, nom, mail, mdp, ddn, tel)
    return redirect(url_for('profil', user=id))