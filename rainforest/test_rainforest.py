
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, User, OrderItem, Order, Product

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

    def tearDown(self):
        """Executed after reach test"""
        pass

    """

    Write at least one test for each test for successful operation and for expected errors.
    """

    """
    / product test
    """

