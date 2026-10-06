from sqlalchemy.future import select
from backend.database import get_db_session 
import models.reportes_model as modelo
from backend.schemas.reportes_schema import NotasDetalle, DetallePerLapso, DetalleFinAnio, Materias, RecibosPendientes, CobroDeudas, RecibosPendientes2, ReporteAcademico, DeudaMes, DeudaRepresentante,DeudaAlumno,DeudaCurso,DeudaGrado, ReporteFinanciaro
from sqlalchemy import select, extract, func, and_

from typing import Optional


async def obtenerNotasFinLapso(lapso:int, periodo_actual: str):
    async with get_db_session() as db:
        consulta =  select(

        modelo.Curso.curso_id,
        modelo.Curso.grado,
        modelo.Alumno.alumno_id,
        modelo.Alumno.nombre.label('nombre_alumno'),
        modelo.Representante.nombre.label('nombre_representante'),
        modelo.Representante.correo
        ).select_from(modelo.Curso).join(modelo.Alumno, modelo.Alumno.curso_id == modelo.Curso.curso_id).join(modelo.Representante, modelo.Representante.representante_id == modelo.Alumno.representante_id).where(modelo.Curso.periodo_escolar == periodo_actual)
        lista_datos = (await db.execute(consulta)).mappings().all()

        if not lista_datos:
            return []
        ids_alumnos = []
        for dato in lista_datos:
            ids_alumnos.append(dato['alumno_id'])
        consulta_notas =  select(
        modelo.Materia.nombre,
        modelo.Inscripcion.alumno_id ,
        modelo.Nota.calificacion,
        modelo.Nota.lapso
        ).select_from(modelo.Inscripcion).join(modelo.Nota, modelo.Nota.inscripcion_id == modelo.Inscripcion.inscripcion_id).join(modelo.Materia ,modelo.Materia.materia_id == modelo.Inscripcion.materia_id).join(modelo.Curso, modelo.Curso.curso_id == modelo.Inscripcion.curso_id).where(modelo.Inscripcion.alumno_id.in_(ids_alumnos), modelo.Nota.lapso <= lapso,modelo.Curso.periodo_escolar== periodo_actual)

        notas = (await db.execute(consulta_notas)).mappings().all()
        detaller_estudiantes = []
        for dato in lista_datos:
            objeto_notas = []
            for nota in notas:
                if nota['alumno_id'] == dato['alumno_id']:
                    detalle_nota = NotasDetalle(materia=nota['nombre'], lapso=nota['lapso'], calificacion=float(nota['calificacion']))
                    objeto_notas.append(detalle_nota)
            detalle = DetallePerLapso(
                nombre_alumno=dato['nombre_alumno'],
                nombre_representante= dato['nombre_representante'],
                correo_representante=dato['correo'],
                periodo_escolar=periodo_actual,
                anio_cursando= dato['grado'],
                lapso_culminado=lapso,
                notas=objeto_notas
                )
            detaller_estudiantes.append(detalle)
        return detaller_estudiantes

