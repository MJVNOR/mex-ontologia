# Preguntas al publicador (sin contactar; redactadas para tramite)

Q-FIEBRE-DICC agrupa 3 columnas ambiguas (6 vinculos) + referencia des_mpo_res por compartir origen (filas 177/178 del diccionario 33d0a99e).
Los literales citados (p. ej. 'a–o', 'año') son exactos de la fuente; la sintesis del agente va separada y no se presenta como literal.

## Q-PEND-SEED

Origen: Descripcion literal 'Pendiente de especificar' en 5 variables del diccionario 12f684e9 (SEED).

Items: S-clues-12f684e9, S-localidadocurrencia-12f684e9, S-localidadocurrenciad-12f684e9, S-municipioocurrencia-12f684e9, S-municipioocurrenciad-12f684e9

Para CLUES, MUNICIPIOOCURRENCIA, MUNICIPIOOCURRENCIAD, LOCALIDADOCURRENCIA y LOCALIDADOCURRENCIAD del diccionario 12f684e9 (conjunto cd3d6e34): proporcionar la descripcion real de cada variable (evento, papel territorial, representacion codigo/nombre). Sin esa descripcion no se puede asignar significado.

## Q-PEND-NAC

Origen: Descripcion literal 'Pendiente de especificar' en 5 variables del diccionario 22202305 (Nacimientos).

Items: S-clues-22202305, S-localidadcertifica-22202305, S-localidadcertificad-22202305, S-municipiocertifica-22202305, S-municipiocertificad-22202305

Para CLUES, MUNICIPIOCERTIFICA, MUNICIPIOCERTIFICAD, LOCALIDADCERTIFICA y LOCALIDADCERTIFICAD del diccionario 22202305 (conjunto 940de7d8): proporcionar la descripcion real de cada variable (p. ej. certificante: persona, institucion, unidad; papel territorial). Sin esa descripcion no se puede asignar significado.

## Q-PEND-MAT

Origen: Descripcion literal 'Pendiente de especificar' en 7 variables del diccionario 8c0e76ff (Matriculas).

Items: S-fecha-de-alternativa-de-titulacion-de-examen-prof-8c0e76ff, S-fecha-de-alternativa-de-titulacion-de-no-exigibilidad-8c0e76ff, S-fecha-de-impresion-del-titulo-profesional-8c0e76ff, S-fecha-de-la-convalidacion-8c0e76ff, S-fecha-de-la-equivalencia-8c0e76ff, S-fecha-de-titulacion-del-titulo-profesional-8c0e76ff, S-fecha-inscripcion-en-ciclo-escolar-senalado-8c0e76ff

Para las 7 variables con 'Pendiente de especificar' del diccionario 8c0e76ff (conjunto e819466c): proporcionar la descripcion real de cada fecha/variable (evento, poblacion). Sin esa descripcion no se puede asignar significado ni deducirlo del nombre.

## Q-CLAVE-GEO

Origen: Estatuto de referencia de CVE_LOC del IML_2020: estructura 9=2+3+4 ya observada, referencia oficial/completitud/vigencia no acreditadas.

Items: S-cve-loc-251309e5

Para CVE_LOC del diccionario 251309e5 (conjunto b54f94ee, huella e94b71...): la composicion CVE_LOC(9)=ENT(2)+MUN(3)+LOC(4) ya esta observada y verificada en IML_2020 (1850/1850, ejemplo 260010001=26+001+0001) y no se pregunta por ella. Aclarar unicamente: (1) si este diccionario adopta esa composicion como referencia y con que formato declarado; (2) si cubre el universo completo de localidades o solo las incluidas en el estudio 2020; (3) corte/vigencia de la referencia. Sin eso no se acredita caracter oficial, completitud ni vigencia.

## Q-TRIMESTRE

Origen: Descripcion generica 'Trimestre del estrato'.

Items: S-trimestre-3f6942e3

Para TRIMESTRE del diccionario 3f6942e3 (conjunto c589afac): indicar a que evento corresponde el trimestre (denuncia, estrato, ocurrencia) y su cobertura. Afirmable con limite: granularidad trimestral.

## Q-FECHA-PRESAS

Origen: Descripcion generica 'Fecha del registro.' (Cuerpos de Agua).

Items: S-fecha-bfb8788b

