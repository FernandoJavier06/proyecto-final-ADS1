from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
loginManager = LoginManager()

loginManager.login_view = 'auth.login'
loginManager.login_message = 'Por favor, inicie sesión para acceder a esta página.'
