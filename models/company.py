from urllib.parse import urlparse
from database import db
from models.esgt_list import ESGTList


class Company(ESGTList, db.Model):
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
    environmental_level = db.Column(
        db.String()
    )
    environmental_grade = db.Column(
        db.String()
    )
    social_level = db.Column(
        db.String()
    )
    social_grade = db.Column(
        db.String()
    )
    governance_level = db.Column(
        db.String()
    )
    governance_grade = db.Column(
        db.String()
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
