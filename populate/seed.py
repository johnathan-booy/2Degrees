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

redmond = Location(
    city="Redmond",
    region="WA",
    country="United States"
)

locations = [
    cupertino,
    new_york,
    redmond
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
    summary="Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide. The company operates in three segments: Productivity and Business Processes, Intelligent Cloud, and More Personal Computing. The Productivity and Business Processes segment offers Office, Exchange, SharePoint, Microsoft Teams, Office 365 Security and Compliance, Microsoft Viva, and Skype for Business; Skype, Outlook.com, OneDrive, and LinkedIn; and Dynamics 365, a set of cloud-based and on-premises business solutions for organizations and enterprise divisions. The Intelligent Cloud segment licenses SQL, Windows Servers, Visual Studio, System Center, and related Client Access Licenses; GitHub that provides a collaboration platform and code hosting service for developers; Nuance provides healthcare and enterprise AI solutions; and Azure, a cloud platform. It also offers enterprise support, Microsoft consulting, and nuance professional services to assist customers in developing, deploying, and managing Microsoft server and desktop solutions; and training and certification on Microsoft products. The More Personal Computing segment provides Windows original equipment manufacturer (OEM) licensing and other non-volume licensing of the Windows operating system; Windows Commercial, such as volume licensing of the Windows operating system, Windows cloud services, and other Windows commercial offerings; patent licensing; and Windows Internet of Things. It also offers Surface, PC accessories, PCs, tablets, gaming and entertainment consoles, and other devices; Gaming, including Xbox hardware, and Xbox content and services; video games and third-party video game royalties; and Search, including Bing and Microsoft advertising. The company sells its products through OEMs, distributors, and resellers; and directly through digital marketplaces, online stores, and retail stores. Microsoft Corporation was founded in 1975 and is headquartered in Redmond, Washington.",
    esg_available=True,
    esg_last_retrieved=datetime.strptime("02-11-2022", "%d-%m-%Y"),
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
microsoft = Company(
    symbol='MSFT',
    name='Microsoft Corporation',
    exchange_symbol=nasdaq.symbol,
    sector_id=technology.id,
    location_id=redmond.id,
    website="https://www.microsoft.com",
    summary="Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. It also sells various related services. In addition, the company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and HomePod. Further, it provides AppleCare support and cloud services store services; and operates various platforms, including the App Store that allow customers to discover and download applications and digital content, such as books, music, video, games, and podcasts. Additionally, the company offers various services, such as Apple Arcade, a game subscription service; Apple Fitness+, a personalized fitness service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It distributes third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was incorporated in 1977 and is headquartered in Cupertino, California.",
    esg_available=True,
    esg_last_retrieved=datetime.strptime("02-11-2022", "%d-%m-%Y"),
    esg_last_updated=datetime.strptime("27-04-2022", "%d-%m-%Y"),
    environmental_score=715,
    environmental_grade='AA',
    environmental_level='Excellent',
    social_score=443,
    social_grade='BBB',
    social_level='High',
    governance_score=375,
    governance_grade='BB',
    governance_level='Medium',
    total_score=1533,
    total_grade='A',
    total_level='High',
)
companies = [
    apple,
    microsoft
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
johnathan.companies.append(microsoft)

db.session.add(johnathan)
db.session.commit()
