from app import app
from database import db
from models.exchange import Exchange
from models.city import City
from models.sector import Sector

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

############
# SECTORS
############

energy = Sector.add(
    name="Energy",
    logo_class="fa-solid fa-lightbulb"
)

utilities = Sector.add(
    name="Utilities",
    logo_class="fa-solid fa-bolt"
)

materials = Sector.add(
    name="Basic Materials",
    logo_class="fa-solid fa-tree"
)

technology = Sector.add(
    name="Technology",
    logo_class="fa-solid fa-microchip"
)

industrials = Sector.add(
    name="Industrials",
    logo_class="fa-solid fa-helmet-safety"
)

consumer_defensive = Sector.add(
    name="Consumer Defensive",
    logo_class="fa-solid fa-utensils"
)
healthcare = Sector.add(
    name="Healthcare",
    logo_class="fa-solid fa-kit-medical"
)
financial_services = Sector.add(
    name="Financial Services",
    logo_class="fa-solid fa-credit-card"
)
real_estate = Sector.add(
    name="Real Estate",
    logo_class="fa-solid fa-house"
)
communication_services = Sector.add(
    name="Communication Services",
    logo_class="fa-solid fa-wifi"
)

consumer_cyclical = Sector.add(
    name="Consumer Cyclical",
    logo_class="fa-solid fa-cart-shopping"
)
