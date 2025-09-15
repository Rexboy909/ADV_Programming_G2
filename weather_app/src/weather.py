# Simple Weather API class
import requests

class WeatherAPI:
    # This logic isn't needed for the starter, but added for later logic.
    """"
    apiKey = "API_KEY_HERE"

    def __init__(self, apiKey=None):
        if apiKey:
            self.apiKey = apiKey

    @staticmethod # This makes the method static, so it belongs to the class, not the object it creates
    def buildRequestUrl(cityName: str) -> str:
        return f"https://api.openweathermap.org/data/2.5/weather?q={cityName}&appid={WeatherAPI.apiKey}&units=imperial"

    def getWeatherData(self, cityName: str) -> dict:
        url = self.buildRequestUrl(cityName)
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            print(f"Current temperature in {cityName}: {data['main']['temp']}°F")
            return data
        print(f"Failed to get weather data for {cityName}.")
        return {}
    """
    # For the starter, we can have a simple method to get user input and display weather data
    @staticmethod # This makes the method static, so it belongs to the class, not the object it creates if we were creating an object but there are examples of this in the logic above
    def displayForStarter():
        print("Please enter a location to get the current weather data.\n")
        cityName = input("Location: ")
        print(f"Fetching weather data for {cityName.strip()}...\n")
WeatherAPI.displayForStarter()