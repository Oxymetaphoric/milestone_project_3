from flask import render_template
from quest_log import app, db
from quest_log.models import Game, Review, User, UserGame
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #check if username already exists
        
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template('login.html')
