from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, login_required, logout_user, current_user
from quest_log import app, db
from quest_log.models import Game, Review, User, UserGame
from werkzeug.security import generate_password_hash 

@app.route("/")
def home():
    return render_template("base.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('newuser-username')
        email = request.form.get('email')
        password = request.form.get('newuser-password')

        if not username or not email or not password or not first_name or not last_name:
            flash('All fields are required.', 'error')
            return redirect(url_for('register'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash('User already exists')
            return redirect(url_for('register'))

        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration Successful')
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('login-username')
        password = request.form.get('login-password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('logged in successfully')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('home'))

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/add_game')
@login_required
def add_game():
    return render_template('add_game.html')

@app.route('/new_game', methods=["POST"])
@login_required
def new_game():
    game_title = request.form.get('game_title')
    game_publisher = request.form.get('game_publisher')
    developer = request.form.get('developer')
    release_date = request.form.get('release_date')
    genre = request.form.get('genre')
    image_url = request.form.get('image_url')

    existing_game = Game.query.filter_by(game_title=game_title),first()
    if existing_game is None:
        new_game = Game(
                game_title = game_title,
                game_publisher = game_publisher,
                developer = developer,
                release_date = release_date,
                genre = genre,
                image_url = image_url
                )
        db.session.add(new_game)
        db.session.commit()
        flash('Game added to database', 'success')
    else:
        flash('Game already exists')
    return redirect(url_for('games'))


@app.route('/profile/<int:user_id>', methods=["GET", "POST"])
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    
    owns_profile = user.user_id == current_user.user_id
    if request.method == "POST" and owns_profile:
        # Get the data from the form
        new_email = request.form.get('email')
        new_password = request.form.get('newauth')
        new_avatar_url = request.form.get('avatar_url')
        if new_email and new_email != user.email:
            user.email = new_email
        if new_password:
            user.password_hash = generate_password_hash(new_password)
        if new_avatar_url:
            user.avatar_url = new_avatar_url
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile', user_id=user.user_id))
    return render_template('profile.html', user=user, owns_profile=owns_profile)
    




