from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from .db import db


app = Flask(__name__)
app.config.from_object('config')


migrate = Migrate(app, db)
lm = LoginManager()
lm.init_app(app)

from app import views, models, scripts


@lm.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))
