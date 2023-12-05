#!/usr/bin/python3
""" The Setting up of API, a Flask web application API """

from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
#from flask_cors import CORS
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
API_HOST = os.getenv("HBNB_API_HOST")
API_PORT = os.getenv("HBNB_API_PORT")


@app.teardown_appcontext
def teardown_db(exception):
    """ Closes the database connection at the end of the request.
        calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def found_not(error):
    """ Handles HTTP error code 404 not found error """
    return (make_response(jsonify({'error': 'Not found'}), 404))

if __name__ == '__main__':
    if not API_HOST:
        API_HOST = "0.0.0.0"
    if not API_PORT:
        API_PORT = "5000"
    app.run(host=API_HOST, port=API_PORT, threaded=True)