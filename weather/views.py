# Standard Library Imports
import datetime as dt
import os

# Third-Party Imports
import pytz
from dotenv import load_dotenv
import urllib.request
import urllib.parse
import json

# Django Imports
from django.shortcuts import render
from django.contrib import messages


def get_date(timezone):
    tz = dt.timezone(dt.timedelta(seconds=int(timezone)))
    return dt.datetime.now(tz = tz).strftime("%Y-%m-%d, %H:%M:%S")

def index(request):
    # Renders the index.html template
    return render(request, 'weather/index.html')


def current(request):
    if request.method == 'GET':
        # Gets the city name and country code from the request
        city_name = request.GET.get('city_name')
        country_code = request.GET.get('country_code')

        if city_name:
            # API key for OpenWeatherMap
            api_key = os.getenv('api_key')

            # Encodes the city name before constructing the URL
            encoded_city_name = urllib.parse.quote(city_name)

            # Constructs the URL to fetch current weather data
            url = f'https://api.openweathermap.org/data/2.5/weather?q={encoded_city_name},{country_code}&appid={api_key}&units=metric'

            try:
                # Opens the URL and read the response
                response = urllib.request.urlopen(url)
                # Loads the response data as JSON
                data = json.loads(response.read())

                # Extracts relevant weather information from the response data
                current_weather = {
                    'city_name': data['name'],
                    'country_code': data['sys']['country'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'weather_description': data['weather'][0]['description'],
                    'forecast_main': data['weather'][0]['main'],
                    'forecast_icon': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}.png"
                }

                # Get the UTC timestamp for the weather data
                utc_timestamp = data['dt']
                # Get timezone offset in seconds
                timezone_offset = data['timezone']
                # Convert UTC timestamp to local time using timezone information
                local_time = dt.datetime.utcfromtimestamp(utc_timestamp).replace(tzinfo=pytz.utc) + dt.timedelta(seconds=timezone_offset)
                local_time = local_time.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
                current_weather['local_time'] = local_time

            except Exception as e:
                # Prints error message if an exception occurs
                print(f"An error occurred: {e}")
                current_weather = None

            # Renders the current.html template with current weather data
            return render(request, 'weather/current.html', {'current_weather': current_weather})
        else:
            # If city name is empty, renders the current.html template without attempting to fetch data
            return render(request, 'weather/current.html')

    # Renders the current.html template
    return render(request, 'weather/current.html')



def group_forecast_by_day(hourly_forecast):
    # Group hourly forecast by day
    grouped_forecast = {}
    for forecast in hourly_forecast:
        day = forecast['day_of_week']
        if day not in grouped_forecast:
            grouped_forecast[day] = []
        grouped_forecast[day].append(forecast)
    return grouped_forecast

def hourly(request):
    if request.method == 'GET':
        # Gets the city name and country code from the request
        city_name = request.GET.get('city_name')
        country_code = request.GET.get('country_code')

        if city_name:
            # API key for OpenWeatherMap
            api_key = os.getenv('api_key')

            # Encodes the city name before constructing the URL
            encoded_city_name = urllib.parse.quote(city_name)

            if country_code:
                # Constructs the URL to fetch hourly forecast data with both city name and country code
                url = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?q={encoded_city_name},{country_code}&appid={api_key}&units=metric'
            else:
                # Constructs the URL to fetch hourly forecast data with only city name
                url = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?q={encoded_city_name}&appid={api_key}&units=metric'

            try:
                # Opens the URL and read the response
                response = urllib.request.urlopen(url)
                # Loads the response data as JSON
                data = json.loads(response.read())
                hourly_forecast = []
                # Extracts relevant forecast information from the response data
                for item in data['list']:
                    forecast = {
                        'time': item['dt_txt'],
                        'temperature': item['main']['temp'],
                        'day_of_week': dt.datetime.utcfromtimestamp(int(item['dt'])).strftime('%A'), # Get day of the week
                        'timezone': (dt.datetime.utcfromtimestamp(int(item['dt'])) + dt.timedelta(hours=int(data['city']['timezone'])/3600)).strftime('%Y-%m-%d %H:%M:%S'),
                        'feels_like': item['main']['feels_like'],
                        'humidity': item['main']['humidity'],
                        'pressure': item['main']['pressure'],
                        'weather_description': item['weather'][0]['description'],
                        'forecast_main': item['weather'][0]['main'],
                        'forecast_icon': f"http://openweathermap.org/img/wn/{item['weather'][0]['icon']}.png"
                    }
                    hourly_forecast.append(forecast)
                
                # Group hourly forecast by day
                grouped_forecast = group_forecast_by_day(hourly_forecast)
                
                # Print the fetched data
                print("Hourly Forecast:")
                print(json.dumps(grouped_forecast, indent=4))
                    
            except Exception as e:
                # Prints error message if an exception occurs
                print(f"An error occurred: {e}")
                grouped_forecast = None

            # Renders the hourly.html template with hourly forecast data
            return render(request, 'weather/hourly.html', {'grouped_forecast': grouped_forecast})
        else:
            # If city name is empty, renders the hourly.html template without attempting to fetch data
            return render(request, 'weather/hourly.html')

    # Renders the hourly.html template
    return render(request, 'weather/hourly.html')


