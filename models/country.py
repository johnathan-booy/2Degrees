from models import db


class Country(db.Model):
    """Model for countries table"""
    __tablename__ = "countries"
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    name = db.Column(
        db.String(),
        nullable=False)
