-- Tabla cursos
CREATE TABLE IF NOT EXISTS cursos(
	curso_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	grado INT NOT NULL CHECK(grado>=1 AND grado <=5),
	seccion char NOT NULL CHECK(seccion IN ('A', 'B', 'C', 'D')),
	periodo_escolar varchar(10) NOT NULL CHECK(periodo_escolar ~'^\d{4}-\d{4}$'),
	CONSTRAINT curso_unico UNIQUE (grado, seccion, periodo_escolar) -- El grado, sección y periodo de cada curso debe ser unico 
);

-- Roles de usuario del sistema
CREATE TABLE IF NOT EXISTS roles(
	rol_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	codigo varchar(20) NOT NULL UNIQUE,
	nombre varchar(30) NOT NULL UNIQUE
);

-- Usuario del sistema
CREATE TABLE IF NOT EXISTS usuarios(
	usuario_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nombre_usuario varchar(100) NOT NULL UNIQUE,
	correo varchar(100) NOT NULL UNIQUE,
	contrasenia varchar(255) NOT NULL,
	rol_id INT NOT NULL,
	fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

	-- Establece relacion 1:1 entre usuario y rol
	CONSTRAINT fk_usuarios_rol 
	FOREIGN KEY (rol_id)
	REFERENCES roles(rol_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

-- Tabla representantes
CREATE TABLE IF NOT EXISTS representantes (
	representante_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nombre varchar(100) NOT NULL,
	cedula varchar(10) NOT NULL UNIQUE,
	correo varchar(100) NOT NULL UNIQUE,
	telefono varchar(20) NOT NULL,
	direccion varchar(200) NOT NULL
);

-- Tabla de estudiantes de la institucion
CREATE TABLE IF NOT EXISTS alumnos(
	alumno_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nombre varchar(100) NOT NULL,
	cedula varchar(10) NOT NULL UNIQUE, -- Cedula escolar
	fecha_nacimiento DATE NOT NULL,
	representante_id INT NOT NULL,
	curso_id INT NOT NULL,

	-- Establece relacion 1:N entre alumnos y representantes mediante la clave primaria del este ultimo
	CONSTRAINT fk_alumnos_representantes
		FOREIGN KEY(representante_id)
		REFERENCES representantes(representante_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,

	-- Establece relacion 1:1 entre alumno y curso a traves de ID de la clave primaria de este ultimo
	CONSTRAINT fk_alumnos_curso
	FOREIGN KEY (curso_id)
	REFERENCES cursos(curso_id)
);

-- Materias de cada annio
CREATE TABLE IF NOT EXISTS materias(
	materia_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nombre varchar(50) NOT NULL,
	codigo varchar(10) NOT NULL UNIQUE,
	grado INT NOT NULL CHECK(grado>=1 AND grado <=5), -- La materia debe estar entre 1er y 5to annio
	CONSTRAINT grado_nombre_unico UNIQUE (nombre, grado) -- Nombre y grado de cada materia debe ser unico
);

-- Tabla de profesores
CREATE TABLE IF NOT EXISTS profesores(
	profesor_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nombre varchar(100) NOT NULL,
	cedula varchar (10) UNIQUE NOT NULL,
	telefono varchar(20) NOT NULL,
	correo varchar(100) NOT NULL UNIQUE,
	especialidad varchar(20) NOT NULL,
	salario_base DECIMAL(8, 2) NOT NULL CHECK( salario_base >0), -- Su salario base no puede ser negativo ni cero
	usuario_id INT NOT NULL UNIQUE, -- ID de usuario dentro del sistema

	-- Establece relacion 1:1 entre profesor y usuario mediante el ID de este ultimo en el sistema
	CONSTRAINT fk_profesores_usuario
	FOREIGN KEY (usuario_id)
	REFERENCES usuarios(usuario_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

-- Tabla de cobranzas
CREATE TABLE IF NOT EXISTS cobranzas(
	cobranza_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	concepto varchar(100) NOT NULL,
	fecha_vencimiento DATE NOT NULL,
	monto numeric(8,2) NOT NULL CHECK(monto >0),
	estado varchar(15) NOT NULL CHECK (estado IN ('pagado', 'por cobrar')),
	alumno_id INT NOT NULL,
	representante_id INT NOT NULL,
	
	-- Indentifica al alumno por el cual se realiza la cobranza
	CONSTRAINT fk_cobranzas_alumno
	FOREIGN KEY (alumno_id)
	REFERENCES alumnos(alumno_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
	
	-- Representa relacion N:1 entre cobranza y representante (Varias cobranzas pueden estar referidas a un mismo representante)
	CONSTRAINT fk_cobranzas_representante
	FOREIGN KEY (representante_id)
	REFERENCES representantes(representante_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

-- Tabla de pagos
CREATE TABLE IF NOT EXISTS pagos (
	pago_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	fecha_pago DATE NOT NULL DEFAULT CURRENT_DATE, -- Se establece la fecha de pago como la actual, por defecto
	concepto varchar(100) NOT NULL,
	monto decimal(8,2) NOT NULL CHECK(monto > 0), -- El monto no puede ser negativo ni nulo
	profesor_id INT NOT NULL,

	-- Se establece la relacion N:1 con el profesor hacia el que se dirige al pago
	CONSTRAINT fk_pagos_profesor
	FOREIGN KEY (profesor_id)
	REFERENCES profesores(profesor_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

-- Tabla puente entre profesor y curso
CREATE TABLE IF NOT EXISTS profesores_cursos(
	profesor_id INT NOT NULL,
	materia_id INT NOT NULL,
	curso_id INT NOT NULL,

	-- Establece relacion entre un profesor, la materia que imparte y el curso(annio) al que va dirigida
	CONSTRAINT pk_profesor_materia
	PRIMARY KEY (profesor_id, materia_id, curso_id),

	-- Referencia a tabla curso(annio)
	CONSTRAINT fk_profesores_cursos_profesor
	FOREIGN KEY (profesor_id)
	REFERENCES profesores(profesor_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	
	-- Referencia a tabla de materias
	CONSTRAINT fk_profesores_cursos_materia
	FOREIGN KEY (materia_id)
	REFERENCES materias(materia_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,

	-- Referencia a tabla cursos
	CONSTRAINT fk_profesores_cursos_curso
	FOREIGN KEY (curso_id)
	REFERENCES cursos(curso_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,

	-- Cada curso(annio) debe ser unico
	CONSTRAINT materia_curso_unico
	UNIQUE (materia_id, curso_id)
);

-- Tabla de inscripciones por cada alumno
CREATE TABLE IF NOT EXISTS inscripciones(
	inscripcion_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	alumno_id INT NOT NULL,
	materia_id INT NOT NULL,
	curso_id INT NOT NULL,

	-- Cada inscripcion tiene un identificador unico
	CONSTRAINT inscripcion_unica
	UNIQUE(alumno_id, materia_id, curso_id),

	-- Referencia a tabla alumno mediante su clave primaria
	CONSTRAINT fk_inscripciones_alumno
	FOREIGN KEY (alumno_id)
	REFERENCES alumnos (alumno_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,

	-- Referencia a la materia inscrita
	CONSTRAINT fk_inscripciones_materia
	FOREIGN KEY (materia_id)
	REFERENCES materias(materia_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
	
	-- Referencia al curso al que pertenece el alumno inscrito
	CONSTRAINT fk_inscripciones_curso
	FOREIGN KEY (curso_id)
	REFERENCES cursos(curso_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

-- Tabla notas
CREATE TABLE IF NOT EXISTS notas (
	nota_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	inscripcion_id INT NOT NULL,
	fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- La fecha de registro de notas se establece como la actual, por defecto
	calificacion DECIMAL(4,2) NOT NULL CHECK(calificacion >= 0 AND calificacion <=20), -- La calificacion debe ser un numero entre 0 y 20 puntos
	lapso INT NOT NULL CHECK (lapso BETWEEN 1 AND 3), -- Solo hay 3 lapsos por annio escolar
	
	-- Referencia a la tabla de inscripcion
	CONSTRAINT fk_notas_inscripcion
	FOREIGN KEY (inscripcion_id)
	REFERENCES inscripciones(inscripcion_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	
	-- El ID de la inscripcion y el nro de lapso deben ser unicos
	CONSTRAINT nota_unica
	UNIQUE (inscripcion_id, lapso)
);

-- Tabla para manejar registro de aulas de la institucion
CREATE TABLE IF NOT EXISTS aulas(
	aula_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	codigo varchar(10) NOT NULL UNIQUE,
	ubicacion varchar(100) NOT NULL
);

-- Tabla bloques
CREATE TABLE IF NOT EXISTS bloques(
	bloque_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	aula_id INT NOT NULL,
	materia_id INT NOT NULL,
	curso_id INT NOT NULL,
	profesor_id INT NOT NULL,
	dia varchar(10) NOT NULL CHECK (dia IN ('lunes', 'martes', 'miercoles', 'jueves', 'viernes')), -- Corresponde a los dias de clase
	hora_inicio time NOT NULL,
	hora_fin time NOT NULL,

	-- Validar que la hora de salida sea despues del tiempo de entrada
	CONSTRAINT hora_valida CHECK (hora_fin > hora_inicio),

	-- Establece relacion N:1 entre bloques y aulas: Una misma aula puede ser utilizada para varios bloques
	CONSTRAINT fk_bloques_aula
	FOREIGN KEY (aula_id)
	REFERENCES aulas(aula_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,

	-- Referencia a la materia de cada bloque
	CONSTRAINT fk_bloques_materia
	FOREIGN KEY (materia_id)
	REFERENCES materias(materia_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,

	-- Referencia al curso(annio) del bloque
	CONSTRAINT fk_bloques_curso
	FOREIGN KEY (curso_id)
	REFERENCES cursos(curso_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,

	-- Referencia al profesor asignado al curso
	CONSTRAINT fk_bloques_profesores_curso
	FOREIGN KEY (profesor_id, materia_id, curso_id)
	REFERENCES profesores_cursos(profesor_id, materia_id, curso_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

-- Auditoria de notas
CREATE TABLE auditorias_notas(
	auditoria_nota_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nota_id INT NOT NULL,
	usuario_id INT NOT NULL,
	fecha_cambio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	calificacion_anterior DECIMAL(4,2) NOT NULL,
	calificacion_modificada DECIMAL(4,2) NOT NULL,

	-- Referencia a la nota a corregir
	CONSTRAINT fk_auditorias_notas_nota
	FOREIGN KEY (nota_id)
	REFERENCES notas(nota_id)
	ON DELETE RESTRICT 
	ON UPDATE CASCADE,

	-- Usuario dentro del sistema que realiza la auditoria
	CONSTRAINT fk_auditorias_notas_usuario 
	FOREIGN KEY (usuario_id)
	REFERENCES usuarios(usuario_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);


-- Creando Triggers

-- Realiza una revision de la disponibilidad de un aula, profesor y seccion en el periodo actual, a fin de realizar la insersion de un regitro
CREATE OR REPLACE FUNCTION revisar_disponibilidad_insert()
RETURNS TRIGGER AS $$
DECLARE 
	-- Booleanos que determinaran si un profesor, aula y seccion estan ocupados, respectivamente
	prof_ocupado BOOL;
	aula_ocupada BOOL;
	seccion_ocupada BOOL;

	-- Periodo actual
	periodo_actual varchar(10);
BEGIN
	SELECT periodo_escolar INTO periodo_actual 
	FROM cursos WHERE curso_id = NEW.curso_id;

	-- Seleccion que verifica si el profesor se encuentra ocupado
	SELECT EXISTS (
		SELECT 1
		FROM bloques b 
		JOIN cursos c ON b.curso_id = c.curso_id
		WHERE LOWER(dia) = LOWER(NEW.dia)
		AND profesor_id = NEW.profesor_id
		AND c.periodo_escolar = periodo_actual
		AND hora_inicio < NEW.hora_fin AND NEW.hora_inicio < hora_fin
		) INTO prof_ocupado;

	-- Seleccion que verifica si el aula esta ocupada
	SELECT EXISTS (
		SELECT 1 FROM bloques b
		JOIN cursos c ON b.curso_id = c.curso_id
		WHERE
			LOWER(dia) =LOWER(NEW.dia) AND
			aula_id = NEW.aula_id AND
			c.periodo_escolar = periodo_actual AND
			hora_inicio < NEW.hora_fin AND NEW.hora_inicio < hora_fin
	) INTO aula_ocupada;

	-- Seleccion que chequea si la seccion esta libre
	SELECT EXISTS (

		SELECT 1 FROM bloques
		WHERE
			LOWER(dia) = LOWER(NEW.dia) AND
			curso_id = NEW.curso_id AND
			hora_inicio < NEW.hora_fin AND NEW.hora_inicio < hora_fin
			
	) INTO seccion_ocupada;

	-- Se cancela la operacion de insercion si se cumple cualquiera de las condiciones siguientes:

	-- El profesor ya esta ocupado
	IF prof_ocupado THEN 
		RAISE EXCEPTION 'Operacion Cancelada: Ya el profesor % esta asignado a una clase entre la hora % y %', NEW.profesor_id, NEW.hora_inicio, NEW.hora_fin;
	END IF;

	-- El aula esta ocupada
	IF aula_ocupada THEN 
		RAISE EXCEPTION 'Operacion Cancelada: Ya el aula % esta asignado a una clase entre la hora % y %', NEW.aula_id, NEW.hora_inicio, NEW.hora_fin;
	END IF;

	-- La seccion esta ocupada
	IF seccion_ocupada THEN 
		RAISE EXCEPTION 'Operacion Cancelada: Ya la seccion % tiene una clase asignada entre la hora % y %', NEW.curso_id, NEW.hora_inicio, NEW.hora_fin;
	END IF;

	RETURN NEW;
END;

-- Establece lenguaje para el motor de PostreSQL
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_evitar_solapamiento_insert
BEFORE INSERT  ON bloques
FOR EACH ROW
EXECUTE FUNCTION revisar_disponibilidad_insert();


-- Trigger update
-- Revisa la disponibilidad de un aula, profesor y una seccion para la actualizacion de un registro 
CREATE OR REPLACE FUNCTION revisar_disponibilidad_update()
RETURNS TRIGGER AS $$
DECLARE 
	-- Booleanos que determinaran si un profesor, aula y seccion estan ocupados, respectivamente
	prof_ocupado BOOL;
	aula_ocupada BOOL;
	seccion_ocupada BOOL;

	-- Periodo actual
	periodo_actual varchar(10);
BEGIN

	-- Realiza una seleccion de un periodo escolar, de acuerdo al ID del curso, si este es igual al del nuevo 
	SELECT periodo_escolar INTO periodo_actual
	FROM cursos WHERE curso_id = NEW.curso_id;
	
	-- Chequea si un profesor se encuentra ocupado
	SELECT EXISTS (
		SELECT 1
		FROM bloques b
		JOIN cursos c ON b.curso_id = c.curso_id
		WHERE LOWER(dia) = LOWER(NEW.dia)
		AND profesor_id = NEW.profesor_id
		AND c.periodo_escolar = periodo_actual
		AND hora_inicio < NEW.hora_fin AND NEW.hora_inicio < hora_fin
		AND bloque_id <> NEW.bloque_id
		) INTO prof_ocupado;

	-- Chequea si un aula se encuentra ocupada
	SELECT EXISTS (
		SELECT 1 FROM bloques b
		JOIN cursos c ON b.curso_id = c.curso_id
		WHERE
			LOWER(dia) = LOWER(NEW.dia) AND
			aula_id = NEW.aula_id AND
			c.periodo_escolar = periodo_actual AND
			hora_inicio < NEW.hora_fin AND NEW.hora_inicio < hora_fin
			AND bloque_id <> NEW.bloque_id
	) INTO aula_ocupada;

	-- Chequea si el bloque ya esta ocupado
	SELECT EXISTS (

		SELECT 1 FROM bloques 
		WHERE
			LOWER(dia) = LOWER(NEW.dia) AND
			curso_id = NEW.curso_id AND 
			hora_inicio < NEW.hora_fin AND NEW.hora_inicio < hora_fin
			AND bloque_id <> NEW.bloque_id
			
	) INTO seccion_ocupada;

	-- Se cancela la operacion de actualizacion si se cumple cualquiera de las condiciones siguientes:

	-- El profesor ya esta ocupado
	IF prof_ocupado THEN 
		RAISE EXCEPTION 'Operacion Cancelada: Ya el profesor % esta asignado a una clase entre la hora % y %', NEW.profesor_id, NEW.hora_inicio, NEW.hora_fin;
	END IF;

	-- El aula ya esta ocupada
	IF aula_ocupada THEN 
		RAISE EXCEPTION 'Operacion Cancelada: Ya el aula % esta asignado a una clase entre la hora % y %', NEW.aula_id, NEW.hora_inicio, NEW.hora_fin;
	END IF;

	-- La seccion esta ocupada
	IF seccion_ocupada THEN 
		RAISE EXCEPTION 'Operacion Cancelada: Ya la seccion % tiene una clase asignada entre la hora % y %', NEW.curso_id, NEW.hora_inicio, NEW.hora_fin;
	END IF;

	RETURN NEW;
END;

$$ LANGUAGE plpgsql;

-- Trigger que evita el solapamiento durante una actualizacion
CREATE OR REPLACE TRIGGER trg_evitar_solapamiento_update
BEFORE UPDATE  ON bloques
FOR EACH ROW
EXECUTE FUNCTION revisar_disponibilidad_update();

	
-- Crear el trigger para validar el grado de la materia y el grado de un curso especifico
CREATE OR REPLACE FUNCTION validar_grado()
RETURNS TRIGGER AS $$
DECLARE 
	grado_materia INT;
	grado_tabla INT;
BEGIN 
	SELECT grado INTO grado_materia FROM materias WHERE materia_id = NEW.materia_id;

	SELECT grado INTO grado_tabla FROM cursos WHERE curso_id = NEW.curso_id;

	IF grado_materia IS DISTINCT FROM grado_tabla THEN
		RAISE EXCEPTION 'Operacion Cancelada: EL grado de la materia % no coincide con el grado del curso % ',
		NEW.materia_id, grado_materia;
	END IF;

	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- INSERTS

-- Validar grado para cada profesor
CREATE OR REPLACE TRIGGER validad_grado_profesores_cursos
BEFORE INSERT ON profesores_cursos
FOR EACH ROW
EXECUTE FUNCTION validar_grado();

-- validad grado por bloque
CREATE OR REPLACE TRIGGER validar_grado_bloques
BEFORE INSERT ON bloques
FOR EACH ROW
EXECUTE FUNCTION validar_grado();

-- validar grado para cada inscripcion
CREATE OR REPLACE TRIGGER validad_grado_inscripciones
BEFORE INSERT ON inscripciones
FOR EACH ROW 
EXECUTE FUNCTION validar_grado();

-- UPDATES

-- Validar grado para cada profesor
CREATE OR REPLACE TRIGGER validad_grado_profesores_cursos_update
BEFORE UPDATE ON profesores_cursos
FOR EACH ROW
EXECUTE FUNCTION validar_grado();

-- validad grado por bloque
CREATE OR REPLACE TRIGGER validar_grado_bloques_update
BEFORE UPDATE ON bloques
FOR EACH ROW
EXECUTE FUNCTION validar_grado();

-- validar grado para cada inscripcion
CREATE OR REPLACE TRIGGER validad_grado_inscripciones_update
BEFORE UPDATE ON inscripciones
FOR EACH ROW 
EXECUTE FUNCTION validar_grado();


-- Trigger auditoria
-- application level audit logs postgresql

CREATE OR REPLACE FUNCTION crear_log_auditoria()
RETURNS TRIGGER AS $$
DECLARE 
	user_id INT; -- ID de usuario dentro del sistema
BEGIN
	user_id := NULLIF(current_setting('app.current_user_id', TRUE), '')::INT;

	-- Abortar operacion, si no hay ID de usuario
	IF user_id IS NULL THEN
		RAISE EXCEPTION 'Operacion Cancela: Se necesita el ID de algun usuario para realizar la actualizacion';
	END IF;

	-- Insertar registro de la auditoria en la tabla auditoria_notas
	INSERT INTO auditorias_notas(nota_id, usuario_id, fecha_cambio, calificacion_anterior, calificacion_modificada)
		VALUES
		(
			OLD.nota_id,
			user_id,
			CURRENT_TIMESTAMP, 
			OLD.calificacion,
			NEW.calificacion
		);
		

	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Ejecutar la creacion del log, si la nueva nota es diferente de la anterior
CREATE OR REPLACE TRIGGER  actualizar_auditoria_notas
AFTER UPDATE ON notas
FOR EACH ROW
WHEN (OLD.calificacion IS DISTINCT FROM NEW.calificacion)
EXECUTE FUNCTION crear_log_auditoria();
