from models import db


class City(db.Model):
    """Model for cities table"""
    __tablename__ = "cities"
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    name = db.Column(
        db.String(),
        nullable=False)
    region_id = db.Column(
        db.Integer,
        db.ForeignKey("regions.id"),
        nullable=False)
