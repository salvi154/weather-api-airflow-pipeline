from airflow.sdk.bases.hook import BaseHook
import mysql.connector
import logging
from src.audit import insert_audit_record

logger = logging.getLogger(__name__)




def load_weather_data(transformed_data):
    conn = BaseHook.get_connection("mysql_connection")
    cursor = None
    db_connection = None
    if not transformed_data:
        logger.warning("No transformed data to load")
        return
    logger.info("Connecting to the database and loading weather data")
    try:
        db_connection = mysql.connector.connect(
                host=conn.host,
                user=conn.login,
                password=conn.password,
                database="weather_api_data"
            )
        cursor = db_connection.cursor()

        create_table_query = """
            CREATE TABLE IF NOT EXISTS weather_table (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                City_name   VARCHAR(255),
                Country     VARCHAR(10),
                Temp_Celsius FLOAT,
                Temp_Kelvin  FLOAT,
                Description  VARCHAR(255),
                temp_min_K   FLOAT,
                temp_max_K   FLOAT,
                Humidity     INT,
                ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        cursor.execute(create_table_query)

        insert_query = """
            INSERT INTO weather_table
                (City_name, Country, Temp_Celsius, Temp_Kelvin, Description, temp_min_K, temp_max_K, Humidity)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)
            """
        for data in transformed_data:
                values = (data["city_name"], data["country"], data["temp_celsius"], data["temp_kelvin"], data["description"], data["temp_min"], data["temp_max"], data["humidity"])
                cursor.execute(insert_query, values)
        db_connection.commit()

        insert_audit_record(
            db_connection=db_connection,
            records_extracted=len(transformed_data),
            records_loaded=len(transformed_data),
            status="SUCCESS"
        )
    except mysql.connector.Error as err:
        logger.error(f"Database Error: {err}")
        if db_connection:
              
            insert_audit_record(
            db_connection=db_connection,
            records_extracted=len(transformed_data),
            records_loaded=0,
            status="FAILED"
        )
        

    finally:
        if cursor:
            cursor.close()

        if db_connection:
            logger.info("Closing database connection")
            db_connection.close()