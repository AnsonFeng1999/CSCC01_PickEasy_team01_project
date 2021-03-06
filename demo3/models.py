# from exts import db
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_sqlalchemy import SQLAlchemy


# user_coupon = db.Table(
#     "user_coupon",
#     db.Column("user_id", db.Integer, db.ForeignKey("user_profile.id"), primary_key=True),
#     db.Column("coupon_id", db.Integer, db.ForeignKey("coupon_info.id"), primary_key=True)
# )

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
if config.STATUS == "TEST":
    # for creating test
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db = SQLAlchemy(app)
else:
    from exts import db


class User(db.Model):
    __tablename__ = "user"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    type = db.Column(db.Integer)

class Coupon(db.Model):
    __tablename__ = "coupons"
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rid = db.Column(db.Integer)
    deleted = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    expiration = db.Column(db.Date, nullable=True)
    begin = db.Column(db.Date, nullable=True)

class Restaurant(db.Model):
    __tablename__ = "restaurant"
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=True)
    uid = db.Column(db.Integer)

class Points(db.Model):
    __tablename__ = "points"
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer)
    rid = db.Column(db.Integer)
    points = db.Column(db.Integer)

class Experience(db.Model):
    __tablename__ = "experience"
    uid = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, primary_key=True)
    experience = db.Column(db.Integer)

class Employee(db.Model):
    __tablename__ = "employee"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rid = db.Column(db.Integer)

class Redeemed_Coupons(db.Model):
    __tablename__ = "redeemed_coupons"
    rcid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cid = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.Integer, nullable=False)
    rid = db.Column(db.Integer, nullable=False)
    valid = db.Column(db.Integer, nullable=False)

class Customer_Achievement_Progress(db.Model):
    __tablename__ = "customer_achievement_progress"
    aid = db.Column(db.Integer, nullable=False, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, primary_key=True)
    progress = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    update = db.Column(db.DateTime, nullable=True)

class Achievements(db.Model):
    __tablename__ = "achievements"
    aid = db.Column(db.Integer, nullable=False, primary_key=True)
    rid = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String(2048), nullable=False)

class Thresholds(db.Model):
    __tablename__ = "thresholds"
    rid = db.Column(db.Integer, primary_key=True, nullable=False)
    level = db.Column(db.Integer, primary_key=True, nullable=False)
    reward = db.Column(db.Integer, nullable=False)

class Favourite(db.Model):
    __tablename__ = "favourite"
    uid = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, primary_key=True)
