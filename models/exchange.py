from database import db
from models.city import City


class Exchange(db.Model):
    """Model for exchanges table"""

    __tablename__ = "exchanges"

    def __repr__(self) -> str:
        return f"<Exchange  {self.symbol}>"

    symbol = db.Column(
        db.String(),
        primary_key=True
    )
    name = db.Column(
        db.String()
    )
    city_id = db.Column(
        db.Integer,
        db.ForeignKey("cities.id")
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
        backref="exchange",
        cascade="all, delete"
    )

    @classmethod
    def add(cls, symbol: str, name: str, city=None):
        """
        Constructor function for the exchange model

        Checks to avoid duplication

        Returns the exchange
        """

        exchange = cls.query.filter_by(symbol=symbol).first()

        if not exchange:
            exchange = cls(symbol=symbol)

        exchange.name = name

        if city:
            exchange.city = city
            exchange.region_id = city.region_id
            exchange.country_id = city.country_id

        db.session.add(exchange)
        db.session.commit()

        return city

    @classmethod
    def remove(cls, symbol):
        """
        Removes an exchange from the database by symbol

        Returns the exchange
        """
        exchange = cls.query.filter_by(symbol=symbol).one()

        db.session.delete(exchange)
        db.session.commit()

        return exchange
