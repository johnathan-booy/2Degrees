from database import db


class Exchange(db.Model):
    """Model for exchanges table"""

    __tablename__ = "exchanges"

    def __repr__(self) -> str:
        return f"<Exchange  {self.symbol}  {self.location.country}>"

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
    companies = db.relationship(
        "Company",
        backref="exchange",
        cascade="all, delete"
    )
