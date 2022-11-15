from app import app
from database import db
from models.exchange import Exchange
from models.city import City

db.create_all()

############
# CITIES
############
amsterdam = City.add(
    "Amsterdam",
    "NH",
    "Netherlands"
)
buenos_aires = City.add(
    "Buenos Aires",
    "BA",
    "Argentina"
)
madrid = City.add(
    "Madrid",
    "M",
    "Spain"
)
milan = City.add(
    "Milan",
    "MI",
    "Italy"
)
new_york = City.add(
    'New York City',
    'NY',
    'United States'
)

stockholm = City.add(
    "Stockholm",
    "SO",
    "Sweden"
)

sydney = City.add(
    'Sydney',
    'NSW',
    'Australia'
)
toronto = City.add(
    'Toronto',
    'ON',
    'Canada'
)


############
# EXCHANGES
############

amex = Exchange.add(
    symbol='AMEX',
    name="American Stock Exchange",
    city=new_york
)
ams = Exchange.add(
    symbol="AMS",
    name="Euronext Amsterdam",
    city=amsterdam
)
asx = Exchange.add(
    symbol='ASX',
    name='Australian Securities Exchange',
    city=sydney
)

bcba = Exchange.add(
    symbol="BCBA",
    name="Buenos Aires Stock Exchange",
    city=buenos_aires
)

bit = Exchange.add(
    symbol="BIT",
    name="Borsa Italiana",
    city=milan
)

bme = Exchange.add(
    symbol="BME",
    name="Bolsa de Madrid",
    city=madrid
)

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
tse = Exchange.add(
    symbol="TSE",
    name="Toronto Stock Exchange",
    city=toronto
)
