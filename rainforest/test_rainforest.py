
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, User, OrderItem, Order, Product

#no auth in this file
#put auth in none test and the postman file,
# no the test uses methods from the mmain app code, it needs auth or just an admin auth
# no just one api
#get admin token from env file

#it should probably should run on a test api on the main api so the test auth cannot do anything even if leaked
class RainforestTestCase(unittest.TestCase):
    """This class represents the Rainforest test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "rainforest_test"
        self.database_path = "postgresql://student:student@{}/{}".format(
            'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            # store values for tests one of each User, Order, OrderItem, Product
            self.user = User(
                name='chris condo'                
            )
            self.product = Product(

            )

            self.order = Order(
                order_items=1,
                user_id=1
            )

    def tearDown(self):
        """Executed after reach test"""
        pass

    """

    Write at least one test for each test for successful operation and for expected errors.
    """

    """
    / product test
    """

