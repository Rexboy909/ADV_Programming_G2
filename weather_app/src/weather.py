import requests  # Library to send HTTP requests to websites or APIs

API_KEY = "04b2c70f5678cb788cb9d62c0325ef32"
CITY = "Salt Lake City"

class WeatherAPI:
    # Base URL for OpenWeatherMap API 
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str):
        # Store the API key when we create a WeatherAPI object
        self.api_key = api_key
        # Cache dictionary, this saves results so we don’t keep calling the API for the same city
        self.cache = {}

    def _build_url(self, city: str) -> str:
        # Helper function that builds the full request URL using the base URL, city, and API key.
        return f"{self.BASE_URL}?q={city}&appid={self.api_key}&units=imperial"

    def _fetch(self, city: str) -> dict:
        
        # This function sends the request to the API.
        # If we've already fetched this city before, use the cached data.
        # Otherwise, make a new request and store the result in the cache.
        
        if city in self.cache:
            return self.cache[city] 

        # Make a GET request to the API
        r = requests.get(self._build_url(city))

        # Check if request was successful the status code 200 means the request worked
        
        if r.status_code == 200:
            data = r.json()         
            self.cache[city] = data 
            return data

        # If something goes wrong, print an error and return an empty dict
        print(f"Failed to fetch data for {city} (status {r.status_code})")
        return {}

    def get_weather(self, city: str) -> None:
        
        #Prints the current temperature for a given city.
        #Uses the _fetch function to get the weather data.
        
        data = self._fetch(city)
        if data:
            print(f"Current temperature in {city}: {data['main']['temp']}F")

    def get_humidity(self, city: str) -> None:
        
        #Prints the current humidity for a given city.
        #Also uses the _fetch function, so it avoids duplicate requests.
        data = self._fetch(city)
        if data:
            print(f"Current humidity in {city}: {data['main']['humidity']}%")
            return data["main"]["humidity"]




api = WeatherAPI(API_KEY)   # Creates a WeatherAPI object
api.get_weather(CITY)       
api.get_humidity(CITY)      
