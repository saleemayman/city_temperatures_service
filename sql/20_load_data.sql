-- give permission to allow db user to execute server-side commands.
GRANT pg_execute_server_program to test_usr;

-- load data using server side COPY.
COPY global_land_temperatures_by_city
FROM '/tmp/GlobalLandTemperaturesByCity.csv' DELIMITER ',' CSV HEADER;

---- create index after data loaded into table for faster index creation.
--CREATE INDEX date_col_idx ON public.global_land_temperatures_by_city (dt);

---- cluster the table on the indexed column so data is order by dt.
--CLUSTER public.global_land_temperatures_by_city USING date_col_idx;

-- allow db planner to collect statistics on table
ANALYZE public.global_land_temperatures_by_city;

