from database import db
from models.esgt_list import ESGTList


class Sector(db.Model, ESGTList):
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
    logo_class = db.Column(
        db.String()
    )
    companies = db.relationship(
        "Company",
        backref="sector",
        cascade="all, delete"
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
