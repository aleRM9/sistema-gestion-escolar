"""CAMBIO: archivo nuevo.

Errores de negocio. Los controllers los lanzan y main.py los convierte en
respuestas HTTP. Por qué: antes cada ruta repetía "if x is None: raise
HTTPException(404)" y además se usaba 404 para duplicados (incorrecto).
Ahora: NoEncontrado -> 404, Conflicto -> 409, y las rutas quedan más cortas.
"""


class ErrorDeNegocio(Exception):
    def __init__(self, detalle: str):
        super().__init__(detalle)
        self.detalle = detalle


class NoEncontrado(ErrorDeNegocio):
    """El recurso pedido no existe (HTTP 404)."""


class Conflicto(ErrorDeNegocio):
    """La operación choca con datos existentes: duplicado, registros
    relacionados, etc. (HTTP 409)."""
