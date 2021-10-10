-- create table in DB
DROP TABLE IF EXISTS public.global_land_temperatures_by_city;

CREATE TABLE public.global_land_temperatures_by_city
(
    dt                          DATE,
    avg_temperature             DOUBLE PRECISION,
    avg_temperature_uncertainty DOUBLE PRECISION,
    city                        VARCHAR(64),
    country                     VARCHAR(64), 
    latitude                    VARCHAR(8),
    longitude                   VARCHAR(8),
    PRIMARY KEY (dt, city, latitude, longitude)
);

