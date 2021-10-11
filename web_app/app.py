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

@app.route('/new', methods = ['POST'])
def create_new_entry():
    """
    Creates a new entry in the monthly city avg. temperature table. Must have
    JSON payload containing the values for columns to be inserted as a new
    record.
    """
    # get JSON payload for new record.
    if request.is_json:
        data = request.get_json()
        dt = data["dt"]
        avg_temperature = data["avg_temperature"]
        avg_temperature_uncertainty = data["avg_temperature_uncertainty"]
        city = data["city"]
        country = data["country"]
        lat = data["lat"]
        lon = data["lon"]

    # validate inputs before inserting into table.
    if dt and avg_temperature and city and country and lat and lon:
        # check for valid date
        try:
            dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
        except:
            bad_request('Invalid date provided. Must be in YYYY-MM-DD format. dt: {}'.format(dt))

        # check for valid temperature value
        if type(avg_temperature) is not float and type(avg_temperature) is not int:
            bad_request('Invalid input for average temperature. Must be a valid number/decimal.')

        # if it makes it till here, then insert new record.
        cities = GlobalCityTemperatures()
        response = cities.add_new_entry(dt=dt, avg_temperature=avg_temperature,
                                        avg_temp_uncert=avg_temperature_uncertainty,
                                        city=city, country=country,
                                        latitude=lat, longitude=lon)
        response = jsonify(response)
        response.status_code = 200
        return response
    else:
        bad_request('Invalid inputs.')

@app.route('/update', methods = ['PUT'])
def update_record():
    """
    Updates the `avg_temperature` and/or `avg_temperature_uncertainity` for a
    row/entry in the table using the given input `city` and `dt` (date) values.

    Input data must be a JSON payload.
    """
    # get JSON payload for new record.
    if request.is_json:
        data = request.get_json()
        dt = data["dt"]
        city = data["city"]
        field_to_update = data["field_to_update"]
        field_new_value = data["field_new_value"]

    # validate inputs
    try:
        dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
    except:
        bad_request('Invalid date provided. Must be in YYYY-MM-DD format. dt: {}'.format(dt))

    # check new value for avg. temp
    if type(field_new_value) is not float and type(field_new_value) is not int:
        bad_request('Invalid input for {f}. Must be a valid number/decimal.'.format(f=field_to_update))

    # if no uncertainty value given then send it as None.
    if field_new_value != "avg_temperature" and field_new_value != "avg_temperature_uncertainty":
        bad_request('Invalid field to update {f}.'.format(f=field_to_update))

    # update the record
    cities = GlobalCityTemperatures()
    response = cities.update_record(dt, city, field_to_update, field_new_value)

    response = jsonify(response)
    response.status_code = 200
    return response

@app.route('/topNcities/', methods = ['GET'])
def get_hottest_cities():
    """
    Returns the top N cities with highest monthly avg. temperature
    in a given time period.

    Example usage: /topNcities/?dtstart=2000-01-01&dtend=2013-01-01&topn=5
    """
    # get params from URL and validate them.
    dtstart = request.args.get('dtstart', default='2000-01-01', type=str)
    dtend = request.args.get('dtend', default='2013-01-01', type=str)
    top_num = request.args.get('topn', default=1, type=int)

    # convert string dates to datetime object.
    start_date = datetime.datetime.strptime(dtstart, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(dtend, '%Y-%m-%d')

    # validate input params.
    if top_num > 100 or top_num == 0:
        top_num = 10
    if start_date > end_date:
        dt_temp = dt_start
        dt_start = dt_end
        dt_end = dt_temp

    # instantiate model object and query the DB table
    cities = GlobalCityTemperatures()
    results = cities.get_hottest_top_N_cities_in_range(start_date, end_date, top_num)

    # return only JSON object if hottest city is requested
    if len(results) == 1:
        return jsonify(results)
    else:
        col_names = ['dt', 'avg_temperature', 'avg_temperature_uncertainty',
                    'city', 'country', 'latitude', 'longtiude']
        return render_template('topNcities.html', headers=col_names, objects=results)


# helper function for handling errors.
def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response

if __name__ == '__main__':
    # run on 0.0.0.0 to enable access to web app from outside the app host container.
    app.run(host='0.0.0.0', port=5000, debug=True)
