from database import db
from models.country import Country


class Region(db.Model):
    """Model for regions table"""

    __tablename__ = "regions"

    def __repr__(self) -> str:
        return f"<Region  {self.name}>"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(),
        nullable=False
    )
    country_id = db.Column(
        db.Integer,
        db.ForeignKey("countries.id")
    )
    cities = db.relationship(
        "City",
        backref="region",
        cascade="all, delete"
    )
    companies = db.relationship(
        "Company",
        backref="region",
        cascade="all, delete"
    )
    exchanges = db.relationship(
        "Exchange",
        backref="region",
        cascade="all, delete"
    )

    @classmethod
    def add(cls, region_name, country_name):
        """
        Constructor function for the region model

        Checks to avoid duplication

        Returns the region
        """

        country = Country.add(country_name)

        region = cls.query.filter_by(
            name=region_name, country_id=country.id).first()

        if not region:
            region = cls(name=region_name, country_id=country.id)
            db.session.add(region)
            db.session.commit()

        return region

    @classmethod
    def remove(cls, region_name, country_name):
        """
        Removes a region from the database by name

        Returns the region
        """
        country = Country.query.filter_by(name=country_name).one()

        region = cls.query.filter_by(
            name=region_name, country_id=country.id).first()

        db.session.delete(region)
        db.session.commit()

        return region
