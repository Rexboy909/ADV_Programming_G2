import requests

class WeatherAPI:
    apiKey = "API_KEY_HERE"

    def __init__(self, apiKey=None):
        if apiKey:
            self.apiKey = apiKey

    @staticmethod
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

    @staticmethod
    def calcFeelsLike(temp: float, humidity: float) -> float:
        feels_like = temp + humidity * 0.1
        print(f"Feels like temperature: {feels_like:.1f}°F")
        return feels_like

    @staticmethod
    def displayForStarter():
        print("Please enter a location to get the current weather data.\n")
        cityName = input("Location: ")
        print(f"Fetching weather data for {cityName.strip()}...\n")

    @staticmethod
    def fahrenheitToCelsius(temp: float) -> float:
        celsius = (temp - 32) * 5 / 9
        print(f"{temp}°F is {celsius:.1f}°C")
        return celsius

    @staticmethod
    def isHumid(humidity: float) -> bool:
        result = humidity > 70
        print(f"Humidity {humidity}% is considered {'high' if result else 'normal'}")
        return result


WeatherAPI.displayForStarter()
