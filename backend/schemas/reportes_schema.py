from pydantic import BaseModel
from typing import List, Union
 

# Desarrollando el envio de la informacion 
# de los estudiantes luego de finalizar el lapso
class Materias(BaseModel): 
    nombre:str
    promedio: float


class NotasDetalle(BaseModel):
    materia: str
    lapso: int
    calificacion : float

class DetallePerLapso(BaseModel):

    nombre_alumno:str
    nombre_representante: str
    correo_representante:str
    periodo_escolar: str
    anio_cursando: int
    lapso_culminado: int
    notas: List[NotasDetalle]

class DetalleFinAnio(BaseModel):
    nombre_alumno:str
    nombre_representante: str
    correo_representante:str
    periodo_escolar: str
    anio_cursando: int
    promedio_periodo: float
    notas: List[NotasDetalle]
    materias_reparar: List[Materias]

class RecibosPendientes(BaseModel):
    id_recibo: int
    id_alumno:int
    nombre_alumno:str
    grado:int
    concepto:str
    monto_pagado:float
    monto_total: float
    monto_faltante: float
    # Falta la fecha de cobro


class RecibosPendientes2(BaseModel):
    id_recibo: int
    id_alumno:int
    id_representante:int
    nombre_alumno:str
    nombre_representante: str
    correo_representante:str
    concepto:str
    monto_total: float
    estado_recibo:str



class CobroDeudas(BaseModel):
    representante_id: int
    nombre_representante:str
    deuda:float
    correo:str
    recibos:List[RecibosPendientes]

class ReporteAcademico(BaseModel):
    filtro_periodo_escolar: str 
    filtro_lapso_inicio: int = 1
    filtro_lapso_fin: int = 3
    filtro_grado:Union[int, str] 
    filtro_seccion: str
    filtro_materia: str 
    filtro_profesor:str 
    cantidad_alumnos: int
    cantidad_aprobados: int
    cantidad_desaprobados: int
    mejor_nota: float
    peor_nota: float
    promedio_notas: float

class DeudaMes(BaseModel):
    monto_deuda:float
    mes:  int
    year: int
class DeudaRepresentante(BaseModel):
    nombre:str
    representante_id: int
    monto_deuda: float
    
class DeudaAlumno(BaseModel):
    nombre:str
    alumno_id: int
    #representante_id: int
    monto_deuda: float
    cantidad_recibos: int
class DeudaCurso(BaseModel):
    curso_id: int
    monto_deuda: float
    cantidad_recibos: int
class DeudaGrado(BaseModel):
    grado: int
    monto_deuda: float
    cantidad_recibos: int

class ReporteFinanciaro(BaseModel):
    cantidad_total_recibos_emitidos: int
    monto_general_generado: float
    monto_total_pagado: float
    monto_deuda_total: float
    cantidad_recibos_deuda: int
    deudas_meses: List[DeudaMes]
    deudas_representantes: List[DeudaRepresentante]
    deudas_alumnos: List[DeudaAlumno]
    deudas_cursos: List[DeudaCurso]
    deudas_grados: List[DeudaGrado]



