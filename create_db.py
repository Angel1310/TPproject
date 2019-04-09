from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
	email = db.Column(db.String(100), nullable = False) 
	username = db.Column(db.String(100), nullable = False)
	password = db.Column(db.String(100), nullable = False)
	game = db.Column(db.Integer, db.ForeignKey('game.id'))

	def __init_(self, name, email, password):
		self.name = name
		self.email = email
		self.password = password

class Game(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
	player1 = db.Column(db.Integer, db.ForeignKey('user.id'))
	player2 = db.Column(db.Integer, db.ForeignKey('user.id'))
	player3 = db.Column(db.Integer, db.ForeignKey('user.id'))
	player4 = db.Column(db.Integer, db.ForeignKey('user.id'))
	