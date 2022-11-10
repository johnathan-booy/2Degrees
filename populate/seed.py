from app import app
from database import db
from models.exchange import Exchange
from models.city import City
from models.region import Region
from models.country import Country
from models.company import Company
from populate.stock_symbols import StockSymbols
from populate.stock_profiles import StockProfiles

db.drop_all()
db.create_all()


############
# COUNTRY
############
us = Country(
    name='United States',
)

countries = [
    us
]
db.session.add_all(countries)
db.session.commit()

############
# REGIONS
############
ny = Region(
    name='NY',
    country_id=us.id
)

regions = [
    ny
]
db.session.add_all(regions)
db.session.commit()

############
# CITIES
############
new_york = City(
    name='New York City',
    region_id=ny.id
)

cities = [
    new_york
]
db.session.add_all(cities)
db.session.commit()

############
# EXCHANGES
############
nasdaq = Exchange(
    symbol='NASDAQ',
    name="Nasdaq, Inc.",
    city_id=new_york.id
)

nyse = Exchange(
    symbol='NYSE',
    name="New York Stock Exchange",
    city_id=new_york.id
)

exchanges = [
    nasdaq,
    nyse
]
db.session.add_all(exchanges)
db.session.commit()

############
# STOCK SYMBOLS
############
StockSymbols.populate_db()


############
# STOCK PROFILES
############
StockProfiles.populate()
