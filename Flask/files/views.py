from .app import *
from flask import render_template, flash, redirect, url_for, request

@app.route("/")
def home():
    return render_template("home.html", title="Home")

