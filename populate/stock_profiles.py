"""
Update profiles from Yahoo Finance API

Should be called as a class constructor method.

    StockProfiles.populate() -> Populates outdated profiles.

    StockProfiles.populate(update='all') -> Populates profiles for all stocks

    StockProfiles.populate(update='symbol', symbol='AAPL') -> Populates profile for given stock symbol
"""

import requests
from datetime import datetime, timezone, timedelta
from sqlalchemy import or_
from app import app
from database import db
from models.company import Company
from models.sector import Sector
from models.country import Country
from models.region import Region
from models.city import City


class StockProfiles():
    """Queries outdated stock"""

    def __init__(self, update, symbol) -> None:
        self.datetime_now = datetime.now(timezone.utc)
        self.datetime_oldest = self.datetime_now - timedelta(days=365)
        self.update = update
        self.symbol = symbol
        self.endpoint = "https://query1.finance.yahoo.com/v10/finance/quoteSummary"
        self.params = {"modules": "assetProfile"}
        self.headers = {'User-agent': 'Mozilla/5.0'}
        self.companies = self.get_companies()
        self.updated = []
        self.errors = []

    @classmethod
    def populate(cls, update="outdated", symbol=""):
        """
        Populates stock profiles and returns an instance of the StockProfiles class. 
        """

        sp = cls(update, symbol)

        for company in sp.companies:
            resp = sp.request(company.symbol)

            if not resp.ok:
                """Log the error and remove the company from list"""
                sp.errors.append(sp.log_error(company, resp))
                continue

            data = resp.json()['quoteSummary']['result'][0]['assetProfile']

            sp.update_website(company, data)
            sp.update_summary(company, data)
            sp.update_sector(company, data)
            sp.update_location(company, data)
            company.profile_last_retrieved = sp.datetime_now

            sp.updated.append(company)

        db.session.commit()
        return sp

    def log_error(self, company, resp) -> dict:
        """Log information about a request error"""
        return {
            "status_code": resp.status_code,
            "reason": resp.reason,
            "company": company,
        }

    def get_companies(self) -> list:
        """Get companies based on the update argument"""
        match self.update:
            case "all":
                return Company.query.all()
            case "outdated":
                return (
                    Company
                    .query
                    .filter(
                        Company.profile_available == True,
                        or_(
                            Company.profile_last_retrieved < self.datetime_oldest,
                            Company.profile_last_retrieved == None
                        )
                    )
                    .all()
                )
            case "symbol":
                return [Company.query.filter_by(symbol=self.symbol).first()]

    def request(self, symbol: list) -> dict:
        """Send get request for one company symbol to Yahoo Finance API"""

        # Yahoo Finance doesn't like dots in the stock symbol
        symbol = symbol.replace(".q", "-")

        resp = (
            requests.get(
                f"{self.endpoint}/{symbol}",
                self.params,
                headers=self.headers
            )
        )
        return resp

    def update_website(self, company, data: dict) -> None:
        """Update company website based on json from Yahoo Finance API"""

        company.website = data.get(
            "website",
            company.website
        )

    def update_summary(self, company, data: dict) -> None:
        """Update company summary based on json from Yahoo Finance API"""

        company.summary = data.get(
            "longBusinessSummary",
            company.summary
        )

    def update_sector(self, company, data: dict) -> None:
        """Update company sector based on json from Yahoo Finance API"""

        sector_name = data.get("sector")

        if not sector_name:
            return

        sector = (Sector.query
                  .filter_by(
                      name=sector_name)
                  .first())

        if not sector:
            print(f"Added sector -> {sector_name}")
            sector = Sector(name=sector_name)
            db.session.add(sector)
            db.session.commit()

        company.sector_id = sector.id

    def update_location(self, company, data: dict) -> None:
        """Update company location based on json from Yahoo Finance API"""

        country_name = data.get("country")
        region_name = data.get("state")
        city_name = data.get("city")

        if country_name:
            country = (Country.query
                       .filter_by(
                           name=country_name)
                       .first())
            if not country:
                print(f"Added country -> {country_name}")
                country = Country(name=country_name)
                db.session.add(country)
                db.session.commit()
            company.country_id = country.id

        if region_name:
            region = (Region.query
                      .filter_by(
                          name=region_name,
                          country_id=company.country_id)
                      .first())
            if not region:
                print(f"Added region -> {region_name}")
                region = Region(name=region_name,
                                country_id=company.country_id)
                db.session.add(region)
                db.session.commit()
            company.region_id = region.id

        if city_name:
            city = (City.query
                    .filter_by(
                        name=city_name,
                        region_id=company.region_id)
                    .first())
            if not city:
                print(f"Added city -> {city_name}")
                city = City(name=city_name,
                            region_id=company.region_id,
                            country_id=company.country_id)
                db.session.add(city)
                db.session.commit()
            company.city_id = city.id
