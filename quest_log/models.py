from datetime import datetime

from sqlalchemy import ForeignKey
from quest_log import db

class User(db.Model):
    user_id =  db.Column(db.Integer, primary_key = True, nullable = False) 
    username =  db.Column(db.String(50), unique = True, nullable = False) 
    email =  db.Column(db.String(50), unique = True, nullable = False)
    password_hash =  db.Column(db.String(100), nullable = False) 
    location =  db.Column(db.String(50), nullable = True) 
    created_at = db.Column(db.DateTime, nullable = False) 

class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key = True)
    game_title = db.Column(db.String(50), unique = True, nullable = False)
    game_publisher = db.Column(db.String(50), nullable = False)
    developer = db.Column(db.String(50), nullable = False) 
    release_date = db.Column(db.DateTime, nullable = False) 
    genre = db.Column(db.String(50), nullable = False)
    image_url = db.Column(db.String(512), nullable = False)
    rating = db.Column(db.Float)

    def __repr__(self):
        return self.game_title

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key = True) 
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable =  False) 
    review_content = db.Column(db.Text, nullable = False)
    hours_played = db.Column(db.Float, nullable = False) 
    completed = db.Column(db.Boolean, nullable = True) 
    rating = db.Column(db.Integer, nullable = False) #must be between 0 - 100 inclusive
    review_created_at = db.Column(db.DateTime, nullable = False) 
    
    game = db.relationship('Game', backref=db.backref('reviews', lazy=True))
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
