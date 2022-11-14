from sqlalchemy import or_
from database import db
from models.region import Region
from models.country import Country


class City(db.Model):
    """Model for cities table"""

    __tablename__ = "cities"

    def __repr__(self) -> str:
        return f"<City  {self.name}>"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(),
        nullable=False
    )
    region_id = db.Column(
        db.Integer,
        db.ForeignKey("regions.id")
    )
    country_id = db.Column(
        db.Integer,
        db.ForeignKey("countries.id")
    )
    companies = db.relationship(
        "Company",
        backref="city",
        cascade="all, delete"
    )
    exchanges = db.relationship(
        "Exchange",
        backref="city",
        cascade="all, delete"
    )

    @classmethod
    def add(cls, city_name, region_name, country_name):
        """
        Constructor function for the city model

        Checks to avoid duplication

        Returns the city
        """

        region = Region.add(region_name, country_name)
        country = region.country

        city = (cls.query
                .filter(
                    cls.name == city_name,
                    or_(
                        cls.region_id == region.id,
                        cls.country_id == country.id))
                .first())

        if not city:
            city = cls(name=city_name)

        city.region_id = region.id
        city.country_id = country.id

        db.session.add(city)
        db.session.commit()

        return city

    @ classmethod
    def remove(cls, city_name, region_name, country_name):
        """
        Removes a city from the database by name

        Returns the city
        """
        country = Country.query.filter_by(name=country_name).one()

        region = Region.query.filter_by(
            name=region_name, country_id=country.id).one()

        city = cls.query.filter_by(
            name=city_name, region_id=region.id).one()

        db.session.delete(city)
        db.session.commit()

        return city
