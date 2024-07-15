from flask import render_template
from quest_log import app, db
from quest_log.models import Game, Review, User, UserGame

@app.route("/")
def home():
    return render_template("base.html")

