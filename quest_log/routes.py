from flask import flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from quest_log import app, db
from quest_log.models import Game, Review, User, UserGame
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError

@app.route("/")
def home():
    return redirect(url_for('games'))

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

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('home'))

@app.route('/games')
def games():
    games = Game.query.order_by(Game.game_title).all()
    if current_user.is_authenticated:
        user_game_ids = db.session.query(UserGame.game_id).filter(UserGame.user_id == current_user.user_id).all()
        in_my_games = [game_id for (game_id,) in user_game_ids]
    else:
        in_my_games = []

    return render_template('games.html', inMyGames=in_my_games,
                           isUserAuthenticated=current_user.is_authenticated,
                           games=games, 
                           in_my_games=in_my_games)

@app.route('/api/games')
def api_games():
    query = request.args.get('query', '')
    games = Game.query.filter(Game.game_title.ilike(f'%{query}%')).all()
    return jsonify([{
        'game_id': game.game_id,
        'game_title': game.game_title,
        'developer': game.developer,
        'genre': game.genre,
        'image_url': game.image_url,
        'game_publisher': game.game_publisher,
        'release_date': game.release_date.isoformat()        
    } for game in games])

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

    existing_game = Game.query.filter_by(game_title=game_title).first()
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

@app.route('/my_games/<int:user_id>')
def my_games(user_id):
    user_games = UserGame.query.filter_by(user_id=user_id).all()
    games = [user_game.game for user_game in user_games]

    return render_template('my_games.html', my_games=games)

@app.route('/game_detail/<int:game_id>')
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
    reviews = Review.query.filter_by(game_id=game_id).all()
    in_my_games = []
    reviewed_games = []
    user_review = None

    if current_user.is_authenticated:
        user_game = UserGame.query.filter_by(user_id = current_user.user_id, game_id=game_id).first()
        in_my_games = [game_id] if user_game else []

        user_review = Review.query.filter_by(user_id=current_user.user_id, game_id=game_id).first()
        reviewed_games = [game_id] if user_review else []
        if user_review:
            reviewed_games = [game_id]

    return render_template('game_detail.html',
                           in_my_games=in_my_games,
                           reviews=reviews,
                           game=game,
                           user_review=user_review,
                           reviewed_games=reviewed_games)

@app.route('/add_library/<int:game_id>', methods=['POST'])
@login_required
def add_library(game_id):
    game = Game.query.get_or_404(game_id)
    if game is None:
        return redirect(url_for('add_game'))
    already_in_lib = UserGame.query.get((current_user.user_id, game_id))
    if already_in_lib is None:
        new_lib = UserGame(
                user_id=current_user.user_id,
                game_id=game_id,
                )
        try:
            db.session.add(new_lib)
            db.session.commit()
            flash('Game added to library', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Game already in Library', 'info')
    else:
        flash('Game already in library', 'info')
    return redirect(url_for('games'))

@app.route('/new_review/<int:game_id>')
@login_required
def new_review(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template('add_review.html', game=game)


@app.route('/add_review/<int:game_id>', methods=["GET","POST"])
@login_required
def add_review(game_id):
    game = Game.query.get_or_404(game_id)
    if request.method == "POST":
        review_content = request.form.get('review_content')
        hours_played = int(request.form.get('hours_played'), 0)
        completed = request.form.get('completed') == 'on'
        rating = int(request.form.get('rating'), 0)

        new_review = Review(
                game_id=game_id,
                user_id=current_user.user_id,
                review_content=review_content,
                hours_played=hours_played, 
                completed=completed,
                rating=rating
                )
        try:
            db.session.add(new_review)
            db.session.commit()
            flash('Your review has been added succesfully', 'success')
            return redirect(url_for('my_games', user_id=current_user.user_id))
        except IntegrityError:
            db.session.rollback()
            flash('An error occured while adding your review to the database')
    return render_template('add_review.html', game=game)

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
    

@app.route('/my_reviews/<int:user_id>')
def my_reviews(user_id):
    reviews = Review.query.filter_by(user_id=user_id).all()
    return render_template('my_reviews.html', my_reviews=reviews)

@app.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.user_id:
        flash('You can only edit your own reviews.', 'error')
        return redirect(url_for('my_reviews'))
    
    if request.method == 'POST':
        review.review_content = request.form.get('review_content')
        review.hours_played = int(request.form.get('hours_played', 0))
        review.completed = request.form.get('completed') == 'on'
        review.rating = int(request.form.get('rating', 0))
 
        db.session.commit()
        flash('Your review has been updated successfully', 'success')
        return redirect(url_for('my_reviews', user_id=current_user.user_id))
    
    return render_template('edit_review.html', review=review)

@app.route('/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.user_id:
        flash('You can only delete your own reviews.', 'error')
        return redirect(url_for('my_reviews'))
    
    try:
        db.session.delete(review)
        db.session.commit()
        flash('Your review has been deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting your review. Please try again.', 'error')
    
    return redirect(url_for('my_reviews', user_id=current_user.user_id))

