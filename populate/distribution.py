from numpy import percentile
from app import app
from database import db
from models.company import Company
from models.distribution import Distribution

companies = Company.query.all()

environmental_scores = [
    company.environmental_score for company in companies if company.environmental_score != None]
social_scores = [
    company.social_score for company in companies if company.social_score != None]
governance_scores = [
    company.governance_score for company in companies if company.governance_score != None]
total_scores = [
    company.total_score for company in companies if company.total_score != None]


def set_percentiles(name, scores):
    """Takes the scores and calculates the 10th/90th percentiles as top/bottom. Append it to the db with name of scores."""
    bottom = round(percentile(scores, 10))
    top = round(percentile(scores, 90))
    distribution = Distribution(name=name, top=top, bottom=bottom)
    db.session.add(distribution)


set_percentiles("environmental", environmental_scores)
set_percentiles("social", social_scores)
set_percentiles("governance", governance_scores)
set_percentiles("total", total_scores)

db.session.commit()
