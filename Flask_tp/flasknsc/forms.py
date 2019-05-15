from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flasknsc.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username',
							validators=[DataRequired(), Length(min=4, max=10)])
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Password',validators=[DataRequired(), Length(min=4, max=20)])
	confirm_password = PasswordField('Password',
						validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Sign Up')

	def validate_username(self, username):

		user = User.query.filter_by(username = username.data).first()

		if user:
			raise ValidationError('That username is taken. Please choose another.')

	def validate_email(self, email):

		user = User.query.filter_by(email = email.data).first()

		if user:
			raise ValidationError('That email is taken. Please choose another.')	


class LoginForm(FlaskForm):
	username = StringField('Username',
							validators=[DataRequired(), Length(min=4, max=10)])
	password = PasswordField('Password', validators=[DataRequired()])

	submit = SubmitField('Login')

class GameForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	submit = SubmitField('Make game')
		