"""
Updates ESG Ratings from ESG Enterprise API

Should be called as a class constructor method.

    esg = ESGRatings.populate()

Return object will include:

    esg.errors -> Logged errors (often 429 for TooManyRequests)
    esg.companies -> All companies initially included in the update
    esg.updated -> Companies that were succesfully updated
"""

import requests
from numpy import average
from api_tokens import ESG_ENTERPRISE_TOKEN
from datetime import datetime, timezone, timedelta
from sqlalchemy import or_
from app import app
from database import db
from models.company import Company
from models.exchange import Exchange
from models.sector import Sector
from models.country import Country
from helpers.strip_date import strip_date
from helpers.divide_list import divide_list


class ESGRatings():
    """Queries outdated ESG ratings and updates from ESG Enterprise API"""

    def __init__(self) -> None:
        # Find valid date range for ESG ratings
        self.datetime_now = datetime.now(timezone.utc)
        self.datetime_oldest = self.datetime_now - timedelta(days=28)
        self.companies = self.get_companies()
        self.updated = []
        self.errors = []
        self.exchange_symbols = self.get_exchange_symbols()

    @classmethod
    def populate(cls):
        esg = cls()
        esg.populate_companies()
        esg.populate_sectors()
        esg.populate_countries()

    def populate_companies(self):
        """Calls the necessary functions to update outdated ESG ratings"""

        groups = divide_list(self.companies, 10)

        for group in groups:
            resp = self.request(group)

            if not resp.ok:
                self.api_error(group, resp)
                return self

            ratings = resp.json()

            for rating in ratings:
                symbol = rating.get('stock_symbol')
                company = (
                    Company
                    .query
                    .filter_by(symbol=symbol).first()
                )

                if not company:
                    continue

                print("Updated company ->", company.name)
                self .update_date(rating, company)
                self.update_ratings(rating, company)
                company.esg_last_retrieved = self.datetime_now

                self.updated.append(company)
            db.session.commit()

    def api_error(self, group, resp) -> dict:
        """Log information about a request error"""
        print("API ERROR ->", resp.status_code)
        error = {
            "status_code": resp.status_code,
            "reason": resp.json()['Error'],
            "companies": group,
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
        # Requests are made like nyse:aapl,nasdaq:msft
        pairs = [f"{c.exchange_symbol}:{c.symbol}" for c in companies]
        q = ",".join(pairs)
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

    def populate_sectors(self) -> None:
        sectors = Sector.query.all()

        for sector in sectors:
            print("Updated sector ->", sector.name)

            e_scores = [
                c.environmental_score for c in sector.companies if c.environmental_score != None]
            s_scores = [
                c.social_score for c in sector.companies if c.social_score != None]
            g_scores = [
                c.governance_score for c in sector.companies if c.governance_score != None]
            t_scores = [
                c.total_score for c in sector.companies if c.total_score != None]

            if not e_scores or not s_scores or not g_scores or not t_scores:
                continue

            sector.environmental_score = round(average(e_scores))
            sector.social_score = round(average(s_scores))
            sector.governance_score = round(average(g_scores))
            sector.total_score = round(average(t_scores))

        db.session.commit()

    def populate_countries(self) -> None:
        countries = Country.query.all()

        for country in countries:
            print("Updated country ->", country.name)

            e_scores = [
                c.environmental_score for c in country.companies if c.environmental_score != None]
            s_scores = [
                c.social_score for c in country.companies if c.social_score != None]
            g_scores = [
                c.governance_score for c in country.companies if c.governance_score != None]
            t_scores = [
                c.total_score for c in country.companies if c.total_score != None]

            if not e_scores or not s_scores or not g_scores or not t_scores:
                continue

            country.environmental_score = round(average(e_scores))
            country.social_score = round(average(s_scores))
            country.governance_score = round(average(g_scores))
            country.total_score = round(average(t_scores))

        db.session.commit()


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
    environmental_score IS NOT NULL
ORDER BY
    environmental_score DESC; 
"""
