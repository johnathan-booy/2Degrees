from populate.esg_ratings import ESGRatings
from populate.profiles import Profiles

esg = ESGRatings.populate()

companies = esg['updated']['companies']
profiles = Profiles.populate("companies", companies=companies)
