from .app import *
from flask import render_template, flash, redirect, url_for, request
from .models import *
from .requetes import *

@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/billeterie/<int:concertId>", methods=["GET", "POST"])
def billeterie(concertId):
    return render_template("billeterie.html", concert=get_info_un_concert(concertId)) 

@app.route("/programmation")
def programmation():
    return render_template("programmation.html", lesConcerts=get_info_concert()) 