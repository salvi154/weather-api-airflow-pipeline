# Weather Data Pipeline using Airflow, AWS S3 and MySQL

## Overview

This project is an end-to-end Data Engineering pipeline that extracts weather data from the OpenWeather API, stores raw data in AWS S3, transforms the data using Python, and loads the curated dataset into MySQL. The pipeline is orchestrated using Apache Airflow and includes audit logging for monitoring pipeline executions.

## Architecture


## Tech Stack

* Python
* Apache Airflow
* AWS S3
* MySQL
* OpenWeather API
* Docker
* Logging & Audit Framework

## Features

* Automated weather data extraction for multiple global cities.
* Stores raw JSON data in AWS S3 using a Bronze Layer architecture.
* Performs data cleansing and transformation.
* Loads curated weather records into MySQL.
* Maintains audit records for monitoring pipeline execution.
* Uses Airflow Variables and Connections for secure configuration management.
* Scheduled execution using Airflow DAGs.

## Project Workflow

### Extract

* Fetches weather data from OpenWeather API.
* Collects weather information for multiple cities.
* Uploads raw JSON data directly to AWS S3.

### Transform

* Reads raw JSON data from S3.
* Converts temperature from Kelvin to Celsius.
* Standardizes city names.
* Extracts weather metrics such as:

  * Temperature
  * Humidity
  * Weather Description
  * Country

### Load

* Creates target table if it does not exist.
* Loads transformed records into MySQL.
* Records pipeline execution metrics in an audit table.

## S3 Data Layout

```text
raw/
└── year=2026/
    └── month=06/
        └── day=27/
            └── weather_20260627_081500.json
```

## Airflow Configuration

### Variables

| Variable            | Description         |
| ------------------- | ------------------- |
| OPENWEATHER_API_KEY | OpenWeather API Key |
| S3_BUCKET_NAME      | AWS S3 Bucket Name  |

### Connections

#### aws_default

AWS credentials used by S3Hook.

#### mysql_connection

MySQL database connection.

## Audit Table

Tracks pipeline execution status.

| Column            |
| ----------------- |
| records_extracted |
| records_loaded    |
| status            |

## How to Run

1. Start Airflow services.
2. Configure Airflow Variables.
3. Configure Airflow Connections.
4. Enable the DAG.
5. Trigger the DAG manually or wait for the scheduled run.

## Future Enhancements

* Incremental data loading.
* Data warehouse integration using Snowflake.
* Dashboarding using Power BI.
* Medallion Architecture (Bronze → Silver → Gold).

## Author

Salvi Tyagi
