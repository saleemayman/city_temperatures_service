GRANT pg_execute_server_program to test_usr;
-- GRANT pg_read_server_files to test_usr;
-- GRANT pg_write_server_files to test_usr;

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
    longitude                   VARCHAR(8)
);
