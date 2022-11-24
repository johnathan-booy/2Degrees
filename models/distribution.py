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

    @classmethod
    def serialize(cls, name) -> dict:
        """Return a serialized object with top and bottom percentile divides for given type (E,S,G or T)"""
        d = cls.query.filter_by(name=name).first()

        serialized = {
            "environmental": {
                "best": d.environmental_best,
                "worst": d.environmental_worst
            },
            "social": {
                "best": d.social_best,
                "worst": d.social_worst
            },
            "governance": {
                "best": d.governance_best,
                "worst": d.governance_worst
            },
            "total": {
                "best": d.total_best,
                "worst": d.total_worst
            }
        }
        return serialized

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self) -> str:
        return f"<Distribution {self.name}>"
