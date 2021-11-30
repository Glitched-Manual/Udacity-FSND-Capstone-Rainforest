import os ,sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from database.models import db_drop_and_create_all, setup_db, User, Order, OrderItem, Product
from auth.auth import AuthError, requires_auth


Results_PER_PAGE = 10

# to paginate user and product data
def paginate_data(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * Results_PER_PAGE
    end = start + Results_PER_PAGE

    data_selction = [data.format() for data in selection]
    selected_data = data_selction[start:end]

    return selected_data



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  #setup_db only needs to be call here locally, because mange.py does not work locally
  setup_db(app)
  CORS(app)

  return app
 
APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)


###########################################################################################
"""

Endpoints


"""
###########################################################################################


@APP.route('/')
def welcome_to_root():
    return "Welcome to Rainforest! :>"

# get products

@APP.route('/products')
def get_products():

    all_products = Product.query.order_by(Product.id).all()
    total_products = len(all_products)

    if total_products <= 0:
        abort(404)

    selected_products = paginate_data(request, all_products)

    return ':>'


@APP.errorhandler(404)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404
'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@APP.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@APP.errorhandler(401)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "resource not found"
                    }), 401


@APP.errorhandler(AuthError)
def handle_auth_error(ex):
    return jsonify({
                    "success": False,
                    "error": ex.status_code,
                    "message": ex.error
                    }), ex.status_code
