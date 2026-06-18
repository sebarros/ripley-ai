import requests


class WeatherAPIClient:


    GEO="https://geocoding-api.open-meteo.com/v1/search"
    WEATHER="https://api.open-meteo.com/v1/forecast"


    def get_weather(self, city):

        city=city.lower().strip()


        geo=requests.get(
            self.GEO,
            params={
                "name":city,
                "count":1,
                "language":"es"
            }
        ).json()


        if "results" not in geo:

            return None


        c=geo["results"][0]


        weather=requests.get(
            self.WEATHER,
            params={
                "latitude":c["latitude"],
                "longitude":c["longitude"],
                "current_weather":True
            }
        ).json()


        w=weather["current_weather"]


        return {

            "city":c["name"],
            "temperature":w["temperature"],
            "windspeed":w["windspeed"]

        }



class ProductAPIClient:


    BASE="https://fakestoreapi.com"



    translations={

        "men's clothing":"Ropa hombre",
        "women's clothing":"Ropa mujer",
        "jewelery":"Joyería",
        "electronics":"Electrónica"

    }


    def get_products(self):


        products=requests.get(
            f"{self.BASE}/products"
        ).json()



        for p in products:

            category=p.get("category","")

            p["category"]=self.translations.get(
                category,
                category
            )


        return products