## Intro.

The code in this repo demonstrates the use of Python as a backend service. It uses a relational
database and exposes a REST interface.

## Folder structure

This repo has the following folder structure:

```bash
.
├── Dockerfile					# main Dockerfile for the app
├── Pipfile
├── README.md
├── data					# empty directory to put the main data file
│   └── GlobalLandTemperaturesByCity.csv	# to be copied here if you want to test this service
├── docker-compose.yml				# docker-compose file for docker dependencies
└── sql						# contains SQL scripts
    ├── 10_create_schema.sql			# this script creates tables in the DB.
    └── 20_load_data.sql			# loads data from CSV to the above created table
```

## How to run it?

First, clone this git repo.
```
git clone ?????
```

Create a `data` directory in root folder if it does not exist and copy the main CSV file there.
```
mv absolute/path/to/GlobalLandTemperaturesByCity.csv data/
```

Now, simply build the project and run it:
```
docker-compose build
docker-compose run python_rest_api
```
