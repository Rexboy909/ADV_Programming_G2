import weather
try:
    temp = weather.api.get_temperature(weather.CITY)
except KeyError:
    temp = "N/A"
try:
    tempMin = weather.api.get_temp_min(weather.CITY)
except KeyError:
    tempMin = "N/A"
try:    
    tempMax = weather.api.get_temp_max(weather.CITY)
except KeyError:
    tempMax = "N/A"
try:
    humidity = weather.api.get_humidity(weather.CITY)
except KeyError:
    humidity = "N/A"
try:
    windSpeed = weather.api.get_wind_speed(weather.CITY)
except KeyError:
    windSpeed = "N/A"
try:    
    windDir = weather.api.get_wind_dir(weather.CITY)
except KeyError:
    windDir = "N/A"
try:
    precipitation = "N/A"
except KeyError:
    precipitation = "N/A"
# print(f"Temperature: {temp}°F")
# print(f"Min Temperature: {tempMin}°F")
# print(f"Max Temperature: {tempMax}°F")
# print(f"Humidity: {humidity}%")
# print(f"Wind Speed: {windSpeed} m/s")
# print(f"Wind Direction: {windDir}°")
# print(f"Precipitation: {precipitation}")