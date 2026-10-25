# Q-unidades v002 — exclusiones y fuera de seleccion

Total inventariado: 61 literales, 259 filas con `Unidad de medida` no vacia (486 diccionarios, base R9).

## Ya en R9 (no se duplica)

- `Hectáreas` (1 fila): vinculada en R9 como P1-Q3 con el mismo literal; no se duplica.

## Fuera de la seleccion de 6

- `Hectáreas` (13 filas): mismo literal ya vinculado en R9 (P1-Q3); la declaracion es por definicion, no se duplica.
- `Milímetros` (1 fila): mismo literal ya vinculado en R9 (P1-Q1); la declaracion es por definicion, no se duplica.
- `Porcentaje` (49 filas): literal compartido por varias definiciones; se propone una sola (alcance de 6 casos).
- `Toneladas` (2 filas): literal compartido por varias definiciones; se propone una sola (alcance de 6 casos).

## Excluidas (no son unidad resoluble)

- `"AAAA"` (1 fila): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `"REPORTE DE LA FAUNA SILVESTRE DE LA TEMPORADA DE CAZA AAAA-AAAA DEL ESTADO DE SONORA"` (1 fila): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `1, 2, 3` (1 fila): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `1-32 (De acuerdo a clasificación de INEGI)` (8 filas): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `1.Otoño-invierno;  2.Primavera-verano; 3.Perennes` (1 fila): enumeracion de categorias o escala; no es unidad.
- `AAAA` (2 filas): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `Abeja; Ave; Caprino; Guajolote; Ovino; Porcino` (1 fila): enumeracion de categorias o escala; no es unidad.
- `Año` (3 filas): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `Barrio; Colonia; Ejido; Fraccionamiento; Privada; Residencial; Unidad habitacional` (1 fila): enumeracion de categorias o escala; no es unidad.
- `C` (1 fila): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `CC` (4 filas): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `CCC` (3 filas): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `CCCC` (1 fila): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `CIERRE DE PRODUCCION AGRICOLA AAAA ; AVANCE DE PRODUCCION AGRICOLA AAAA` (1 fila): enumeracion de categorias o escala; no es unidad.
- `CIERRE DE PRODUCCION PECUARIA AAAA ; AVANCE DE PRODUCCION PECUARIA AAAA` (1 fila): enumeracion de categorias o escala; no es unidad.
- `Cabezas` (15 filas): conteo; sin termino fisico exacto local.
- `Cantidad de cintillos` (2 filas): conteo; sin termino fisico exacto local.
- `Captura; Cosecha; Aguas Continentales` (1 fila): enumeracion de categorias o escala; no es unidad.
- `Carne; Huevo; Leche; Miel` (1 fila): enumeracion de categorias o escala; no es unidad.
- `De acuerdo a clasificación de INEGI` (12 filas): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `Del 1 al 32` (1 fila): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `Edad en años` (1 fila): magnitud con la unidad embebida en el nombre ('años'); fuera de la seleccion de 6.
- `Grados` (2 filas): ambiguo sin calificativo (angulo vs temperatura); existe ademas 'Grados celcius' en otra definicion.
- `Hectómetros cúbicos` (1 fila): hm3: busqueda agotada (HectoM3 404 + ausente del indice QUDT 3.5.3, sello W v003); no se repite ni se sustituye por M3.
- `La unidad de medida que se indica en la siguiente variable` (3 filas): referencia indirecta a otra columna; sin literal propio.
- `Mantiene las unidades indicadas en UMED` (1 fila): referencia indirecta a otra columna; sin literal propio.
- `Miles de litros; Toneladas` (1 fila): unidad compuesta: mezcla dos unidades (litros y toneladas) para una columna UMED; no se resuelve localmente.
- `Miles de pesos MXN` (2 filas): moneda o escala de moneda; no es magnitud fisica con termino exacto local.
- `Muy bajo; Bajo; Medio; Alto; Muy alto` (4 filas): enumeracion de categorias o escala; no es unidad.
- `N/A` (9 filas): sin dato declarado; no es unidad.
- `No aplica` (5 filas): sin dato declarado; no es unidad.
- `Nombre de entidad` (8 filas): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `Nombre de localidad` (3 filas): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `Nombre de municipio` (7 filas): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `Número de adultos mayores (de 60 años y más) por cada 100 personas jóvenes (de 0 a 14 años)` (1 fila): razon o indicador expresado en prosa; no es unidad.
- `Número de adultos mayores (de 65 años y más) por cada 100 personas jóvenes (de 0 a 14 años)` (1 fila): razon o indicador expresado en prosa; no es unidad.
- `Número de adultos mayores dependientes (de 65 años y más) por cada 100 personas en edad productiva (de 15 a 64 años)` (1 fila): razon o indicador expresado en prosa; no es unidad.
- `Número de dependientes (de 0 a 14 años y de 65 años y más) por cada 100 personas en edad productiva (de 15 a 64 años)` (1 fila): razon o indicador expresado en prosa; no es unidad.
- `Número de habitantes` (40 filas): conteo; sin termino fisico exacto local.
- `Número de habitantes en el municipio por cada 100 habitantes en el estado` (1 fila): razon o indicador expresado en prosa; no es unidad.
- `Número de inafantes (de 0 a 14 años) por cada 100 personas en edad productiva (de 15 a 64 años)` (1 fila): razon o indicador expresado en prosa; no es unidad.
- `Pesos MXN` (1 fila): moneda o escala de moneda; no es magnitud fisica con termino exacto local.
- `Pesos Mexicanos` (13 filas): moneda o escala de moneda; no es magnitud fisica con termino exacto local.
- `Pesos Mexicanos (MXN)` (1 fila): moneda o escala de moneda; no es magnitud fisica con termino exacto local.
- `Pesos por tonelada` (1 fila): unidad compuesta (precio o rendimiento por unidad); requiere termino precoordinado que Q no acredita localmente.
- `Pesos/kilogramo` (3 filas): unidad compuesta (precio o rendimiento por unidad); requiere termino precoordinado que Q no acredita localmente.
- `Productores` (1 fila): conteo; sin termino fisico exacto local.
- `Sexo` (2 filas): codigo, nombre, clasificacion, rango o texto: no es unidad.
- `Toneladas/hectáreas` (1 fila): unidad compuesta (precio o rendimiento por unidad); requiere termino precoordinado que Q no acredita localmente.
- `Total de habitantes` (5 filas): conteo; sin termino fisico exacto local.
- `Total de habitantes hombres por cada 100 mujeres` (1 fila): razon o indicador expresado en prosa; no es unidad.
- `cantidad de mujeres atendidas` (1 fila): conteo; sin termino fisico exacto local.
- `des_cal` (2 filas): referencia indirecta a otra columna; sin literal propio.

## Notas

- **hm3**: busqueda agotada en W v003 (HectoM3 404 + ausente del indice QUDT 3.5.3). No se repite sin pista primaria distinta; no se usa M3 ni factor alguno.
- **Compuestas** (`Pesos/kilogramo`, `Toneladas/hectáreas`, `Pesos por tonelada`, `Miles de litros; Toneladas`): requieren termino precoordinado que Q no puede acreditar localmente; sin peticion.
- **`Grados`**: literal compartido por Latitud/Longitud (angulo) y ambiguo frente a `Grados celcius`; no se propone.
- **`Porcentaje`** (50 filas): se propone una sola definicion (ANALF). La escala de valores (0-100 vs 0-1) no esta declarada localmente: no se infiere factor; I no debe calcular tasas.
- **`Toneladas`** (3 filas): la ambiguedad de variante afecta a las 3; ver `casos.json` Q-U01.
