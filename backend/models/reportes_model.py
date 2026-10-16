from base import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date, DateTime, text, Enum, PrimaryKeyConstraint,UniqueConstraint
from sqlalchemy.sql import func
import enum
#CREATE TYPE estado_recibo AS ENUM('pendiente', 'pagado');
#CREATE TYPE metodos_pago AS ENUM ('efectivo', 'trasferencia', 'pago_movil', 'zelle', 'binance', 'punto_venta');
class EstadoReciboEnum(str, enum.Enum):
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
class MetodoPagoEnum(str, enum.Enum):
    PAGO_MOVIL = "pago_movil"
    EFECTIVO = "efectivo"
    ZELLE = "zelle"
    BINANCE = "binance"
    TRANSFERENCIA = "transferencia"
    PUNTO_VENTA = "punto_venta"

class Representante(Base):
    __tablename__ = "representantes"
    representante_id = Column(Integer, primary_key=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    cedula = Column(String(10), nullable=False, unique=True)
    correo = Column(String(100), nullable=False, unique=True)
    telefono =Column(String(20), nullable=False)
    direccion = Column(String(200), nullable=False)
    monto_deuda = Column(Numeric(10,2), nullable=False, server_default=text('0'))


class Curso(Base):
    __tablename__ = "cursos"
    curso_id = Column(Integer, primary_key=True, index=True, nullable=False)
    grado =Column(Integer, nullable=False)
    seccion =  Column(String(1), nullable=False)
    periodo_escolar = Column(String(10), nullable=False)



class Alumno(Base):
    __tablename__ = "alumnos"
    alumno_id = Column(Integer, primary_key=True, index=True, nullable=False)
    nombre  = Column(String(100), nullable=False)
    cedula  = Column(String(10), nullable=False, unique=True)
    fecha_nacimiento = Column(Date, nullable=False)
    representante_id = Column(Integer, ForeignKey('representantes.representante_id'), nullable=False)
    curso_id = Column(Integer, ForeignKey('cursos.curso_id'), nullable=False )



class Materia(Base):
    __tablename__ = "materias"
    materia_id = Column(Integer, primary_key=True, index=True, nullable=False )
    nombre = Column(String(50), nullable=False)
    codigo = Column(String(10), nullable=False, unique=True)
    grado = Column(Integer, nullable=False)
 



class Inscripcion(Base):
    __tablename__ = "inscripciones"
    inscripcion_id = Column(Integer, primary_key=True, index=True, nullable=False)
    alumno_id = Column(Integer, ForeignKey('alumnos.alumno_id'), nullable=False)
    materia_id = Column(Integer, ForeignKey('materias.materia_id'), nullable=False)
    curso_id = Column(Integer, ForeignKey('cursos.curso_id'), nullable=False)


class Nota(Base):
    __tablename__ = "notas"
    nota_id = Column(Integer, primary_key=True, index=True, nullable=False)
    fecha_registro = Column(DateTime, nullable=False, server_default=func.now())
    calificacion = Column(Numeric(4,2), nullable=False)
    lapso = Column(Integer, nullable=False)
    inscripcion_id = Column(Integer, ForeignKey('inscripciones.inscripcion_id'), nullable=False)


class ReciboCobro(Base):
    __tablename__ = "recibos_cobro"
    recibo_id = Column(Integer, primary_key=True, index=True, nullable=False )
    concepto = Column(String(100), nullable=False)
    fecha_generacion = Column(Date, nullable=False, server_default=text('CURRENT_DATE'))
    monto_total = Column(Numeric(8,2), nullable=False)
    monto_pagado = Column(Numeric(8,2), nullable=False, server_default=text('0'))
    estado = Column(
        Enum(EstadoReciboEnum, name="estado_recibo", create_type=False),
        nullable=False,
        server_default="pendiente"
    )
    alumno_id = Column(Integer, ForeignKey('alumnos.alumno_id'), nullable=False)

class PagoRepresentante(Base):
    __tablename__ = "pagos_representantes"
    pago_representante_id =Column(Integer, primary_key=True, index=True, nullable=False)
    monto = Column(Numeric(8,2), nullable=False)
    fecha_pago = Column(DateTime, nullable=False, server_default=func.now())
    metodo_pago =Column(
        Enum(MetodoPagoEnum, name="metodos_pago", create_type=False),
        nullable=False
    )
    referencia_pago = Column(String(100), nullable=False)
    representante_id = Column(Integer, ForeignKey('representantes.representante_id'), nullable=False)


class Profesor(Base):
    __tablename__ = "profesores"
    profesor_id = Column(Integer, primary_key=True, index=True)
    nombre =  Column(String(100), nullable=False)
    cedula = Column(String(10), nullable=False, unique=True)
    telefono =  Column(String(20), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    especialidad = Column(String(20), nullable=False)
    salario_base = Column(Numeric(8,2), nullable=False) # Es decimal en la base de datos

class CursoProfesor(Base):

    __tablename__ = "cursos_profesores"
    profesor_id = Column(Integer, ForeignKey('profesores.profesor_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    materia_id = Column(Integer, ForeignKey('materias.materia_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    curso_id = Column(Integer, ForeignKey('cursos.curso_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('profesor_id', 'materia_id', 'curso_id', name='pk_profesor_materia'),
        UniqueConstraint('materia_id', 'curso_id', name='materia_curso_unico')
    )

