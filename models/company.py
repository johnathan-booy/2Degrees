from urllib.parse import urlparse
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

    @property
    def logo_url(self):
        """Parse website and create logo url via Clearbit"""
        if not self.website:
            return

        domain = urlparse(self.website).netloc.replace("www.", "")

        return f"https://logo.clearbit.com/{domain}"

    @classmethod
    def ranked(cls, type: str, count: int, offset: int, ranking: str) -> list:
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
            .offset(offset)
            .all()
        )

        return companies

    @classmethod
    def esg_ranges(cls) -> dict:
        """Return the highest and lowests scores for each category in the database"""
        qe = cls.environmental_score
        qs = cls.social_score
        qg = cls.governance_score
        qt = cls.total_score

        max_e = cls.query.filter(qe != None).order_by(
            qe.desc()).first().environmental_score
        max_s = cls.query.filter(qs != None).order_by(
            qs.desc()).first().social_score
        max_g = cls.query.filter(qg != None).order_by(
            qg.desc()).first().governance_score
        max_t = cls.query.filter(qt != None).order_by(
            qt.desc()).first().total_score

        min_e = cls.query.filter(qe != None).order_by(
            qe).first().environmental_score
        min_s = cls.query.filter(
            qs != None).order_by(qs).first().social_score
        min_g = cls.query.filter(qg != None).order_by(
            qg).first().governance_score
        min_t = cls.query.filter(
            qt != None).order_by(qt).first().total_score

        ranges = {
            "environmental": {"min": min_e, "max": max_e},
            "social": {"min": min_s, "max": max_s},
            "governance": {"min": min_g, "max": max_g},
            "total": {"min": min_t, "max": max_t}
        }

        return ranges

    @classmethod
    def num_of_rated(cls) -> int:
        return cls.query.filter(cls.total_score != None).count()

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
            "id": self.id,
            "profile": profile,
            "esg_ratings": esg_ratings
        }
        return response
