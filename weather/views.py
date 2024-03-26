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

# Country codes and names
COUNTRY_CODES = {
    "AF": "Afghanistan",
    "AL": "Albania",
    "DZ": "Algeria",	
    "AS": "American Samoa",	
    "AD": "Andorra",	
    "AO": "Angola",	
    "AI": "Anguilla",	
    "AQ": "Antarctica",	
    "AG": "Antigua and Barbuda",	
    "AR": "Argentina",	
    "AM": "Armenia",	
    "AW": "Aruba",	
    "AU": "Australia",	
    "AT": "Austria",	
    "AZ": "Azerbaijan",	
    "BS": "Bahamas (the)",	
    "BH": "Bahrain",	
    "BD": "Bangladesh",	
    "BB": "Barbados",	
    "BY": "Belarus",	
    "BE": "Belgium",	
    "BZ": "Belize",	
    "BJ": "Benin",	
    "BM": "Bermuda",	
    "BT": "Bhutan",	
    "BO": "Bolivia (Plurinational State of)",	
    "BQ": "Bonaire, Sint Eustatius and Saba",	
    "BA": "Bosnia and Herzegovina",	
    "BW": "Botswana",	
    "BV": "Bouvet Island",	
    "BR": "Brazil",	
    "IO": "British Indian Ocean Territory (the)",	
    "BN": "Brunei Darussalam",	
    "BG": "Bulgaria",	
    "BF": "Burkina Faso",	
    "BI": "Burundi",	
    "CV": "Cabo Verde",	
    "KH": "Cambodia",	
    "CM": "Cameroon",	
    "CA": "Canada",	
    "KY": "Cayman Islands (the)",	
    "CF": "Central African Republic (the)",	
    "TD": "Chad",	
    "CL": "Chile",	
    "CN": "China",	
    "CX": "Christmas Island",	
    "CC": "Cocos (Keeling) Islands (the)",	
    "CO": "Colombia",	
    "KM": "Comoros (the)",	
    "CD": "Congo (the Democratic Republic of the)",	
    "CG": "Congo (the)",	
    "CK": "Cook Islands (the)",	
    "CR": "Costa Rica",	
    "HR": "Croatia",	
    "CU": "Cuba",	
    "CW": "Curaçao",	
    "CY": "Cyprus",	
    "CZ": "Czechia",	
    "CI": "Côte d'Ivoire",	
    "DK": "Denmark",	
    "DJ": "Djibouti",	
    "DM": "Dominica",	
    "DO": "Dominican Republic (the)",	
    "EC": "Ecuador",	
    "EG": "Egypt",	
    "SV": "El Salvador",	
    "GQ": "Equatorial Guinea",	
    "ER": "Eritrea",	
    "EE": "Estonia",	
    "SZ": "Eswatini",	
    "ET": "Ethiopia",	
    "FK": "Falkland Islands (the) [Malvinas]",	
    "FO": "Faroe Islands (the)",	
    "FJ": "Fiji",	
    "FI": "Finland",	
    "FR": "France",	
    "GF": "French Guiana",	
    "PF": "French Polynesia",	
    "TF": "French Southern Territories (the)",	
    "GA": "Gabon",	
    "GM": "Gambia (the)",	
    "GE": "Georgia",	
    "DE": "Germany",	
    "GH": "Ghana",	
    "GI": "Gibraltar",	
    "GR": "Greece",	
    "GL": "Greenland",	
    "GD": "Grenada",	
    "GP": "Guadeloupe",
    "GU": "Guam",	
    "GT": "Guatemala",	
    "GG": "Guernsey",	
    "GN": "Guinea",	
    "GW": "Guinea-Bissau",	
    "GY": "Guyana",	
    "HT": "Haiti",	
    "HM": "Heard Island and McDonald Islands",	
    "VA": "Holy See (the)",	
    "HN": "Honduras",	
    "HK": "Hong Kong",	
    "HU": "Hungary",	
    "IS": "Iceland",	
    "IN": "India",	
    "ID": "Indonesia",	
    "IR": "Iran (Islamic Republic of)",	
    "IQ": "Iraq",	
    "IE": "Ireland",	
    "IM": "Isle of Man",	
    "IL": "Israel",	
    "IT": "Italy",	
    "JM": "Jamaica",	
    "JP": "Japan",	
    "JE": "Jersey",	
    "JO": "Jordan",	
    "KZ": "Kazakhstan",	
    "KE": "Kenya",	
    "KI": "Kiribati",	
    "KP": "Korea (the Democratic People's Republic of)",	
    "KR": "Korea (the Republic of)",	
    "KW": "Kuwait",	
    "KG": "Kyrgyzstan",	
    "LA": "Lao People's Democratic Republic (the)",	
    "LV": "Latvia",	
    "LB": "Lebanon",	
    "LS": "Lesotho",	
    "LR": "Liberia",	
    "LY": "Libya",	
    "LI": "Liechtenstein",	
    "LT": "Lithuania",	
    "LU": "Luxembourg",	
    "MO": "Macao",	
    "MG": "Madagascar",	
    "MW": "Malawi",	
    "MY": "Malaysia",	
    "MV": "Maldives",
    "ML": "Mali",	
    "MT": "Malta",	
    "MH": "Marshall Islands (the)",
    "MQ": "Martinique",	
    "MR": "Mauritania",	
    "MU": "Mauritiu",	
    "YT": "Mayotte",	
    "MX": "Mexico",	
    "FM": "Micronesia (Federated States of)",	
    "MD": "Moldova (the Republic of)",	
    "MC": "Monaco",	
    "MN": "Mongolia",	
    "ME": "Montenegro",	
    "MS": "Montserrat",	
    "MA": "Morocco",	
    "MZ": "Mozambique",	
    "MM": "Myanmar",	
    "NA": "Namibia",	
    "NR": "Nauru",	
    "NP": "Nepal",	
    "NL": "Netherlands (the)",	
    "NC": "New Caledonia",	
    "NZ": "New Zealand",	
    "NI": "Nicaragua",	
    "NE": "Niger (the)",	
    "NG": "Nigeria",
    "NU": "Niue",	
    "NF": "Norfolk Island",	
    "MP": "Northern Mariana Islands (the)",	
    "NO": "Norway",	
    "OM": "Oman",	
    "PK": "Pakistan",	
    "PW": "Palau",	
    "PS": "Palestine, State of",	
    "PA": "Panama",	
    "PG": "Papua New Guinea",	
    "PY": "Paraguay",	
    "PE": "Peru",	
    "PH": "Philippines (the)",	
    "PN": "Pitcairn",	
    "PL": "Poland",	
    "PT": "Portugal",	
    "PR": "Puerto Rico",	
    "QA": "Qatar",	
    "MK": "Republic of North Macedonia",		
    "RO": "Romania",	
    "RU": "Russian Federation (the)",	
    "RW": "Rwanda",	
    "RE": "Réunion",	
    "BL": "Saint Barthélemy",	
    "SH": "Saint Helena, Ascension and Tristan da Cunha",	
    "KN": "Saint Kitts and Nevis",	
    "LC": "Saint Lucia",	
    "MF": "Saint Martin (French part)",	
    "PM": "Saint Pierre and Miquelon",	
    "VC": "Saint Vincent and the Grenadines",	
    "WS": "Samoa",	
    "SM": "San Marino",	
    "ST": "Sao Tome and Principe",	
    "SA": "Saudi Arabia",	
    "SN": "Senegal",	
    "RS": "Serbia",	
    "SC": "Seychelles",	
    "SL": "Sierra Leone",	
    "SG": "Singapore",	
    "SX": "Sint Maarten (Dutch part)",	
    "SK": "Slovakia",	
    "SI": "Slovenia",	
    "SB": "Solomon Islands",	
    "SO": "Somalia",	
    "ZA": "South Africa",	
    "GS": "South Georgia and the South Sandwich Islands",	
    "SS": "South Sudan",	
    "ES": "Spain",	
    "LK": "Sri Lanka",	
    "SD": "Sudan (the)",	
    "SR": "Suriname",	
    "SJ": "Svalbard and Jan Mayen",	
    "SE": "Sweden",	
    "CH": "Switzerland",	
    "SY": "Syrian Arab Republic",	
    "TW": "Taiwan (Province of China)",	
    "TJ": "Tajikistan",	
    "TZ": "Tanzania, United Republic of",	
    "TH": "Thailand",	
    "TL": "Timor-Leste",	
    "TG": "Togo",	
    "TK": "Tokelau",
    "TO": "Tonga",	
    "TT": "Trinidad and Tobago",	
    "TN": "Tunisia",	
    "TR": "Turkey",	
    "TM": "Turkmenistan",	
    "TC": "Turks and Caicos Islands (the)",	
    "TV": "Tuvalu",	
    "UG": "Uganda",	
    "UA": "Ukraine",	
    "AE": "United Arab Emirates (the)",	
    "GB": "United Kingdom of Great Britain and Northern Ireland (the)",	
    "UM": "United States Minor Outlying Islands (the)",	
    "US": "United States of America (the)",	
    "UY": "Uruguay",	
    "UZ": "Uzbekistan",	
    "VU": "Vanuatu",	
    "VE": "Venezuela (Bolivarian Republic of)",	
    "VN": "Viet Nam",
    "VG": "Virgin Islands (British)",	
    "VI": "Virgin Islands (U.S.)",	
    "WF": "Wallis and Futuna",	
    "EH": "Western Sahara",	
    "YE": "Yemen",	
    "ZM": "Zambia",	
    "ZW": "Zimbabwe",	
    "AX": "Åland Islands",
}


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
            return render(request, 'weather/current.html', {'current_weather': current_weather, 'country_codes': COUNTRY_CODES})
        else:
            # If city name is empty, renders the current.html template without attempting to fetch data
            return render(request, 'weather/current.html', {'country_codes': COUNTRY_CODES})

    # Renders the current.html template
    return render(request, 'weather/current.html', {'country_codes': COUNTRY_CODES})




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
            return render(request, 'weather/hourly.html', {'grouped_forecast': grouped_forecast, 'country_codes': COUNTRY_CODES})
        else:
            # If city name is empty, renders the hourly.html template without attempting to fetch data
            return render(request, 'weather/hourly.html', {'country_codes': COUNTRY_CODES})

    # Renders the hourly.html template
    return render(request, 'weather/hourly.html', {'country_codes': COUNTRY_CODES})


