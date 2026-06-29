import requests
from airflow.models import Variable
import logging
from datetime import datetime
from src.s3_utils import upload_to_s3

logger = logging.getLogger(__name__)


cities = [
    # India
    "Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata",
    "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow",

    # Europe
    "London", "Paris", "Berlin", "Madrid", "Rome",
    "Amsterdam", "Vienna", "Zurich", "Stockholm", "Prague"]

def extract_weather_data():
    api_key = Variable.get("OPENWEATHER_API_KEY")
    logger.info("Starting weather data extraction")
    weather_data = []
    timestamp = datetime.now()
    s3_key = (
    f"raw/"
    f"year={timestamp.year}/"
    f"month={timestamp.month:02d}/"
    f"day={timestamp.day:02d}/"
    f"weather_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
)
    for city in cities:
        logger.info(f"Extracting weather data for {city}")
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url,timeout=30) #to prevent the request from hanging indefinitely, we set a timeout of 30 seconds
        if response.status_code == 200:
            weather_data.append(response.json())
        else:
            logger.warning(f"Failed to fetch weather data for {city}: {response.status_code}")
    logger.info(f"Finished weather data extraction {len(weather_data)} records extracted")
    if not weather_data:
        raise ValueError("No weather data extracted from API")
    logger.info(f"Uploading {len(weather_data)} records to S3: {s3_key}")
    
    upload_to_s3(
    data=weather_data,
    s3_key=s3_key)
    logger.info("Successfully uploaded weather data to S3")

    return s3_key