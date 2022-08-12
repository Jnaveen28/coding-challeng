
CREATE TABLE weather (
    `date` date,
    max_tmp int,
    min_tmp int,
    precipitation int,
    location_id varchar(16)
)

CREATE TABLE weather_stage (
    `date` date,
    max_tmp int,
    min_tmp int,
    precipitation int,
    location_id varchar(16)
)