from flask import Flask, render_template, redirect, jsonify, request
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
    return redirect('/companies/best/e')


@app.route("/companies/<ranking>/<type>")
def list_top_companies(ranking, type):
    """List the best or worst companies, ranked by ESG or Total scores."""

    type = type.upper()
    ranking = ranking.lower()

    if ranking not in ["best", "worst"]:
        return redirect("/companies/best/e")

    if type not in "ESGT" or len(type) != 1:
        return redirect("/companies/best/e")

    companies = Company.ranked(type, count=20, offset=0, ranking=ranking)
    return render_template("ranked.html", companies=companies, ranking=ranking, type=type)


@ app.route('/api/companies/<symbol>', methods=['GET'])
def get_companies(symbol):
    """Get all companies with the provided symbol"""

    symbol = symbol.upper()
    companies = Company.query.filter_by(symbol=symbol).all()
    if not companies:
        raise APINotFoundError("Symbol not available")

    data = [c.serialize() for c in companies]
    return jsonify({"companies": data})


@app.route('/api/companies/ranked/<ranking>/<type>', methods=['GET'])
def get_best_companies(ranking, type):
    """Get the best companies based on Environmental, Social, Governance or Total scores"""

    ranking = ranking.lower()
    type = type.upper()
    count = request.args.get("count", 10, type=int)
    offset = request.args.get("offset", 0, type=int)

    if ranking not in ["best", "worst"]:
        raise APIInvalidError("Ranking must be 'best' or 'worst'")

    if type not in "ESGT" or len(type) != 1:
        raise APIInvalidError("Type must be one of E, S, G, or T")

    if count not in range(1, 21):
        raise APIInvalidError("Count must be between 1 and 20 (inclusive)")

    if offset < 0:
        raise APINotFoundError("Offset cannot be less than 0")

    companies = Company.ranked(type, count, offset, ranking)

    if not companies:
        raise APINotFoundError(
            "No companies found. Perhaps the offset is too high.")

    data = [company.serialize() for company in companies]

    return jsonify({"companies": data})


@app.route('/api/esg/ranges')
def get_esg_ranges():
    """Get the highest and lowest scores for each category (E, S, G and T)"""
    ranges = Company.esg_ranges()
    return jsonify({"ranges": ranges})


@app.errorhandler(APIError)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    # Add some logging so that we can monitor different types of errors
    app.logger.error(f"{err.description}: {response['message']}")
    return jsonify(response), err.code
