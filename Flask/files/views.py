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


PROCHAIN=get_prochain_concert()


@app.route("/")
def home():
    return render_template("home.html", title="Home", lesConcerts=get_info_concert(),prochain=PROCHAIN)


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

        print(nom, email, mdp, ddn, tel)
    

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
   

@app.route("/modifier_artiste")
def modifier_artiste():
    return render_template("modifier_artiste.html")

@app.route("/modifier_groupe")
def modifier_groupe():
    return render_template("modifier_groupe.html")

@app.route("/modifier_utilisateur")
def modifier_utilisateur():
    return render_template("modifier_utilisateur.html")

@app.route("/creation_concert")
def creation_concert():
    return render_template("creation_concert.html")

@app.route("/creation_groupe")
def creation_groupe():
    return render_template("creation_groupe.html")

@app.route("/creation_artiste")
def creation_artiste():
    return render_template("creation_artiste.html")

class LoginForm(FlaskForm):
    emailUtilisateur = StringField('Username')
    motDePasse = PasswordField('Password')
    next = HiddenField()
    def get_authenticated_user(self):
        user = get_user_by_email(self.emailUtilisateur.data)
        print(user.MDPUtilisateur)
        if user is None:
            return None
        m = sha256()
        m.update(self.motDePasse.data.encode())
        passwd = m.hexdigest()      
        return user if passwd == user.MDPUtilisateur else print("Mot de passe incorrect")

@app.route("/connexion/", methods =("GET","POST",))
def connexion():
    f = LoginForm()
    print(f)
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        print(user)
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

