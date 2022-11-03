from flask_sqlalchemy import SQLAlchemy
from models.company import Company
from models.user import User
from models.exchange import Exchange
from models.location import Location
from models.industry import Industry
from models.sector import Sector

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()
