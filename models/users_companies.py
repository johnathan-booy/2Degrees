from database import db

users_companies = db.Table(
    "users_companies",
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'company_symbol',
        db.Integer,
        db.ForeignKey('companies.id'),
        primary_key=True
    )
)
