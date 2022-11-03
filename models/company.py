from models import db


class Company(db.Model):
    """Model for the companies table"""
    __tablename__ = "companies"
    symbol = db.Column(
        db.String(),
        primary_key=True)
    exchange_symbol = db.Column(
        db.String(),
        db.ForeignKey('exchanges.symbol'))
    sector_id = db.Column(
        db.Integer,
        db.ForeignKey('sectors.id'))
    location_id = db.Column(
        db.Integer,
        db.ForeignKey('locations.id'))
    website = db.Column(
        db.String())
    summary = db.Column(
        db.Text)
    esg_last_retrieved = db.Column(
        db.DateTime)
    esg_last_updated = db.Column(
        db.DateTime)
    environmental_score = db.Column(
        db.Integer)
    environmental_level = db.Column(
        db.String())
    environmental_grade = db.Column(
        db.String())
    social_score = db.Column(
        db.Integer)
    social_level = db.Column(
        db.String())
    social_grade = db.Column(
        db.String())
    governance_score = db.Column(
        db.Integer)
    governance_level = db.Column(
        db.String())
    governance_grade = db.Column(
        db.String())
    total_score = db.Column(
        db.Integer)
    total_level = db.Column(
        db.String())
    total_grade = db.Column(
        db.String())
