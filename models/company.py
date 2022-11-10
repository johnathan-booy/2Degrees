from database import db


class Company(db.Model):
    """Model for the companies table"""

    __tablename__ = "companies"

    def __repr__(self) -> str:
        return f"<Company  '{self.name}'  {self.symbol} >"

    symbol = db.Column(
        db.String(),
        primary_key=True
    )
    name = db.Column(
        db.String()
    )
    exchange_symbol = db.Column(
        db.String(),
        db.ForeignKey('exchanges.symbol')
    )
    sector_id = db.Column(
        db.Integer,
        db.ForeignKey('sectors.id')
    )
    city_id = db.Column(
        db.Integer,
        db.ForeignKey('cities.id')
    )
    website = db.Column(
        db.String()
    )
    summary = db.Column(
        db.Text
    )
    profile_available = db.Column(
        db.Boolean,
        default=True
    )
    profile_last_retrieved = db.Column(
        db.DateTime
    )
    esg_available = db.Column(
        db.Boolean,
        default=True
    )
    esg_last_retrieved = db.Column(
        db.DateTime
    )
    esg_last_updated = db.Column(
        db.DateTime
    )
    environmental_score = db.Column(
        db.Integer
    )
    environmental_level = db.Column(
        db.String()
    )
    environmental_grade = db.Column(
        db.String()
    )
    social_score = db.Column(
        db.Integer
    )
    social_level = db.Column(
        db.String()
    )
    social_grade = db.Column(
        db.String()
    )
    governance_score = db.Column(
        db.Integer
    )
    governance_level = db.Column(
        db.String()
    )
    governance_grade = db.Column(
        db.String()
    )
    total_score = db.Column(
        db.Integer
    )
    total_level = db.Column(
        db.String()
    )
    total_grade = db.Column(
        db.String()
    )
