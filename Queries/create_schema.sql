-- Create the schema
CREATE SCHEMA `safe_havens`;

-- Select the schema to use
USE `safe_haven-detection`;

CREATE TABLE us_counties(
	fips_code INT PRIMARY KEY,
    state_id VARCHAR(5),
    county_name VARCHAR(100),
    state_name VARCHAR(100)
);

CREATE TABLE us_cities(
	city_id VARCHAR(50) PRIMARY KEY,
    fips_code INT,
    city_name VARCHAR(100),
    FOREIGN KEY (fips_code) REFERENCES us_counties(fips_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE education (
    fips_code INT,
    pct_no_hs_degree_18_22 FLOAT,
    pct_no_hs_degree_08_12 FLOAT,
    pct_no_hs_degree_2000 FLOAT,
    FOREIGN KEY (fips_code) REFERENCES us_counties(fips_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE population (
    fips_code INT,
    population_estimate_2020 BIGINT UNSIGNED,
    population_estimate_2021 BIGINT UNSIGNED,
    population_estimate_2022 BIGINT UNSIGNED,
    population_estimate_2023 BIGINT UNSIGNED,
    FOREIGN KEY (fips_code) REFERENCES us_counties(fips_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE poverty (
    fips_code INT,
    poverty_percentage FLOAT,
    poverty_percentage_under_18 FLOAT,
    poverty_percentage_18_to_64 FLOAT,
    poverty_percentage_65_and_over FLOAT,
    FOREIGN KEY (fips_code) REFERENCES us_counties(fips_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE unemployment (
    fips_code INT,
    unemployment_rate_2020 FLOAT,
    unemployment_rate_2021 FLOAT,
    unemployment_rate_2022 FLOAT,
	FOREIGN KEY (fips_code) REFERENCES us_counties(fips_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE food_banks (
	city_id VARCHAR(50),
	food_banks_id INT PRIMARY KEY,
    food_bank_name VARCHAR(100),
    address VARCHAR(255),
    status VARCHAR(50),
    FOREIGN KEY (city_id) REFERENCES us_cities(city_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE fire_emergency_services (
	city_id VARCHAR(50),
    fire_emergency_id INT PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(255),
    FOREIGN KEY (city_id) REFERENCES us_cities(city_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE hospitals (
    hospital_id INT PRIMARY KEY,
    city_id VARCHAR(50),
    name VARCHAR(100),
    address VARCHAR(255),
    status VARCHAR(50),
    ownership_information VARCHAR(100),
    FOREIGN KEY (city_id) REFERENCES us_cities(city_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE local_law_enforcement (
	local_law_id INT PRIMARY KEY,
    city_id VARCHAR(50),
    address VARCHAR(255),
    type_of_law_enforcement VARCHAR(100),
    FOREIGN KEY (city_id) REFERENCES us_cities(city_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE crime (
    fips_code INT,
    crime_rate_per_100000 FLOAT,
    crime_id INT PRIMARY KEY,
    murder INT,
    rape INT,
    robbery INT,
    burglry INT,
    FOREIGN KEY (fips_code) REFERENCES us_counties(fips_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
