from app import app
from database import db
from models.exchange import Exchange
from models.city import City
from models.region import Region
from models.country import Country
from models.company import Company
from populate.stock_symbols import StockSymbols
from populate.stock_profiles import StockProfiles

db.create_all()

############
# CITIES
############
new_york = City.add(
    'New York City',
    'NY',
    'United States'
)

toronto = City.add(
    'Toronto',
    'ON',
    'Canada'
)

sydney = City.add(
    'Sydney',
    'NSW',
    'Australia'
)

############
# EXCHANGES
############
nasdaq = Exchange.add(
    symbol='NASDAQ',
    name="Nasdaq",
    city=new_york
)

nyse = Exchange.add(
    symbol='NYSE',
    name="New York Stock Exchange",
    city=new_york
)

amex = Exchange.add(
    symbol='AMEX',
    name="American Stock Exchange",
    city=new_york
)

tse = Exchange.add(
    symbol="TSE",
    name="Toronto Stock Exchange",
    city=toronto
)
asx = Exchange.add(
    symbol='ASX',
    name='Australian Securities Exchange',
    city=sydney
)
