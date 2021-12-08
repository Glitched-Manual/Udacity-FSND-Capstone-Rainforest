import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy, model
from flask_cors import CORS, cross_origin
from sqlalchemy.sql.sqltypes import REAL


if __name__ == 'rainforest.app':
    from .database.models import db_drop_and_create_all, setup_db, User, Order, OrderItem, Product
    from .auth.auth import AuthError, requires_auth

elif __name__ == 'app':
    try:

        from database.models import db_drop_and_create_all, setup_db, User, Order, OrderItem, Product
        from auth.auth import AuthError, requires_auth

    except BaseException:
        pass


Results_PER_PAGE = 10

# to paginate user and product data


def paginate_data(request, selection):
    page = request.args.get("page", 1, type=int)
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

        # test to see if any products exist within the selection

        if len(selected_products) == 0:
            abort(404)

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

    @app.route('/products', methods=['POST'])
    @requires_auth('post:products')
    def create_product(payload):
        body = request.get_json()

        new_product_name = body.get("name", None)
        new_product_description = body.get("description", None)
        new_product_price = body.get("price", None)

        product_attributes = [
            new_product_name,
            new_product_description,
            new_product_price]

        for attr in product_attributes:
            if attr is None:
                abort(422)

        try:
            product = Product(
                name=new_product_name,
                description=new_product_description,
                price=new_product_price
            )

            product.insert()

            
            all_products = Product.query.all()
            total_products = len(all_products)            

            return jsonify(
                {
                    "success": True,
                    "created": product.id,
                    "product": product.format(),
                    "total_products": total_products
                }
            )
        except BaseException:
            abort(422)

    @app.route('/products/<int:product_id>', methods=['DELETE'])
    @requires_auth('delete:products')
    def delete_product(payload, product_id):
        try:
            product = Product.query.get(product_id)

            if product is None:
                abort(404)

            product.delete()

            all_products = Product.query.order_by(Product.id).all()
            

            return jsonify(
                {
                    "success": True,
                    "deleted": product.id,                    
                    "total_products": len(all_products)
                }
            )
        except BaseException:
            abort(422)

    @app.route('/products/<int:product_id>', methods=['PATCH'])
    @requires_auth('patch:products')
    def patch_product(payload, product_id):

        try:
            if product_id is None:
                abort(422)

            product = Product.query.get(product_id)

            if product is None:
                abort(404)

            body = request.get_json()

            new_product_name = body.get("name", None)
            new_product_description = body.get("description", None)
            new_product_price = body.get("price", None)

            if new_product_name:
                product.name = new_product_name

            if new_product_description:
                product.description = new_product_description

            if new_product_price:

                if not isinstance(new_product_price, type(1.1)):
                    abort(422)
                product.price = new_product_price

            return jsonify({
                'success': True,
                'patched': product_id,
                'product_name': product.name,
                'product_description': product.description,
                'product_price': product.price
            })
        except:
            abort(422)

#----------------------------------------------------------------------------#
# Users
#----------------------------------------------------------------------------#

    @app.route('/users')
    @requires_auth('get:users')
    def get_users(payload):

        try:
            all_users = User.query.order_by(User.id).all()

            if all_users is None:
                abort(404)

            total_users = len(all_users)

            paginated_user_list = paginate_data(request, all_users)

            if len(paginated_user_list) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'users': paginated_user_list,
                'total_users': total_users
            })
        except:
            abort(422)

    @app.route('/users/<int:user_id>')
    @requires_auth('get:users')
    def get_user_by_id(payload, user_id):

        try:
            user = User.query.get(user_id)

            if user is None:
                abort(404)

            return jsonify({
                'success': True,
                'user': user.format()
            })
        except BaseException:
            abort(422)

    @app.route('/users', methods=['POST'])
    @requires_auth('post:users')
    def create_user(payload):

        body = request.get_json()
        new_user_name = body.get("name", None)

        if new_user_name is None:
            abort(422)

        try:

            new_user = User(name=new_user_name)
            new_user.insert()

            return jsonify({
                'success': True,
                'created': new_user.id,
                'user': new_user.format()

            })
        except:
            abort(422)

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    @requires_auth('delete:users')
    def delete_user(payload, user_id):
        try:
            user = User.query.get(user_id)

            if user is None:
                abort(404)

            user.delete()

            return jsonify({
                'success': True,
                'deleted': user_id
            })

        except BaseException:
            abort(422)

