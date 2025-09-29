import requests
from typing import Optional


API_KEY = '04b2c70f5678cb788cb9d62c0325ef32' #Hard coded for simplicity right now
CITY = 'Salt Lake City'
URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=imperial'


response = requests.get(URL)
data = response.json()

'''
if response.status_code == 200:
    temp = data['main']['temp']
    description = data['weather'][0]['description']
    print(f"Current temperature in {CITY}: {temp}°F")
    print(f"Weather description: {description}")
else:
    print("Error fetching data:", data.get("message", "Unknown error"))
'''

class WeatherAPI:
    apiKey = API_KEY
    cityName = CITY
    response = requests.get(URL)
    data = response.json()

    @staticmethod
    def buildRequestUrl(cityName: str) -> str:
        return f"https://api.openweathermap.org/data/2.5/weather?q={cityName}&appid={WeatherAPI.apiKey}&units=imperial"

    def getWeatherData(self, cityName: str) -> dict:
        url = self.buildRequestUrl(cityName)
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            self._last_city = cityName
            self._last_data = data
            print(f"Current temperature in {cityName}: {data['main']['temp']}°F")
            return data
        print(f"Failed to get weather data for {cityName}.")
        return {}

    def getHumidity(self, cityName: str):
        # if we've already fetched data for this city, reuse it instead of calling the API again
        data = None
        if getattr(self, '_last_city', None) == cityName and getattr(self, '_last_data', None):
            data = self._last_data
        else:
            data = self.getWeatherData(cityName)

        if not data:
            print(f"No weather data available for {cityName}.")
            return None
        
        humidity = data.get('main', {}).get('humidity')
        if humidity is None:
            print(f"Humidity value missing in API response for {cityName}.")
            return None
        print(f"Current humidity in {cityName}: {humidity}%")
        return humidity

#if __name__ == "__main__":
api = WeatherAPI()
api.getWeatherData(CITY)
hum = api.getHumidity(CITY)
