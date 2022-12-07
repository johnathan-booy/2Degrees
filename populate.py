from app import app
from populate.esg_ratings import ESGRatings
from populate.profiles import Profiles

with app.app_context():
    esg = ESGRatings.populate()

    companies = esg.updated["companies"]
    if companies:
        profiles = Profiles.populate("companies", companies=companies)
