from numpy import average
from app import app
from database import db
from models.sector import Sector
from models.company import Company


sectors = Sector.query.all()

for sector in sectors:
    print("#########################")
    print("#########################")
    print("#########################")
    print(sector.name)
    print("-------------------------")

    companies = Company.query.filter_by(sector_id=sector.id).all()

    e_scores = [
        c.environmental_score for c in companies if c.environmental_score != None]
    s_scores = [
        c.social_score for c in companies if c.social_score != None]
    g_scores = [
        c.governance_score for c in companies if c.governance_score != None]
    t_scores = [
        c.total_score for c in companies if c.total_score != None]

    if not e_scores or not s_scores or not g_scores or not t_scores:
        continue

    sector.environmental_score = round(average(e_scores))
    sector.social_score = round(average(s_scores))
    sector.governance_score = round(average(g_scores))
    sector.total_score = round(average(t_scores))

    print("Environmental:", sector.environmental_score)
    print("Social:", sector.social_score)
    print("Governance:", sector.governance_score)
    print("Total:", sector.total_score)

db.session.commit()