Para Fecha del diccionario bfb8788b (conjunto 8c1f452e): indicar que fecha registra (alta del registro, medicion, captura). Afirmable con limite: referencia temporal de registro.

## Q-PERIODO-CERESOS

Origen: Descripcion con erratas 'perido del cual se informa la numero de poblacion'.

Items: S-periodo-2fc2fbc6

Para periodo del diccionario 2fc2fbc6 (conjunto 5f2e31dd): corregir/precisar el periodo (cobertura, granularidad, unidad). Afirmable con limite: periodo de referencia de la poblacion informada.

## Q-MES-MINERA

Origen: Descripcion 'Registro cronologico...' para la variable Mes (Produccion minera).

Items: S-mes-587a3ccd

Para Mes del diccionario 587a3ccd (conjunto 7e97d026): precisar si Mes es la granularidad del registro o el evento de extraccion, y el anio de contexto. Afirmable con limite: dimension cronologica de produccion minera.

## Q-MUN-MATRICULAS

Origen: Descripcion truncada 'Municipio donde el alumno'.

Items: S-municipio-8c0e76ff

Para Municipio del diccionario 8c0e76ff (conjunto e819466c, huella ad4584...): completar la frase (residencia, escuela, nacimiento, otro papel). Afirmable con limite: referencia municipal vinculada al alumno.

## Q-EGRESOS

Origen: Contradiccion Total_Egresos vs 'Total de urgencias atendidas'.

Items: O-egresos

Para Total_Egresos del recurso ad6f77b8 (diccionario f89137ba, huella 98c73e..., descripcion original 'Total de urgencias atendidas'): aclarar si la columna cuenta egresos hospitalarios o urgencias atendidas, y corregir el nombre o la descripcion para que coincidan.

## Q-FORMATO-MUN

Origen: Formato 'nnn' frente a ejemplo '26048' (CVE_MUN, IMM 2020).

Items: O-mun-formato

Para CVE_MUN del recurso 046c2f52 (diccionario 3395795d, huella 35fb21..., descripcion original 'Clave del municipio'): corregir el formato declarado 'nnn' o el ejemplo '26048' (cinco caracteres) e indicar la composicion del codigo. Afirmable con limite: significado municipal; codificacion y correspondencia con CVEGEO sin resolver.

## Q-FECHA-NUM

Origen: Formato 'DD/MM/AAAA' frente a ejemplo '45658' (Precipitacion).

Items: O-fecha-num

Para Fecha del recurso c07fe117 (diccionario 6713de4e, huella 30327f..., descripcion original 'Fecha del registro diario de precipitación'): indicar la representacion real de las fechas (formato declarado 'DD/MM/AAAA' frente a ejemplo '45658') antes de convertir o cruzar. Afirmable con limite: fecha de registro diario.

## Q-ANIO-NAC2024

Origen: Campo 'a–o' en el esquema frente a variable 'año' en el diccionario (Nacimientos 2024).

Items: O-anio-nac2024

Para el campo 'a–o' del recurso ffca84a8 (Nacimientos 2024, columna https://example.org/mex-ontologi/column/ffca84a8-155e-41af-8223-0e098966cadf/a%E2%80%93o): confirmar el nombre correcto del campo y si equivale a la variable 'año' del diccionario. No se corrige automaticamente ni se transfiere la revision de 2022.

## Q-FIEBRE-DICC

Origen: Filas 177/178 degeneradas del diccionario 33d0a99e (ide_id/ide_col, catalogo des_mpo_res).

Items: A-30b18862, A-4121cf57, A-cc6c566f, R-des-mpo-res

Para el diccionario 33d0a99e de Fiebre manchada (conjunto 5494daa1): (1) aclarar que describen las lineas 177 (huella 4b1762..., ejemplo ide_cp) y 178 (huella b5dbcd..., ejemplo id_cp) con celdas ide_id/ide_col/des_jur_res/des_mpo_res/cve_loc_res; (2) indicar si existe un catalogo publicado 'des_mpo_res' y donde; el catalogo.xlsx del conjunto (sha256 3b8546..., 3 hojas) no lo contiene. Afecta a las columnas ide_id de los recursos 30b18862, 4121cf57 y cc6c566f (Hoja1/1, 6 vinculos ambiguos) y a la referencia des_mpo_res: sin esta aclaracion no se elige vinculo ni se identifica catalogo.
