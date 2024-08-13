CREATE DATABASE IF NOT EXISTS ZillowHomeValueForecast;
USE ZillowHomeValueForecast;

CREATE TABLE forecast (
    RegionID INT,
    SizeRank INT,
    RegionName VARCHAR(255),
    RegionType VARCHAR(50),
    StateName VARCHAR(50),
    St VARCHAR(50),
    City VARCHAR(100),
    Metro VARCHAR(255),
    CountyName VARCHAR(100),
    BaseDate DATE,
    `2024-08-31` FLOAT,
    `2024-10-31` FLOAT,
    `2025-07-31` FLOAT
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/2024data.csv'
INTO TABLE forecast
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;