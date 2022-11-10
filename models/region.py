from database import db


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
