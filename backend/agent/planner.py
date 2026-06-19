import re


class Planner:

    def create_plan(self, query: str):

        q = query.lower()

        # CLIMA
        if re.search(
            r"clima|tiempo|temperatura|pronostico|pronóstico|weather",
            q
        ):
            return {"tool": "weather"}

        # PRODUCTOS
        if re.search(
            r"ropa|polera|poleron|polerón|jean|jeans|zapatilla|zapatillas|chaqueta|parka|vestir|iphone|notebook|televisor|celular|telefono|teléfono|audifono|audífono|mochila|reloj|perfume",
            q
        ):
            return {"tool": "search_product"}

        # LISTADO
        if re.search(
            r"catálogo|catalogo|lista|productos",
            q
        ):
            return {"tool": "list_products"}

        return {"tool": None}