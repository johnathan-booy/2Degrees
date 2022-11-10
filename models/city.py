from database import db


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
