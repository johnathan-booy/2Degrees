from math import ceil
from flask import Flask, render_template, redirect, jsonify, request, abort, url_for, flash, session, g
from functools import wraps
from sqlalchemy import func, within_group, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
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
from forms import SignUpForm, LoginForm

CURR_USER_KEY = "curr_user"
URL_KEY = "url"

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
        user_id = None
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
        elif name == "mylist":
            cls_ = Company
            if not g.user:
                flash("Please login first!", "danger")
                return redirect(url_for('.login'))
            user_id = g.user.id
        else:
            abort(404)

        if ranking not in ["best", "worst"]:
            abort(404)

        if type not in "ESGT" or len(type) != 1:
            abort(404)

        return f(cls_, name, ranking, type, user_id, sector_id, country_id)
    return wrapper


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@ app.route('/')
def homepage():
    """Show homepage"""
    session[URL_KEY] = request.full_path
    return render_template("homepage.html")


def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@ app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup"""
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            db.session.add(user)
            db.session.commit()

            name = user.first_name
            if not name:
                name = user.username
            flash(f"Welcome to 2Degrees, {name}!", "success")

            do_login(user)

            return redirect(url_for("homepage"))
        except IntegrityError as e:
            error = e.orig.args[0]
            if "users_username_key" in error:
                flash(
                    f"Username '{form.username.data}' already exists.", "danger")
            if "users_email_key" in error:
                flash(
                    f"Email '{form.email.data}' has already been registered.", "danger")

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login"""
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            name = user.first_name
            if not name:
                name = user.username
            flash(f"Welcome {name}!", "success")
            return redirect("/")

        flash("Invalid username or password.")

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You've been logged out. See you again!", "success")
    return redirect(url_for("homepage"))


@app.route('/mylist/add/<int:id>', methods=['POST'])
def add_mylist(id):
    """Add a company to the currently-logged-in users' list."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect(session.get('url', '/'))

    company = Company.query.get_or_404(id)

    g.user.companies.append(company)
    db.session.commit()

    flash(f"You have added '{company.name}' to your list.", "success")
    return redirect(session.get(URL_KEY, "/"))


@app.route('/mylist/remove/<int:id>', methods=['POST'])
def remove_mylist(id):
    """Remove a company from the currently-logged-in users' list."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect(session.get('url', '/'))

    company = Company.query.get_or_404(id)

    g.user.companies.remove(company)
    db.session.commit()

    flash(f"You have removed '{company.name}' from your list.", "danger")
    return redirect(session.get(URL_KEY, "/"))


def list_title(name, sector, country):
    if name == "companies":
        return "Companies"
    elif name == "mylist":
        return "My List"
    elif name == "sectors":
        return sector.name
    elif name == "countries":
        return country.name


@app.route("/<name>/<ranking>/<type>")
@validate_list
def list_objects(cls_, name, ranking, type, user_id, sector_id, country_id):
    """List the best or worst objects, ranked by ESGT scores."""
    session[URL_KEY] = request.full_path
    count = 10
    page = int(request.args.get("page", 0))
    offset = page * count

    sector = (Sector.query.get_or_404(sector_id)
              if sector_id
              else None)
    country = (Country.query.get_or_404(country_id)
               if country_id
               else None)

    objects = cls_.ranked(ranking, type, user_id,
                          sector_id, country_id, count, offset)

    distribution = Distribution.query.filter_by(name="companies").first(
    ) if name == "mylist" else Distribution.query.filter_by(name=name).first()

    page_count = ceil(cls_.num_of_rated(
        user_id, sector_id, country_id) / count)

    return render_template("list.html",
                           name=name,
                           user_id=user_id,
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
    session[URL_KEY] = request.full_path
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
