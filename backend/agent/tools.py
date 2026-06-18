from langchain_core.tools import Tool
from backend.agent.api_clients import WeatherAPIClient, ProductAPIClient
import re

weather_client = WeatherAPIClient()
product_client = ProductAPIClient()


# =========================
# WEATHER TOOL
# =========================
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
# PRODUCT SEARCH
# =========================
def search_product_tool(query: str):

    products = product_client.get_products()

    results = [
        p for p in products
        if query.lower() in p["title"].lower()
    ]

    if not results:
        results = products[:5]

    out = "🛍️ Productos:\n"
    for p in results:
        out += f"- {p['title']} | ${p['price']}\n"

    return out


# =========================
# LIST PRODUCTS
# =========================
def list_products_tool(_):

    products = product_client.get_products()

    out = "🛍️ Catálogo:\n"
    for p in products[:10]:
        out += f"- {p['title']} | ${p['price']}\n"

    return out


# =========================
# TOOL REGISTRY
# =========================
TOOL_LIST = [
    Tool(name="weather", func=weather_tool, description="Clima"),
    Tool(name="search_product", func=search_product_tool, description="Buscar productos"),
    Tool(name="list_products", func=list_products_tool, description="Listar productos")
]

TOOL_MAP = {t.name: t for t in TOOL_LIST}