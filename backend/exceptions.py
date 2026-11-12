"""
MODIFICADO: C5 debe ser agrgados al main.py ya que si no todo se vuelve error 500 caida de servidor dejo el modelo 
del cuerpo para el main.

@app.exception_handler(NoEncontrado)
async def no_encontrado_handler(request: Request, exc: NoEncontrado):
    \"""Captura tu excepción NoEncontrado y la traduce en un HTTP 404 limpio.\"""
    return JSONResponse(
        status_code=404,
        content={"detail": exc.detalle}
    )

@app.exception_handler(Conflicto)
async def conflicto_handler(request: Request, exc: Conflicto):
    \"""Captura tu excepción Conflicto y la traduce en un HTTP 409 limpio.\"""
    return JSONResponse(
        status_code=409,
        content={"detail": exc.detalle}
    )


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
