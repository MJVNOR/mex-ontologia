# S3-matrículas — entrega R8 v001 (2026-10-24)

30/30 decisiones: brecha_externa, 0 propuestas. Sin pista primaria nueva en ningún ID.
Evidencia previa re-verificada desde bytes (hashes coinciden con R7). Cero peticiones
web nuevas: WEB-MAT-02 quedó cerrada sin hallazgo por W-web v004 (F-V004-01);
WEB-MAT-01 parcial-negativa y WEB-MAT-00 revisión local, ambas ya atendidas.
No se repiten búsquedas agotadas. No se tocó Gemma/chat, no se contactó publicadores.

## Brechas (documento faltante por ID)

- /8 Inscrito ciclo escolar actual: definición del valor '222 (Reing)' y del ciclo actual de referencia.
- /11 Ciclo escolar actual motivo no inscrito: dominio de motivos de no inscripción con ejemplos.
- /12 Inscritos ciclo escolar señalado: definición del valor '222 (Reing)' y del ciclo señalado de referencia.
- /13 Grupos asignaturas inscrito en ciclo escolar señalado: qué ciclo remite 'señalado' y qué denotan los códigos.
- /14 Fecha inscripción en ciclo escolar señalado: evento y ciclo de la fecha.
- /17 Se realizó equivalencia en el ciclo actual: dominio y representación del campo.
- /20 Municipio: función municipal (residencia, registro u otra).
- /25 Estímulo Ciclo Actual: dominio del campo (catálogo o indicador) con ejemplos.
- /26 Grupo Indig. (Pertenece): instrumento o diccionario corregido, faceta pertenencia.
- /27 Grupo Indig. (Habla): instrumento o diccionario corregido, faceta habla.
- /28 Grupo Indig. (Vive en Comunidad): instrumento o diccionario corregido, faceta residencia.
- /29 Grupo Indig. (Padres): instrumento o diccionario corregido, faceta padres.
- /35 Área Bachillerato: dominio del campo con ejemplos.
- /47 Promedio anterior (solo aprobadas): escala, rango, método y cobertura.
- /48 Promedio anterior (todas): escala, rango, método y cobertura.
- /49 Num. reprobadas ciclo anterior: método de conteo.
- /52 Promedio periodo inscrito (solo aprobadas): escala y método (doble escala sin declarar).
- /53 Promedio periodo inscrito (todas): escala y método (doble escala sin declarar).
- /54 Inscrito ciclo actual (solo Serv.Soc./Pract.Prof.): representación y dominio.
- /58 Periodo escolar de egreso: definición y representación con ejemplos.
- /61 Tipo de baja: dominio y valores admisibles con ejemplos.
- /62 Cambio de Unidad Académica: representación y dominio con ejemplos.
- /63 Alternativa de no exigibilidad: norma UES que la defina y su registro.
- /64 Fecha de alternativa de no exigibilidad: evento y norma.
- /65 Alternativa de examen profesional: norma UES que la defina y su registro.
- /66 Fecha de alternativa de examen profesional: evento y norma.
- /67 Fecha de titulación del título profesional: evento de titulación.
- /68 Fecha de impresión del título profesional: evento de impresión.
- /69 Fecha de la convalidación: evento y norma.
- /70 Fecha de la equivalencia: evento y norma.

## Verificación (pruebas)

Comando ejecutado (sin instalar nada, solo stdlib):

`uv run python -c` — valida `v001/entrega.json`: 30 IDs exactos de asignación,
estados en {brecha_externa}, cada evidencia con `ruta+sha256+localizador`, y que
cada SHA-256 citado coincide con los bytes del archivo en disco (incluida la
fuente W-v004 citada en /63–/66). Resultado: OK 30/30, 0 propuestas, 0 fallos.

## Archivos

- v001/entrega.json
- v001/entrega.md
- v001/congelada.json (SHA-256 de entrega.json y entrega.md, calculados por código)
