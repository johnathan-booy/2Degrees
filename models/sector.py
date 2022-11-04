from database import db


class Sector(db.Model):
    """Model for sectors table"""

    __tablename__ = "sectors"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(),
        nullable=False
    )
