import datetime

from flask import Flask, jsonify, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy

from models import GlobalCityTemperatures

# init Flask app
app = Flask(__name__, template_folder='templates')

# load db configuration
app.config.from_pyfile('config.py')

# bind SQLAlchemy instance to Flask app
db = SQLAlchemy(app)

@app.route('/')
def home_page():
    """ Main index page. """
    return """<html><head></head><body>Global City Temperatures "REST" API.</body></html>"""

@app.route('/topNcities', methods = ['GET'])
def get_hottest_cities():
    """
    Returns the top N cities with highest monthly avg. temperature
    in a given time period.

    Example usage: /topNcities?dtstart=2000-01-01&dtend=2013-01-01&topn=5
    """
    # get params from URL and validate them.
    dtstart = request.args.get('dtstart', default='2000-01-01', type=str)
    dtend = request.args.get('dtend', default='2013-01-01', type=str)
    top_num = request.args.get('topn', default=10, type=int)

    # convert string dates to datetime object.
    start_date = datetime.datetime.strptime(dtstart, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(dtend, '%Y-%m-%d')

    # validate input params.
    if top_num > 100 or top_num < 0:
        top_num = 10
    if start_date > end_date:
        dt_temp = dt_start
        dt_start = dt_end
        dt_end = dt_temp

    # instantiate model object and query the DB table
    cities = GlobalCityTemperatures()
    results = cities.get_hottest_top_N_cities_in_range(start_date, end_date, top_num)

    col_names = ['dt', 'avg_temperature', 'avg_temperature_uncertainty', 'city', 'country', 'latitude', 'longtiude']
    return render_template('topNcities.html', headers=col_names, objects=results)

#@app.route('/add_new', methods = ['POST'])
#def add_new_entry():
#    city_temperature = GlobalCityTemperatures(data['dt'], \
#                                                data['avg_temperature'], \
#                                                data['avg_temperature_uncertainty'], \
#                                                data['city'], \
#                                                data['country'], \
#                                                data['latitude'], \
#                                                data['longtiude'])
#    return make_response(jsonify({'city_temperature': city_temperature}),201)

# helper error functions for common errors
def not_found(message):
    response = jsonify({'error': message})
    response.status_code = 404
    return response

def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
