from models import db


class Region(db.Model):
    """Model for regions table"""
    __tablename__ = "regions"
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    name = db.Column(
        db.String(),
        nullable=False)
    country_id = db.Column(
        db.Integer,
        db.ForeignKey("countries.id"),
        nullable=False)
