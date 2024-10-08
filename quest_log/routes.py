from flask import flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from quest_log import app, db
from quest_log.models import Game, Review, User, UserGame
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func


@app.route("/")
def home():
    return redirect(url_for("games"))

@app.errorhandler(404)
def page_not_found(e):
    flash("Error: page not found", "error")
    return render_template('404.html'), 404

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("newuser-username")
        email = request.form.get("email")
        password = request.form.get("newuser-password")

        if not username or not email or not password or not first_name or not last_name:
            flash("All fields are required.", "error")
            return redirect(url_for("register"))

        user = User.query.filter_by(username=username).first()
        if user:
            flash("User already exists")
            return redirect(url_for("register"))

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.user_id == current_user.user_id:
        db.session.delete(user)
        db.session.commit()
        flash("Your account has been successfully deleted.", "success")
        return redirect(url_for("home"))
    else:
        flash("You don't have permission to delete this account.", "error")
    return redirect(url_for("profile", user_id=user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("login-username")
        password = request.form.get("login-password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("logged in successfully")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for("home"))

@app.route("/games")
def games():
    games = Game.query.order_by(Game.game_title).all()
    if current_user.is_authenticated:
        user_game_ids = (
            db.session.query(UserGame.game_id)
            .filter(UserGame.user_id == current_user.user_id)
            .all()
        )
        in_my_games = [game_id for (game_id,) in user_game_ids]
    else:
        in_my_games = []

    return render_template(
        "games.html",
        inMyGames=in_my_games,
        isUserAuthenticated=current_user.is_authenticated,
        games=games,
        in_my_games=in_my_games,
    )

@app.route("/api/games")
def api_games():
    query = request.args.get("query", "")
    if query:
        games = Game.query.filter(Game.game_title.ilike(f"%{query}%")).all()
        game_list = [
            {
                "game_id": game.game_id,
                "game_title": game.game_title,
                "developer": game.developer,
                "genre": game.genre,
                "image_url": game.image_url,
                "game_publisher": game.game_publisher,
                "release_date": game.release_date.isoformat(),
            }
            for game in games
        ]
    else:
        game_list = []

    return jsonify(game_list)

@app.route("/add_game")
@login_required
def add_game():
    return render_template("add_game.html")

@app.route("/new_game", methods=["POST"])
@login_required
def new_game():
    game_title = request.form.get("game_title")
    game_publisher = request.form.get("game_publisher")
    developer = request.form.get("developer")
    release_date = request.form.get("release_date")
    genre = request.form.get("genre")
    image_url = request.form.get("image_url")

    existing_game = Game.query.filter_by(game_title=game_title).first()
    if existing_game is None:
        new_game = Game(
            game_title=game_title,
            game_publisher=game_publisher,
            developer=developer,
            release_date=release_date,
            genre=genre,
            image_url=image_url,
        )
        db.session.add(new_game)
        db.session.commit()
        flash("Game added to database", "success")
    else:
        flash("Game already exists")
    return redirect(url_for("games"))

@app.route("/my_games/<int:user_id>")
def my_games(user_id):
    user = User.query.get_or_404(user_id)
    user_games = UserGame.query.filter_by(user_id=user_id).all()
    games = [user_game.game for user_game in user_games]
    owns_profile = user.user_id == current_user.user_id
    
    return render_template(
        "my_games.html", owns_profile=owns_profile, current_user=current_user, user=user, my_games=games
    )

@app.route("/delete_game/<int:game_id>", methods=["POST"])
@login_required
def delete_game(game_id):
    if not current_user.is_admin:
        flash("You don't have permission to delete games", "error")
        return redirect(url_for("games"))

    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    flash(f"Game '{game.game_title}' has been deleted", "success")
    return redirect(url_for("games"))

@app.route("/make_admin/<int:user_id>", methods=['POST'])
@login_required
def make_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user:
        user.is_admin = True
        db.session.commit()
        flash('{{user.username}} is now an admin!')
    else:
        flash('User not found!')

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/edit_game/<int:game_id>", methods=["GET", "POST"])
@login_required
def edit_game(game_id):
    game=Game.query.get_or_404(game_id)
    if request.method == "POST":
        game.game_title = request.form.get("game_title")
        game.game_publisher = request.form.get("game_publisher")
        game.developer = request.form.get("developer")
        game.release_date = request.form.get("release_date")
        game.genre = request.form.get("genre")
        game.image_url = request.form.get("image_url")
        db.session.commit()
        flash("Game edited", "error")
        return redirect(url_for("game_detail", game_id=game_id))
    return render_template("edit_game.html", game=game)

@app.route("/game_detail/<int:game_id>")
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
    reviews = Review.query.filter_by(game_id=game_id).all()
    in_my_games = []
    reviewed_games = []
    user_review = None
    avg_rating = (
        db.session.query(func.avg(Review.rating))
        .filter(Review.game_id == game_id)
        .scalar()
    )
    if avg_rating is not None:
        avg_rating = avg_rating / 10
        avg_rating = round(avg_rating, 1)
    else:
        avg_rating = "N/A"

    if current_user.is_authenticated:
        user_game = UserGame.query.filter_by(
            user_id=current_user.user_id, game_id=game_id
        ).first()
        in_my_games = [game_id] if user_game else []

        user_review = Review.query.filter_by(
            user_id=current_user.user_id, game_id=game_id
        ).first()
        reviewed_games = [game_id] if user_review else []
        if user_review:
            reviewed_games = [game_id]

    return render_template(
        "game_detail.html",
        in_my_games=in_my_games,
        reviews=reviews,
        game=game,
        user_review=user_review,
        reviewed_games=reviewed_games,
        avg_rating=avg_rating,
    )

@app.route("/add_library/<int:game_id>", methods=["POST"])
@login_required
def add_library(game_id):
    game = Game.query.get_or_404(game_id)
    if game is None:
        return redirect(url_for("add_game"))
    already_in_lib = UserGame.query.get((current_user.user_id, game_id))
    if already_in_lib is None:
        new_lib = UserGame(
            user_id=current_user.user_id,
            game_id=game_id,
        )
        db.session.add(new_lib)
        db.session.commit()
        flash("Game added to library", "success")
    else:
        flash("Game already in library", "info")
    return redirect(url_for("games"))

@app.route("/remove_from_library/<int:game_id>", methods=["POST"])
@login_required
def remove_from_library(game_id):
    user_game = UserGame.query.filter_by(
        user_id=current_user.user_id, game_id=game_id
    ).first_or_404()
    db.session.delete(user_game)
    db.session.commit()
    flash("game removed from your library successfully", "success")

    return redirect(url_for("my_games", user_id=current_user.user_id))

@app.route("/new_review/<int:game_id>")
@login_required
def new_review(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template("add_review.html", game=game)

@app.route("/add_review/<int:game_id>", methods=["GET", "POST"])
@login_required
def add_review(game_id):
    game = Game.query.get_or_404(game_id)
    if request.method == "POST":
        review_content = request.form.get("review_content")
        hours_played = int(request.form.get("hours_played"), 0)
        completed = request.form.get("completed") == "on"
        rating = int(request.form.get("rating"), 0)

        new_review = Review(
            game_id=game_id,
            user_id=current_user.user_id,
            review_content=review_content,
            hours_played=hours_played,
            completed=completed,
            rating=rating,
        )
        db.session.add(new_review)
        db.session.commit()
        flash("Your review has been added succesfully", "success")
        return redirect(url_for("my_games", user_id=current_user.user_id))
    return render_template("add_review.html", game=game)

@app.route("/my_reviews/<int:user_id>")
def my_reviews(user_id):
    reviews = Review.query.filter_by(user_id=user_id).all()
    user = User.query.get_or_404(user_id)
    owns_profile = user.user_id == current_user.user_id
    return render_template("my_reviews.html",
                           owns_profile=owns_profile,
                           user=user,
                           my_reviews=reviews
                           )

@app.route("/edit_review/<int:review_id>", methods=["GET", "POST"])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.user_id:
        flash("You can only edit your own reviews.", "error")
        return redirect(url_for("my_reviews"))

    if request.method == "POST":
        review.review_content = request.form.get("review_content")
        review.hours_played = int(request.form.get("hours_played", 0))
        review.completed = request.form.get("completed") == "on"
        review.rating = int(request.form.get("rating", 0))

        db.session.commit()
        flash("Your review has been updated successfully", "success")
        return redirect(url_for("game_detail", game_id=review.game.game_id))

    return render_template("edit_review.html", review=review)

@app.route("/delete_review/<int:review_id>", methods=["POST"])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.user_id:
        flash("You can only delete your own reviews.", "error")
        return redirect(url_for("my_reviews"))
    db.session.delete(review)
    db.session.commit()
    flash("Your review has been deleted successfully", "success")

    return redirect(url_for("my_reviews", user_id=current_user.user_id))

@app.route("/profile/<int:user_id>", methods=["GET", "POST"])
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    owns_profile = user.user_id == current_user.user_id

    if request.method == "POST" and owns_profile:
        # Get the data from the form
        new_email = request.form.get("email")
        new_password = request.form.get("newauth")
        new_avatar_url = request.form.get("avatar_url")
        if new_email and new_email != user.email:
            user.email = new_email
        if new_password:
            user.password_hash = generate_password_hash(new_password)
        if new_avatar_url:
            user.avatar_url = new_avatar_url
        db.session.commit()
        flash("Profile updated successfully", "success")
        return redirect(url_for("profile", user_id=user.user_id))
    return render_template("profile.html", user=user, owns_profile=owns_profile)
