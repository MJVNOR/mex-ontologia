# Resultado matriculas (ronda 5)

Asignados: 30. Decisiones: 0 proponer, 30 pendiente, 0 artefacto_documental.
Reglas nuevas: 0. Conceptos nuevos: 0 (bloqueo auditor: retiradas r5mat-001 a r5mat-015).
Reutilizacion de vigentes: ninguna.
Columnas: 8 candidatas verificadas fisicamente (esquema 70 campos, nombres unicos, IRI exacta) pero sin vinculo: 0 proponer (dependian de reglas retiradas).
Vinculos: 0. Solicitudes web: 5 (MAT-W-01 a MAT-W-05).

## Bloqueo auditor y nueva version (caso por caso)

- r5mat-001 (/13), r5mat-002 (/14), r5mat-004 a r5mat-008 (/47,/48,/49,/52,/53), r5mat-010 a r5mat-015 (/64,/66,/67,/68,/69,/70):
  descripcion 'Pendiente de especificar'; respaldo era solo nombre+tipo/ejemplo. RETIRADAS.
- r5mat-003 (/20 Municipio): descripcion trunca 'Municipio donde el alumno' sin verbo; la funcion municipal,
  nucleo del significado, ausente. No sustantiva. RETIRADA.
- r5mat-009 (/61 Tipo de baja): descripcion 'Tipo de baja' tautologica (repite el nombre; sin sujeto, dominio ni valores).
  No sustantiva. RETIRADA.
- Las 8 columnas y 8 vinculos dependientes, retirados con sus reglas; las correspondencias quedan candidatas.

## Dictamen previo revisado (no repetido)

- Agente-8 educacion marco /11, /12, /13 y /17 pendientes por descripcion vacia ('Pendiente de especificar').
- Ronda-4 INV-P-07 exigio respaldo explicito de las 28 definiciones vacias de Matriculas.
- Revision propia: filas completas (tipo/formato/ejemplo) + esquema del recurso + huellas recomputadas 30/30.
- Ninguna fila tiene descripcion sustantiva ni evidencia externa vinculada: 30 pendientes con evidencia faltante precisa.

## Verificacion

- Huellas de fila recomputadas con huella() de scripts/consolidar_semantica.py: 30/30 OK.
- Huella de esquema recomputada (tabla Estudiantes 2022-2): ae4056d7c6061d7fe592405869ca2944964278784834ddf69af8ffe6b7cdc82a.
- 8 columnas localizadas (posicion, nombre unico e IRI verificados); sin vinculo por reglas retiradas.
- Reglas, conceptos y vinculos: 0 (retirados; sin colisiones que verificar).

## Busquedas negativas

- Descarga directa del portal (API CKAN package_show del dataset) bloqueada por WAF del sitio (pagina 'Acceso no permitido', CODIGO BWAF);
  se usan las instantaneas congeladas data/portal/inspecciones (2026-10-23) como fuente primaria. Sin archivo de intento conservado.
- Sin diccionario corregido UES ni norma de titulacion/evaluacion en fuentes locales: 30 pendientes con evidencia faltante precisa.
- Ninguna fuente externa respalda aplicacion local: no se promociona por nombre, clasificador ni documentacion nacional.

## Pendientes (30)

Motivos y evidencia faltante en entrega.json -> pendientes; solicitudes web en solicitudes_web.json.

## Archivos

- entrega.json, solicitudes_web.json, resultado.md, listo.json, construir.py
- sha256(entrega.json) = e8ce4f70c618570aa56ba97adab35c47f31f7ae8478eb541ca724daa5902dc35
