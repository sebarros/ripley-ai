from langchain_core.tools import Tool
from backend.agent.api_clients import WeatherAPIClient
from langsmith import traceable
import re
import json
import requests

weather_client = WeatherAPIClient()


# =========================
# WEATHER TOOL
# =========================
@traceable(name="tool_weather")
def weather_tool(city: str):

    city = city.lower().strip()

    # Eliminar frases comunes
    city = re.sub(
        r"(cual es el|cuál es el|como esta el|cómo está el|que clima hay en|qué clima hay en|clima en|tiempo en|temperatura en)",
        "",
        city
    )

    city = city.strip()

    # Buscar ciudades conocidas
    known_cities = [
        "puerto montt",
        "santiago",
        "temuco",
        "osorno"
    ]

    detected_city = next(
        (c for c in known_cities if c in city),
        city
    )

    print("DEBUG CITY CLEAN:", detected_city)

    data = weather_client.get_weather(detected_city)

    print("DEBUG WEATHER RAW:", data)

    if not data or "error" in data:
        return {
            "city": detected_city,
            "temperature": "No disponible",
            "windspeed": "No disponible"
        }

    return {
        "city": data.get("city", detected_city),
        "temperature": data.get("temperature", "N/A"),
        "windspeed": data.get("windspeed", "N/A")
    }

# =========================
# LOAD LOCAL CATALOG
# =========================
def load_local_products():
    with open("data/products.json", "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# FAKESTORE API
# =========================
def load_fakestore_products():
    try:
        r = requests.get("https://fakestoreapi.com/products")
        return r.json()
    except:
        return []


# =========================
# SEARCH HYBRID
# =========================
@traceable(name="tool_search_product")
def search_product_tool(query: str):

    query = query.lower().strip()

    local = load_local_products()
    remote = load_fakestore_products()

    keywords = query.split()

    # CATÁLOGO LOCAL
    local_results = [
        {
            "nombre": p["name"],
            "precio_clp": p["price_clp"],
            "categoria": p["category"],
            "source": "local"
        }
        for p in local
        if any(
            k in p["name"].lower()
            or k in p["category"].lower()
            for k in keywords
        )
    ]

    # FAKESTORE
    remote_results = [
        {
            "nombre": p["title"],
            "precio_clp": int(float(p["price"]) * 900),
            "categoria": p["category"],
            "source": "fakestore"
        }
        for p in remote
        if any(
            k in p["title"].lower()
            or k in p["category"].lower()
            for k in keywords
        )
    ]

    results = local_results + remote_results

    if not results:
        results = local[:5]

    return results


# =========================
# LIST PRODUCTS
# =========================
@traceable(name="tool_list_products")
def list_products_tool(_):
    
    local = load_local_products()
    remote = load_fakestore_products()

    return {
        "local": local[:20],
        "fakestore": remote[:10]
    }


# =========================
# TOOL REGISTRY
# =========================
TOOL_LIST = [
    Tool(name="weather", func=weather_tool, description="Clima"),
    Tool(name="search_product", func=search_product_tool, description="Buscar productos"),
    Tool(name="list_products", func=list_products_tool, description="Listar productos")
]

TOOL_MAP = {t.name: t for t in TOOL_LIST}