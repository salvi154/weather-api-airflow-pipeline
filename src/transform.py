import logging
import json
from src.s3_utils import read_json_from_s3


logger = logging.getLogger(__name__)



def clean_city_name(city_name):
    return city_name.strip().title()

def convert_kelvin_to_celsius(temp_kelvin):
    return round(temp_kelvin - 273.15,2)




def transform_weather_record(record):
    city_name = clean_city_name(record['name'])
    temp_celsius = convert_kelvin_to_celsius(record['main']['temp'])
    weather_description = record['weather'][0].get('description',"Unknown")
    humidity = record["main"].get("humidity", 0)

    return {
        "city_name": city_name,
        "country": record['sys']['country'],
        "temp_kelvin": record['main']['temp'],
        "temp_celsius": temp_celsius,
        "description": weather_description,
        "temp_min": convert_kelvin_to_celsius(record['main']['temp_min']),
        "temp_max": convert_kelvin_to_celsius(record['main']['temp_max']),
        "humidity": humidity
    }

def transform_weather_data(s3_key):
    logger.info("Starting weather data transformation")
    weather_data = read_json_from_s3(s3_key=s3_key)
    if not weather_data:
        logger.warning(f"No weather data found in S3 key: {s3_key}")
        return []
    
    transformed_data = []
    if weather_data:
        for data in weather_data:
            transformed_data.append(transform_weather_record(data))
    logger.info(f"Finished weather data transformation {len(transformed_data)} records transformed")
    return transformed_data
