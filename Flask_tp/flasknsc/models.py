from flasknsc import db, lm
from flask_login import UserMixin

@lm.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(10), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(20), nullable=False)
	game = db.Column(db.Integer, db.ForeignKey('game.id'))
	
	def __repr__(self):
		return "User(" + self.username + " " + self.email + ")"

class Game(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(10), unique=True, nullable=False)
	player1 = db.relationship('User', backref='player1', lazy=True)
	player2 = db.relationship('User', backref='player2', lazy=True)
	player3 = db.relationship('User', backref='player3', lazy=True)
	player4 = db.relationship('User', backref='player4', lazy=True)
	

	def __repr__(self):
		return "Game(" + self.name + ")"