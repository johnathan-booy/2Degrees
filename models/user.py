from database import db
from models.users_companies import users_companies


class User(db.Model):
    """Model for the users table"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    username = db.Column(
        db.String(),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(),
        nullable=False
    )
    email = db.Column(
        db.String(),
        nullable=False
    )
    first_name = db.Column(
        db.String()
    )
    last_name = db.Column(
        db.String()
    )
    companies = db.relationship(
        "Company",
        secondary=users_companies
    )
