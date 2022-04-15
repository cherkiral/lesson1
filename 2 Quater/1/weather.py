from pprint import pprint
import requests
import json

# city = input('Input city name:\n')
city = 'moscow'
api_key = 'c1b430450ae6de824b084b7d0a5b0773'
base_url = 'https://api.openweathermap.org/data/2.5/weather'
lat = '55.75222'
lon = '37.61556'
params = {
    'lat' : lat,
    'lon' : lon,
    'lang' : 'ru',
    'q' : city,
    'units' : 'metric',
    'appid' : api_key,
}
responce = requests.get(base_url, params = params)
weather = {
    'City' : city,
    'Temperature' : f"{responce.json()['main']['temp']} C",
    'Weather conditions' : responce.json()['weather'][0]['description']
}
pprint(weather)