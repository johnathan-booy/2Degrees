from math import ceil
from flask import Flask, render_template, redirect, jsonify, request, abort, url_for
from functools import wraps
from sqlalchemy import func, within_group, select
from sqlalchemy.orm import Session
from database import db, connect_db
from news import News
from exceptions import APIError, APINotFoundError, APIInvalidError
from models.company import Company
from models.exchange import Exchange
from models.city import City
from models.region import Region
from models.country import Country
from models.sector import Sector
from models.user import User
from models.users_companies import users_companies
from models.distribution import Distribution


app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI='postgresql:///2degrees',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=False,
    DEBUG_TB_INTERCEPT_REDIRECTS=False,
    SECRET_KEY="thisismysecret"
)

connect_db(app)


def validate_list(f):
    @wraps(f)
    def wrapper(name, ranking, type):
        name = name.lower()
        ranking = ranking.lower()
        type = type.upper()
        sector_id = None
        country_id = None
        cls_ = None

        if name == "companies":
            cls_ = Company
            sector_id = request.args.get("sector_id")
            if not sector_id:
                country_id = request.args.get("country_id")
        elif name == "sectors":
            cls_ = Sector
        elif name == "countries":
            cls_ = Country
        else:
            abort(404)

        if ranking not in ["best", "worst"]:
            abort(404)

        if type not in "ESGT" or len(type) != 1:
            abort(404)

        return f(cls_, name, ranking, type, sector_id, country_id)
    return wrapper


@ app.route('/')
def homepage():
    """Show homepage"""
    return render_template("homepage.html")


@app.route("/<name>/<ranking>/<type>")
@validate_list
def list_objects(cls_, name, ranking, type, sector_id, country_id):
    """List the best or worst objects, ranked by ESGT scores."""

    count = 10
    page = int(request.args.get("page", 0))
    offset = page * count

    sector = (Sector.query.get_or_404(sector_id)
              if sector_id
              else None)
    country = (Country.query.get_or_404(country_id)
               if country_id
               else None)

    objects = cls_.ranked(ranking, type, sector_id, country_id, count, offset)

    distribution = Distribution.query.filter_by(name=name).first()
    print(distribution)

    page_count = ceil(cls_.num_of_rated(sector_id, country_id) / count)

    return render_template("list.html",
                           name=name,
                           sector=sector,
                           country=country,
                           objects=objects,
                           distribution=distribution,
                           ranking=ranking,
                           type=type,
                           page=page,
                           page_count=page_count,
                           offset=offset)


@app.route("/companies/<int:id>")
def company_details(id):
    company = Company.query.get_or_404(id)
    distribution = Distribution.query.filter_by(name='companies').first()
    articles = News.get_articles(company.symbol)
    return render_template("company.html",
                           company=company,
                           distribution=distribution,
                           articles=articles)


@app.route("/sectors/<int:id>")
def sector_details(id):
    sector = Sector.query.get_or_404(id)
    return redirect(f"/companies/best/t?sector_id={id}")


@app.route("/countries/<int:id>")
def country_details(id):
    country = Country.query.get_or_404(id)
    return redirect(f"/companies/best/t?sector_id={id}")


@ app.route('/api/companies/<symbol>', methods=['GET'])
def get_companies(symbol):
    """Get all companies with the provided symbol"""

    symbol = symbol.upper()
    companies = Company.query.filter_by(symbol=symbol).all()
    if not companies:
        raise APINotFoundError("Symbol not available")

    data = [c.serialize() for c in companies]
    return jsonify({"companies": data})


@ app.route('/api/companies/ranked/<ranking>/<type>', methods=['GET'])
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


@ app.route('/api/esg/ranges')
def get_esg_ranges():
    """Get the highest and lowest scores for each category (E, S, G and T)"""
    ranges = Company.esg_ranges()
    return jsonify({"ranges": ranges})


@ app.route('/api/esg/distributions/<name>')
def get_esg_distributions(name):
    """Get the top and bottom percentile divides for all types (E, S, G and T)"""
    distributions = Distribution.serialize(name)
    return jsonify({"distributions": distributions})


@ app.errorhandler(APIError)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    # Add some logging so that we can monitor different types of errors
    app.logger.error(f"{err.description}: {response['message']}")
    return jsonify(response), err.code


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
