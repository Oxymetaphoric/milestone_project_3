from flask import render_template
from quest_log import app, db

@app.route("/")
def home():
    return render_template("base.html")