async def obtenerNotasFinAnio(periodo_actual: str):
    async with get_db_session() as db:
        consulta_estudiantes = select(
            modelo.Curso.curso_id,
            modelo.Alumno.alumno_id,
            modelo.Alumno.nombre.label('nombre_alumno'),
            modelo.Representante.nombre.label('nombre_representante'),
            modelo.Representante.correo,
            modelo.Curso.grado
        ).select_from(modelo.Curso).join(modelo.Alumno, modelo.Alumno.curso_id == modelo.Curso.curso_id).join(modelo.Representante, modelo.Alumno.representante_id ==  modelo.Representante.representante_id).where(modelo.Curso.periodo_escolar == periodo_actual)
        datos_alumnos = (await db.execute(consulta_estudiantes)).mappings().all()
        if not (datos_alumnos):
            return []
        alumnos_ids=[]
        for alumno in datos_alumnos:
            alumnos_ids.append(alumno['alumno_id'])

        consulta_notas = select(
            modelo.Materia.nombre,
            modelo.Nota.calificacion,
            modelo.Nota.lapso,
            modelo.Inscripcion.alumno_id
        ).select_from(modelo.Inscripcion).join(modelo.Nota, modelo.Nota.inscripcion_id == modelo.Inscripcion.inscripcion_id).join(modelo.Materia, modelo.Materia.materia_id == modelo.Inscripcion.materia_id).join(modelo.Curso, modelo.Curso.curso_id == modelo.Inscripcion.curso_id).where(modelo.Inscripcion.alumno_id.in_(alumnos_ids), modelo.Curso.periodo_escolar==periodo_actual)
        notas = (await db.execute(consulta_notas)).mappings().all()

        notas_materias = {}
        notas_alumnos = {}

        for alumno in datos_alumnos:
            notas_alumnos[alumno['alumno_id']]= []
            notas_materias[alumno['alumno_id']] = {}

        for nota in notas:
            alumno_id = nota['alumno_id']
            materia = nota['nombre']
            calificacion = float(nota['calificacion'])
            notas_alumnos[alumno_id].append(calificacion)
            if materia not in notas_materias[alumno_id]:
                notas_materias[alumno_id][materia].append(calificacion)
        promedios = {}

        for alumno_id, lista_notas in notas_alumnos.items():
            longitud = len(lista_notas)
            promedio = 0
            for nota in lista_notas:
                promedio+= float(nota)
            promedio/=longitud
            promedios[alumno_id] = promedio
        detalles_estudiantes = []

        for dato in datos_alumnos:
            detalle_notas = []
            materias_reparar = []
            for materia, notas_int in notas_materias[dato['alumno_id']].items():
                promedio_materia =  sum(notas_int)/len(notas_int)
                if promedio_materia <10:
                    mat =  Materias(
                        nombre=materia,
                        promedio=promedio_materia
                    )
                    materias_reparar.append(mat)
            for nota in notas:
                if nota['alumno_id'] == dato['alumno_id']:
                    detalle_nota = NotasDetalle(
                        materia=nota['nombre'],
                        lapso=nota['lapso'],
                        calificacion=float(nota['calificacion'])
                    )
                    detalle_notas.append(detalle_nota)
            detalle = DetalleFinAnio(
                nombre_alumno=dato['nombre_alumno'],
                nombre_representante=dato['nombre_representante'],
                correo_representante= dato['correo'],
                periodo_escolar= periodo_actual,
                anio_cursando=dato['grado'],
                promedio_periodo=float(promedios[dato['alumno_id']]),
                notas=detalle_notas,
                materias_reparar=materias_reparar

            )
            detalles_estudiantes.append(detalle)
        return detalles_estudiantes

async def generarCobros(periodo_actual:str, mensualidades:list[float], mes:int):
    async with get_db_session() as db:

        consulta_alumnos = select(
                modelo.Alumno.alumno_id,
                modelo.Curso.grado
            ).select_from(modelo.Alumno).join(modelo.Curso, modelo.Curso.curso_id ==  modelo.Alumno.curso_id).where(modelo.Curso.periodo_escolar == periodo_actual)
        datos = (await db.execute(consulta_alumnos)).mappings().all()

        if not datos:
            return []
        cobros = []
        for dato in datos:
            alumno_id = dato['alumno_id']
            grado = dato['grado']
            mes_actual = meses(mes) # falta la funcio
            cobro =  modelo.ReciboCobro(
                alumno_id=alumno_id,
                concepto=f"Mensualidad {mes_actual}",
                monto_total=mensualidades[grado-1]
            )
            cobros.append(cobro)
        db.add_all(cobros)
        await db.commit()
        return {
            "message": f"Se generaron exitosamente {len(cobros)} recibos de cobro",
            "cantidad_recibos": len(cobros)
        }
