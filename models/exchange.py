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
    location_id = db.Column(
        db.Integer,
        db.ForeignKey("locations.id")
    )
    companies = db.relationship(
        "Company",
        backref="exchange",
        cascade="all, delete"
    )
