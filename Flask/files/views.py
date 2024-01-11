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


@app.route("/connexion")
def connexion1():
    return render_template("connexion.html")

@app.route("/inscription")
def inscription():
    return render_template("inscription.html")

@app.route("/accueil_administrateur")
def accueil():
    return render_template("accueil_administrateur.html")

   

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
                return redirect(url_for("accueil_administrateur"))
    return render_template("connexion.html", form=f)


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('connexion'))