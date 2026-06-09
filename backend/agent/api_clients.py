import requests
from urllib.parse import quote


class WeatherAPIClient:

    GEO = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, city: str):

        # =========================
        # CLEAN INPUT
        # =========================
        city = city.lower().strip()

        city = city.replace("clima en", "")
        city = city.replace("tiempo en", "")
        city = city.replace("temperatura en", "")
        city = city.replace("que clima hay en", "")
        city = city.strip()

        print("DEBUG CITY FINAL:", city)

        # =========================
        # GEO REQUEST
        # =========================
        geo = requests.get(self.GEO, params={
            "name": city,
            "count": 3,        
            "language": "es"
        }).json()

        print("DEBUG GEO:", geo)

        if "results" not in geo or not geo["results"]:
            return {
                "error": "city_not_found",
                "city": city
            }

        city_data = geo["results"][0]

        # =========================
        # WEATHER REQUEST
        # =========================
        weather = requests.get(self.WEATHER, params={
            "latitude": city_data["latitude"],
            "longitude": city_data["longitude"],
            "current_weather": True
        }).json().get("current_weather", {})

        return {
            "city": city_data["name"],
            "temperature": weather.get("temperature", "N/A"),
            "windspeed": weather.get("windspeed", "N/A")
        }

class ProductAPIClient:

    BASE = "https://fakestoreapi.com"

    def get_products(self):
        return requests.get(f"{self.BASE}/products").json()