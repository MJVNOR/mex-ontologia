# Resultado — catalogos, R6 (línea nueva edición-recurso-periodo)

17/17 referencias decididas (pendiente), 0 propuestas al núcleo, 0 vínculos, 0 joins por Clave.
Base R5 intacta: ningún pendiente revertido, ningún negativo R5 presentado como hallazgo nuevo.

## Línea nueva R6 (no duplica R4/R5)

- **C1 — API estructurada CKAN** (`package_show` de los 11 packages, 2026-10-23;
  R5 solo vio páginas HTML W01–W09): `version=null` en los 11, `extras` vacíos,
  recursos Diccionario/Catalogo con fechas placeholder `1989-06-04`.
  Excepciones registradas como cobertura, no edición: Egresados-Catalogo
  `2016-01-01/2025-01-01` (neutro: coincidencia numérica con CMPE 2016 no es
  adopción) y Rickettsia Catalogo/Diccionario `2022-01-01/2026-12-31`.
  `fuentes_extras` CONAPO/SESNSP confirmadas en API sin edición del xlsx local.
  Tamaños API = archivos locales byte a byte.
- **C2 — propiedades internas xlsx** (R5 revisó celdas, no `core-properties`):
  `3b8546ac` creator `openpyxl`, created 2026-04-15 → export generado posterior
  a los periodos 2022-2024, sin versión. Creadores restantes coinciden con los
  publicadores API (Sandoval/UTH, SESNSP, Pivac, Admin, Practicante2); ninguno
  declara versión.
- **V05**: constancia a nivel API del hueco 1960-1969 — recurso
  `4d1bb645-19da-407f-8182-b0be2d7b7485`, state active, size 541916, **url vacía**
  (confirma W03 con precisión estructurada, no solo observación HTML).
- **des_mpo_res**: inventario API cerrado (Diccionario + Catalogo + 3 datos);
  ningún recurso de municipios de residencia.

## Cuentas verificadas

- Referencias: 17 (V01–V16 + des_mpo_res). Decisiones: 17 pendiente.
- Reglas/conceptos/vínculos/columnas nuevos: 0.
- Fuentes nuevas R6: 2 (C1 estructurada-negativa, C2 archivo-negativa).
- Local re-verificado: 6 sha coinciden; sizes = API; cmpe pdf `66ba2fd2…`.

## Dependencia del publicador (sin prueba pública nueva)

No se re-pidieron páginas sin versión. Lo que falta está en manos del
publicador (detalle por ID en `entrega.json → pendientes` + `solicitudes-web.json`):
UTH (adopción CMPE 2016 por periodos, V01–V04), CEA/recursos hídricos (edición
Catálogo_estatal + constancia 1960-1969 y vínculo por décadas, V05), Salud
(versión de catálogos Rickettsia + fe de erratas des_mpo_res, V06–V08),
COESPO (versión catalogo.xlsx + vínculo 1990-2040 y desfase CONAPO, V09–V12,
V15–V16), SESNSP/Seguridad (edición y corte de catálogos delictivos, V13–V14).
