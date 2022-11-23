from database import db


class Country(db.Model):
    """Model for countries table"""

    __tablename__ = "countries"

    def __repr__(self) -> str:
        return f"<Country  {self.name}>"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(),
        nullable=False
    )
    environmental_score = db.Column(
        db.Integer
    )
    social_score = db.Column(
        db.Integer
    )
    governance_score = db.Column(
        db.Integer
    )
    total_score = db.Column(
        db.Integer
    )
    cities = db.relationship(
        "City",
        backref="country",
        cascade="all, delete"
    )
    regions = db.relationship(
        "Region",
        backref="country",
        cascade="all, delete"
    )
    companies = db.relationship(
        "Company",
        backref="country",
        cascade="all, delete"
    )
    exchanges = db.relationship(
        "Exchange",
        backref="country",
        cascade="all, delete"
    )

    @classmethod
    def ranked(cls, type: str, ranking: str) -> list:
        """Return sectors ranked best or worst based on ESGT ratings"""

        if ranking != "worst" and ranking != "best":
            return

        q1 = None
        q2 = cls.total_score

        match type:
            case "E":
                q1 = cls.environmental_score
            case "S":
                q1 = cls.social_score
            case "G":
                q1 = cls.governance_score
            case "T":
                q1 = cls.total_score
                q2 = cls.environmental_score

        return (
            cls.query
            .filter(q1 != None)
            .order_by(
                q1.desc() if ranking == "best" else q1,
                q2.desc() if ranking == "best" else q2)
            .all()
        )

    @classmethod
    def add(cls, name):
        """
        Constructor function for the country model

        Checks to avoid duplication

        Returns the country
        """

        country = cls.query.filter_by(name=name).first()

        if country:
            return country

        country = cls(name=name)
        db.session.add(country)
        db.session.commit()

        return country

    @classmethod
    def remove(cls, name):
        """
        Removes a country from the database by name

        Returns the country
        """

        country = cls.query.filter_by(name=name).one()
        db.session.delete(country)
        db.session.commit()

        return country
