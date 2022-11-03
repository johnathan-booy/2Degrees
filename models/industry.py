from models import db


class Industry(db.Model):
    """Model for industries table"""
    __tablename__ = "industries"
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    name = db.Column(
        db.String(),
        nullable=False)
    sector_id = db.Column(
        db.Integer,
        db.ForeignKey("sectors.id"),
        nullable=False)
