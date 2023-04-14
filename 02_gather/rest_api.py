# This program defines two functions, is_raining(city_name) 
# and will_rain(city_name, class_datetime). The former checks 
# if it's currently raining in the given city, and the latter 
# checks if it will rain at the given datetime. Both functions 
# make requests to the Open Weathermap API, parse the JSON response, 
# and return a boolean value based on the weather conditions.
import requests
import json
from datetime import datetime
API_KEY = '71b6679a769a1801f80103003ce32d92'

def is_raining(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={API_KEY}&q={city_name}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404" and "weather" in data:
        weather = data["weather"]
        main_weather = weather[0]["main"]
        return main_weather.lower() == "rain"
    else:
        return False

def will_rain(city_name, class_datetime):
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = f"{base_url}appid={API_KEY}&q={city_name}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404" and "list" in data:
        forecasts = data["list"]
        for forecast in forecasts:
            forecast_datetime = datetime.fromtimestamp(forecast["dt"])
            if forecast_datetime >= class_datetime:
                main_weather = forecast["weather"][0]["main"]
                if main_weather.lower() == "rain":
                    return True
                else:
                    return False
    return False

city_name = "Portland,OR"
class_datetime_str = "2023-04-20 14:00:00"
class_datetime = datetime.strptime(class_datetime_str, "%Y-%m-%d %H:%M:%S")

print(f"Is it raining in {city_name}? {is_raining(city_name)}")
print(f"Will it be raining when our class next meets? {will_rain(city_name, class_datetime)}")