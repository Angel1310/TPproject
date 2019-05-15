from flask import render_template, url_for, flash, redirect
from flasknsc import app, db, bc
from flasknsc.models import User, Game
from flasknsc.forms import RegistrationForm, LoginForm, GameForm
from flask_login import logout_user, login_user, current_user, login_required

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', title='Home')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pass = bc.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pass, game = 0)
		db.session.add(user)
		db.session.commit()
		flash('Account created for ' + form.username.data + '!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bc.check_password_hash(user.password, form.password.data):
			login_user(user)
			flash('You have logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash("Couldn't login. Check your username and password!")
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/profile")
@login_required
def profile():
	return render_template('profile.html', title='Profile')

@app.route("/game/new", methods=['GET', 'POST'])
@login_required
def new_game():
	form = GameForm()
	
	if form.validate_on_submit():
		flash('Your game has been created!', 'success')
		game = Game(name=form.name.data, player1=[current_user])
		db.session.add(game)
		db.session.commit()
		return redirect(url_for('home'))
	
	return render_template('create_game.html', form = form, title='New Game')

@app.route("/games")
def games():
	games = Game.query.all()
	return render_template('games.html', games=games ,title='Games')

@app.route("/game/<int:game_id>")
def game(game_id):
	game = Game.query.filter_by(id=game_id).first()
	return render_template("game.html", game=game)

@app.route("/join_game/<int:game_id>")
def join_game(game_id):
	game = Game.query.get_or_404(game_id)
	if not game.player2:
		game.player2=[current_user]
		db.session.commit()
	if not game.player3:
		game.player3=[current_user]
		db.session.commit()
	if not game.player4:
		game.player4=[current_user]
		db.session.commit()
	return render_template("game.html", game=game)