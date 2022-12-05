from populate.esg_ratings import ESGRatings
from populate.profiles import Profiles

esg = ESGRatings.populate()

profiles = Profiles.populate("companies", companies=esg.updated["companies"])
