
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

        self.owner_token = os.environ['OWNER_TOKEN']
        self.staff_token = os.environ['STAFF_TOKEN']
        
        
        models.setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            # store values for tests one of each User, Order, OrderItem, Product
            self.user = models.User(
                name= "chris condo"                
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

    def test_404_product_page_not_found(self):
        res = self.client().get("/products?page=1000")
        data = json.loads(res.data)        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_product_by_id(self):

        self.product.insert()

        product_id = self.product.id
        res = self.client().get('/products/'+ str(product_id))

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['product']['id'], product_id)



    def test_404_product_not_found_error(self):
        res = self.client().get("/products/9001")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    
    def test_create_products(self):
               
        res = self.client().post('/products', headers={
            'Authorization': "Bearer {}".format(self.owner_token)},
            json=self.product.format())

        data = json.loads(res.data)        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['created'], True)
        self.assertTrue(data['products'], True)
        self.assertTrue(data['total_products'], True)
        
    #invalid product attributes fail

    def test_422_create_products_fail(self):
        
        res = self.client().post('/products', headers={
            'Authorization': "Bearer {}".format(self.owner_token)},
            json={'name': self.product.name, 'description': self.product.description})

        data = json.loads(res.data)       
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "unprocessable")        

    #
    #invalid auth permission product create fail
    #
    def test_create_product_invalid_auth_error(self):        
        # the user with the staff role cannot create a new product
        res = self.client().post('/products', headers={
            'Authorization': "Bearer {}".format(self.staff_token)},
            json=self.product.format())

        data = json.loads(res.data)   
                  
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'], 'permission not found')
        self.assertEqual(data['message']['code'], 'unauthorized')
        

    def test_delete_product(self):

        sample_product = models.Product(name='skittles', description='bag of sweet candy', price=3.99)
        sample_product.insert()

        sample_id = sample_product.id

        res = self.client().delete(f'/products/{sample_id}',headers={
            'Authorization': "Bearer {}".format(self.owner_token)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertEqual(data['deleted'], sample_id)
        self.assertTrue(sample_product, None)


    def test_delete_product_out_of_bounds(self):                

        res = self.client().delete(f'/products/1080',headers={
            'Authorization': "Bearer {}".format(self.owner_token)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    
    def test_delete_product_auth_error(self):
        sample_product = models.Product(name='mars bar', description='a chocolate bar', price=2.99)
        sample_product.insert()

        sample_id = sample_product.id

        res = self.client().delete(f'/products/{sample_id}',headers={
            'Authorization': "Bearer {}".format(self.staff_token)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'], 'permission not found')
        self.assertEqual(data['message']['code'], 'unauthorized')
        self.assertTrue(sample_product, True)


    def test_patch_product(self):
        sample_product = models.Product(name='snickers bar', description='a chocolate bar', price=2.99)
        sample_product.insert()

        product_id = sample_product.id

        new_name = 'hersheys bar'
        new_description = "A creamy milk chocolate bar"
        new_price = 1.10

        res = self.client().patch(f'/products/{product_id}',headers={
            'Authorization': "Bearer {}".format(self.owner_token)}, json={
                'name': new_name, 'description': new_description, 'price': new_price
            })

        data = json.loads(res.data)        

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['product_name'], new_name)
        self.assertEqual(data['product_description'], new_description)
        self.assertEqual(data['product_price'], new_price)

    def test_422_patch_product_invailid_failure(self):
        sample_product = models.Product(name='snickers bar', description='a chocolate bar', price=2.99)
        sample_product.insert()

        product_id = sample_product.id

        new_name = 'hersheys bar'
        new_description = "A creamy milk chocolate bar"
        #wrong value type
        new_price = '1.10' 

        res = self.client().patch(f'/products/{product_id}',headers={
            'Authorization': "Bearer {}".format(self.owner_token)}, json={
                'name': new_name, 'description': new_description, 'price': new_price
            })

        data = json.loads(res.data)    
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

#--------------------------------------------------
# Users
#--------------------------------------------------

    def test_get_users(self):
        res = self.client().get('/users', headers={
            'Authorization': "Bearer {}".format(self.staff_token)}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['users'], True)
        self.assertTrue(data['total_users'], True)

    def test_page_of_users_out_of_bounds_error(self):
        res = self.client().get('/users?page=987654321', headers={
            'Authorization': "Bearer {}".format(self.staff_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    
    def test_get_users_no_permission_failure(self):
        #shows that the permission 'get:users' is needed to access user data
        res = self.client().get('/users')
        data = json.loads(res.data)        
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'], 'Authorization header is expected.')
        self.assertEqual(data['message']['code'], 'authorization_header_missing')

    def test_get_user_by_id(self):
                
        self.user.insert()
        new_user_id = self.user.id

        res = self.client().get('/users/' + str(new_user_id), headers={
            'Authorization': "Bearer {}".format(self.staff_token)}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['user']['id'], new_user_id)

    def test_get_user_by_id_out_of_bounds_failure(self):
        res = self.client().get('/users?page=' + str(500000), headers={
            'Authorization': "Bearer {}".format(self.staff_token)}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_create_user(self):

        new_username = 'false_bell'
        res = self.client().post('/users', headers={
            'Authorization': "Bearer {}".format(self.staff_token)}, json={'name': new_username } )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'], True)
        self.assertEqual(data['user']['name'], new_username)

    def test_create_user_failure(self):
        new_username = None
        res = self.client().post('/users', headers={
            'Authorization': "Bearer {}".format(self.staff_token)}, json={'name': new_username } )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_user(self):

        self.user.insert()
        new_user_id = self.user.id

        res = self.client().delete('/users/' + str(new_user_id),
         headers={
            'Authorization': "Bearer {}".format(self.staff_token)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], new_user_id)

    def test_delete_user_422_failure(self):

        res = self.client().delete('/users/' + str(700000),
         headers={
            'Authorization': "Bearer {}".format(self.staff_token)})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_delete_user_no_auth_failure(self):
        self.user.insert()
        new_user_id = self.user.id

        res = self.client().delete('/users/' + str(new_user_id))
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'], 'Authorization header is expected.')
        self.assertEqual(data['message']['code'], 'authorization_header_missing')

#----------------------------------------------------------------------------#
# Orders
#----------------------------------------------------------------------------#

    def test_get_orders(self):
        res = self.client().get('/orders', headers={
            'Authorization': "Bearer {}".format(self.staff_token)
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['orders'], True)
        self.assertTrue(data['total_orders'], True)

    def test_get_orders_out_of_bounds_fail(self):
        res = self.client().get('/orders?page='+ str(9001), headers={
            'Authorization': "Bearer {}".format(self.staff_token)
            })

        data = json.loads(res.data)        
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_order_by_id(self):
        self.order.insert()

        order_id = self.order.id

        res = self.client().get('/orders/'+ str(order_id), headers={
            'Authorization': "Bearer {}".format(self.staff_token)
            })
        
        data = json.loads(res.data)        

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['order']['id'], order_id)

    def test_get_order_by_id_fail(self):
        res = self.client().get('/orders/'+ str(98077), headers={
            'Authorization': "Bearer {}".format(self.staff_token)
            })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_order(self):
        #create dummy user
        self.user.insert()
        dummy_user_id = self.user.id

        res = self.client().post('/orders', headers={
            'Authorization': "Bearer {}".format(self.staff_token)
            }, json={
                'user_id': dummy_user_id
            })
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'], True)
        self.assertTrue(data['order'], True)

    def test_create_order_failure(self):
        bad_user_id = ":>"

        res = self.client().post('/orders', headers={
            'Authorization': "Bearer {}".format(self.staff_token)
            }, json={
                'user_id': bad_user_id
            })

        data = json.loads(res.data)        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_order(self):
        self.user.insert()
        dummy_user_id = self.user.id
        dummy_order = models.Order(user_id=dummy_user_id)
        dummy_order.insert()
        dummy_order_id = dummy_order.id

        res = self.client().delete('/orders/' + str(dummy_order_id), headers={
            'Authorization': "Bearer {}".format(self.staff_token)
            })

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], dummy_order_id)

    def test_delete_order_failure(self):
        res = self.client().delete('/orders/' + str(9999999999), headers={
            'Authorization': "Bearer {}".format(self.staff_token)
            })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")
#----------------------------------------------------------------------------#
# OrderItems
#----------------------------------------------------------------------------#    


# Make the tests conveniently executable
# I forgot to use this
if __name__ == "__main__":
    unittest.main() 