from database import db


class Distribution(db.Model):
    """Model for ESG Percentiles"""

    __tablename__ = "distributions"

    name = db.Column(db.String(), primary_key=True)
    bottom = db.Column(db.Integer)
    top = db.Column(db.Integer)

    @classmethod
    def serialize(cls) -> dict:
        """Return a serialized object with top and bottom percentile divides for given type (E,S,G or T)"""
        e = cls.query.get("environmental")
        s = cls.query.get("social")
        g = cls.query.get("governance")
        t = cls.query.get("total")

        serialized = {
            "environmental": {
                "top": e.top,
                "bottom": e.bottom
            },
            "social": {
                "top": s.top,
                "bottom": s.bottom
            },
            "governance": {
                "top": g.top,
                "bottom": g.bottom
            },
            "total": {
                "top": t.top,
                "bottom": t.bottom
            }
        }

        return serialized
