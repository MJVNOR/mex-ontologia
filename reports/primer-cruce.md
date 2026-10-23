# Primer cruce: Registro Civil, 2022

Conteos independientes por código municipal local y año de registro; unión externa de agregados

Cruce exploratorio dentro del Registro Civil de Sonora. Coincidencia de códigos locales y definiciones; catálogo oficial de correspondencia no publicado en estos diccionarios.

Se consultaron exclusivamente `_id`, `municipio` y el año. Se descartaron las filas tras contarlas.

| Fuente | Filas | Municipios observados |
| --- | ---: | ---: |
| Matrimonios 2022 | 13881 | 67 |
| Divorcios 2022 | 6064 | 62 |

| Código local | Año | Matrimonios | Divorcios |
| --- | ---: | ---: | ---: |
| 01 | 2022 | 16 | 3 |
| 02 | 2022 | 145 | 125 |
| 03 | 2022 | 90 | 55 |
| 04 | 2022 | 34 | 15 |
| 05 | 2022 | 15 | 3 |
| 06 | 2022 | 11 | 1 |
| 08 | 2022 | 5 | 2 |
| 09 | 2022 | 3 | 1 |
| 10 | 2022 | 4 | 2 |
| 11 | 2022 | 12 | 5 |
| 12 | 2022 | 175 | 72 |
| 13 | 2022 | 8 | 4 |
| 14 | 2022 | 16 | 12 |
| 15 | 2022 | 4 | 1 |
| 16 | 2022 | 30 | 29 |
| 17 | 2022 | 104 | 113 |
| 18 | 2022 | 1516 | 951 |
| 19 | 2022 | 200 | 123 |
| 20 | 2022 | 36 | 9 |
| 21 | 2022 | 176 | 70 |
| 22 | 2022 | 7 | 3 |
| 23 | 2022 | 37 | 14 |
| 24 | 2022 | 2 | Sin filas observadas |
| 25 | 2022 | 250 | 113 |
| 26 | 2022 | 200 | 94 |
| 27 | 2022 | 332 | 42 |
| 28 | 2022 | 5 | 5 |
| 29 | 2022 | 826 | 458 |
| 30 | 2022 | 3610 | 1414 |
| 31 | 2022 | 6 | Sin filas observadas |
| 32 | 2022 | 4 | 1 |
| 33 | 2022 | 227 | 127 |
| 34 | 2022 | 5 | 2 |
| 35 | 2022 | 557 | 112 |
| 36 | 2022 | 94 | 56 |
| 37 | 2022 | 12 | 5 |
| 38 | 2022 | 35 | 9 |
| 40 | 2022 | 4 | 6 |
| 41 | 2022 | 62 | 41 |
| 42 | 2022 | 777 | 367 |
| 43 | 2022 | 738 | 363 |
| 45 | 2022 | 7 | 5 |
| 46 | 2022 | 58 | 12 |
| 47 | 2022 | 261 | 74 |
| 48 | 2022 | 335 | 171 |
| 49 | 2022 | 17 | 7 |
| 50 | 2022 | 10 | 4 |
| 51 | 2022 | 20 | 13 |
| 52 | 2022 | 8 | 15 |
| 55 | 2022 | 2177 | 664 |
| 56 | 2022 | 105 | 20 |
| 57 | 2022 | 10 | 3 |
| 58 | 2022 | 74 | 51 |
| 59 | 2022 | 34 | 6 |
| 60 | 2022 | 9 | Sin filas observadas |
| 61 | 2022 | 37 | 8 |
| 62 | 2022 | 6 | Sin filas observadas |
| 63 | 2022 | 18 | Sin filas observadas |
| 64 | 2022 | 8 | 3 |
| 65 | 2022 | 6 | 4 |
| 66 | 2022 | 70 | 51 |
| 67 | 2022 | 5 | 2 |
| 68 | 2022 | 11 | 3 |
| 69 | 2022 | 13 | 5 |
| 70 | 2022 | 92 | 42 |
| 71 | 2022 | 41 | 50 |
| 72 | 2022 | 59 | 23 |

## Interpretación y límites

- No vincula personas ni matrimonios con sus divorcios.
- No mide probabilidad de divorcio ni relación causal.
- Código sin filas en una fuente se conserva como null; no se infiere cero.
- Conteo de filas publicadas, sin deduplicación de eventos no identificables.
- No se asignan nombres ni códigos INEGI sin catálogo de correspondencia.
- Consultas paginadas y comprobación de totales; API no ofrece instantánea transaccional.

## Fuentes consultadas

- [Matrimonios 2022](https://datos.sonora.gob.mx/dataset/1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98/resource/7b8638e8-d0d5-4311-b43f-51e2d343efb1)
- [Diccionario](https://datos.sonora.gob.mx/dataset/1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98/resource/364ffa5c-e1c2-4185-a22f-80bede6735d0)
- [Divorcios 2022](https://datos.sonora.gob.mx/dataset/c6140d53-1f16-4dd8-8ab3-d2b47f03a921/resource/63940761-d099-4a39-bb92-e81e4a6d31e1)
- [Diccionario](https://datos.sonora.gob.mx/dataset/c6140d53-1f16-4dd8-8ab3-d2b47f03a921/resource/10357304-e171-44ca-a453-f989e6a2ff83)
