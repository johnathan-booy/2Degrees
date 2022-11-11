from flask import Flask, render_template, jsonify, request
from database import db, connect_db
from exceptions import APIError, APINotFoundError, APIInvalidError
from models.company import Company
from models.exchange import Exchange
from models.city import City
from models.region import Region
from models.country import Country
from models.sector import Sector
from models.user import User
from models.users_companies import users_companies


app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI='postgresql:///2degrees',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=False,
    DEBUG_TB_INTERCEPT_REDIRECTS=False,
    SECRET_KEY="thisismysecret"
)

connect_db(app)


@ app.route('/')
def homepage():
    """Show homepage"""
    return render_template("base.html")


@ app.route('/api/companies', methods=['GET'])
def get_companies():
    """Get information about companies from given symbols"""

    q = request.args.get("q", default="", type=str)
    q = q.replace(" ", "")

    if q == "":
        raise APIInvalidError("No symbol provided")

    symbols = q.split(",")

    data = []
    for symbol in symbols:
        symbol = symbol.upper()
        company = Company.query.get(symbol)
        if not company:
            continue
        data.append(company.serialize())

    if not data:
        raise APINotFoundError("Symbol not available")

    return jsonify(data)


@app.route('/api/esg/top')
@app.errorhandler(APIError)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    # Add some logging so that we can monitor different types of errors
    app.logger.error(f"{err.description}: {response['message']}")
    return jsonify(response), err.code
