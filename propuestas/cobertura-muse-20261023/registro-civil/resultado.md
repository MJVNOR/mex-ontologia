# Cobertura Muse — registro civil (agente 7, 163 definiciones)

Insumos verificados contra manifiesto (17 copias + 6 centrales, 0 diferencias). Base: 103 conceptos, 232 respaldadas, 836 revisadas, 118 candidatas, 23 candidatas iniciales y 232 respaldadas preservadas (0 intersección).

## Delta auditado-76 vs entrega-75

La auditoría inicial cubrió 76 reglas; el hallazgo accionable RESIDEEXTRANJERO separó el par código/texto (D a pendiente por contradicción) y la entrega congelada quedó en 75 reglas y 50 conceptos. `auditoria.json` ya dictamina esas 75 (52 aceptar + 23 condicionado); su `resultado.md` conserva texto de la pasada de 76 (61/15): vale el JSON máquina por IRI, verificado idéntico al congelado.

## Corrección de los 23 condicionados

- 18 reglas: concepto neutralizado (sujeto fuera del concepto) + calificador formal (difunto/madre/nacido, alcance inferencia-contextual-publicada; el integrador lo soportará antes de aplicar).
- fecha-nacimiento-madre, edad-madre, edad-padre: definición sin añadido fuera del literal + límite + calificador de vínculo.
- TIPOCESAREAD: límite PROGRAMADO≠binario + calificador de evento (comparte con TIPOCESAREA).
- RESIDEEXTRANJERO-código (nac): límite de separación; D sigue pendiente con contradicción.
- EDADPADRE: límite 99 posible nulo no documentado; no se usa como edad.
Extranjería (seed + madre) comparte un concepto neutro con calificador por regla; conceptos nuevos 50→49, propuestas 75 (máximo 76, sin inventar).

| Resultado | Cantidad |
| --- | ---: |
| Decisiones (proponer / pendiente) | 75 / 88 |
| Reglas | 75 (22 con calificador) |
| Conceptos nuevos / reutilizados | 49 / 1 (sexo-difunto) |
| Correspondencias | 0 |

Verificador propio `scripts/verificar.py` OK (positivos en pipeline, negativos solo-nombre/contexto/otra-IRI, evidencia por representación, 23+232 preservadas). Preguntas en `pendientes.json` (6). `listo.json` cierra la entrega.
