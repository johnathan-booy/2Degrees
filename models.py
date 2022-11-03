from flask_sqlalchemy import SQLAlchemy
from models.company import Company
from models.user import User
from models.exchange import Exchange
from models.location import Location
from models.sector import Sector
from models.users_companies import users_companies

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()
