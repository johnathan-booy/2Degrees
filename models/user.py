from flask_bcrypt import Bcrypt
from database import db
from models.users_companies import users_companies

bcrypt = Bcrypt()


class User(db.Model):
    """Model for the users table"""

    __tablename__ = "users"

    def __repr__(self) -> str:
        return f"<User  {self.username}>"

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
        unique=True,
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
        secondary=users_companies,
        backref="users"
    )

    @classmethod
    def signup(cls, username, password, email, first_name=None, last_name=None):
        """Sign up user.

        Hashes password with bcrypt and creates a user
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = cls(
            username=username,
            password=hashed_pwd,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        if not user:
            return

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`. """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
