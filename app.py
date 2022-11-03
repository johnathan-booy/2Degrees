from flask import Flask, render_template
from models import db, connect_db, User, Company, Exchange, City, Region, Country, Industry

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "thisismysecret"

connect_db(app)


@app.route('/')
def homepage():
    """Show homepage"""
    return render_template("base.html")