#----------------------------------------------------------------------------#
# Orders
#----------------------------------------------------------------------------#

    @app.route('/orders')
    @requires_auth('get:orders')
    def get_orders(payload):

        try:
            orders = Order.query.order_by(Order.id).all()

            if orders is None:
                abort(404)

            total_orders = len(orders)
            selected_orders = paginate_data(request, orders)

            if len(selected_orders) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'orders': selected_orders,
                'total_orders': total_orders

            })
        except BaseException:
            abort(422)

    @app.route('/orders/<int:order_id>')
    @requires_auth('get:orders')
    def get_order_by_id(payload, order_id):
        try:
            order = Order.query.get(order_id)

            if order is None:
                abort(404)

            return jsonify({
                'success': True,
                'order': order.format()
            })

        except BaseException:
            abort(422)

    @app.route('/orders', methods=['POST'])
    @requires_auth('post:orders')
    def create_order(payload):
        try:
            body = request.get_json()

            passed_user_id = body.get('user_id', None)

            if passed_user_id is None:
                abort(422)

            if not isinstance(passed_user_id, type(21)):
                abort(422)

            new_order = Order(user_id=passed_user_id)

            new_order.insert()

            return jsonify({
                'success': True,
                'created': new_order.id,
                'order': new_order.format()
            })

        except BaseException:
            abort(422)

    @app.route('/orders/<int:order_id>', methods=['DELETE'])
    @requires_auth('delete:orders')
    def delete_order(payload, order_id):
        try:
            order = Order.query.get(order_id)

            if order is None:
                abort(404)

            order.delete()

            return jsonify({
                'success': True,
                'deleted': order_id
            })

        except BaseException:
            abort(422)

#----------------------------------------------------------------------------#
# OrderItems
#----------------------------------------------------------------------------#
    @app.route('/order_items')
    @requires_auth('get:order_items')
    def get_order_items(payload):
        try:

            order_items = OrderItem.query.order_by(OrderItem.id).all()

            if order_items is None:
                abort(404)

            total_order_items = len(order_items)

            selected_order_items = paginate_data(request, order_items)

            if len(selected_order_items) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'order_items': selected_order_items,
                'total_order_items': total_order_items
            })
        except BaseException:
            abort(422)

    @app.route('/order_items/<int:order_item_id>')
    @requires_auth('get:order_items')
    def get_order_item_by_id(payload, order_item_id):
        try:
            order_item = OrderItem.query.get(order_item_id)

            if order_item is None:
                abort(404)

            return jsonify({
                'success': True,
                'order_item': order_item.format()
            })

        except BaseException:
            abort(422)

    @app.route('/order_items', methods=['POST'])
    @requires_auth('post:order_items')
    def create_order_item(payload):
        try:

            body = request.get_json()

            order_order_id = body.get('order_id', None)
            order_product_id = body.get('product_id', None)
            order_product_quantity = body.get('product_quantity', None)
          

            if (order_order_id is None) or (type(order_order_id)) != type(51):
                abort(422) 

            if (order_order_id is None) or (type(order_product_id)) != type(51):
                abort(422)

            if (order_product_quantity is None) or (type(order_product_quantity)) != type(51):
                abort(422)

            order_item = OrderItem(
                order_id=order_order_id,
                product_id=order_product_id,
                product_quantity=order_product_quantity)

            order_item.insert()
            return jsonify({
                'success': True,
                'created': order_item.id,
                'order_item': order_item.format()
            })

        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/order_items/<int:order_item_id>', methods=['DELETE'])
    @requires_auth('delete:order_items')
    def delete_order_item(payload, order_item_id):
        try:
            order_item = Product.query.get(order_item_id)

            if order_item is None:
                abort(404)

            order_item.delete()

            return jsonify(
                {
                    "success": True,
                    "deleted": order_item_id,
                }
            )
        except:
            abort(422)

#----------------------------------------------------------------------------#
# Error Handling
#----------------------------------------------------------------------------#

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400,
                       "message": "bad request"}), 400

    @app.errorhandler(401)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "resource not found"
        }), 401

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        return jsonify({
            "success": False,
            "error": ex.status_code,
            "message": ex.error
        }), ex.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()