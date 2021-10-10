import os, datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, insert, select, desc, func, and_
from sqlalchemy.schema import Table
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from config import SQLALCHEMY_DATABASE_URI

# get engine for postgres
#engine = create_engine("postgresql://test_usr:test_pswd@pg_image:5432/global_temperatures")
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# get the base class
Base = declarative_base()

# load all existing table info into model metadata.
Base.metadata.reflect(engine)

#define resource model for the DB.
db = SQLAlchemy()

class GlobalCityTemperatures(Base):
    """
    Defines the model for the table containing global city
    temperatures.
    """
    postgres_table = Table('global_land_temperatures_by_city', Base.metadata,
                            autoload=True, autoload_with=engine)
    __table__ = postgres_table
    dt = postgres_table.c.dt
    avg_temperature = postgres_table.c.avg_temperature
    avg_temperature_uncertainty = postgres_table.c.avg_temperature_uncertainty
    city = postgres_table.c.city
    country = postgres_table.c.country
    latitude = postgres_table.c.latitude
    longitude = postgres_table.c.longitude

    def add_new_entry(self, dt, avg_temperature, avg_temperature_uncertainty,
                            city, country, latitude, longitude):
        # create new entry in table
        stmt = insert(self.postgres_table).values(dt=dt,
                                            avg_temperature=avg_temperature,
                                            avg_temperature_uncertainty=avg_temperature_uncertainty,
                                            city=city,
                                            country=country,
                                            latitude=latitude, longitude=longitude)

        # write new entry into table and commit result.
        with Session(engine) as session:
            result = session.execute(stmt)
            session.commit()

    def get_hottest_top_N_cities_in_range(self, dt_start=datetime.date(2000, 1, 1),
                                                dt_end=datetime.date(2021, 10, 10),
                                                top_n=10):
        """
        Queries the DB table to get the cities with highest monthly avg. temperature
        within the given time period.

        Parameters:
            dt_start : datetime.date
                - The start date of the time period - exclusive.
            dt_end : datetime.date
                - The end date of the time period - exclusive.
            top_n : int
                - The number of cities to get.

        Returns:
            results : dict
                - If DB query successful then contains the query rows. Otherwise the
                error message.
        """
        results = None

        # check input parameters validity
        if top_n > 100 or top_n < 0:
            top_n = 100
        if dt_start > dt_end:
            dt_temp = dt_start
            dt_start = dt_end
            dt_end = dt_temp

        # open session for ORM objects.
        with Session(engine) as session:
            # create subquery which ranks all cities based on their highest avg.
            # temperature in a given time range. The ranks are in the column
            # `city_rnk` and are calculated per city (partitioned by city). For
            # a given city the highest rank is for the most recent row with the
            # highest temperature.
            subquery = session.query(self.postgres_table,
                                        func.rank().over(
                                            order_by=[
                                                        self.postgres_table.c.avg_temperature.desc(),
                                                        self.postgres_table.c.dt.desc()
                                                        ],
                                            partition_by=self.postgres_table.c.city
                                            ).label('city_rnk')
                                        ).filter(and_(self.postgres_table.c.dt > dt_start,
                                                    self.postgres_table.c.dt < dt_end)
                                            ).subquery()
            # from the ranked entries per city above, get the top N cities
            # with the highest temperatures.
            query = session.query(subquery).filter(subquery.c.city_rnk == 1
                                                    ).order_by(
                                                            subquery.c.avg_temperature.desc()
                                                            ).limit(top_n)
            results = [dict(r) for r in session.execute(query)]

        return results

