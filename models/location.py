from models import db


class Location(db.Model):
    """Model for locations table"""
    __tablename__ = "locations"
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    city = db.Column(
        db.String(),
        nullable=False)
    region = db.Column(
        db.String(),
        nullable=False)
    country = db.Column(
        db.String(),
        nullable=False)