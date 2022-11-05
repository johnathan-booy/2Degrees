from database import db


class Location(db.Model):
    """Model for locations table"""

    __tablename__ = "locations"

    def __repr__(self) -> str:
        return f"<Location  {self.city}, {self.region}, {self.country}>"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    city = db.Column(
        db.String(),
        nullable=False
    )
    region = db.Column(
        db.String(),
        nullable=False
    )
    country = db.Column(
        db.String(),
        nullable=False
    )
    companies = db.relationship(
        "Company",
        backref="location",
        cascade="all, delete"
    )
    exchanges = db.relationship(
        "Exchange",
        backref="location",
        cascade="all, delete"
    )
