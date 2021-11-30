
import os
import unittest
import json
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref


database_path = os.environ['DATABASE_URL_FIXED']

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    #db_drop_and_create_all()

"""
object creation process

1.
user
product

2. order
    user.id

3. order_item

    Order.id
    Product.id
    ItemQuantity int

"""

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    # create a dummy product, user, order, and order_item for development

    user = User(
        name = 'slippery sam'
    )
    
    user.insert()
    
    product = Product(
        name = "Rainforset t-shirt - black/green",
        description = "a Rainforest exclusive t-shirt",
        price = 10.99

    )
    product.insert()

    order = Order(
        user_id = 1
    )
    order.insert()

    order_item = OrderItem(
        order_id = 1,
        product_id = 1
    )
    order_item.insert()
#
# lol I found these. I thought this was part of sqlalchemy

"""
object creation process

1.
user
product

2. order
    user.id

3. order_item

    Order.id
    Product.id
    ItemQuantity int

"""

# User
"""
The class to carry the user's profile

attributes:

Orders (array of order ids ) [int]
"""

class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    #address = db.Column(db.String, nullable=False) #not needed
    #number = db.Column(db.String, nullable=False)  #not needed
    orders = db.relationship('Order', backref='user', lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


# Order
"""
The class that contains all the orderItems for a users transaction

attributes:

User.id int


"""
class Order(db.Model):
    __tablename__ ='Order'

    id = db.Column(db.Integer, primary_key=True)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

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
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

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

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()