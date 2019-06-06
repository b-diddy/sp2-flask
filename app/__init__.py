from flask import Flask
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "SecretKeyToPreventXSS"

login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)

from app import main
