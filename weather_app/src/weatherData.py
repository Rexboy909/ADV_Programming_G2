import weather

# Module-level defaults; these will be updated by fetch_for_city
temp = "N/A"
tempMin = "N/A"
tempMax = "N/A"
humidity = "N/A"
windSpeed = "N/A"
windDir = "N/A"
precipitation = "N/A"


def fetch_for_city(city: str) -> dict:
    """Fetch weather for `city` using weather.api and update module-level variables.

    Returns a dict with keys: temp, tempMin, tempMax, humidity, windSpeed, windDir, precipitation
    Any missing values are set to 'N/A'.
    """
    global temp, tempMin, tempMax, humidity, windSpeed, windDir, precipitation
    if not city:
        return {
            'temp': temp,
            'tempMin': tempMin,
            'tempMax': tempMax,
            'humidity': humidity,
            'windSpeed': windSpeed,
            'windDir': windDir,
            'precipitation': precipitation,
        }

    try:
        t = weather.api.get_temperature(city)
    except Exception:
        t = "N/A"
    try:
        tmin = weather.api.get_temp_min(city)
    except Exception:
        tmin = "N/A"
    try:
        tmax = weather.api.get_temp_max(city)
    except Exception:
        tmax = "N/A"
    try:
        hum = weather.api.get_humidity(city)
    except Exception:
        hum = "N/A"
    try:
        ws = weather.api.get_wind_speed(city)
    except Exception:
        ws = "N/A"
    try:
        wd = weather.api.get_wind_dir(city)
    except Exception:
        wd = "N/A"

    # precipitation isn't provided by the current API wrapper; leave as N/A
    pr = "N/A"

    temp = t
    tempMin = tmin
    tempMax = tmax
    humidity = hum
    windSpeed = ws
    windDir = wd
    precipitation = pr

    return {
        'temp': temp,
        'tempMin': tempMin,
        'tempMax': tempMax,
        'humidity': humidity,
        'windSpeed': windSpeed,
        'windDir': windDir,
        'precipitation': precipitation,
    }
# print(f"Temperature: {temp}°F")
# print(f"Min Temperature: {tempMin}°F")
# print(f"Max Temperature: {tempMax}°F")
# print(f"Humidity: {humidity}%")
# print(f"Wind Speed: {windSpeed} m/s")
# print(f"Wind Direction: {windDir}°")
# print(f"Precipitation: {precipitation}")