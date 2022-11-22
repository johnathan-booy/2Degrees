from numpy import percentile
from app import app
from database import db
from models.company import Company
from models.sector import Sector
from models.distribution import Distribution


def get_scores(entities) -> dict:
    return {
        "environmental":
        [entity.environmental_score for entity in entities if entity.environmental_score != None],
        "social":
        [entity.social_score for entity in entities if entity.social_score != None],
        "governance":
        [entity.governance_score for entity in entities if entity.governance_score != None],
        "total":
        [entity.total_score for entity in entities if entity.total_score != None]
    }


def set_percentiles(name: str, scores: dict):
    """Takes the scores and calculates the 10th/90th percentiles as top/bottom. Append it to the db with name of scores."""
    d = Distribution.query.filter_by(name=name).first()
    if not d:
        d = Distribution(name=name)
        db.session.add(d)
    d.environmental_best = round(percentile(scores["environmental"], 90))
    d.environmental_worst = round(percentile(scores["environmental"], 10))
    d.social_best = round(percentile(scores["social"], 90))
    d.social_worst = round(percentile(scores["social"], 10))
    d.governance_best = round(percentile(scores["governance"], 90))
    d.governance_worst = round(percentile(scores["governance"], 10))
    d.total_best = round(percentile(scores["total"], 90))
    d.total_worst = round(percentile(scores["total"], 10))
    db.session.commit()


companies = Company.query.all()
companies_scores = get_scores(companies)
set_percentiles("companies", companies_scores)

sectors = Sector.query.all()
sector_scores = get_scores(sectors)
set_percentiles("sectors", sector_scores)
