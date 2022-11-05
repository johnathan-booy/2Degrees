from datetime import datetime, timezone
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


############
# SECTORS
############
technology = Sector(
    name='Technology'
)
sectors = [
    technology
]
db.session.add_all(sectors)
db.session.commit()


############
# LOCATIONS
############
cupertino = Location(
    city='Cupertino',
    region='CA',
    country='United States'
)

new_york = Location(
    city='New York City',
    region='NY',
    country='United States'
)
locations = [
    cupertino,
    new_york
]
db.session.add_all(locations)
db.session.commit()

############
# EXCHANGES
############
nasdaq = Exchange(
    symbol='NASDAQ',
    name="Nasdaq, Inc.",
    location_id=new_york.id
)
exchanges = [
    nasdaq
]
db.session.add_all(exchanges)
db.session.commit()


############
# COMPANIES
############
apple = Company(
    symbol='AAPL',
    name='Apple Inc.',
    exchange_symbol=nasdaq.symbol,
    sector_id=technology.id,
    location_id=cupertino.id,
    website="https://www.apple.com",
    summary="Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. It also sells various related services. In addition, the company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and HomePod. Further, it provides AppleCare support and cloud services store services; and operates various platforms, including the App Store that allow customers to discover and download applications and digital content, such as books, music, video, games, and podcasts. Additionally, the company offers various services, such as Apple Arcade, a game subscription service; Apple Fitness+, a personalized fitness service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It distributes third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was incorporated in 1977 and is headquartered in Cupertino, California.",
    esg_last_retrieved=datetime.now(timezone.utc),
    esg_last_updated=datetime.strptime("16-04-2022", "%d-%m-%Y"),
    environmental_score=355,
    environmental_grade='BB',
    environmental_level='Medium',
    social_score=281,
    social_grade='B',
    social_level='Medium',
    governance_score=255,
    governance_grade='B',
    governance_level='Medium',
    total_score=891,
    total_grade='BB',
    total_level='Medium',
)
companies = [
    apple
]
db.session.add_all(companies)
db.session.commit()

############
# USERS
############

johnathan = User(
    username="johnathanbooy",
    password="Password",
    email="johnathan.booy@gmail.com",
    first_name="Johnathan",
    last_name="Booy",)

johnathan.companies.append(apple)

db.session.add(johnathan)
db.session.commit()

import pdb
pdb.set_trace()
