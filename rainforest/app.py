import os ,sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from .database.models import db_drop_and_create_all, setup_db
from .auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  return app
 
APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

@APP.route('/')
def welcome_to_root():
    return "Welcome to Rainforest! :>"

# Error Handling


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
