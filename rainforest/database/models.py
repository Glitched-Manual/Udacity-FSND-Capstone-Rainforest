
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import backref


database_path = os.environ['DATABASE_URL_FIXED']

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

# User
"""
The class to carry the user's profile

attributes:

Orders (array of odred ids ) [int]
"""

class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    number = db.Column(db.String, nullable=False)
    orders = db.Column(db.Array(db.relationship('Order', backref='user', lazy=True)))


# Order
"""
The class that contains all the orderItems for a users transaction

attributes:

User.id int
orderItems [int]

"""
class Order(db.Model):
    __tablename__ ='Order'

    id = db.Column(db.Integer, primary_key=True)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    user_id = db.Column(db.Integer, db.Foriegn_key('User.id'), nullable=False)

# OrderItem
"""
An Item within the order with a quantity (delete if quatity is zero)

attributes:
Order.id
Product.id
ItemQuantity int
"""


# Product
"""
the class for ever item that is for sale

attributes:

- name
- description
- price

"""