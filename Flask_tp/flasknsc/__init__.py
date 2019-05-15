from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bf6423960e622d5907915c5292cab550'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bc = Bcrypt(app)
lm = LoginManager(app)
lm.login_view = 'login'

from flasknsc import routes