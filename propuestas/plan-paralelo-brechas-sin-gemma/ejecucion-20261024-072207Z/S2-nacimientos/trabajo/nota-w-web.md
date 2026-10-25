# Nota cruce W-web → S2 (2026-10-24): paquete revisado, sin cambios por ID

Paquete W (`W-web/paquete/`, congelado; solo lectura): F-W02-SINAC-CAT trae
los enlaces formales `sinac_catalogos_2020_2023.zip?V=1.1`,
`sinac_catalogos_2024.zip?V=2025.06.24`, `sinac_catalogos_2025.zip?V=2026.07.09`
y re-descarga del descriptor 2020-2025 `?V=2026.07.09`.

Verificaciones propias (sin re-descargar lo mismo):
- Descriptor idéntico local: zip local
  `cierre-brechas-post-r6/significados-salud/evidencia/sinac_descriptores_2020_2025.zip`
  sha `61be6ed4…` == sha W. Sin bytes nuevos; corrobora estabilidad de la edición
  citada en v002 (no es evidencia nueva para decisiones).
- Catálogo 2020-2023: el zip de v002 (`trabajo/evidencia/…zip`, sha `9c7dcd52…`,
  24408182 B ≈ 23.2 Mb, misma URL que F-W02) es el mismo archivo apuntado por W.
  No re-descargado por orden expresa.
- Catálogos 2024/2025: ediciones fuera del periodo del recurso (2022-01-01 a
  2022-09-26); descargarlos no cambiaría la prueba de representación 2022 y
  mezclaría ediciones. No descargados, con motivo (no es omisión: es criterio
  de edición).
- W no atendía peticiones hermanas (cobertura: `sin_peticiones`); no hay
  resultado pendiente que declarar.

Impacto por ID: ninguno cambia. v002 ya incorpora el contenido 2020-2023 con
prueba computable por ID (31 propuestas tier A1–A5 + 22 brechas con desajuste
estructural). El paquete W corrobora (descriptor idéntico, enlaces formales)
pero no aporta documento resolutivo adicional ni invalida ninguna decisión.
Por eso no se crea v003: versión nueva solo ante evidencia que cambie
decisiones. v001 y v002 quedan congeladas e intactas (hashes re-verificados).
