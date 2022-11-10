from database import db


class Country(db.Model):
    """Model for countries table"""

    __tablename__ = "countries"

    def __repr__(self) -> str:
        return f"<Country  {self.name}>"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(),
        nullable=False
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
