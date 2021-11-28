
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import backref


database_path = os.environ['DATABASE_URL_FIXED']

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #db.create_all()



def db_drop_and_create_all():
    db.drop_all()
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
    #address = db.Column(db.String, nullable=False) #not needed
    #number = db.Column(db.String, nullable=False)  #not needed
    orders = db.relationship('Order', backref='user', lazy=True)


# Order
"""
The class that contains all the orderItems for a users transaction

attributes:

User.id int
orderItems [int] not needed just check where the customer id exists in the orders

"""
class Order(db.Model):
    __tablename__ ='Order'

    id = db.Column(db.Integer, primary_key=True)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)


# Product
"""
the class for ever item that is for sale

attributes:

- name
- description
- price

"""
class Product(db.Model):
    __tablename__='Product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=True)

# OrderItem
"""
An Item within the order with a quantity (delete if quatity is zero)
 2 x foriegn keys
attributes:
Order.id
Product.id
ItemQuantity int
"""
class OrderItem(db.Model):
    __tablename__='OrderItem'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'), nullable=False)

