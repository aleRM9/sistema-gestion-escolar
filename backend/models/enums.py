import enum

from sqlalchemy.dialects.postgresql import ENUM as PgEnum

class EstadoRecibo(str, enum.Enum):
    pendiente = "pendiente"
    pagado = "pagado"

class MetodoPago(str, enum.Enum):
    efectivo = "efectivo"
    transferencia = "transferencia"
    pago_movil = "pago_movil"
    zelle = "zelle"
    binance = "binance"
    punto_venta = "punto_venta"

estado_recibo_enum = PgEnum(EstadoRecibo, name="estado_recibo", create_type=False)
metodo_pago_enum = PgEnum(MetodoPago, name="metodos_pago", create_type=False)
