from app import app
from models import db, User, Company, Exchange, Location, Sector, users_companies

db.drop_all()
db.create_all()
