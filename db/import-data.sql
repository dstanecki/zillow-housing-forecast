CREATE DATABASE IF NOT EXISTS ZillowHomeValueForecast;
USE ZillowHomeValueForecast;

DROP TABLE IF EXISTS forecast;
CREATE TABLE forecast (
  RegionID INT PRIMARY KEY,
  SizeRank INT,
  RegionName CHAR(5) NOT NULL,      -- ZIP
  RegionType VARCHAR(10),
  StateName VARCHAR(50),
  St CHAR(2),
  City VARCHAR(80),
  Metro VARCHAR(120),
  CountyName VARCHAR(80),
  BaseDate DATE,
  MonthForecast   DECIMAL(5,2),
  QuarterForecast DECIMAL(5,2),
  YearForecast    DECIMAL(5,2)
);

LOAD DATA LOCAL INFILE '/docker-entrypoint-initdb.d/data.csv'
INTO TABLE forecast
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(RegionID, SizeRank, RegionName, RegionType, StateName, St, City, Metro, CountyName,
 @BaseDate, MonthForecast, QuarterForecast, YearForecast)
SET BaseDate = STR_TO_DATE(@BaseDate, '%Y-%m-%d');

CREATE INDEX idx_zip ON forecast(RegionName);

CREATE TABLE IF NOT EXISTS zip_centroids (
  zip CHAR(5) PRIMARY KEY,
  lon DOUBLE NOT NULL,
  lat DOUBLE NOT NULL
);
CREATE INDEX idx_zip_centroids ON zip_centroids(zip);

LOAD DATA LOCAL INFILE '/docker-entrypoint-initdb.d/zip_centroids.csv'
INTO TABLE zip_centroids
FIELDS TERMINATED BY ',' IGNORE 1 ROWS
(zip, lon, lat);
