from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, login_required, logout_user, current_user
from quest_log import app, db
from quest_log.models import Game, Review, User, UserGame

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

@app.route('/profile/<int:user_id>', methods=["GET", "POST"])
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    
    owns_profile = user.user_id == current_user.user_id
    if request.method == "POST" and owns_profile:
         user.username = request.form.get('username')
         user.email = request.form.get('email')
         user.password = request.form.get('password')
         db.session.commit()
         flash('Profile updated successfully', 'success')
    return render_template('profile.html', user=user, owns_profile=owns_profile)
    




