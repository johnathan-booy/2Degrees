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
    logo_class = db.Column(
        db.String()
    )
    companies = db.relationship(
        "Company",
        backref="sector",
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
    def add(cls, name: str, logo_class: str):
        """
        Constructor function for the sector model

        Checks to avoid duplication

        Returns the sector
        """

        sector = cls.query.filter_by(name=name).first()

        if not sector:
            sector = cls(name=name)
            db.session.add(sector)

        sector.logo_class = logo_class

        db.session.commit()

        return sector
