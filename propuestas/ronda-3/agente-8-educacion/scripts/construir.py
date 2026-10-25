# -*- coding: utf-8 -*-
"""Construye propuestas.json del agente 8 (ronda 3) desde evidencia local.

Solo lee fuera de esta carpeta. No genera nada central ni descarga nada.
Las decisiones estan codificadas por IRI; los literales se copian byte-exactos
de la inspeccion y la asignacion (se verifica igualdad en construir y verificar).
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, "C:/Users/marti/Documents/MEX-Ontologi/scripts")
from integrar_contenido import clave  # noqa: E402 (funcion pura: normalizacion)

BASE = Path(__file__).resolve().parent.parent
R3A8 = "r3a8-"

CENTRO = Path("C:/Users/marti/Documents/MEX-Ontologi")


def sha256_archivo(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest(), Path(p).stat().st_size


asig = json.load(open(CENTRO / "propuestas/ronda-3/integrador/asignaciones-semanticas.json", encoding="utf-8"))
MINE = asig["asignaciones"]["8"]["variables"]
SEM = json.load(open(CENTRO / "ontologia/semantica.json", encoding="utf-8"))
INSP = json.load(open(BASE / "fuente/inspeccion-126.json", encoding="utf-8"))
META = {d["id"]: d for d in json.load(open(CENTRO / "data/catalogo/metadatos.json", encoding="utf-8"))}
A3 = json.load(open(CENTRO / "propuestas/ronda-3/agente-3-cobertura/propuestas.json", encoding="utf-8"))

# ---------------------------------------------------------------- conceptos
# slug: [label, definicion, broader]
CONCEPTOS_NUEVOS = {
    "estudiantes-nuevo-ingreso-sede": ["Estudiantes de nuevo ingreso por sede",
        "Número de estudiantes de nuevo ingreso por programa educativo en una sede (municipio) de la institución, según el diccionario. La sede se conserva por calificador formal de cada regla; no se afirma identidad con municipios oficiales ni se cruza con poblaciones de otros conjuntos.", None],
    "estudiantes-egresados-sede": ["Estudiantes egresados por sede",
        "Número de estudiantes egresados por programa educativo en una sede (municipio) de la institución, según el diccionario. La sede se conserva por calificador formal de cada regla; no se afirma identidad con municipios oficiales.", None],
    "estudiantes-reingreso-sede": ["Estudiantes de reingreso por sede",
        "Número de estudiantes que reingresaron por programa educativo en una sede (municipio) de la institución, según el diccionario. La sede se conserva por calificador formal de cada regla; distinto de nuevo ingreso.", None],
    "estudiantes-titulados-sede": ["Estudiantes titulados por sede",
        "Número de estudiantes titulados por programa educativo en una sede (municipio) de la institución, según el diccionario. La sede se conserva por calificador formal de cada regla; distinto de egreso (titulación posterior a culminar estudios).", None],
    "hombres-titulados-programa-anio": ["Hombres titulados por programa y año",
        "Total de hombres titulados durante el año a reportar por programa educativo, según el diccionario. Población: hombres; evento: titulación; sin homologar con egresados.", None],
    "mujeres-tituladas-programa-anio": ["Mujeres tituladas por programa y año",
        "Total de mujeres tituladas durante el año a reportar por programa educativo, según el diccionario. Población: mujeres; evento: titulación; sin homologar con egresadas.", None],
    "hombres-egresados-programa-anio": ["Hombres egresados por programa y año",
        "Total de hombres egresados durante el año a reportar por programa educativo, según el diccionario. Población: hombres; evento: egreso (culminación de estudios); distinto de titulación.", None],
    "mujeres-egresadas-programa-anio": ["Mujeres egresadas por programa y año",
        "Total de mujeres egresadas durante el año a reportar por programa educativo, según el diccionario. Población: mujeres; evento: egreso (culminación de estudios); distinto de titulación.", None],
    "mujeres-nuevo-ingreso-tsu": ["Mujeres de nuevo ingreso a TSU",
        "Total de mujeres matriculadas de nuevo ingreso al primer cuatrimestre de nivel Técnico Superior Universitario, por programa educativo, según el diccionario. Población: mujeres; nivel: TSU; tramo: primer cuatrimestre.", None],
    "hombres-nuevo-ingreso-tsu": ["Hombres de nuevo ingreso a TSU",
        "Total de hombres matriculados de nuevo ingreso al primer cuatrimestre de nivel Técnico Superior Universitario, por programa educativo, según el diccionario. Población: hombres; nivel: TSU; tramo: primer cuatrimestre.", None],
    "mujeres-reingreso-institucion": ["Mujeres de reingreso a la institución",
        "Total de mujeres de reingreso a la institución por programa educativo, según el diccionario (incluye reingreso a primer cuatrimestre de nivel TSU). Población: mujeres; evento: reingreso; distinto de nuevo ingreso.", None],
    "hombres-reingreso-institucion": ["Hombres de reingreso a la institución",
        "Total de hombres de reingreso a la institución por programa educativo, según el diccionario (incluye reingreso a primer cuatrimestre de nivel TSU). Población: hombres; evento: reingreso; distinto de nuevo ingreso.", None],
    "nivel-estudios-matriculado": ["Nivel de estudios matriculado",
        "Nivel de estudios en el que el estudiante se encuentra matriculado, según el diccionario (ejemplos publicados: T.S.U., TSU). Denota el nivel del registro; no precisa plan ni sede.", None],
    "campo-formacion-academica": ["Campo de formación académica",
        "Campo de formación académica del registro de estudiantes, según el diccionario. La edición 2016 de la clasificación mexicana consta solo donde la fila la declara y publica su catálogo; fuera de esas filas no se afirma edición ni equivalencia de catálogos.", None],
    "sexo-alumno": ["Sexo del alumno",
        "Sexo del alumno o estudiante según el diccionario, con categorías y codificación propias de cada fila (ejemplos: Masculino, M, H). Población: alumnado; sin homologar categorías entre filas.", None],
    "sexo-titulado": ["Sexo del titulado",
        "Sexo del titulado según el diccionario (ejemplo publicado: M). Población: titulados; distinto de sexo del alumno; sin homologar.", None],
    "unidad-academica-municipio": ["Municipio de la unidad académica",
        "Nombre del municipio donde se encuentra la unidad académica del estudiante, según el diccionario. Denota municipio de ubicación de la unidad; no implica residencia del estudiante.", "municipio"],
    "sede-matricula-municipio": ["Municipio sede de matrícula",
        "Municipio sede donde el estudiante se encuentra matriculado, según el diccionario. Denota sede de matrícula; no se afirma identidad con municipios oficiales.", "municipio"],
    "unidad-academica-sede": ["Unidad académica sede",
        "Unidad donde se imparte el programa educativo, según el diccionario (nombre de sede publicado). Denota la unidad/sede; distinta del municipio donde se encuentra.", "organizacion"],
    "tipo-programa-educativo": ["Tipo de programa educativo",
        "Tipo de programa educativo según el diccionario (ejemplo publicado: Licenciatura). Denota el tipo, no el programa; sin leyenda global de tipos.", None],
    "tipo-periodo-programa": ["Tipo de periodo del programa",
        "Tipo de periodo del programa educativo según el diccionario (ejemplo publicado: Semestral). Denota el tipo de periodo; distinto del periodo concreto cursado.", None],
    "modalidad-programa-educativo": ["Modalidad del programa educativo",
        "Modalidad del programa educativo según el diccionario (ejemplo publicado: Escolarizado). Denota la modalidad del programa; distinta de la modalidad cursada por el estudiante.", None],
    "modalidad-cursada": ["Modalidad cursada",
        "Modalidad cursada por el estudiante según el diccionario, con dominio publicado: Escolarizada, No escolarizada o Mixta. Población: estudiante matriculado.", None],
    "grupos-asignaturas-inscripcion": ["Grupos y asignaturas de inscripción",
        "Conjunto de grupos a los cuales el alumno se inscribió, con claves de grupo-asignatura publicadas como ejemplo. Denota inscripción a grupos; no acredita equivalencia de asignaturas entre planes.", None],
    "nacionalidad-alumno": ["Nacionalidad del alumno",
        "Nacionalidad del alumno según el diccionario. El ejemplo de la fila está vacío; el significado no depende del ejemplo.", None],
    "edad-alumno": ["Edad del alumno",
        "Edad del alumno o estudiante según el diccionario, en enteros publicados como ejemplo. Sin unidad declarada en la fila; no se afirma unidad temporal.", None],
    "tipo-discapacidad-alumno": ["Tipo de discapacidad del alumno",
        "Tipo de discapacidad que posee el alumno, de tenerla, según el diccionario. El ejemplo de la fila está vacío; presencia y tipo no quedan acreditados por ejemplo.", None],
    "indicador-discapacidad-alumno": ["Indicador de discapacidad del alumno",
        "Indicador de discapacidad según el diccionario (ejemplo publicado: N). Denota presencia/ausencia declarada; distinto del tipo de discapacidad.", None],
    "estado-civil-alumno": ["Estado civil del alumno",
        "Estado civil del alumno o estudiante registrado según el diccionario (ejemplos publicados: SOLTERO (A), Soltero). Sin homologar categorías entre filas.", None],
    "lugar-nacimiento-alumno": ["Lugar de nacimiento del alumno",
        "Lugar de nacimiento del alumno según el diccionario (ejemplo publicado: CD. OBREGON). Texto libre de la fuente; sin georreferencia oficial.", None],
    "entidad-nacimiento-estudiante": ["Entidad de nacimiento del estudiante",
        "Estado de nacimiento del estudiante según el diccionario (ejemplo publicado: Sonora). Denota entidad federativa de nacimiento; distinta del lugar libre.", "entidad"],
    "institucion-bachillerato-alumno": ["Institución de bachillerato del alumno",
        "Nombre de la institución donde el alumno cursó el bachillerato, según el diccionario. Texto libre de la fuente; sin identidad institucional global.", "organizacion"],
    "promedio-bachillerato-alumno": ["Promedio de bachillerato del alumno",
        "Promedio final al salir del bachillerato, según el diccionario. Medida de aprovechamiento previo al ingreso; distinta de promedios del ciclo actual.", None],
    "entidad-curso-bachillerato": ["Entidad donde cursó el bachillerato",
        "Estado en el cual el alumno cursó el bachillerato, según el diccionario (ejemplo publicado: SONORA). Denota entidad federativa; distinta de la entidad de nacimiento.", "entidad"],
    "ciudad-curso-bachillerato": ["Ciudad donde cursó el bachillerato",
        "Ciudad en la cual el alumno cursó el bachillerato, según el diccionario. Texto libre de la fuente; sin georreferencia oficial.", None],
    "anio-egreso-bachillerato": ["Año de egreso del bachillerato",
        "Año en el cual el alumno egresó del bachillerato, según el diccionario. El ejemplo de la fila está vacío; el año concreto no queda acreditado por ejemplo.", "anio"],
    "clave-periodo-ingreso-alumno": ["Clave del periodo de ingreso del alumno",
        "Clave del periodo escolar cuando el alumno ingresó, según el diccionario. Representación código local; sistema de claves no acreditado.", "periodo-escolar"],
    "creditos-cursados-alumno": ["Créditos cursados del alumno",
        "Total de créditos cursados del alumno según el diccionario (literal con errata 'cursoados' preservada de origen). Medida acumulada; distinta del total del plan.", None],
    "total-creditos-plan-alumno": ["Total de créditos del plan del alumno",
        "Total de créditos del plan de estudio que cursa el alumno, según el diccionario. Denota el tamaño del plan; distinto de créditos cursados o acumulados.", None],
    "creditos-acumulados-alumno": ["Créditos acumulados del alumno",
        "Créditos totales del alumno según el diccionario. Medida acumulada del estudiante; sin equiparar con créditos cursados de otro conjunto.", None],
    "indicador-ingreso-reingreso-alumno": ["Indicador de nuevo ingreso o reingreso",
        "Indicador de si el alumno es de nuevo ingreso o reingreso, según el diccionario. Denota la condición de ingreso del registro; distinto de los conteos por sede.", None],
    "semestres-cursados-con-actual": ["Semestres cursados contando el ciclo actual",
        "Número de semestres cursados por el alumno contando el ciclo actual, según el diccionario. Incluye el ciclo en curso; distinto del conteo sin ciclo actual.", None],
    "semestres-cursados-sin-actual": ["Semestres cursados sin el ciclo actual",
        "Número de semestres cursados por el alumno sin contar el ciclo actual, según el diccionario. Excluye el ciclo en curso; distinto del conteo con ciclo actual.", None],
    "clave-ultimo-ciclo-cursado": ["Clave del último ciclo cursado",
        "Clave del último ciclo escolar cursado por el alumno, según el diccionario. Representación código local; sistema de claves no acreditado.", "periodo-escolar"],
    "clave-periodo-baja-alumno": ["Clave del periodo de baja del alumno",
        "Clave del periodo en el cual el alumno se dio de baja, según el diccionario. Denota periodo de baja en código; distinta de la fecha de baja ya respaldada; ejemplo vacío en la fila.", "periodo-escolar"],
    "promedio-ultimo-ciclo-aprobadas": ["Promedio del último ciclo solo aprobadas",
        "Promedio del último ciclo que cursó el alumno solo en las asignaturas que aprobó, según el diccionario. Rango: solo aprobadas; distinto del promedio de todas.", None],
    "promedio-ultimo-ciclo-todas": ["Promedio del último ciclo todas las asignaturas",
        "Promedio del último ciclo que cursó el alumno en todas las asignaturas, según el diccionario. Rango: todas; distinto del promedio de solo aprobadas.", None],
    "promedio-general-aprobadas": ["Promedio general solo aprobadas",
        "Promedio general de solo las asignaturas aprobadas, según el diccionario. Rango: solo aprobadas; distinto del promedio general de todas.", None],
    "promedio-general-todas": ["Promedio general de todas las asignaturas",
        "Promedio general de todas las asignaturas, según el diccionario. Rango: todas; distinto del promedio de solo aprobadas.", None],
    "promedio-actual-alumno": ["Promedio actual del alumno",
        "Promedio actual del alumno según el diccionario. Medida del momento del registro; sin rango de asignaturas declarado.", None],
    "promedio-general-alumno": ["Promedio general del alumno",
        "Promedio general del alumno según el diccionario. Sin rango de asignaturas declarado; distinto de los promedios con rango explícito de otro conjunto.", None],
    "asignaturas-reprobadas-ultimo-ciclo": ["Asignaturas reprobadas del último ciclo",
        "Número de asignaturas que reprobó el alumno en el último ciclo cursado, según el diccionario. Conteo de reprobadas; distinto de promedios.", None],
    "indicador-regularidad-alumno": ["Indicador de regularidad del alumno",
        "Indicador de si el alumno es regular o irregular, según el diccionario. Denota condición de regularidad declarada.", None],
    "indicador-alumno-activo": ["Indicador de alumno activo",
        "Indicador de si el alumno está activo o no, según el diccionario. Denota condición de actividad declarada.", None],
    "indicador-residencias-alumno": ["Indicador de inscripción en residencias",
        "Indicador sobre si el alumno está inscrito en residencias, según el diccionario. Denota inscripción declarada a residencias.", None],
    "indicador-seguro-escolar-alumno": ["Indicador de seguro escolar",
        "Indicador sobre si el alumno cuenta con seguro escolar, según el diccionario. Denota cobertura declarada; no acredita afiliación.", None],
    "grado-cuatrimestre-cursado": ["Grado o cuatrimestre cursado",
        "Grado o cuatrimestre cursado por el estudiante según el diccionario. Denota el tramo curricular en curso.", None],
    "cuatrimestre-reporte": ["Cuatrimestre del reporte",
        "Cuatrimestre del que se reporta la información según el diccionario (Enero - Abril, Mayo - Agosto y Septiembre - Diciembre). Denota periodo de reporte; distinto del cuatrimestre cursado.", "tiempo"],
    "alumnos-evaluados-programa": ["Alumnos evaluados del programa",
        "Cantidad de alumnos evaluados del programa educativo, según el diccionario. Población evaluada; ejemplo vacío en la fila.", None],
    "alumnos-rango-menor-7": ["Alumnos con calificación menor a 7",
        "Cantidad de alumnos evaluados con calificación menor a 7, según nombre y descripción del diccionario. Rango excluyente: <7.", None],
    "alumnos-rango-7-79": ["Alumnos con calificación de 7 a 7.9",
        "Cantidad de alumnos evaluados con calificación de 7 hasta 7.9, según nombre y descripción del diccionario. Rango: [7, 7.9].", None],
    "alumnos-rango-8-89": ["Alumnos con calificación de 8 a 8.9",
        "Cantidad de alumnos evaluados con calificación de 8 hasta 8.9, según nombre y descripción del diccionario. Rango: [8, 8.9].", None],
    "alumnos-rango-9-10": ["Alumnos con calificación de 9 a 10",
        "Cantidad de alumnos evaluados con calificación de 9 hasta 10, según nombre y descripción del diccionario. Rango: [9, 10].", None],
    "promedio-global-programa": ["Promedio global del programa",
        "Promedio general del programa educativo según el diccionario. Medida agregada por programa; ejemplo vacío en la fila.", None],
    "promedio-aprovechamiento-mujeres-programa": ["Promedio de aprovechamiento de mujeres",
        "Promedio académico (mujeres) durante el año a reportar por programa educativo, según el diccionario. Población: mujeres; medida anual por programa.", None],
    "promedio-aprovechamiento-hombres-programa": ["Promedio de aprovechamiento de hombres",
        "Promedio académico (hombres) durante el año a reportar por programa educativo, según el diccionario. Población: hombres; medida anual por programa.", None],
}

CONCEPTOS_REUTILIZADOS = ["programa-educativo"]

# ---------------------------------------------------------------- decisiones
# iri -> dict(decision, concepto|motivo, representacion, calificador, nota)
SEDE_NI = "Número de estudiantes de nuevo ingreso por programa educativo en la sede; la sede la da el calificador."
SEDE_EG = "Número de estudiantes egresados por programa educativo en la sede; la sede la da el calificador."
SEDE_RE = "Número de estudiantes que reingresaron por programa educativo en la sede; la sede la da el calificador."
SEDE_TI = "Número de estudiantes titulados por programa educativo en la sede; la sede la da el calificador."

PROP = {}
for iri, var, concepto, rep, extra in [
    # Poblacion - Nuevo ingreso (5 sedes)
    ("2a679b35-0e8f-4793-9898-12c92fc3cfeb%2F2", "San Luis R.C.", "estudiantes-nuevo-ingreso-sede", "no_especificada", {"calificador": {"sede": "San Luis R.C."}, "nota": SEDE_NI}),
    ("2a679b35-0e8f-4793-9898-12c92fc3cfeb%2F3", "Hermosillo", "estudiantes-nuevo-ingreso-sede", "no_especificada", {"calificador": {"sede": "Hermosillo"}, "nota": SEDE_NI}),
    ("2a679b35-0e8f-4793-9898-12c92fc3cfeb%2F4", "Navojoa", "estudiantes-nuevo-ingreso-sede", "no_especificada", {"calificador": {"sede": "Navojoa"}, "nota": SEDE_NI}),
    ("2a679b35-0e8f-4793-9898-12c92fc3cfeb%2F5", "Magdalena", "estudiantes-nuevo-ingreso-sede", "no_especificada", {"calificador": {"sede": "Magdalena"}, "nota": SEDE_NI}),
    ("2a679b35-0e8f-4793-9898-12c92fc3cfeb%2F6", "Benito Juárez", "estudiantes-nuevo-ingreso-sede", "no_especificada", {"calificador": {"sede": "Benito Juárez"}, "nota": SEDE_NI}),
    # Egresados (5 sedes)
    ("2b0630a2-dd4f-4b93-a321-d4a6c47a522b%2F2", "San Luis R.C.", "estudiantes-egresados-sede", "no_especificada", {"calificador": {"sede": "San Luis R.C."}, "nota": SEDE_EG}),
    ("2b0630a2-dd4f-4b93-a321-d4a6c47a522b%2F3", "Hermosillo", "estudiantes-egresados-sede", "no_especificada", {"calificador": {"sede": "Hermosillo"}, "nota": SEDE_EG}),
    ("2b0630a2-dd4f-4b93-a321-d4a6c47a522b%2F4", "Navojoa", "estudiantes-egresados-sede", "no_especificada", {"calificador": {"sede": "Navojoa"}, "nota": SEDE_EG}),
    ("2b0630a2-dd4f-4b93-a321-d4a6c47a522b%2F5", "Magdalena", "estudiantes-egresados-sede", "no_especificada", {"calificador": {"sede": "Magdalena"}, "nota": SEDE_EG}),
    ("2b0630a2-dd4f-4b93-a321-d4a6c47a522b%2F6", "Benito Juárez", "estudiantes-egresados-sede", "no_especificada", {"calificador": {"sede": "Benito Juárez"}, "nota": SEDE_EG}),
    # Poblacion - Reingreso (5 sedes)
    ("7bf622c7-356c-4b5c-a371-bacf762aaa88%2F2", "San Luis R.C.", "estudiantes-reingreso-sede", "no_especificada", {"calificador": {"sede": "San Luis R.C."}, "nota": SEDE_RE}),
    ("7bf622c7-356c-4b5c-a371-bacf762aaa88%2F3", "Hermosillo", "estudiantes-reingreso-sede", "no_especificada", {"calificador": {"sede": "Hermosillo"}, "nota": SEDE_RE}),
    ("7bf622c7-356c-4b5c-a371-bacf762aaa88%2F4", "Navojoa", "estudiantes-reingreso-sede", "no_especificada", {"calificador": {"sede": "Navojoa"}, "nota": SEDE_RE}),
    ("7bf622c7-356c-4b5c-a371-bacf762aaa88%2F5", "Magdalena", "estudiantes-reingreso-sede", "no_especificada", {"calificador": {"sede": "Magdalena"}, "nota": SEDE_RE}),
    ("7bf622c7-356c-4b5c-a371-bacf762aaa88%2F6", "Benito Juárez", "estudiantes-reingreso-sede", "no_especificada", {"calificador": {"sede": "Benito Juárez"}, "nota": SEDE_RE}),
    # Titulados (5 sedes)
    ("7c745246-2821-4690-9095-afd7be0383d4%2F2", "San Luis R.C.", "estudiantes-titulados-sede", "no_especificada", {"calificador": {"sede": "San Luis R.C."}, "nota": SEDE_TI}),
    ("7c745246-2821-4690-9095-afd7be0383d4%2F3", "Hermosillo", "estudiantes-titulados-sede", "no_especificada", {"calificador": {"sede": "Hermosillo"}, "nota": SEDE_TI}),
    ("7c745246-2821-4690-9095-afd7be0383d4%2F4", "Navojoa", "estudiantes-titulados-sede", "no_especificada", {"calificador": {"sede": "Navojoa"}, "nota": SEDE_TI}),
    ("7c745246-2821-4690-9095-afd7be0383d4%2F5", "Magdalena", "estudiantes-titulados-sede", "no_especificada", {"calificador": {"sede": "Magdalena"}, "nota": SEDE_TI}),
    ("7c745246-2821-4690-9095-afd7be0383d4%2F6", "Benito Juárez", "estudiantes-titulados-sede", "no_especificada", {"calificador": {"sede": "Benito Juárez"}, "nota": SEDE_TI}),
]:
    PROP["https://example.org/mex-ontologi/definition/" + iri] = {
        "decision": "propuesta", "concepto": concepto, "representacion": rep,
        "calificador": extra["calificador"], "nota": extra["nota"]}

SIMPLE = [
    ("3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F3", "Sexo", "sexo-titulado", "no_especificada", "Sexo del titulado con ejemplo M; población titulados de posgrado."),
    ("5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F3", "Sexo", "sexo-titulado", "no_especificada", "Sexo del titulado con ejemplo M; población titulados de licenciatura."),
    ("508da131-e18f-45ac-9ec0-8aac03cea798%2F1", "Nivel", "nivel-estudios-matriculado", "nombre", "Nivel de estudios matriculado; ejemplo T.S.U."),
    ("508da131-e18f-45ac-9ec0-8aac03cea798%2F3", "Campo de Formación Académica", "campo-formacion-academica", "codigo", "Campo con clasificación 2016 declarada y catálogo publicado en la fila; ejemplo 7."),
    ("508da131-e18f-45ac-9ec0-8aac03cea798%2F4", "Hombres Titulados", "hombres-titulados-programa-anio", "no_especificada", "Total anual de hombres titulados por programa; ejemplo 41."),
    ("508da131-e18f-45ac-9ec0-8aac03cea798%2F5", "Mujeres Tituladas", "mujeres-tituladas-programa-anio", "no_especificada", "Total anual de mujeres tituladas por programa; ejemplo 6."),
    ("598dbd86-0a0b-42a4-ab3d-6cb656f9b605%2F1", "Nivel", "nivel-estudios-matriculado", "nombre", "Nivel de estudios matriculado; ejemplo T.S.U."),
    ("598dbd86-0a0b-42a4-ab3d-6cb656f9b605%2F3", "Campo de Formación Académica", "campo-formacion-academica", "codigo", "Campo con clasificación 2016 declarada y catálogo publicado en la fila; ejemplo 7."),
    ("598dbd86-0a0b-42a4-ab3d-6cb656f9b605%2F4", "Hombres Egresados", "hombres-egresados-programa-anio", "no_especificada", "Total anual de hombres egresados por programa; ejemplo 41."),
    ("598dbd86-0a0b-42a4-ab3d-6cb656f9b605%2F5", "Mujeres Egresadas", "mujeres-egresadas-programa-anio", "no_especificada", "Total anual de mujeres egresadas por programa; ejemplo 6."),
    ("a9685674-a360-4eec-9293-05ccede4a447%2F1", "Nivel", "nivel-estudios-matriculado", "nombre", "Nivel de estudios matriculado; ejemplo TSU."),
    ("a9685674-a360-4eec-9293-05ccede4a447%2F3", "Mujeres Nuevo Ingreso", "mujeres-nuevo-ingreso-tsu", "no_especificada", "Mujeres de nuevo ingreso a primer cuatrimestre de TSU; ejemplo 1."),
    ("a9685674-a360-4eec-9293-05ccede4a447%2F4", "Hombres Nuevo Ingreso", "hombres-nuevo-ingreso-tsu", "no_especificada", "Hombres de nuevo ingreso a primer cuatrimestre de TSU; ejemplo 19."),
    ("fe8e7f84-8ae2-4a26-95f2-f88579f198af%2F1", "Nivel", "nivel-estudios-matriculado", "nombre", "Nivel de estudios matriculado; ejemplo TSU."),
    ("fe8e7f84-8ae2-4a26-95f2-f88579f198af%2F3", "Mujeres Reingreso", "mujeres-reingreso-institucion", "no_especificada", "Mujeres de reingreso por programa; ejemplo 94."),
    ("fe8e7f84-8ae2-4a26-95f2-f88579f198af%2F4", "Hombres Reingreso", "hombres-reingreso-institucion", "no_especificada", "Hombres de reingreso por programa; ejemplo 51."),
    ("ed82f8a6-6414-4ce4-94df-302408eb2f67%2F1", "NIVEL", "nivel-estudios-matriculado", "nombre", "Nivel de estudios matriculado; ejemplo TSU."),
    ("ed82f8a6-6414-4ce4-94df-302408eb2f67%2F2", "CUATRIMESTRE", "cuatrimestre-reporte", "nombre", "Cuatrimestre reportado con periodos publicados; ejemplo Enero - Abril."),
    ("ed82f8a6-6414-4ce4-94df-302408eb2f67%2F5", "CAMPO DE FORMACIÓN ACADÉMICA", "campo-formacion-academica", "codigo", "Campo con clasificación 2016 declarada y catálogo publicado en la fila; ejemplo 07."),
    ("ed82f8a6-6414-4ce4-94df-302408eb2f67%2F6", "PROMEDIO DE APROVECHAMIENTO MUJER", "promedio-aprovechamiento-mujeres-programa", "no_especificada", "Promedio anual de mujeres por programa; ejemplo 8.66."),
    ("ed82f8a6-6414-4ce4-94df-302408eb2f67%2F7", "PROMEDIO DE APROVECHAMIENTO HOMBRE", "promedio-aprovechamiento-hombres-programa", "no_especificada", "Promedio anual de hombres por programa; ejemplo 8.78."),
    ("b3d332cd-ead7-4efd-ac03-25d8901aead7%2F1", "Programa academico", "programa-educativo", "nombre", "Nombre del programa académico que cursa el alumno; reutiliza concepto vigente exacto."),
    ("b3d332cd-ead7-4efd-ac03-25d8901aead7%2F3", "Sexo", "sexo-alumno", "no_especificada", "Sexo registrado del alumno; ejemplo M."),
    ("b3d332cd-ead7-4efd-ac03-25d8901aead7%2F4", "Promedio Actual", "promedio-actual-alumno", "no_especificada", "Promedio actual del alumno; ejemplo 7.9."),
    ("b3d332cd-ead7-4efd-ac03-25d8901aead7%2F5", "Promedio General", "promedio-general-alumno", "no_especificada", "Promedio general del alumno sin rango declarado; ejemplo 7.8."),
    ("b3d332cd-ead7-4efd-ac03-25d8901aead7%2F6", "Créditos Acumulados", "creditos-acumulados-alumno", "no_especificada", "Créditos totales del alumno; ejemplo 240."),
    ("b3d332cd-ead7-4efd-ac03-25d8901aead7%2F7", "Inscrito en Residencias", "indicador-residencias-alumno", "no_especificada", "Indicador de inscripción en residencias; ejemplo N."),
    ("b3d332cd-ead7-4efd-ac03-25d8901aead7%2F8", "Seguro Escolar", "indicador-seguro-escolar-alumno", "no_especificada", "Indicador de seguro escolar; ejemplo N."),
    ("b3d332cd-ead7-4efd-ac03-25d8901aead7%2F9", "Discapacidad", "indicador-discapacidad-alumno", "no_especificada", "Indicador de discapacidad; ejemplo N; distinto del tipo."),
    ("dc87a5be-8ef7-4e90-af72-ea5053423fad%2F2", "Sede", "sede-matricula-municipio", "nombre", "Municipio sede de matrícula; ejemplo Sede Hermosillo."),
    ("dc87a5be-8ef7-4e90-af72-ea5053423fad%2F3", "Nivel", "nivel-estudios-matriculado", "nombre", "Nivel de estudios matriculado; ejemplo TSU."),
    ("dc87a5be-8ef7-4e90-af72-ea5053423fad%2F4", "Modalidad", "modalidad-cursada", "nombre", "Modalidad cursada con dominio publicado de tres valores; ejemplo Escolarizada."),
    ("dc87a5be-8ef7-4e90-af72-ea5053423fad%2F6", "Campo de Formación Académica", "campo-formacion-academica", "codigo", "Campo con clasificación 2016 declarada y catálogo publicado en la fila; ejemplo 7."),
    ("dc87a5be-8ef7-4e90-af72-ea5053423fad%2F7", "Grado (Cuatrimestre)", "grado-cuatrimestre-cursado", "no_especificada", "Grado o cuatrimestre cursado; ejemplo 1."),
    ("dc87a5be-8ef7-4e90-af72-ea5053423fad%2F8", "Sexo", "sexo-alumno", "no_especificada", "Sexo del alumno; ejemplo H."),
    ("dc87a5be-8ef7-4e90-af72-ea5053423fad%2F9", "Estado de Nacimiento", "entidad-nacimiento-estudiante", "nombre", "Estado de nacimiento del estudiante; ejemplo Sonora."),
    ("dc87a5be-8ef7-4e90-af72-ea5053423fad%2F10", "Estado civil", "estado-civil-alumno", "nombre", "Estado civil del registro de matrícula; la población la fija el conjunto; ejemplo Soltero."),
    ("dc87a5be-8ef7-4e90-af72-ea5053423fad%2F11", "Edad", "edad-alumno", "no_especificada", "Edad del estudiante; ejemplo 20."),
    ("deecb2e7-a1b8-40ea-a13e-31e3322bff4b%2F1", "Unidad Académica", "unidad-academica-sede", "nombre", "Unidad donde se imparte el programa; ejemplo San Luis R.C."),
    ("deecb2e7-a1b8-40ea-a13e-31e3322bff4b%2F3", "Evaluados", "alumnos-evaluados-programa", "no_especificada", "Cantidad de alumnos evaluados; ejemplo vacío en la fila."),
    ("deecb2e7-a1b8-40ea-a13e-31e3322bff4b%2F4", "Menos de 7", "alumnos-rango-menor-7", "no_especificada", "Alumnos en rango <7; el rango lo da el nombre exacto."),
    ("deecb2e7-a1b8-40ea-a13e-31e3322bff4b%2F5", "de 7 hasta 7.9", "alumnos-rango-7-79", "no_especificada", "Alumnos en rango [7, 7.9]; el rango lo da el nombre exacto."),
    ("deecb2e7-a1b8-40ea-a13e-31e3322bff4b%2F6", "de 8 hasta 8.9", "alumnos-rango-8-89", "no_especificada", "Alumnos en rango [8, 8.9]; el rango lo da el nombre exacto."),
    ("deecb2e7-a1b8-40ea-a13e-31e3322bff4b%2F7", "de 9 hasta 10", "alumnos-rango-9-10", "no_especificada", "Alumnos en rango [9, 10]; el rango lo da el nombre exacto."),
    ("deecb2e7-a1b8-40ea-a13e-31e3322bff4b%2F8", "Promedio Global", "promedio-global-programa", "no_especificada", "Promedio general del programa; ejemplo vacío en la fila."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F1", "Unidad Académica", "unidad-academica-municipio", "nombre", "Municipio donde se encuentra la unidad académica; ejemplo Hermosillo."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F2", "Plan de Estudio", "programa-educativo", "codigo", "Clave del plan de estudio; reutiliza concepto vigente exacto con representación código; ejemplo 14."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F4", "Tipo de programa académico", "tipo-programa-educativo", "nombre", "Tipo de programa educativo; ejemplo Licenciatura."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F5", "Tipo de periodo", "tipo-periodo-programa", "nombre", "Tipo de periodo del programa; ejemplo Semestral."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F6", "Modalidad", "modalidad-programa-educativo", "nombre", "Modalidad del programa; ejemplo Escolarizado."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F9", "Grupos asignaturas inscrito ciclo escolar actual", "grupos-asignaturas-inscripcion", "no_especificada", "Grupos a los que se inscribió el alumno; ejemplo con claves de grupo."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F15", "Clave de Formación Académica", "campo-formacion-academica", "codigo", "Clave de formación académica sin catálogo declarado en esta fila; ejemplo 07; no se afirma edición ni equivalencia."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F16", "Campo de Formación Académica", "campo-formacion-academica", "nombre", "Campo en texto libre; ejemplo Ingeniería, manufactura y construcción; comparte concepto con su clave por mismo objeto denotado en el registro."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F18", "Nacionalidad", "nacionalidad-alumno", "nombre", "Nacionalidad del alumno; ejemplo vacío en la fila."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F21", "Sexo", "sexo-alumno", "no_especificada", "Sexo del alumno; ejemplo Masculino."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F22", "Edad", "edad-alumno", "no_especificada", "Edad del alumno; ejemplo 21."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F23", "Discapacidad_Tipo", "tipo-discapacidad-alumno", "no_especificada", "Tipo de discapacidad de tenerla; ejemplo vacío en la fila."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F24", "Estado civil", "estado-civil-alumno", "nombre", "Estado civil del alumno; ejemplo SOLTERO (A)."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F30", "Lugar de nacimiento", "lugar-nacimiento-alumno", "nombre", "Lugar de nacimiento del alumno; ejemplo CD. OBREGON."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F31", "Bachillerato", "institucion-bachillerato-alumno", "nombre", "Institución donde cursó el bachillerato; ejemplo GRIMAC."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F32", "Promedio de bachillerato", "promedio-bachillerato-alumno", "no_especificada", "Promedio final al salir del bachillerato; ejemplo 0.00."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F33", "Estado Bachillerato", "entidad-curso-bachillerato", "nombre", "Estado donde cursó el bachillerato; ejemplo SONORA."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F34", "Ciudad Bachillerato", "ciudad-curso-bachillerato", "nombre", "Ciudad donde cursó el bachillerato; ejemplo HUATABAMPO."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F36", "Egreso Bachillerato", "anio-egreso-bachillerato", "anio", "Año de egreso del bachillerato; ejemplo vacío en la fila."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F37", "Periodo escolar de ingreso", "clave-periodo-ingreso-alumno", "codigo", "Clave del periodo escolar de ingreso; ejemplo 201; sistema no acreditado."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F39", "Créditos cursados", "creditos-cursados-alumno", "no_especificada", "Total de créditos cursados; ejemplo 173; errata de origen preservada."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F40", "Nuevo Ingreso/Reingreso", "indicador-ingreso-reingreso-alumno", "nombre", "Indicador de nuevo ingreso o reingreso; ejemplo Reingreso."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F41", "Semestres cursados incluye ciclo actual", "semestres-cursados-con-actual", "no_especificada", "Semestres contando el ciclo actual; ejemplo 6."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F42", "Semestres cursados sin ciclo actual", "semestres-cursados-sin-actual", "no_especificada", "Semestres sin contar el ciclo actual; ejemplo 5."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F43", "Ultimo ciclo  escolar cursado", "clave-ultimo-ciclo-cursado", "codigo", "Clave del último ciclo cursado; ejemplo 222; sistema no acreditado."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F44", "Promedio ultimo ciclo cursado (Solo asig. aprobadas)", "promedio-ultimo-ciclo-aprobadas", "no_especificada", "Promedio del último ciclo solo aprobadas; ejemplo 0."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F45", "Promedio ultimo ciclo cursado(Todas las asignaturas)", "promedio-ultimo-ciclo-todas", "no_especificada", "Promedio del último ciclo todas; ejemplo 0."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F46", "Num. asignaturas reprobadas en ultimo ciclo cursado", "asignaturas-reprobadas-ultimo-ciclo", "no_especificada", "Reprobadas del último ciclo; ejemplo 0."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F50", "Promedio general (Solo asig. aprobadas)", "promedio-general-aprobadas", "no_especificada", "Promedio general solo aprobadas; ejemplo 8.85."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F51", "Promedio general (Todas las asignaturas)", "promedio-general-todas", "no_especificada", "Promedio general de todas; ejemplo 8.75."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F55", "Alumnos regulares e irregulares", "indicador-regularidad-alumno", "nombre", "Indicador regular/irregular; ejemplo Irregular."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F56", "Total de créditos del plan de estudio", "total-creditos-plan-alumno", "no_especificada", "Total de créditos del plan; ejemplo 320."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F57", "Alumno activo", "indicador-alumno-activo", "nombre", "Indicador de alumno activo o no; ejemplo ACTIVO."),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F60", "Periodo de la baja", "clave-periodo-baja-alumno", "codigo", "Clave del periodo de baja; ejemplo vacío; distinta de la fecha de baja ya respaldada."),
]
for iri, var, concepto, rep, nota in SIMPLE:
    PROP["https://example.org/mex-ontologi/definition/" + iri] = {
        "decision": "propuesta", "concepto": concepto, "representacion": rep,
        "calificador": None, "nota": nota}

PEND = {
    "3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F1": "Descripción genérica de orden de fila ('Numero de la entrada'); sin referente al objeto. Pendiente.",
    "5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F1": "Descripción genérica de orden de fila ('Numero de la entrada'); sin referente al objeto. Pendiente.",
    "b3d332cd-ead7-4efd-ac03-25d8901aead7%2F2": "Descripción confusa o truncada ('Semestre en el hasta el cual persiven los datos del alumno'); no defendible. Pendiente.",
    "dc87a5be-8ef7-4e90-af72-ea5053423fad%2F1": "Número consecutivo de fila de matrícula ('Número consecutivo, que significa estudiante matriculado'); identificador de orden, no denota objeto. Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F7": "Descripción genérica sin referente publicado ('Numero del alumno'); podría ser orden de fila. Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F8": "Descripción vacía ('Pendiente de especificar'); el ejemplo no sustituye la descripción. Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F11": "Descripción vacía ('Pendiente de especificar'). Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F12": "Descripción vacía ('Pendiente de especificar'). Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F13": "Descripción vacía ('Pendiente de especificar'). Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F17": "Descripción vacía ('Pendiente de especificar'). Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F25": "Descripción vacía ('Pendiente de especificar'); no se infiere etnia por el nombre. Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F26": "Descripción vacía ('Pendiente de especificar'); no se infiere etnia por el nombre. Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F27": "Descripción vacía ('Pendiente de especificar'); no se infiere etnia por el nombre. Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F28": "Descripción vacía ('Pendiente de especificar'); no se infiere etnia por el nombre. Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F29": "Descripción vacía ('Pendiente de especificar'); no se infiere etnia por el nombre. Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F35": "Descripción vacía ('Pendiente de especificar'); no se infiere área por el nombre. Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F47": "Descripción vacía ('Pendiente de especificar'); el ejemplo 8.2 no sustituye la descripción. Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F48": "Descripción vacía ('Pendiente de especificar'); el ejemplo 8.2 no sustituye la descripción. Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F49": "Descripción vacía ('Pendiente de especificar'); el ejemplo 0 no sustituye la descripción. Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F52": "Descripción vacía ('Pendiente de especificar'). Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F53": "Descripción vacía ('Pendiente de especificar'). Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F54": "Descripción vacía ('Pendiente de especificar'). Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F58": "Descripción vacía ('Pendiente de especificar'). Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F61": "Descripción genérica sin leyenda publicada ('Tipo de baja'); dominio de valores no acreditado. Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F62": "Descripción vacía ('Pendiente de especificar'). Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F63": "Descripción vacía ('Pendiente de especificar'); no se promueve a catálogo ni a identidad. Pendiente.",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F65": "Descripción vacía ('Pendiente de especificar'); no se promueve a catálogo ni a identidad. Pendiente.",
}
PEND = {"https://example.org/mex-ontologi/definition/" + k: v for k, v in PEND.items()}

# ---------------------------------------------------------------- build
asig_by_iri = {v["definicion_iri"]: v for v in MINE}
insp_by_iri = {r["iri"]: r for r in INSP}
assert len(asig_by_iri) == 126 and len(insp_by_iri) == 126
assert set(asig_by_iri) == set(insp_by_iri), "particion asignada != inspeccion"
assert set(PROP) | set(PEND) == set(asig_by_iri) and not (set(PROP) & set(PEND)), "decision incompleta o solapada"

decisiones, reglas = [], []
n = 0
for iri in sorted(asig_by_iri):
    a = asig_by_iri[iri]
    r = insp_by_iri[iri]
    assert a["variable"].strip() == r["var"].strip(), iri
    assert a["descripcion"] == r["desc"], iri
    assert a["huella_fila_diccionario"] == r["huella"], iri
    meta = META.get(a["conjunto"], {})
    recs = [x for x in meta.get("resources", []) if x["id"] == a["diccionario"]]
    fuente_url = recs[0]["url"] if recs and recs[0].get("url") else ""
    ctx = {"notas_conjunto": r["notas_conjunto"], "grupos": r["grupos"],
           "frecuencia": meta.get("frequency"), "organizacion": (meta.get("organization") or {}).get("title"),
           "fuente_diccionario_url": fuente_url}
    if iri in PEND:
        decisiones.append({"definicion_iri": iri, "conjunto": a["conjunto"], "diccionario": a["diccionario"],
            "variable": a["variable"], "descripcion": a["descripcion"],
            "huella_fila_diccionario": a["huella_fila_diccionario"], "tipo_de_dato": r["tipo"], "formato": r["formato"],
            "unidad_de_medida": r["unidad"], "catalogo_de_referencia": r["catalogo"],
            "ejemplo_de_dato": r["ejemplo"], "decision": "pendiente", "motivo": PEND[iri],
            "contexto_conjunto": ctx})
        continue
    p = PROP[iri]
    n += 1
    rid = "%s%03d" % (R3A8, n)
    decisiones.append({"definicion_iri": iri, "conjunto": a["conjunto"], "diccionario": a["diccionario"],
        "variable": a["variable"], "descripcion": a["descripcion"],
        "huella_fila_diccionario": a["huella_fila_diccionario"], "tipo_de_dato": r["tipo"], "formato": r["formato"],
        "unidad_de_medida": r["unidad"], "catalogo_de_referencia": r["catalogo"],
        "ejemplo_de_dato": r["ejemplo"], "decision": "propuesta", "concepto": p["concepto"],
        "regla_id": rid, "criterio": p["nota"], "contexto_conjunto": ctx})
    ev = {"variable": a["variable"], "descripcion": a["descripcion"], "definicion_iri": iri,
          "diccionario": a["diccionario"], "conjunto": a["conjunto"],
          "huella_fila_diccionario": a["huella_fila_diccionario"],
          "unidad_de_medida": r["unidad"], "tipo_de_dato": r["tipo"],
          "ejemplo_de_dato": r["ejemplo"], "catalogo_de_referencia": r["catalogo"]}
    contra = "No aplica a otra definición: la regla exige conjunto, diccionario, IRI, nombre y descripción exactos."
    lim = "Alcance fijado a esta definición; sin correspondencia columna-variable; sin vigencia, identidad ni cruce."
    if p["calificador"]:
        lim += " Calificador formal pendiente de propagación por el pipeline (ver requisitos_integracion)."
    if (r["catalogo"] or "").strip():
        lim += " Catálogo solo referencia declarada sin resolver; no acredita sistema de identificadores."
    if p["concepto"] == "unidad-academica-municipio":
        lim += " El nombre dice unidad; la descripción denota municipio (manda la descripción)."
    if p["concepto"] in ("clave-periodo-ingreso-alumno", "clave-ultimo-ciclo-cursado",
                         "clave-periodo-baja-alumno", "programa-educativo") and "clave" not in clave(a["variable"]):
        lim += " El nombre no dice clave; la descripción sí (manda la descripción); sistema de claves no acreditado."
    if p["concepto"] == "estado-civil-alumno" and "alumno" not in clave(a["descripcion"]):
        lim += " Descripción sin población explícita; la población la fijan conjunto y notas publicadas (matrícula inscrita clasificada por atributos del estudiante)."
    if p["concepto"] in ("nacionalidad-alumno", "lugar-nacimiento-alumno",
                         "entidad-nacimiento-estudiante", "entidad-curso-bachillerato",
                         "ciudad-curso-bachillerato"):
        lim += " Lugar o entidad de nacimiento y nacionalidad son conceptos distintos; no se infiere extranjería ni residencia."
    if p["concepto"] == "campo-formacion-academica":
        lim += " Código y nombre del mismo registro comparten concepto; no se afirma correspondencia código↔valor ni edición fuera de la fila que la declara."
    if p["concepto"] in ("sexo-alumno", "sexo-titulado", "estado-civil-alumno", "nacionalidad-alumno",
                         "tipo-discapacidad-alumno", "lugar-nacimiento-alumno", "institucion-bachillerato-alumno",
                         "entidad-curso-bachillerato", "ciudad-curso-bachillerato", "modalidad-programa-educativo",
                         "modalidad-cursada", "tipo-programa-educativo", "unidad-academica-sede",
                         "unidad-academica-municipio", "sede-matricula-municipio", "campo-formacion-academica"):
        lim += " Categorías y textos propios de la fuente; sin homologar entre filas ni con catálogos oficiales."
    regla = {"id": rid, "concepto": p["concepto"], "representacion": p["representacion"],
             "descripciones": [a["descripcion"]], "nombres": [a["variable"]],
             "conjuntos": [a["conjunto"]], "diccionarios": [a["diccionario"]],
             "definiciones": [iri],
             "criterio": "Revisión agente 8 ronda 3; lectura completa de la fila; " + p["nota"],
             "fuente_revision": "propuestas/ronda-3/agente-8-educacion/propuestas.json",
             "alcance": "Solo este conjunto, diccionario, definición y nombre.",
             "contraejemplo": contra, "limite": lim, "evidencia": [ev]}
    if p["calificador"]:
        regla["calificador"] = p["calificador"]
    reglas.append(regla)

usados = {d["concepto"] for d in decisiones if d["decision"] == "propuesta"}
assert usados <= set(CONCEPTOS_NUEVOS) | set(CONCEPTOS_REUTILIZADOS)
conceptos_nuevos = {k: v for k, v in CONCEPTOS_NUEVOS.items() if k in usados}

insumos = {"asignaciones": CENTRO / "propuestas/ronda-3/integrador/asignaciones-semanticas.json",
           "pendientes": CENTRO / "reports/pendientes-semanticos.json",
           "cobertura": CENTRO / "data/semantica/cobertura.json",
           "semantica": CENTRO / "ontologia/semantica.json"}
huellas = {}
for k, pth in insumos.items():
    h, b = sha256_archivo(pth)
    huellas[k] = {"sha256": h, "bytes": b, "ruta": str(pth.relative_to(CENTRO))}
h_insp = hashlib.sha256()
for r in sorted(INSP, key=lambda x: x["iri"]):
    h_insp.update(json.dumps(r, ensure_ascii=False, sort_keys=True).encode("utf-8"))

propuesta = {
    "generado_en_utc": datetime.now(timezone.utc).isoformat(),
    "agente": "agente-8-educacion",
    "base_iri": "https://example.org/mex-ontologi/",
    "huellas_entrada": huellas,
    "huella_inspeccion_126": h_insp.hexdigest(),
    "alcance": "Partición exclusiva del agente 8: 126 variables fuera del núcleo (educación), con decisión tras lectura literal individual.",
    "decisiones": decisiones,
    "reglas": reglas,
    "conceptos_nuevos": conceptos_nuevos,
    "conceptos_reutilizados": CONCEPTOS_REUTILIZADOS,
    "limites": [
        "Sin nuevas correspondencias columna-variable; las candidatas futuras requieren revisión documental.",
        "Sin owl:sameAs ni skos:exactMatch; sin equivalencia de catálogos.",
        "Sin descargas ni contactos: evidencia local publicada; URLs de diccionarios registradas sin descargar microdatos.",
        "Literales con caracteres latinos preservados byte-exactos; ninguna normalización ñ→n.",
        "Las 20 reglas con calificador de sede requieren propagación del calificador por el pipeline antes de aplicar (ver requisitos_integracion); el pipeline actual no lo preserva.",
    ],
    "requisitos_integracion": {
        "calificador_sede": "Las 20 reglas de conteos por sede comparten concepto con calificador formal distinto por sede. interpretacion()/construir() no propagan calificador a la variable documentada ni al grafo (misma limitación documentada por agente 3). Requisito antes de aplicar: propagar el calificador y validar sede distinta por regla. Alternativa: 4×5 conceptos estrechos por sede.",
        "aritmetica_simulada": {"respaldadas": 232 + len(reglas), "fuera_del_nucleo": 1308 - len(reglas),
                                "candidatas_agente4": 23, "conceptos": 103 + len(conceptos_nuevos),
                                "revisadas_intactas": 836, "candidatas_columna": 118},
    },
    "nota": "Propuestas de significado separadas del inventario. Ninguna crea correspondencia columna-variable ni uso automático en cruces. Los 23 significados candidatos del agente 4 no se tocan.",
}
json.dump(propuesta, open(BASE / "propuestas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
huellas_fuente = dict(huellas)
huellas_fuente["huella_inspeccion_126"] = h_insp.hexdigest()
huellas_fuente["inspecciones_diccionarios"] = {}
for dic in sorted({v["diccionario"] for v in MINE}):
    pth = CENTRO / ("data/portal/inspecciones/%s.json" % dic)
    h, b = sha256_archivo(pth)
    huellas_fuente["inspecciones_diccionarios"][dic] = {"sha256": h, "bytes": b}
h, b = sha256_archivo(CENTRO / "data/catalogo/metadatos.json")
huellas_fuente["metadatos"] = {"sha256": h, "bytes": b,
                               "ruta": "data/catalogo/metadatos.json"}
json.dump(huellas_fuente, open(BASE / "fuente/huellas.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("decisiones=%d reglas=%d conceptos_nuevos=%d pendientes=%d" % (
    len(decisiones), len(reglas), len(conceptos_nuevos),
    sum(1 for d in decisiones if d["decision"] == "pendiente")))
