# S3-matrículas — nota de primera puerta (2026-10-24)

Alcance: 30 IDs UES, filas 8–70 del diccionario 8c0e76ff, recurso 58f2d5a6 (Matrículas 2022-2).

## Verificación local

- SHA-256 re-calculados desde bytes el 2026-10-24: los 3 archivos de evidencia
  coinciden con los hashes citados en antecedentes (inspecciones JSON,
  datastore_diccionario.json, Matrículas-2022-2.xlsx). Sin cambios.

## Comprobaciones web independientes (sin Obscura, sin repetir búsquedas agotadas)

1. CSV `diccionario-matriculas-de-estudiantes.csv` (dataset e819466c…, recurso
   8c0e76ff): YA EXAMINADO (ronda-2/ronda-3). No es pista nueva. Su contenido
   confirma `Pendiente de especificar` + ejemplos por fila; los ejemplos no son
   definiciones.
2. Guía informativa de titulación XLV sesión agosto 2023: YA EXAMINADA en R5
   (sin `no exigibilidad`/`examen profesional` como alternativa). Posterior al
   periodo 2022-2. No es pista nueva.
3. Reglamento de Titulación UES planes 1995 (copia studylib, arts. 5/8/24-28:
   examen profesional y constancia de no exigibilidad como conceptos generales,
   vigencia 1999/2012): copia terciaria, era distinta al periodo 2022-2, sin
   vínculo campo/recurso/edición/periodo. Norma general: no acredita /63–/70.
4. `https://ues.mx/archivos/conocenos/normatividad` vía webfetch: 403.
   Requiere navegador → queda para W-web dentro de la petición WEB-MAT-02
   ya pendiente (norma UES era-2022). No se re-emite petición duplicada.

## Resultado de puerta

30/30 `sin_pista_nueva` → `brecha_externa`. Cero peticiones web nuevas emitidas.
Petición previa WEB-MAT-02 (norma UES era-2022, URLs ues.mx / ues.sonora.edu.mx)
sigue pendiente en W-web; si resuelve, el coordinador hará adenda aparte.
