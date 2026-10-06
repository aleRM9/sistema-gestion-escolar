# sistema-gestion-escolar

Sistema web de gestión escolar que permite la administración de colegios y
automatización de reportes. En desarrollo con FastAPI, PostgreSQL y Docker.

## Estado actual

Módulo académico: materias, inscripciones y notas (con promedio por materia y
boletín por alumno). Pendiente: representantes, alumnos, profesores, cobranza,
nómina, autenticación con roles, interfaz y docker-compose.

## Requisitos

- Python 3.12
- PostgreSQL

## Instalación

```bash
# 1. Entorno virtual e instalación de dependencias
python -m venv .venv
.venv\Scripts\activate          # Windows   (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt

# 2. Variables de entorno
copy .env.example .env          # Linux/Mac: cp .env.example .env
#    ...y edita .env con tus datos de PostgreSQL

# 3. Base de datos: crea la BD vacía y ejecuta el script
createdb -U postgres gestion_escolar
psql -U postgres -d gestion_escolar -f "PROYECTO LENGUAJES.sql"

# 4. Levantar la API (desde la carpeta raíz del proyecto)
uvicorn src.main:app --reload
```

Documentación interactiva en http://127.0.0.1:8000/docs

## Endpoints

| Recurso | Rutas |
|---|---|
| Materias | `POST/GET /materias/`, `GET/PUT/DELETE /materias/{id_materia}` |
| Inscripciones | `POST/GET /inscripciones/`, `GET/PUT/DELETE /inscripciones/{id_inscripcion}` |
| Notas | `POST/GET /notas/`, `GET/PUT/DELETE /notas/{id_notas}` |
| Promedio | `GET /notas/promedio/{id_alumno}/{id_materia}?periodo=2025-2026` |
| Boletín | `GET /notas/boletin/{id_alumno}?periodo=2025-2026` |

Sin `periodo`, el promedio y el boletín usan el periodo más reciente del alumno.
Errores: `404` si no existe el recurso, `409` si hay duplicados o registros relacionados.
CAMBIO: `PUT /notas/{id_notas}` requiere el encabezado `X-Usuario-Id` con un
`usuario_id` existente en `usuarios`; la base lo usa para auditar cambios de
calificación. Es un valor declarado por el cliente, no una identidad autenticada;
al implementar autenticación debe derivarse del usuario validado por el servidor.

## Notas para el equipo

- CAMBIO: `PROYECTO LENGUAJES.sql` es la fuente de verdad de la base de datos;
  los modelos de `src/models` se alinean con sus tablas académicas. La app no
  crea tablas por sí sola.

## Historial de la corrección (para el equipo)

En el código, cada ajuste queda marcado con un comentario `CAMBIO:` que explica
qué se hizo y por qué. Los modelos y contratos deben seguir el SQL canónico.
