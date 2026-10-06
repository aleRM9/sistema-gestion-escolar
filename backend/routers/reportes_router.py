from fastapi import APIRouter, Body
from backend.controllers import reportes_controller
from typing import Optional

from backend.schemas.reportes_schema import(
    DetallePerLapso,
    DetalleFinAnio,
    CobroDeudas,
    RecibosPendientes2, 
    ReporteAcademico,
    ReporteFinanciaro
)

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

# CRON
@router.get(
        "/cron/fin-lapso",
        response_model=list[DetallePerLapso]
)
async def obtener_notas_fin_lapso(lapso: int, periodo_actual:str):
    return await reportes_controller.obtenerNotasFinLapso(lapso, periodo_actual)

@router.get( "/cron/fin-anio", response_model=list[DetalleFinAnio])
async def obtener_notas_fin_anio(periodo_actual: str):
    return await reportes_controller.obtenerNotasFinAnio(periodo_actual)

@router.post("/cron/crear-cobros")
async def generar_cobros(periodo_actual: str, mes: int, mensualidades: list[float]):
    return await reportes_controller.generarCobros(periodo_actual, mensualidades, mes)

@router.get("/cron/cobrar-deuda", response_model=list[CobroDeudas])
async def cobrar_deuda():
    return await reportes_controller.cobrarDeuda()

@router.get("/cron/recibos-pendientes", response_model=list[RecibosPendientes2])
async def obtener_recibos_pendientes():
    return await reportes_controller.obtenerRecibosPendientes()

# Reportes

@router.get("/academico", response_model=ReporteAcademico)
async def obtener_reporte_academico(
    periodo_escolar: Optional[str]= None,
    lapso_inicio: Optional[int] = None,
    lapso_fin: Optional[int] = None,
    grado: Optional[int] = None,
    seccion: Optional[str] = None,
    materia: Optional[str] = None,
    profesor: Optional[str] = None
    ):
    return await reportes_controller.obtenerInformacion(periodo_escolar, lapso_inicio, lapso_fin, grado, seccion, materia, profesor)

@router.get("/finanzas", response_model=ReporteFinanciaro)
async def obtener_reporte_finanzas(limit: Optional[int] = None):
    return await reportes_controller.ObtenerDatosFinanzas(limit)



