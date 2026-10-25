"""Tablas de corrección auditada para la entrega territorio-economia.

Base: copias congeladas manifiesto 2026-10-23 (agente-10 + agente-3).
Cada entrada cita el motivo: auditoría-11, criterio de integración, o
respaldo literal (unidad/objeto). Sin red, sin tocar el núcleo.
"""

# Conceptos nuevos para separar IM normalizado (medida distinta de IM).
NUEVOS_IMN = {
    "indice-marginacion-normalizado-localidad": [
        "Índice de marginación normalizado (localidad)",
        "Índice de marginación normalizado a nivel localidad, 2020. Medida: índice. Nivel: localidad.",
        None,
    ],
    "indice-marginacion-normalizado-municipio": [
        "Índice de marginación normalizado (municipio)",
        "Índice de marginación normalizado, 2020. Medida: índice. Nivel: municipio.",
        None,
    ],
    "indice-marginacion-normalizado-ageb": [
        "Índice de marginación normalizado (AGEB)",
        "Índice de marginación normalizado, 2020. Medida: índice. Nivel: AGEB.",
        None,
    ],
    "indice-marginacion-normalizado-colonia": [
        "Índice de marginación normalizado (colonia)",
        "Índice de marginación normalizado. Medida: índice. Nivel: colonia.",
        None,
    ],
    "indice-marginacion-normalizado-entidad": [
        "Índice de marginación normalizado (entidad)",
        "Índice de marginación normalizado, 2020. Medida: índice. Nivel: entidad.",
        None,
    ],
}

# regla_id -> concepto nuevo (separación IM/IMN)
CONCEPTO_SET = {
    "r3a10-0109": "indice-marginacion-normalizado-localidad",
    "r3a10-0131": "indice-marginacion-normalizado-municipio",
    "r3a10-0174": "indice-marginacion-normalizado-ageb",
    "r3a10-0217": "indice-marginacion-normalizado-colonia",
    "r3a10-0247": "indice-marginacion-normalizado-entidad",
}

# regla_id -> representación corregida (literal no declara la forma del valor)
REP_SET = {
    "r3a10-0148": "no_especificada",
    "r3a10-0366": "no_especificada",
    "r3a10-0367": "no_especificada",
    "r3a10-0373": "no_especificada",
    "r3a3-ddr-registro-cultivo-nombre-1": "no_especificada",
    "r3a3-ddr-registro-pesquero-nombre-1": "no_especificada",
}

# regla_id -> sufijo añadido al límite congelado
LIM_ADD = {
    "r3a10-0148": " Representación conservadora: la descripción no declara la forma del valor.",
    "r3a10-0366": " Representación conservadora: la descripción no declara la forma del valor.",
    "r3a10-0367": " Representación conservadora: la descripción no declara la forma del valor.",
    "r3a10-0373": " Representación conservadora: la descripción no declara la forma del valor.",
    "r3a10-0246": " Ejemplo 'Bajo' conservado literal; incoherente con tipo Numérico declarado; no se tipifican valores.",
    "r3a3-ddr-registro-cultivo-nombre-1": " Representación conservadora: la descripción no declara la forma del valor.",
    "r3a3-ddr-registro-pesquero-nombre-1": " Representación conservadora: la descripción no declara la forma del valor.",
}

# Conjunto -> sufijo de límite (origen conjunto de población / proyección)
LIM_CONJUNTO = {
    "03a33e71-d447-47b1-aa0d-b341996e023c": " La descripción dice reconstruida y ajustada; 'proyección' viene del título del conjunto; no se acredita método ni periodo.",
    "1b6d0817-66a9-4b25-9468-efca73e3ce20": " 'Proyección' viene del título del conjunto; no se acredita método ni periodo.",
    "f1bbd13b-3364-441c-81b4-7b7c548be39f": " 'Proyección' viene del título del conjunto; no se acredita método ni periodo.",
    "89e8c891-5987-44ba-b11-9508e3dd87e6": " Población del conjunto 'Registro de Usuarios Beneficiados' según título publicado; la descripción no la nombra.",
}

# concepto -> definición corregida (sin unidades/objetos inventados)
DEF_FIX = {
    "volumen-total-produccion-pecuaria": "Volumen total producido en ganadería según literal. Medida: volumen.",
    "encargados-evento-capacitacion": "Encargados de impartir el evento de capacitación (literal con errata conservado). Sujeto: encargados según función descrita.",
    "sexo-victima-desaparecida": "Sexo de la víctima según literal. Objeto: víctima.",
    "nacionalidad-victima-desaparecida": "Nacionalidad de la víctima según literal. Objeto: víctima.",
    "entidad-nacimiento-victima-desaparecida": "Estado de nacimiento de la víctima según literal. Objeto: entidad federativa.",
    "entidad-desaparicion-victima": "Estado de desaparición de la víctima según literal. Objeto: entidad federativa.",
    "estatus-victima-desaparecida": "Estatus en que se encuentra la víctima según literal.",
}

# Reemplazos de sufijo en definiciones (neutralizar "Población: personas.")
SUFIJOS = [
    ("en proyecciones por grupos quinquenales. Población: personas. Medida: conteo.",
     "en proyecciones por grupos quinquenales. Población del grupo de edad según literal. Medida: conteo."),
    ("en proyecciones por grupos quinquenales de edad. Población: personas. Medida: conteo.",
     "en proyecciones por grupos quinquenales de edad. Población total según literal. Medida: conteo."),
    ("en proyecciones por grandes grupos de edad. Población: personas. Medida: conteo.",
     "en proyecciones por grandes grupos de edad. Población del gran grupo según literal. Medida: conteo."),
    ("Suma de población total en proyecciones por grandes grupos de edad. Población: personas. Medida: conteo.",
     "Suma de población total en proyecciones por grandes grupos de edad. Población total según literal. Medida: conteo."),
    ("Población a mitad de año del municipio en proyecciones. Población: personas. Medida: conteo.",
     "Población a mitad de año del municipio en proyecciones. Población del municipio según literal. Medida: conteo."),
    ("Población a mitad de año de la entidad federativa del municipio según literal. Población: personas. Medida: conteo.",
     "Población a mitad de año de la entidad federativa del municipio según literal. Población de la entidad según literal. Medida: conteo."),
    ("Población total de 0 a 14 años en proyecciones de indicadores demográficos. Población: personas. Medida: conteo.",
     "Población total de 0 a 14 años en proyecciones de indicadores demográficos. Población del rango según literal. Medida: conteo."),
    ("Población total de 15 a 64 años en proyecciones de indicadores demográficos. Población: personas. Medida: conteo.",
     "Población total de 15 a 64 años en proyecciones de indicadores demográficos. Población del rango según literal. Medida: conteo."),
    ("Población total de 60 años y más en proyecciones de indicadores demográficos. Población: personas. Medida: conteo.",
     "Población total de 60 años y más en proyecciones de indicadores demográficos. Población del rango según literal. Medida: conteo."),
    ("Población total de 65 años y más en proyecciones de indicadores demográficos. Población: personas. Medida: conteo.",
     "Población total de 65 años y más en proyecciones de indicadores demográficos. Población del rango según literal. Medida: conteo."),
    ("Porcentaje de población de 15 años y más analfabeta. Población: personas. Medida: porcentaje.",
     "Porcentaje de población de 15 años y más analfabeta. Población de 15 años y más según literal. Medida: porcentaje."),
    ("Porcentaje de población de 15 años y más sin educación básica. Población: personas. Medida: porcentaje.",
     "Porcentaje de población de 15 años y más sin educación básica. Población de 15 años y más según literal. Medida: porcentaje."),
]
