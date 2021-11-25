
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

# User
"""
The class to carry the user's profile

attributes:

Orders (array of odred ids ) [int]
"""

# Order
"""
The class that contains all the orderItems for a users transaction

attributes:

User.id int
orderItems [int]

"""

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