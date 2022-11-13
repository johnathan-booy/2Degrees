import requests
import json
from api_tokens import ESG_ENTERPRISE_TOKEN
from datetime import datetime, timezone, timedelta
from sqlalchemy import or_
from app import app
from database import db
from models.company import Company
from models.exchange import Exchange
from helpers.strip_date import strip_date
from helpers.divide_list import divide_list


class ESGRatings():
    """Queries outdated ESG ratings and updates from ESG Enterprise API"""

    def __init__(self) -> None:
        # Find valid date range for ESG ratings
        self.datetime_now = datetime.now(timezone.utc)
        self.datetime_oldest = self.datetime_now - timedelta(days=28)
        self.companies = self.get_companies()
        self.not_found = []
        self.errors = []
        self.exchange_symbols = self.get_exchange_symbols()

    @classmethod
    def populate(cls):
        """Calls the necessary functions to update outdated ESG ratings"""
        esg = cls()

        # Each API query can request up to 50 ESG Ratings
        groups = divide_list(esg.companies, 50)

        for group in groups:
            resp = esg.request(group)

            if not resp.ok:
                esg.error(group, resp)
                return esg

            ratings = resp.json()
            updated = []

            for rating in ratings:
                symbol = rating.get('stock_symbol')
                company = (
                    Company
                    .query
                    .filter_by(symbol=symbol).first()
                )

                if not company:
                    continue

                esg.update_name(rating, company)
                esg.update_date(rating, company)
                esg.update_ratings(rating, company)
                esg.update_exchange(rating, company)
                company.esg_last_retrieved = esg.datetime_now

                updated.append(company)
            db.session.commit()

            for company in group:
                if company not in updated:
                    esg.companies.remove(company)
                    esg.not_found.append(company)

        return esg

    def error(self, group, resp) -> dict:
        """Log information about a request error"""
        symbols = [company.symbol for company in group]
        error = {
            "status_code": resp.status_code,
            "reason": resp.json()['Error'],
            "symbols": symbols,
        }
        self.errors.append(error)
        for company in group:
            self.companies.remove(company)

    def get_exchange_symbols(self) -> list:
        exchanges = Exchange.query.all()
        return [e.symbol for e in exchanges]

    def get_companies(self) -> list:
        return (
            Company
            .query
            .filter(
                Company.esg_available == True,
                or_(
                    Company.esg_last_retrieved < self.datetime_oldest,
                    Company.esg_last_retrieved == None
                )
            )
            .order_by(Company.esg_last_retrieved.desc())
            .all()
        )

    def request(self, companies: list):
        """Send get requests to ESG Enterprise. Max 50 company symbols per request"""
        symbols = [company.symbol for company in companies]
        q = ",".join(symbols)
        resp = (
            requests.get(
                "https://tf689y3hbj.execute-api.us-east-1.amazonaws.com/prod/authorization/search",
                params={
                    'q': q,
                    'token': ESG_ENTERPRISE_TOKEN
                }
            )
        )
        return resp

    def update_name(self, rating: dict, company) -> None:
        """Update company name based on json from ESG Enterprise API"""

        company.name = rating.get(
            'company_name', company.name)

    def update_date(self, rating: dict, company) -> None:
        """Update esg_last_updated based on json from ESG Enterprise API"""

        last_processing_date = rating.get("last_processing_date")
        if last_processing_date:
            company.esg_last_updated = (
                strip_date(
                    last_processing_date, "DD-MM-YYYY")
            )

    def update_ratings(self, rating: dict, company) -> None:
        """Update esg ratings based on json from ESG Enterprise API"""

        company.environmental_score = rating.get(
            'environment_score', company.environmental_score)
        company.environmental_level = rating.get(
            'environment_level', company.environmental_level)
        company.environmental_grade = rating.get(
            'environment_grade', company.environmental_grade)
        company.social_score = rating.get(
            'social_score', company.social_score)
        company.social_level = rating.get(
            'social_level', company.social_level)
        company.social_grade = rating.get(
            'social_grade', company.social_grade)
        company.governance_score = rating.get(
            'governance_score', company.governance_score)
        company.governance_level = rating.get(
            'governance_level', company.governance_level)
        company.governance_grade = rating.get(
            'governance_grade', company.governance_grade)
        company.total_score = rating.get(
            'total', company.total_score)
        company.total_level = rating.get(
            'total_level', company.total_level)
        company.total_grade = rating.get(
            'total_grade', company.total_grade)

    def update_exchange(self, rating: dict, company) -> None:
        """Update exchange symbol based on json from ESG Enterprise API"""

        exchange_symbol = rating.get('exchange_symbol')

        if not exchange_symbol:
            return

        if exchange_symbol not in self.exchange_symbols:
            new_exchange = Exchange(symbol=exchange_symbol)
            self.exchange_symbols.append(exchange_symbol)
            db.session.add(new_exchange)
            db.session.commit()

        company.exchange_symbol = exchange_symbol


esg_ratings = ESGRatings.populate()

# TEST WITH THE FOLLOWING QUERY IN PSQL
""" 
SELECT
    symbol,
    name,
    exchange_symbol,
    environmental_score,
    social_score,
    governance_score,
    total_score,
    esg_last_retrieved,
    esg_last_updated
FROM 
    companies
WHERE
    exchange_symbol IS NOT NULL
ORDER BY
    environmental_score DESC; 
"""
