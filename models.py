from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# define resource model for the DB.
db = SQLAlchemy()

class GlobalCityTemperatures(db.Model):
    """
    Defines the model for the table containing global city
    temperatures.
    """
    __tablename__ = 'global_land_temperatures_by_city'
    dt = db.Column(db.Date, primary_key=True, nullable=False)
    avg_temperature = db.Column(db.Float)
    avg_temperature_uncertainty = db.Column(db.Float)
    city = db.Column(db.String(64), nullable=False)
    country = db.Column(db.String(64), nullable=False)
    latitude = db.Column(db.String(8))
    longitude = db.Column(db.String(8))

    def __init__(self, dt, avg_temperature, avg_temperature_uncertainty, \
                        city, country, latitude, longitude):
        self.dt = dt
        self.avg_temperature = avg_temperature
        self.avg_temperature_uncertainty = avg_temperature_uncertainty
        self.city = city
        self.country = country
        self.latitude = latitude
        self.longitude = longitude