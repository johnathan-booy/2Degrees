import requests
from numpy import average, percentile
from api_tokens import ESG_ENTERPRISE_TOKEN
from datetime import datetime, timezone, timedelta
from sqlalchemy import or_
from app import app
from database import db
from models.company import Company
from models.exchange import Exchange
from models.sector import Sector
from models.country import Country
from models.distribution import Distribution
from helpers.strip_date import strip_date
from helpers.divide_list import divide_list


class ESGRatings():
    """
    Updates ESG Ratings from ESG Enterprise API

    Should be called as a class constructor method.

        `esg = ESGRatings.populate()`

    Return object will include:

        `esg.errors` -> Logged errors (often 429 for TooManyRequests)

        `esg.companies` -> All companies initially included in the update

        `esg.updated` -> Companies that were succesfully updated

    """

    def __init__(self) -> None:
        # Find valid date range for ESG ratings
        self.datetime_now = datetime.now(timezone.utc)
        self.datetime_oldest = self.datetime_now - timedelta(days=28)

        # Get companies with missing or expired esg ratings
        self.companies = self.get_companies()

        # Arrays for logging updates and errors
        self.updated = {"companies": [], "sectors": [],
                        "countries": [], "exchanges": [], "distributions": []}
        self.errors = []
        self.responses = []

    ###########################
    # Constructor function
    ###########################
    @classmethod
    def populate(cls):
        esg = cls()
        esg.updated["companies"] = esg.populate_companies()
        esg.updated["sectors"] = esg.populate_avg_scores(Sector)
        esg.updated["countries"] = esg.populate_avg_scores(Country)
        esg.updated["distributions"] = esg.populate_distributions()
        return esg

    ###########################
    # Companies
    ###########################
    def populate_companies(self) -> list:
        """Calls the necessary functions to update outdated ESG ratings"""

        updated = []

        for company in self.companies:
            resp = self.request(company)

            if not resp.ok:
                self.api_error(company, resp)
                return self

            ratings = resp.json()
            self.responses.append(ratings)

            for rating in ratings:
                stock_symbol = rating.get("stock_symbol")
                company_name = rating.get("company_name")
                if (stock_symbol != company.symbol.upper() and company_name != company.name):
                    continue

                self.update_symbol(rating, company)
                self.update_exchange_symbol(rating, company)
                self.update_date(rating, company)
                self.update_ratings(rating, company)
                updated.append(company)
                print("Updated", "->", company)

            if company not in updated:
                self.esg_error(company)
                company.esg_available = False

            company.esg_last_retrieved = self.datetime_now

        db.session.commit()
        return updated

    def api_error(self, company, resp):
        """Log information about a request error"""
        error = {
            "status_code": resp.status_code,
            "reason": resp.json()['Error'],
            "company": company,
        }
        print("API ERROR", "->", error)
        self.errors.append(error)

    def esg_error(self, company):
        """Log information about a missing company"""
        error = {
            "status_code": 404,
            "reason": "Company not found",
            "company": company
        }
        print("ESG ERROR", "->", error)
        self.errors.append(error)

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

    def request(self, company: list):
        """Send get request to ESG Enterprise"""
        resp = (
            requests.get(
                "https://tf689y3hbj.execute-api.us-east-1.amazonaws.com/prod/authorization/search",
                params={
                    'q': company.name,
                    'token': ESG_ENTERPRISE_TOKEN
                }
            )
        )
        return resp

    def update_symbol(self, rating: dict, company) -> None:
        """Update stock symbol if it's not available in ESG Enterprise"""

        symbol = rating.get("stock_symbol")

        if not symbol:
            return

        company.symbol = symbol

    def update_exchange_symbol(self, rating: dict, company) -> None:
        """Update exchange symbol"""

        exchange_symbol = rating.get("exchange_symbol")

        if not exchange_symbol:
            return

        if not Exchange.query.filter_by(symbol=exchange_symbol).first():
            new_exchange = Exchange(symbol=exchange_symbol)
            db.session.add(new_exchange)
            db.session.commit()
            print("Added", "->", new_exchange)

        company.exchange_symbol = exchange_symbol

    def update_date(self, rating: dict, company) -> None:
        """Update esg_last_updated based on json from ESG Enterprise API"""

        last_processing_date = rating.get("last_processing_date")
        if last_processing_date:
            company.esg_last_updated = (
                strip_date(
                    last_processing_date, "DD-MM-YYYY")
            )

    def update_ratings(self, rating: dict, company) -> None:
        """Update company esg ratings based on json from ESG Enterprise API"""

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

    ###########################
    # Sectors, Countries, Exchanges
    ###########################
    def populate_avg_scores(self, cls_) -> list:
        """Update average ESG-T scores for given objects (sectors, countries or exchanges)"""
        objects = cls_.query.all()
        updated = []
        for object in objects:
            e_scores = [
                c.environmental_score for c in object.companies if c.environmental_score != None]
            s_scores = [
                c.social_score for c in object.companies if c.social_score != None]
            g_scores = [
                c.governance_score for c in object.companies if c.governance_score != None]
            t_scores = [
                c.total_score for c in object.companies if c.total_score != None]

            if not e_scores or not s_scores or not g_scores or not t_scores:
                continue

            object.environmental_score = round(average(e_scores))
            object.social_score = round(average(s_scores))
            object.governance_score = round(average(g_scores))
            object.total_score = round(average(t_scores))
            updated.append(object)
            print("Updated", "->", object)

        db.session.commit()
        return updated

    ###########################
    # Distributions
    ###########################
    def populate_distributions(self) -> list:
        """Updates the best/worst percentiles for ESGT in each object (Company, Sector, Country, Exchange)"""
        updated = []
        for cls_ in [Company, Sector, Country]:
            d = self.update_distribution(cls_)
            updated.append(d)
            print("Updated", "->", d)
        return updated

    def update_distribution(self, cls_):
        """Calculates the best/worst percentiles and appends it to the db with name of scores."""

        scores = self.get_scores(cls_)
        name = cls_.__tablename__

        d = Distribution.query.filter_by(name=name).first()

        if not d:
            d = Distribution(name=name)
            db.session.add(d)

        for type in ["environmental", "social", "governance", "total"]:
            d[f"{type}_best"] = round(percentile(scores[type], 90))
            d[f"{type}_worst"] = round(percentile(scores[type], 10))

        db.session.commit()

        return d

    def get_scores(self, cls_) -> dict:
        objects = cls_.query.all()

        return {
            "environmental":
            [object.environmental_score for object in objects if object.environmental_score != None],
            "social":
            [object.social_score for object in objects if object.social_score != None],
            "governance":
            [object.governance_score for object in objects if object.governance_score != None],
            "total":
            [object.total_score for object in objects if object.total_score != None]
        }
