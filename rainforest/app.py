import os ,sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin


if __name__ == 'rainforest.app':    
    from .database.models import db_drop_and_create_all, setup_db, User, Order, OrderItem, Product
    from .auth.auth import AuthError, requires_auth
    #print("__name__ == 'rainforest.app'")
elif  __name__ == 'app':
    try:
        #print("xxxxxxxx __name__ :" + __name__)
        from database.models import db_drop_and_create_all, setup_db, User, Order, OrderItem, Product
        from auth.auth import AuthError, requires_auth
        #print("__name__ != 'rainforest.app'")

    except:
        pass


Results_PER_PAGE = 10

# to paginate user and product data
def paginate_data(request, selection):
    page = request.args.get("page", 1, type=int)
    print(" page # " + str(page))
    start = (page - 1) * Results_PER_PAGE
    end = start + Results_PER_PAGE

    data_selection = [data.format() for data in selection]
    selected_data = data_selection[start:end]

    return selected_data

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    #setup_db only needs to be call here locally, because mange.py does not work locally
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS"
        )
        return response 
 
#APP = create_app()

#if __name__ == '__main__':
#    APP.run(host='0.0.0.0', port=8080, debug=True)

#elif __name__ == 'app':
#    app.run(host='0.0.0.0', port=8080, debug=True)


#----------------------------------------------------------------------------#
# #Endpoints
#----------------------------------------------------------------------------#


    @app.route('/')
    def welcome_to_root():
        return "Welcome to Rainforest! :>"

    # get products

    @app.route('/products')
    def get_products():

        all_products = Product.query.order_by(Product.id).all()
        total_products = len(all_products)

        if total_products <= 0:
            abort(404)

        selected_products = paginate_data(request, all_products)

        return jsonify({
            'success': True,
            'products': selected_products,
            'total_products': total_products

        })
    
    @app.route('/products/<product_id>')
    def get_product_by_id(product_id):
        product = Product.query.get(product_id)

        if product is None:
            abort(404)

        return jsonify({
            'success': True,
            'product': product.format()           

        })


    # post products

    """
    name
- description
- price
    """

    @app.route('/products', methods=['POST'])
    @requires_auth('post:products')
    def create_product(payload):
        body = request.get_json()

        new_product_name = body.get("name", None)
        new_product_description = body.get("description", None)
        new_product_price = body.get("price", None)

        try:
            product = Product(
                name=new_product_name,
                description=new_product_description,
                price=new_product_price
            )

            product.insert()

            product_catalog = Product.query.order_by(Product.id).all()
            displayed_products = paginate_data(request, product_catalog)


            return jsonify(
                {
                    "success": True,
                    "created": product.id,
                    "products": displayed_products,
                    "total_products": len(product_catalog)
                }
            )
        except:
            abort(422)
        

    @app.route('/products/<int:product_id>', methods=['DELETE'])
    @requires_auth('delete:products')
    def delete_product(payload,product_id):
        try:
            product = Product.query.filter(Product.id == product_id).all()

            if product is None:
                abort(404)

            product.delete()

            product_catalog = Product.query.order_by(Product.id).all()
            displayed_products = paginate_data(request, product_catalog)


            return jsonify(
                {
                    "success": True,
                    "deleted": product.id,
                    "products": displayed_products,
                    "total_products": len(product_catalog)
                }
            )
        except:
            abort(422)

#----------------------------------------------------------------------------#
# Error Handling
#----------------------------------------------------------------------------#    
    

    @app.errorhandler(404)
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
    @app.errorhandler(422)
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
    @app.errorhandler(401)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 401,
                        "message": "resource not found"
                        }), 401


    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        return jsonify({
                        "success": False,
                        "error": ex.status_code,
                        "message": ex.error
                        }), ex.status_code

    return app
