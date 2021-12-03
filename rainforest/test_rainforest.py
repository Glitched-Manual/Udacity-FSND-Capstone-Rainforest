
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


import sys
#print(sys.executable)
#print(sys.modules)
from app import create_app
from database import models

# I need to use pytest or stick with unittest which ever works
#pytest supports tokens. no the token method has nothing to do with pytest
# ** The rubric calls for using unittest
"""
Includes at least one test for expected success and error behavior for each endpoint using the unittest library
Includes tests demonstrating role-based access control, at least two per role.

Roles:

Staff, Owner

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
        self.database_name = "rainforest_db"
        self.database_path = "postgresql://student:student@{}/{}".format(
            'localhost:5432', self.database_name)
         
        self.staff_token = os.environ['STAFF_TOKEN']
        self.owner_token = os.environ['OWNER_TOKEN']
        
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
                name = "Test Nova TX7",
                description = "The bleedind edge of Tesla Hydro car innovation",
                price = 1780000.99
            )

            self.order = models.Order(
                user_id=1
            )

    def tearDown(self):
        """Executed after reach test"""
        pass

    """

    Write at least one test for each test for successful operation and for expected errors.
    """

    """
     product test
    """

    def test_get_products(self):
        
        res = self.client().get('/products')
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['products'], True)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/products/9001")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    
    def test_create_products(self):

        """res = self.client().post('/products', headers={
            'Authorization': "Bearer {}".format(self.owner_token)},
            json={'name': self.product.name, 'description': self.product.description,'price': self.product.price})"""
       
        res = self.client().post('/products', headers={
            'Authorization': "Bearer {}".format(self.owner_token)},
            json=self.product.format())

        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created', True])
        self.assertTrue(data['products', True])
        self.assertTrue(data['total_products', True])
        

    #--------------------------------------------------
    # Users
    #--------------------------------------------------

# Make the tests conveniently executable
# I forgot to use this
if __name__ == "__main__":
    unittest.main()