def meses(mes):
    meses = [
    "Enero", "Febrero", "Marzo", "Abril", 
    "Mayo", "Junio", "Julio", "Agosto", 
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    return meses[mes-1]

async def cobrarDeuda():
    async with get_db_session() as db:
        consulta = select(
            modelo.Representante.representante_id,
            modelo.Representante.nombre,
            modelo.Representante.monto_deuda,
            modelo.Representante.correo
        ).select_from(modelo.Representante).where(modelo.Representante.monto_deuda>0)
        representantes_deudores = (await db.execute(consulta)).mappings().all()
        if not representantes_deudores:
            return []
        ids_representantes = []
        for representante in representantes_deudores:
            ids_representantes.append(representante['representante_id'])

        consulta_recibos_cobro = select(
            modelo.ReciboCobro.recibo_id,
            modelo.Alumno.representante_id,
            modelo.Alumno.alumno_id,
            modelo.Alumno.nombre,
            modelo.Curso.grado,
            modelo.ReciboCobro.concepto,
            modelo.ReciboCobro.monto_total,
            modelo.ReciboCobro.monto_pagado
        ).select_from(modelo.ReciboCobro).join(modelo.Alumno, modelo.Alumno.alumno_id == modelo.ReciboCobro.alumno_id).join(modelo.Curso, modelo.Curso.curso_id == modelo.Alumno.curso_id).where(modelo.Alumno.representante_id.in_(ids_representantes), modelo.ReciboCobro.estado == 'pendiente', modelo.ReciboCobro.monto_pagado < modelo.ReciboCobro.monto_total)
        recibos_cobro = (await db.execute(consulta_recibos_cobro)).mappings().all()
        objetos_representantes = []
        for representante in representantes_deudores:
            recibos = []
            for recibo in recibos_cobro:
                if recibo['representante_id'] == representante['representante_id']:
                    objeto_recibo = RecibosPendientes(
                        id_recibo=recibo['recibo_id'],
                        id_alumno=recibo['alumno_id'],
                        nombre_alumno=recibo['nombre'],
                        grado=recibo['grado'],
                        monto_pagado=float(recibo['monto_pagado']),
                        monto_total=float(recibo['monto_total']),
                        monto_faltante= float(recibo['monto_total'])- float(recibo['monto_pagado'])
                        # Falta Fecha
                    )
                    recibos.append(objeto_recibo)
            objetos_representante = CobroDeudas(
                representante_id=representante['representante_id'],
                nombre_representante=representante['nombre'],
                deuda=float(representante['monto_deuda']),
                correo=representante['correo'],
                recibos=recibos
            )
            objetos_representantes.append(objetos_representante)
        return objetos_representantes

async def obtenerRecibosPendientes():
    async with get_db_session() as db:
        consulta_recibos = select(
            modelo.ReciboCobro.recibo_id,
            modelo.ReciboCobro.alumno_id,
            modelo.Representante.representante_id,
            modelo.Alumno.nombre.label('nombre_alumno'),
            modelo.ReciboCobro.concepto,
            modelo.ReciboCobro.estado,
            modelo.ReciboCobro.monto_total,
            modelo.Representante.nombre.label('nombre_representante'),
            modelo.Representante.correo

            ).select_from(modelo.ReciboCobro).join(modelo.Alumno, modelo.Alumno.alumno_id == modelo.ReciboCobro.alumno_id).join(modelo.Representante,modelo.Representante.representante_id == modelo.Alumno.representante_id).where(modelo.ReciboCobro.estado == 'pendiente')
        recibos_pendientes = (await db.execute(consulta_recibos)).mappings().all()
        if not recibos_pendientes:
            return []
        objeto_recibos_pendientes = []
        for recibo in recibos_pendientes:
            objeto_recibo = RecibosPendientes2(
                id_recibo=recibo['recibo_id'],
                id_alumno=recibo['alumno_id'],
                id_representante=recibo['representante_id'],
                nombre_alumno=recibo['nombre_alumno'],
                nombre_representante=recibo['nombre_representante'],
                correo_representante=recibo['correo'],
                concepto=recibo['concepto'],
                monto_total=recibo['monto_total'],
                estado_recibo=recibo['estado']
                )
            objeto_recibos_pendientes.append(objeto_recibo)
        return objeto_recibos_pendientes

async def obtenerInformacion(
        periodo_escolar: Optional[str] = None,
        lapso_inicio: Optional[int] = None,
        lapso_fin: Optional[int] = None,
        grado: Optional[int] = None,
        seccion: Optional[str]=None,
        materia: Optional[str]=None,
        profesor: Optional[str]= None,

):
    async with get_db_session() as db:
        consulta = (select(
            modelo.Nota.calificacion,
            modelo.Nota.lapso,
            modelo.Inscripcion.materia_id,
            modelo.Materia.nombre.label('nombre_materia'),
            modelo.Curso.grado,
            modelo.Curso.periodo_escolar,
            modelo.Curso.seccion,
            modelo.Inscripcion.alumno_id
        ).select_from(modelo.Nota).
        join(modelo.Inscripcion, modelo.Inscripcion.inscripcion_id == modelo.Nota.inscripcion_id)
        .join(modelo.Curso, modelo.Curso.curso_id == modelo.Inscripcion.curso_id)
        .join(modelo.Materia, modelo.Materia.materia_id== modelo.Inscripcion.materia_id)
        )
        if periodo_escolar is not None:
            consulta = consulta.where(modelo.Curso.periodo_escolar == periodo_escolar)
            if lapso_inicio is not None and lapso_fin is not None:
                consulta =consulta.where(modelo.Nota.lapso >= lapso_inicio, modelo.Nota.lapso <=lapso_fin)

        if grado is not None:
            consulta= consulta.where(modelo.Curso.grado == grado)
        if seccion is not None:
            consulta =consulta.where(modelo.Curso.seccion == seccion)
        if materia is not None:
            consulta = consulta.where(modelo.Materia.nombre == materia)
        if profesor is not None:
            consulta = consulta.join(modelo.CursoProfesor, and_(modelo.CursoProfesor.materia_id == modelo.Inscripcion.materia_id, modelo.CursoProfesor.curso_id == modelo.Inscripcion.curso_id)).join(modelo.Profesor, modelo.Profesor.profesor_id == modelo.CursoProfesor.profesor_id).where(modelo.Profesor.nombre == profesor)
        notas = (await db.execute(consulta)).mappings().all()

        almuno_notas = {}

        for registro in notas:
            alumno_id = registro['alumno_id']
            calificacion =  float(registro['calificacion'])
            if alumno_id not in almuno_notas:
                almuno_notas[alumno_id] = []
            almuno_notas[alumno_id].append(calificacion)
        alumno_promedio = {}
        for alumno, lista_notas in almuno_notas.items():
            cantidad_calificaciones = len(lista_notas)
            promedio =  sum(lista_notas)/cantidad_calificaciones
            alumno_promedio[alumno] = promedio 
        aprobados = 0
        reprobados = 0
        mejor_promedio =0
        peor_promedio  =1000
        cantidad_total_alumnos = 0
        promedio_notas_total = 0
        for promedio in alumno_promedio.values():
            cantidad_total_alumnos +=1
            if promedio >=10:
                aprobados+=1
            else:
                reprobados+=1
            if promedio> mejor_promedio:
                mejor_promedio=promedio
            if promedio < peor_promedio:
                peor_promedio = promedio
            promedio_notas_total+=promedio
        promedio_notas_total = promedio_notas_total/cantidad_total_alumnos

        objeto_reporte = ReporteAcademico(

            filtro_periodo_escolar= (periodo_escolar if periodo_escolar else "TODOS"),
            filtro_lapso_inicio=(lapso_inicio if lapso_inicio else 1),
            filtro_lapso_fin=(lapso_fin if lapso_fin else 3),
            filtro_grado=(grado if grado else "TODOS"),
            filtro_seccion=(seccion if seccion else "TODAS"),
            filtro_materia=(materia if materia else "TODAS"),
            filtro_profesor=(profesor if profesor else "TODOS"),
            cantidad_alumnos=cantidad_total_alumnos,
            cantidad_aprobados=aprobados,
            cantidad_desaprobados=reprobados,
            mejor_nota=mejor_promedio,
            peor_nota=peor_promedio,
            promedio_notas=promedio_notas_total
        )
        return objeto_reporte

async def obtenerDatosFinanzas(limit:Optional[int] = None):
    async with get_db_session() as db:
        saldo_pendiente = func.sum(modelo.ReciboCobro.monto_total-modelo.ReciboCobro.monto_pagado)

        consulta_meses = select(
            func.count(modelo.ReciboCobro.recibo_id).label('cantidad_recibos'),
            saldo_pendiente.label('deuda'),
            extract('month', modelo.ReciboCobro.fecha_generacion).label('mes'),
            extract('year', modelo.ReciboCobro.fecha_generacion).label('year')
        ).select_from(modelo.ReciboCobro).where(modelo.ReciboCobro.estado == 'pendiente').group_by(extract('year',modelo.ReciboCobro.fecha_generacion), extract('month', modelo.ReciboCobro.fecha_generacion)).having(saldo_pendiente>0).order_by(saldo_pendiente.desc())
        consulta_representantes = select(
            modelo.Representante.nombre,
            modelo.Representante.representante_id,
            modelo.Representante.monto_deuda
        ).select_from(modelo.Representante).where(modelo.Representante.monto_deuda> 0).order_by(modelo.Representante.monto_deuda.desc())
        consulta_alumnos = (
            select(
                modelo.Alumno.nombre,
                modelo.Alumno.alumno_id,
                saldo_pendiente.label('deuda'),
                func.count(modelo.ReciboCobro.recibo_id).label('cantidad_recibos')
        
            ).select_from(modelo.ReciboCobro).join(modelo.Alumno, modelo.Alumno.alumno_id == modelo.ReciboCobro.alumno_id).where(modelo.ReciboCobro.estado == 'pendiente').group_by(modelo.Alumno.alumno_id, modelo.Alumno.nombre).having(saldo_pendiente> 0).order_by(saldo_pendiente.desc())
        )
        consulta_grados =  (
            select(
                modelo.Curso.grado,
                saldo_pendiente.label('deuda'),
                func.count(modelo.ReciboCobro.recibo_id).label('cantidad_recibos')
            ).select_from(modelo.ReciboCobro)
            .join(modelo.Alumno, modelo.Alumno.alumno_id == modelo.ReciboCobro.alumno_id)
            .join(modelo.Curso, modelo.Curso.curso_id == modelo.Alumno.curso_id).where(modelo.ReciboCobro.estado == 'pendiente')
            .group_by(modelo.Curso.grado).having(saldo_pendiente > 0)
            .order_by(saldo_pendiente.desc())
        )

        consulta_curso = (
            select(
                modelo.Curso.curso_id,
                func.count(modelo.ReciboCobro.recibo_id).label('cantidad_recibos'),
                saldo_pendiente.label('deuda')
            ).select_from(modelo.ReciboCobro).join(modelo.Alumno, modelo.Alumno.alumno_id == modelo.ReciboCobro.alumno_id)
            .join(modelo.Curso, modelo.Curso.curso_id == modelo.Alumno.curso_id).where(modelo.ReciboCobro.estado == 'pendiente')
            .group_by(modelo.Curso.curso_id).having(saldo_pendiente> 0).order_by(saldo_pendiente.desc())
        )
        consulta_general_deuda = select(func.count(modelo.ReciboCobro.recibo_id).label('total_recibos'),saldo_pendiente.label('deuda')).select_from(modelo.ReciboCobro).where(modelo.ReciboCobro.estado == 'pendiente')
        consulta_general =select(
            func.count(modelo.ReciboCobro.recibo_id).label('total_recibos'),
            func.sum(modelo.ReciboCobro.monto_total).label('monto_total_generado'),
            func.sum(modelo.ReciboCobro.monto_pagado).label('monto_total_pagado')
        ).select_from(modelo.ReciboCobro)

        if limit:
            consulta_meses= consulta_meses.limit(limit)
            consulta_curso =consulta_curso.limit(limit)
            consulta_grados=consulta_grados.limit(limit)
            consulta_representantes= consulta_representantes.limit(limit)
            consulta_alumnos = consulta_alumnos.limit(limit)
        deudas_mes = (await db.execute(consulta_meses)).mappings().all()
        deudas_representantes = (await db.execute(consulta_representantes)).mappings().all()
        deudas_alumnos = (await db.execute(consulta_alumnos)).mappings().all()
        deudas_cursos =  (await db.execute(consulta_curso)).mappings().all()
        deudas_grados = (await db.execute(consulta_grados)).mappings().all()
        deudas_general = (await db.execute(consulta_general_deuda)).mappings().first() or {}
        recibos_general =  (await db.execute(consulta_general)).mappings().first() or {}
        
        
        deudas_alumnos_objeto = []
        deudas_cursos_objeto = []
        deudas_grados_objeto = []
        deudas_representantes_objeto = []
        deudas_mes_objeto = []

        if deudas_alumnos:
            for deuda in deudas_alumnos:
                deuda_objeto = DeudaAlumno(
                    nombre=deuda['nombre'],
                    alumno_id=deuda['alumno_id'],
                    monto_deuda=float(deuda['deuda']),
                    cantidad_recibos=int(deuda['cantidad_recibos'])
                )
                deudas_alumnos_objeto.append(deuda_objeto)

        if deudas_mes:
            for deuda in deudas_mes:
                deuda_objeto = DeudaMes(
                    monto_deuda=float(deuda['deuda']),
                    mes=int(deuda['mes']),
                    year=int(deuda['year'])
                )
                deudas_mes_objeto.append(deuda_objeto)
        if deudas_representantes:
            for deuda in deudas_representantes:
                deuda_objeto = DeudaRepresentante(
                    representante_id=deuda['representante_id'],
                    nombre=deuda['nombre'],
                    monto_deuda=float(deuda['monto_deuda'])
                )
                deudas_representantes_objeto.append(deuda_objeto)
        if deudas_cursos:
            for deuda in deudas_cursos:
                deuda_objeto = DeudaCurso(
                    curso_id=int(deuda['curso_id']),
                    monto_deuda=float(deuda['deuda']),
                    cantidad_recibos=int(deuda['cantidad_recibos'])
                )
                deudas_cursos_objeto.append(deuda_objeto)
        if deudas_grados:
            for deuda in deudas_grados:
                deuda_objeto = DeudaGrado(
                    grado=int(deuda['grado']),
                    monto_deuda=float(deuda['deuda']),
                    cantidad_recibos= int(deuda['cantidad_recibos'])
                )
                deudas_grados_objeto.append(deuda_objeto)
        reporte_objeto = ReporteFinanciaro(
            cantidad_total_recibos_emitidos=int(recibos_general.get('total_recibos') or 0),
            monto_general_generado= float(recibos_general.get('monto_total_generado') or 0),
            monto_total_pagado= float(recibos_general.get('monto_total_pagado') or 0),
            monto_deuda_total=float(deudas_general.get('deuda') or 0),
            cantidad_recibos_deuda=int(deudas_general.get('total_recibos') or 0),
            deudas_meses=deudas_mes_objeto,
            deudas_representantes=deudas_representantes_objeto,
            deudas_alumnos=deudas_alumnos_objeto,
            deudas_cursos=deudas_cursos_objeto,
            deudas_grados=deudas_grados_objeto
        )
        return reporte_objeto
        


                


                        




                    
