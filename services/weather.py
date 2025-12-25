import requests

# How to get API key:
# 1) Create free account at openweathermap.org
# 2) Copy your API key and paste below
OPENWEATHER_API_KEY = "a63ef996abdb5dbf7e1884ad3c0203cd"

def _get_city_coords(city: str):
    """Get lat/lon for city (OpenWeather Geocoding API)."""
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OPENWEATHER_API_KEY}"
    r = requests.get(url, timeout=10)
    data = r.json()
    if not data:
        return {"error": f"City '{city}' not found"}
    return {"lat": data[0]["lat"], "lon": data[0]["lon"]}

def get_weather(city: str):
    """
    Returns dict {temp, humidity, rainfall, city}
    temp (°C), humidity (%), rainfall (mm in last 1h if available)
    """
    if not OPENWEATHER_API_KEY or "PUT_YOUR_API_KEY_HERE" in OPENWEATHER_API_KEY:
        return {"error": "OpenWeather API key missing in services/weather.py"}

    coords = _get_city_coords(city)
    if "error" in coords:
        return coords

    lat, lon = coords["lat"], coords["lon"]
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        return {"error": f"Weather API error: {r.text}"}

    data = r.json()
    temp = data.get("main", {}).get("temp")
    humidity = data.get("main", {}).get("humidity")
    rainfall = 0.0
    # rainfall can be under "rain":{"1h": x}
    try:
        rainfall = float(data.get("rain", {}).get("1h", 0.0))
    except Exception:
        rainfall = 0.0

    return {
        "temp": temp,
        "humidity": humidity,
        "rainfall": rainfall,
        "city": city
    }
