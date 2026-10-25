# Adenda web — matrículas (ronda 5, seguimiento)

30/30 pendientes confirmados. 0 propuestas. Entrega cerrada intacta
(`entrega.json` sha `e8ce4f70…`, sin tocar).

## Fuentes examinadas (solo lectura)

| PDF | sha256 | Edición |
| --- | --- | --- |
| `UES_Reglamento_Escolar_2022_01.pdf` (939684 B) | `c4523ae5…b0e023` | Actualización XLI, sep-2022 — aplicable al dato 2022-2 |
| `UES_Reglamento_Escolar_previo.pdf` (216233 B) | `b8343af9…57076a8` | XXX, 16-dic-2019 — contexto de era |
| `UES_Guia_Opciones_Titulacion_2023.pdf` (1274532 B) | `a70b5ea9…d9a1ff958` | XLV, 25-ago-2023 — posterior al dato, no intercambiable |

Verificación propia por extracción directa: arts. 23-25 (revalidación/equivalencia/convalidación),
art. 4 (calendario), art. 9 (regular/irregular), art. 21 (cambio de unidad), art. 55
(baja = separación temporal o definitiva, **sin tipos**), art. 63 (título exige opción de la Guía).
Guía 2023: Tesis, EGEL/EXIL, Experiencia, Alto Desempeño, Investigación, Trabajo,
Innovación, Diplomado — **sin "no exigibilidad" ni "examen profesional"**.
"222" en el PDF es ruido de fuente, no clave de ciclo.

## Por solicitud

- **MAT-W-01** (negativo-portal): sin descripciones ni dominios. No resuelve.
- **MAT-W-02** (parcial-documento): reglamento genérico sin vínculo
  variable/periodo/sujeto/código; guía posterior con otra terminología.
  Equivalencia definida como proceso, no como representación de /17. No resuelve.
- **MAT-W-03** (parcial+negativo): calendario 2022-2 no localizado; "222"/"Reing"/
  "ciclo señalado" sin definición pública. No resuelve.
- **MAT-W-04** (negativo-portal): sin dominios de baja, estímulo, unidad, facetas.
  Art. 21 regula el trámite, no el dominio de /62. No resuelve.
- **MAT-W-05** (parcial-documento): previo art. 30 **sí** trae equivalente 10–6
  (corrección parcial a S06: "sin escala numérica" era impreciso), pero sin
  definición de promedio, redondeo ni conjuntos. No resuelve; no se supone 0-10.

## Cautelas

- Transitorios del PDF 2022_01 aún citan XXX 16-dic-2019 (posible arrastre;
  se conserva sin curar; la aplicabilidad 2022-2 se apoya en portada XLI sep-2022).
- Ningún contexto se convierte en codebook; ningún reglamento aprueba por nombre.
- Brechas mejoradas por variable en `adenda-web.json` → `solicitudes[].brecha_mejorada`.
