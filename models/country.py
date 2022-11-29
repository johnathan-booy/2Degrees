from database import db
from models.esgt_list import ESGTList


class Country(ESGTList, db.Model):
    """Model for countries table"""

    __tablename__ = "countries"

    def __repr__(self) -> str:
        return f"<Country {self.name}>"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(),
        nullable=False
    )
    code = db.Column(
        db.String()
    )
    cities = db.relationship(
        "City",
        backref="country",
        cascade="all, delete"
    )
    regions = db.relationship(
        "Region",
        backref="country",
        cascade="all, delete"
    )
    companies = db.relationship(
        "Company",
        backref="country",
        cascade="all, delete"
    )
    exchanges = db.relationship(
        "Exchange",
        backref="country",
        cascade="all, delete"
    )

    @classmethod
    def add(cls, name):
        """
        Constructor function for the country model

        Checks to avoid duplication

        Returns the country
        """

        country = cls.query.filter_by(name=name).first()

        if country:
            return country

        country = cls(name=name)
        db.session.add(country)
        db.session.commit()

        return country

    @classmethod
    def remove(cls, name):
        """
        Removes a country from the database by name

        Returns the country
        """

        country = cls.query.filter_by(name=name).one()
        db.session.delete(country)
        db.session.commit()

        return country
