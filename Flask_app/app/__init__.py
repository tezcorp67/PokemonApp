from flask import Flask
from config import Config
from flask_login import LoginManager
from app.models import db, User
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()

login_manager.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

# login manager meaasges and config
login_manager.login_view ='auth.login'
login_manager.login_message = 'You must login to gain access!'
login_manager.login_message_category = 'danger'


# import my blueprint onto app
from app.blueprints.auth import auth
from app.blueprints.main import main
from app.blueprints.post import post

# register blueprint onto app
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(post)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

