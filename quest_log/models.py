from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy import ForeignKey, CheckConstraint
from quest_log import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    user_id =  db.Column(db.Integer, autoincrement=True, primary_key = True, nullable = False) 
    username =  db.Column(db.String(50), unique = True, nullable = False)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable= False)
    email =  db.Column(db.String(50), unique = True, nullable = False)
    password_hash =  db.Column(db.String(256), nullable = False) 
    location =  db.Column(db.String(50), nullable = True) 
    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc), nullable = True)
    avatar_url = db.Column(db.String(512), nullable = True)
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')
    user_games = db.relationship('UserGame', back_populates='user', cascade='all, delete-orphan')
    def __init__(self, username, email, first_name, last_name, password, location=None, avatar_url=None):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.set_password(password)
        self.location = location
        self.avatar_url = avatar_url

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def get_id(self):
        return str(self.user_id)

class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key = True)
    game_title = db.Column(db.String(50), unique = True, nullable = False)
    game_publisher = db.Column(db.String(50), nullable = False)
    developer = db.Column(db.String(50), nullable = False) 
    release_date = db.Column(db.DateTime,  default = lambda: datetime.now(timezone.utc), nullable = False) 
    genre = db.Column(db.String(50), nullable = False)
    image_url = db.Column(db.String(512), nullable = False)
    rating = db.Column(db.Float)
    __table_args__ = (
        CheckConstraint('rating >= 0 AND rating <= 10', name='check_rating_range'),
    )

    def __repr__(self):
        return self.game_title

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key = True) 
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable =  False) 
    review_content = db.Column(db.Text, nullable = False)
    hours_played = db.Column(db.Integer, nullable = False) 
    completed = db.Column(db.Boolean, nullable = True) 
    rating = db.Column(db.Integer, nullable = False) #must be between 0 - 10 inclusive
    review_created_at = db.Column(db.DateTime, nullable = False, default = lambda: datetime.now(timezone.utc)) 
    
    game = db.relationship('Game', backref=db.backref('reviews', lazy=True))
    user = db.relationship('User', back_populates='reviews')
    __table_args__ = (
            CheckConstraint('rating >= 0 AND rating <= 100', name='check_rating_range'),
            )


class UserGame(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'), primary_key=True)
    added_at = db.Column(db.DateTime, nullable=False, default = lambda: datetime.now(timezone.utc))
     
    game = db.relationship('Game', backref=db.backref('user_games', lazy=True))
    user = db.relationship('User', back_populates='user_games')

    def __repr__(self):
        return f'<UserGame {self.user_id}:{self.game_id}>'
