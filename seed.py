from app import app
from database import db
from models.company import Company
from models.exchange import Exchange
from models.location import Location
from models.sector import Sector
from models.user import User
from models.users_companies import users_companies

db.drop_all()
db.create_all()
