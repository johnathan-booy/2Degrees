from database import db


class Company(db.Model):
    """Model for the companies table"""

    __tablename__ = "companies"

    def __repr__(self) -> str:
        return f"<Company  {self.symbol} {self.exchange_symbol} '{self.name}'>"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    symbol = db.Column(
        db.String(),
        nullable=False
    )

    exchange_symbol = db.Column(
        db.String(),
        db.ForeignKey('exchanges.symbol'),
        nullable=False
    )

    name = db.Column(
        db.String(),
        nullable=False
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

    @classmethod
    def ranked(cls, type, count, ranking) -> list:
        """Return companies ranked best or worst based on ESGT ratings"""

        if ranking != "worst" and ranking != "best":
            return

        q1 = None
        q2 = cls.total_score

        match type:
            case "E":
                q1 = cls.environmental_score
            case "S":
                q1 = cls.social_score
            case "G":
                q1 = cls.governance_score
            case "T":
                q1 = cls.total_score
                q2 = cls.environmental_score

        companies = (
            cls.query
            .filter(q1 != None)
            .order_by(
                q1.desc() if ranking == "best" else q1,
                q2.desc() if ranking == "best" else q2)
            .limit(count)
            .all()
        )

        return [company.serialize() for company in companies]

    def serialize(self) -> dict:
        """Return a dict representation of Company"""
        location = {
            "city": self.city.name if self.city else None,
            "region": self.region.name if self.region else None,
            "country": self.country.name if self.country else None
        }

        profile = {
            "symbol": self.symbol,
            "name": self.name,
            "exchange_symbol": self.exchange_symbol,
            "sector": self.sector.name if self.sector else None,
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
