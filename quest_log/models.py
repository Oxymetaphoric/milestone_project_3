from datetime import datetime, timezone

from sqlalchemy import ForeignKey, CheckConstraint
from quest_log import db

class User(db.Model):
    user_id =  db.Column(db.Integer, primary_key = True, nullable = False) 
    username =  db.Column(db.String(50), unique = True, nullable = False) 
    email =  db.Column(db.String(50), unique = True, nullable = False)
    password_hash =  db.Column(db.String(20), nullable = False) 
    location =  db.Column(db.String(50), nullable = True) 
    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc), nullable = False)
    avatar_url = db.Column(db.String(512), nullable = True)

class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key = True)
    game_title = db.Column(db.String(50), unique = True, nullable = False)
    game_publisher = db.Column(db.String(50), nullable = False)
    developer = db.Column(db.String(50), nullable = False) 
    release_date = db.Column(db.DateTime,  default = lambda: datetime.now(timezone.utc), nullable = False) 
    genre = db.Column(db.String(50), nullable = False)
    image_url = db.Column(db.String(512), nullable = False)
    rating = db.Column(db.Float, nullable = True)
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
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    __table_args__ = (
            CheckConstraint('rating >= 0 AND rating <= 100', name='check_rating_range'),
            )


class UserGame(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'), primary_key=True)
    added_at = db.Column(db.DateTime, nullable=False, default = lambda: datetime.now(timezone.utc))
     
    game = db.relationship('Game', backref=db.backref('user_games', lazy=True))
    user = db.relationship('User', backref=db.backref('user_games', lazy=True))

    def __repr__(self):
        return f'<UserGame {self.user_id}:{self.game_id}>'
