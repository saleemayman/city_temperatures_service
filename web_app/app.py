from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

from models import GlobalCityTemperatures

# init Flask app
app = Flask(__name__)

# load db configuration
app.config.from_pyfile('config.py')

# bind SQLAlchemy instance to Flask app
db = SQLAlchemy(app)

@app.route('/')
def home_page():
    return """<html><head></head><body>Global City Temperatures "REST" API.</body></html>"""


# helper error functions for common errors
def not_found(message):
    response = jsonify({'error': message})
    response.status_code = 404
    return response

def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)