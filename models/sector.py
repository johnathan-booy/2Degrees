from database import db


class Sector(db.Model):
    """Model for sectors table"""

    __tablename__ = "sectors"

    def __repr__(self) -> str:
        return f"<Sector {self.name}>"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(),
        nullable=False
    )
    companies = db.relationship(
        "Company",
        backref="sector",
        cascade="all, delete"
    )
