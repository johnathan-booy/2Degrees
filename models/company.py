from database import db


class Company(db.Model):
    """Model for the companies table"""

    __tablename__ = "companies"

    def __repr__(self) -> str:
        return f"<Company  {self.symbol} '{self.name}'>"

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
    region_id = db.Column(
        db.Integer,
        db.ForeignKey('regions.id')
    )
    country_id = db.Column(
        db.Integer,
        db.ForeignKey('countries.id')
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

    def serialize(self):
        location = {
            "city": self.city.name,
            "region": self.region.name,
            "country": self.country.name,
        }

        profile = {
            "symbol": self.symbol,
            "name": self.name,
            "exchange_symbol": self.exchange_symbol,
            "sector": self.sector.name,
            "location": location,
            "website": self.website,
            "summary": self.summary
        }

        esg_ratings = None
        if self.environmental_score and self.social_score and self.governance_score and self.total_score:
            esg_ratings = {
                "scores": {
                    "environmental_score": self.environmental_score,
                    "social_score": self.social_score,
                    "governance_score": self.governance_score,
                    "total_score": self.total_score
                },
                "levels": {
                    "environmental_levels": self.environmental_level,
                    "social_levels": self.social_level,
                    "governance_levels": self.governance_level,
                    "total_levels": self.total_level
                },
                "grades": {
                    "environmental_grade": self.environmental_grade,
                    "social_grade": self.social_grade,
                    "governance_grade": self.governance_grade,
                    "total_grade": self.total_grade
                }
            }

        response = {
            "profile": profile,
            "esg_ratings": esg_ratings
        }
        return response
