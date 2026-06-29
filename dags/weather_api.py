from src.load import load_weather_data
from src.transform import transform_weather_data
from src.extract import extract_weather_data
from airflow.sdk import dag, task
from pendulum import datetime




@dag(
    dag_id = "weather_api",
    start_date = datetime(2026,6,16),
    schedule = "@daily",
    catchup = False,
    default_args={
        "retries": 1
    }
)




def weather_api():
    @task.python
    def get_weather():
        return extract_weather_data()
        
        
    @task.python
    def process_weather_data(weather_data):
        return transform_weather_data(weather_data)

    @task.python
    def save_to_db(transformed_data):
        load_weather_data(transformed_data)



    
    #define task dependencies
    
    weather_data = get_weather()
    transformed_data = process_weather_data(weather_data)
    save_data = save_to_db(transformed_data)
  




# Call the DAG function to create the DAG object

weather_api()

