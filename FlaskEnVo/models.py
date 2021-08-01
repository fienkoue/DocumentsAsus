from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_required,login_user,current_user,logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class CarsModel(db.Model):
    __tablename__="cars"

    id=db.Column(db.Integer,primary_key=True)
    brand=db.Column(db.String(50))
    model=db.Column(db.String(50))
    prices=db.Column(db.Integer)
    year=db.Column(db.String(50))
    fuel=db.Column(db.String(50))
    kms=db.Column(db.Integer)

    def __init__(self,brand,model,prices,year,fuel,kms):
        self.brand=brand
        self.model=model
        self.prices=prices
        self.year=year
        self.fuel=fuel
        self.kms=kms

    def __repr__(self):
        return f"{self.brand}:{self.model}:{self.prices}"

# Create User Model which contains id [Auto Generated], name, username, email and password

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password) 

