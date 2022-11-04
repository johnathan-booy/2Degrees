from flask import Flask, render_template
from database import db, connect_db
from models.company import Company
from models.exchange import Exchange
from models.location import Location
from models.sector import Sector
from models.user import User
from models.users_companies import users_companies


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///2degrees'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "thisismysecret"

connect_db(app)


@app.route('/')
def homepage():
    """Show homepage"""
    return render_template("base.html")
