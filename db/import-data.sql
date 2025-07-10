CREATE DATABASE IF NOT EXISTS ZillowHomeValueForecast;
    USE ZillowHomeValueForecast;

    CREATE TABLE forecast (
        RegionID INT,
        SizeRank INT,
        RegionName VARCHAR(50),
        RegionType VARCHAR(50),
        StateName VARCHAR(50),
        St VARCHAR(50),
        City VARCHAR(50),
        Metro VARCHAR(50),
        CountyName VARCHAR(50),
        BaseDate DATE,
        MonthForecast DECIMAL(4, 2),
        QuarterForecast DECIMAL(4, 2),
        YearForecast DECIMAL(4, 2)
    );

    LOAD DATA LOCAL INFILE '/docker-entrypoint-initdb.d/data.csv'
    INTO TABLE forecast
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;
