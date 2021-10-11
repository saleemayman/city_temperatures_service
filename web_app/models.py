import os, datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, insert, select, update, desc, func, and_
from sqlalchemy.schema import Table
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from config import SQLALCHEMY_DATABASE_URI

# get engine for postgres
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
    # init the model table based on the existing table in postgres.
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

    def add_new_entry(self, dt, avg_temperature, avg_temp_uncert,
                            city, country, latitude, longitude):
        """
        Creates a new record in the table `global_land_temperatures_by_city` using
        the inputs provided.

        Parameters:
            dt : datetime.date
                - The date for the new record.
            avg_temperature : float/int
                - The value of average temperature.
            avg_temp_uncert : float/int
                - The uncertainty value for the average temperature.
            city : string
                - The city name for the new record.
            country : string
                - Name of the country from where the record originates.
            latitude : string
                - Latitude of the new temperature observation, e.g., `53.25N`
                format: `xx.xxA` where x := {1, 2, ..., 9, 0} and A := {N, S}
            longitude: string
                - Longitude of the new temperature observation, e.g., `13E`
                format: `xx.xxA` where x := {1, 2, ..., 9, 0} and A := {E, W}

        Returns:
            results : dict
                - If DB query successful then a success message else the error message.
        """
        try:
            # create new entry in table
            stmt = insert(self.postgres_table).values(dt=dt,
                                                avg_temperature=avg_temperature,
                                                avg_temperature_uncertainty=avg_temp_uncert,
                                                city=city,
                                                country=country,
                                                latitude=latitude, longitude=longitude)

            # write new entry into table and commit result.
            with Session(engine) as session:
                result = session.execute(stmt)
                session.commit()

            # return success message.
            return {'success':
                    """New record successfully created for record:
                        date: {d}, city: {ci}, Temperature: {t}
                        """.format(d=dt, ci=city, t=avg_temperature)}
        except Exception as err:
            return {'error': 
                        """Could not create new record for dt: {d} and city: {ci}.
                            Error message: {e}
                        """.format(d=dt, ci=city, e=err)}

    def update_record(self, dt, city, new_target_value, update_target):
        """
        Update an existing row using the given `dt` and `city` values. The
        update target is `avg_temperature` and/or `avg_temperature_uncertainty`.

        Parameters:
            dt : datetime.date
                - The date for the record to be updated.
            city : string
                - The city name for which the records will be updated for date=dt.
            new_target_value: float/int
                - The new value of average temperature or temperature uncertainty.
                Acceptable values := {"avg_temperature" or "avg_temperature_uncertainty"}.
                Only one of the above columns is updated in the DB for above `city` and `dt`
            update_target : string
                - The name of the decimal column being updated.
                Acceptable values := {"avg_temperature" or "avg_temperature_uncertainty"}.

        Returns:
            results : dict
                - If DB query successful then a success message else the error message.
        """
        # TODO: add check to validate values of update_target.

        try:
            stmt = update(self.postgres_table
                            ).where(and_(self.postgres_table.c.dt == dt,
                                        self.postgres_table.c.city == city)
                                    ).values(
                                                {
                                                    update_target: new_target_value
                                                } )
            # update entry into table and commit result.
            with Session(engine) as session:
                result = session.execute(stmt)
                session.commit()

            # return success message.
            return {'success':
                        """Updated {u} to {t} record for date: {d} and city: {ci}
                        """.format(u=update_target, t=new_target_value, d=dt, ci=city)}
        except Exception as err:
            return {'error':
                        """Could not update {u} for record for dt: {d}, city: {c}.
                            Error message: {e}
                        """.format(u=update_target, d=dt, c=city, e=err)}

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

        try:
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
                                                    self.postgres_table.c.dt < dt_end,
                                                    self.postgres_table.c.avg_temperature != None)
                                                ).subquery()

                # from the ranked entries per city above, get the top N cities
                # with the highest temperatures.
                # Get all original columns and discard rank column.
                query = session.query(
                                        subquery.c.dt,
                                        subquery.c.avg_temperature,
                                        subquery.c.avg_temperature_uncertainty,
                                        subquery.c.city,
                                        subquery.c.country,
                                        subquery.c.latitude,
                                        subquery.c.longitude
                                    ).filter(subquery.c.city_rnk == 1
                                                    ).order_by( subquery.c.avg_temperature.desc()
                                                                ).limit(top_n)
                results = [dict(r) for r in session.execute(query)]

            return results
        except Exception as err:
            return {'error':
                        """Could not query DB table for top {n} cities in time period {s} to {f}.
                            Error message: {e}
                        """.format(n=top_n, s=dt_start, f=dt_end, e=err)}

