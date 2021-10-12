## Intro.

The code in this repo demonstrates the use of Python as a backend service. It uses a relational
database and exposes a REST interface.

## Folder structure

This repo has the following folder structure - or it should look like that after copying GlobalLandTemperaturesByCity.csv in `data` dir.:

```bash
.
├── README.md
├── bin
│   └── env.sh					# environmental variables common to the DB and Flask app.
├── data
│   └── GlobalLandTemperaturesByCity.csv	# place your data here.
├── docker-compose.yml				# all services (DB, web app) are defined here.
├── sql						# dir. containing sql scripts to init and load data to postgres DB.
│   ├── 10_create_schema.sql			# creates table.
│   └── 20_load_data.sql			# loads data to table.
└── web_app					# root dir. of the Flask web app.
    ├── Dockerfile				# docker file to manage the web app container.
    ├── Pipfile
    ├── Pipfile.lock
    ├── app.py					# contains the web app with API calls GET, PUT, POST.
    ├── bin
    │   └── wait_for_postgres.sh		# wait-for script to wait for postgres DB to allow connections to it.
    ├── config.py				# app config variables.
    ├── models.py				# contains the DB object model.
    ├── requirements.txt			# needed for running the app - all python package requirements.
    └── templates
        └── topNcities.html			# HTML template for rending in table form the top N hottest cities.
```

## How to run it?

1. Clone this git repo.
```
git clone https://github.com/saleemayman/city_temperatures_service.git
```

2. `cd` into the cloned repo: `cd city_temperatures_service`.

3. Create a `data` directory in the above folder if it does not exist and copy the main CSV file there.
[Kaggle Link for file: GlobalLandTemperaturesByCity.csv](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data?select=GlobalLandTemperaturesByCity.csv)

```
mkdir data/
mv absolute/path/to/downloaded/GlobalLandTemperaturesByCity.csv data/
```

4. Create a docker network named `test_network`. All other services will attach to this network so that they are able to communicate with each other.
```
docker network create test_network
```

5. Finally, build the project and run it using `docker-compose`:
```
docker-compose build
docker-compose run python_web_app
```

**NOTE:** The first build will take a few minutes (5 to 6 minutes) for all services to start, example, setting up PostgresDB and loading data to it. The below is a sample output of a successful build and launch of the web app:

```bash
[+] Running 9/9
 ⠿ pg_image Pulled                                                                                                                                                                                    10.1s
[+] Running 2/2
 ⠿ Volume "city_temperatures_service_pg_db_data"   Created                                                                                                                                             0.0s
 ⠿ Container city_temperatures_service-pg_image-1  Created                                                                                                                                             0.1s
[+] Running 1/1
 ⠿ Container city_temperatures_service-pg_image-1  Started                                                                                                                                             0.6s

Postgres is starting, will take 4 to 5 minutes . . .

psql: could not connect to server: Connection refused
	Is the server running on host "pg_image" (192.168.128.2) and accepting
	TCP/IP connections on port 5432?

Postgres not yet accepting connections, retrying . . .
Connection to PostgresDB success. Proceeding with launching app . . .

 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://192.168.128.3:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 148-843-666
192.168.128.3 - - [11/Oct/2021 21:29:13] "GET /topNcities/?dtstart=1999-12-31&dtend=2021-10-11&topn=1 HTTP/1.1" 200 -
192.168.128.3 - - [11/Oct/2021 21:29:34] "POST /new HTTP/1.1" 200 -
192.168.128.3 - - [11/Oct/2021 21:29:55] "PUT /update HTTP/1.1" 200 -

```

## Examples:

To run the below examples, please replace `host` value with the corresponding values when it runs on your machine. The host value is shown once the app starts, for example: `* Running on http://192.168.96.3:5000/ (Press CTRL+C to quit)` here, `host=192.168.96.3`.

NOTE: The below `curl` commands can only be executed inside the Flask app container named `python_web_app`.

To get the container name, run: `docker ps` and copy the `NAME` which contains `python_web_app` and then run the following to enter `bash` inside the web app container where you can execute the below requests:
`docker exec -it <container_service_name_with_web_app_run_in_the_name> bash`

1. Find the city with the highest average temperature since 2000.

**Request:** `curl -X GET "http://<host>:5000/topNcities/?dtstart=1999-12-31&dtend=2021-10-11&topn=1"`

**Response:**
```
[
  {
    "avg_temperature": 39.156, 
    "avg_temperature_uncertainty": 0.37, 
    "city": "Ahvaz", 
    "country": "Iran", 
    "dt": "Mon, 01 Jul 2013 00:00:00 GMT", 
    "latitude": "31.35N", 
    "longitude": "49.01E"
  }
]
```

2. Create a new record for the city above with a new high temperature. New temperature is 0.1C higher than the temperature in 1.

**Request:** `curl -X POST  http://<host>:5000/new -H 'Content-Type: application/json' -d '{"avg_temperature": 39.256, "avg_temperature_uncertainty": 0.37, "city": "Ahvaz", "country": "Iran", "dt": "2021-09-30", "lat": "31.35N", "lon": "49.01E"}'`

**Response:**
```
{
  "success": "New record successfully created for record:\n                        date: 2021-09-30 00:00:00, city: Ahvaz, Temperature: 39.256\n                        "
}
```

3. Assuming the record in 1. is wrong, correct it. Actual temperature is 2.5C lower.

**Request:** `curl -X PUT  http://<host>:5000/update -H 'Content-Type: application/json' -d '{"dt" : "2013-07-01","city" : "Ahvaz", "field_to_update" : 36.656, "field_new_value": "avg_temperature"}'`

**Response:**
```
{
  "success": "Updated avg_temperature to 36.656 record for date: 2013-07-01 00:00:00 and city: Ahvaz\n                        "
}
```

