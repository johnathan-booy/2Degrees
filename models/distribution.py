from database import db


class Distribution(db.Model):
    """Model for ESG Percentiles"""

    __tablename__ = "distributions"

    name = db.Column(db.String(), primary_key=True)
    environmental_best = db.Column(db.Integer)
    environmental_worst = db.Column(db.Integer)
    social_best = db.Column(db.Integer)
    social_worst = db.Column(db.Integer)
    governance_best = db.Column(db.Integer)
    governance_worst = db.Column(db.Integer)
    total_best = db.Column(db.Integer)
    total_worst = db.Column(db.Integer)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self) -> str:
        return f"<Distribution {self.name}>"
