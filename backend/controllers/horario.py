from sqlalchemy.orm import Session
from models.bloque import Bloque
from models.curso import Curso

def crear_horario(db: Session, datos: dict) -> dict:
    nuevo_horario = Bloque(**datos)
    db.add(nuevo_horario)
    db.commit()
    db.refresh(nuevo_horario)
    return _formatear_respuesta(db, nuevo_horario)

def listar_horarios(db: Session) -> list[dict]:
    bloques = db.query(Bloque).all()
    return [_formatear_respuesta(db, b) for b in bloques]

def obtener_horario(db: Session, horario_id: int) -> dict | None:
    bloque = db.query(Bloque).filter(Bloque.bloque_id == horario_id).first()
    if not bloque:
        return None
    return _formatear_respuesta(db, bloque)

def actualizar_horario(db: Session, horario_id: int, datos: dict) -> dict | None:
    bloque = db.query(Bloque).filter(Bloque.bloque_id == horario_id).first()
    if not bloque:
        return None

    for key, value in datos.items():
        setattr(bloque, key, value)
        
    db.commit()
    db.refresh(bloque)
    return _formatear_respuesta(db, bloque)

def eliminar_horario(db: Session, horario_id: int) -> dict | None:
    bloque = db.query(Bloque).filter(Bloque.bloque_id == horario_id).first()
    if not bloque:
        return None
        
    db.delete(bloque)
    db.commit()
    return {"mensaje": f"El horario con ID {horario_id} ha sido eliminado"}

# --- Función auxiliar para adaptar Bloque a HorarioRespuesta ---
def _formatear_respuesta(db: Session, bloque: Bloque) -> dict:
    # Buscamos el curso para obtener su nombre/grado
    curso = db.query(Curso).filter(Curso.curso_id == bloque.curso_id).first()
    nombre_curso = f"{curso.grado}{curso.seccion}" if curso else str(bloque.curso_id)

    return {
        "id": bloque.bloque_id,
        "curso": nombre_curso,
        "dia": bloque.dia,
        "hora_inicio": str(bloque.hora_inicio),
        "hora_fin": str(bloque.hora_fin)
    }
