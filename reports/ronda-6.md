# Ronda 6: vínculo documental de Presas (cat_estatal/Clave → /4)

Integración R6 de Presas, de extremo a extremo, con el modelo
`opencode-go/muse-spark-1.3-contributor`. Un solo vínculo documental nuevo
(Clase `clave-identificadora-presa`, definición `/4` de `Catalogo_estatal`);
0 reglas, 0 conceptos. Núcleo en **4475 correspondencias revisadas, 20
candidatas, 0 ambiguas**; **1392 significados, 1075 conceptos, sin cambio**.

Las **142 pruebas pasan**. SHACL del grafo completo y del estado previsto de
Studio termina sin violaciones; los SELECT del Studio vivo confirman el
resultado. Studio queda en **321210 triples** (+1 neto exacto sobre 321209,
explicado abajo), incluidas sus ediciones ajenas a la ampliación.

## Alcance documental (autoridad única)

`cat_estatal/Clave` (recurso `4219d141-5084-4308-bda3-d44ca28a4f53`) denota la
clave declarada del registro de catálogo según la definición `/4`
(`Texto/CCCCC`, "Contiene la clave identificadora de cada presa", hoja
`Catalogo_estatal`). Nada de joins por Clave, nada de identidad entre
catálogos, nada de vigencias históricas, nada de definiciones agregadas. Los
límites van fijados en el vínculo y en la adenda.

## Evidencia verificada (recomputada, no transcrita)

- `adenda-presas.json` SHA `18689699…` = marker `adenda-presas.sha.json` =
  dictamen-presas `sha_adenda`; copia en `data/integracion-ronda-6/` idéntica.
- `huella_esquema 29af60e8…` (inspección `tablas[0]`) y
  `huella_fila_diccionario d1208344…` (`definiciones[3]`) recomputadas OK.
- `web/evidencia/cat_estatal_1.xlsx`: 11981 B, magia PK, SHA `b7a398a0` =
  `sha256_fragmento_o_archivo` de la inspección; 1 hoja `cat_estatal`, 17
  columnas, 10 filas, 9 Claves CCCCC únicas.
- 13 columnas hermanas `documental_revisada` a `Catalogo_estatal` en cobertura
  (15 del recurso = 13 + 2 ambiguas Clave); exclusión de `/1` por perfil
  (serie Clave-Fecha-Almacenamiento vs hoja física sin fecha/almacenamiento).
- Dos auditores: `dictamen-presas.json` (aceptar pin /4) y
  `dictamen-codigo-r6.json` (aprobar-staging). SHAs de staging verificados
  antes de instalar (4/4 coinciden).

## Corrección aplicada (divergencia del staging, documentada)

El staging aprobado dejaba `if rules != expected` incondicional antes de
delegar, lo que rechaza la extensión R6 válida (reproducido por ejecución:
`ValueError: Ronda 5 permite solo la base...`). Se completó el arreglo en
`scripts/integrar_ronda_5.py`: duplicados y aprobaciones R5 siempre antes de
delegar; la exactitud R5 solo rige en la ruta sin-R6; con config R6 se delega
a `integrar_ronda_6` (máximo 1 vínculo, sin reglas/conceptos). Ningún test
aprobado cambia de resultado (21/21 R5+R6 específicos). Ajustes R6-aware
mínimos en `integrar_entregas.py`, `integrar_ronda_2.py` (esperado leído de
`revision-ronda-6`, manifiestos previos intactos) y en 3 conteos históricos de
pruebas (mismo patrón que R5 ya usaba en `test_ronda_3_integrada`, con
manifiesto R6 validado por `cargar_r6`).

## Resultado y verificación

| Indicador | R5 | R6 |
|---|---:|---:|
| Correspondencias revisadas | 4474 | 4475 |
| Candidatas | 20 | 20 |
| Ambiguas (vínculos) | 2 | 0 |
| Significados respaldados / conceptos | 1392 / 1075 | 1392 / 1075 |
| Triples portal combinado | 320600 | 320601 |
| Triples Studio | 321209 | 321210 (+10/−9, +1 neto auditado abajo) |

Mecánica exacta del +1 (diff respaldo-vs-observado, sin duplicación ni
residuo): el nodo del mapeo /4 se promueve in situ (conserva tipo, etiqueta,
columnaOrigen, variableDestino, evidencia y 2 derivedFrom; cambia estado
ambigua→revisada y suma criterioRevision, limiteSemantico, 2 huellas,
derivedFrom a reglas y a la adenda); el nodo /1 se retira por completo (8
triples); la procedencia añade el nodo Entity de la adenda (tipo + SHA) y el
`significadoDocumentado` en la columna. Retirados 9 = 2 estados ambiguos + 7
del /1; insertados 10 = 1 estado revisado + 6 de revisión + 3 de
procedencia/columna. 321209 es inalcanzable con el delta aplicado; no se
fuerza artificialmente.

SHACL: conforme, 0 violaciones, 32410 focus nodes (grafo y Studio).
Pruebas: 142/142 OK. Contactos externos: 0.

## Brechas documentales que siguen abiertas

- Catálogos: 17 referencias V01–V16 + `des_mpo_res` sin F4/F3 faltante; solo el
  publicador puede acreditar edición-recurso-periodo (R6-C1/C2 aportaron
  evidencia negativa estructurada sin revertir ningún pendiente).
- 171 significados restantes. Presas queda resuelta con los límites anotados.

Respaldo pre-R6: `data/backups/antes-r6-presas-20261024T042259Z.zip`
(sha `ebb782d6…`). Respaldo Studio pre-sync:
`data\backups\studio-antes-portal-20261024T043421628103Z.ttl`.
Manifiesto R6: `2b618252…`. Hashes y pruebas en `reports/ronda-6.json`.
