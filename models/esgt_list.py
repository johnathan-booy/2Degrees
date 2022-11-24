from urllib.parse import urlparse
from database import db


class ESGTList(object):
    """Contains methods for creating ranked and paginated lists with ESGT scores"""

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

    @classmethod
    def ranked(cls, type: str, count: int, offset: int, ranking: str) -> list:
        """Return objects ranked best or worst based on ESGT ratings"""

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

        objects = (
            cls.query
            .filter(q1 != None)
            .order_by(
                q1.desc() if ranking == "best" else q1,
                q2.desc() if ranking == "best" else q2)
            .limit(count)
            .offset(offset)
            .all()
        )

        return objects

    @classmethod
    def num_of_rated(cls) -> int:
        return cls.query.filter(cls.total_score != None).count()
