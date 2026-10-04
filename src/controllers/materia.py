from sqlalchemy.orm import Session

from src.controllers.utils import confirmar
from src.exceptions import Conflicto, NoEncontrado
from src.models.materia import Materia
from src.schemas.materia import MateriaCreate, MateriaUpdate


# CAMBIO: función nueva. Se usa al crear y al actualizar para detectar un
# código repetido. "excluir_id" evita que una materia choque consigo misma
# al editarla.
def _codigo_en_uso(db: Session, codigo: str, excluir_id: int | None = None) -> bool:
    consulta = db.query(Materia).filter(Materia.codigo == codigo)
    if excluir_id is not None:
        # CAMBIO: el modelo y SQL llaman materia_id a la clave primaria.
        consulta = consulta.filter(Materia.materia_id != excluir_id)
    return consulta.first() is not None


def _nombre_grado_en_uso(
    db: Session, nombre: str, grado: int, excluir_id: int | None = None
) -> bool:
    consulta = db.query(Materia).filter(
        Materia.nombre == nombre,
        Materia.grado == grado,
    )
    if excluir_id is not None:
        # CAMBIO: se excluye la propia materia al verificar su clave compuesta.
        consulta = consulta.filter(Materia.materia_id != excluir_id)
    return consulta.first() is not None


def registrar_materia(db: Session, datos: MateriaCreate) -> Materia:
    # CAMBIO: antes devolvía None y la ruta respondía 404 por un duplicado.
    # Ahora lanza Conflicto (409), que es el código correcto.
    if _codigo_en_uso(db, datos.codigo):
        raise Conflicto(f"Código [{datos.codigo}] ya registrado")
    # CAMBIO: replica la restricción grado_nombre_unico para dar un conflicto
    # claro antes de que PostgreSQL rechace el INSERT.
    if _nombre_grado_en_uso(db, datos.nombre, datos.grado):
        raise Conflicto("Ya existe una materia con ese nombre para ese grado")

    materia = Materia(**datos.model_dump())
    db.add(materia)
    confirmar(db, f"Código [{datos.codigo}] ya registrado")
    db.refresh(materia)
    return materia


def obtener_materia(db: Session, id_materia: int) -> Materia:
    # CAMBIO: antes devolvía None y cada ruta decidía el 404. Ahora lanza
    # NoEncontrado directamente (menos código repetido en las rutas).
    materia = db.get(Materia, id_materia)
    if materia is None:
        raise NoEncontrado("Materia no encontrada")
    return materia


def listar_materias(db: Session) -> list[Materia]:
    # CAMBIO: se ordena por la PK materia_id que realmente expone el modelo.
    return db.query(Materia).order_by(Materia.materia_id).all()


def actualizar_materia(db: Session, id_materia: int, datos: MateriaUpdate) -> Materia:
    materia = obtener_materia(db, id_materia)
    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)

    # CAMBIO: antes se podía editar el código a uno ya existente y el error
    # reventaba al hacer commit (500). Ahora se valida antes y da 409.
    nuevo_codigo = cambios.get("codigo")
    if nuevo_codigo is not None and _codigo_en_uso(db, nuevo_codigo, id_materia):
        raise Conflicto(f"Código [{nuevo_codigo}] ya registrado")
    nombre = cambios.get("nombre", materia.nombre)
    grado = cambios.get("grado", materia.grado)
    if _nombre_grado_en_uso(db, nombre, grado, id_materia):
        raise Conflicto("Ya existe una materia con ese nombre para ese grado")

    for campo, valor in cambios.items():
        setattr(materia, campo, valor)

    confirmar(db, "No se pudo actualizar la materia")
    db.refresh(materia)
    return materia


def eliminar_materia(db: Session, id_materia: int) -> None:
    materia = obtener_materia(db, id_materia)
    db.delete(materia)
    # CAMBIO: si la materia tiene inscripciones, la BD lo impide (RESTRICT).
    # Antes eso producía un error 500; ahora responde 409 con un mensaje claro.
    confirmar(
        db, "No se puede eliminar la materia porque tiene inscripciones asociadas"
    )
