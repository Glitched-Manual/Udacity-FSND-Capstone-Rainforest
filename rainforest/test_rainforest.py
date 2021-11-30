
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


import sys
#print(sys.executable)
#print(sys.modules)
from app import create_app, setup_db
from database import models

# I need to use pytest or stick with unittest which ever works
#pytest supports tokens. no the token method has nothing to do with pytest
# ** The rubric calls for using unittest
"""
Includes at least one test for expected success and error behavior for each endpoint using the unittest library
Includes tests demonstrating role-based access control, at least two per role.

Roles:

Clerk, Manager

"""



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

        models.setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            # store values for tests one of each User, Order, OrderItem, Product
            self.user = models.User(
                name='chris condo'                
            )
            self.product = models.Product(

            )

            self.order = models.Order(
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

    def test_get_products(self):
        res = self.client().get('/products')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['products'], True)



# Make the tests conveniently executable
# I forgot to use this
if __name__ == "__main__":
    unittest.main()