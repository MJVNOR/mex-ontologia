# B — Auditoría FINAL material K v001: ACEPTAR

`auditoria-material.json` es el dictamen (formato requerido auditor-b, listo
para `auditorias/auditoria-b.json` al instalar). v001/v002/v003-revision-i
preservados; I-código descartado (no final); sin modificar material, scripts
ni producción; sin Gemma. Suite K del coordinador ausente al auditar:
sustituida por batería propia sobre material real + 23 mutaciones.

## Veredicto: aceptar P1-Q1, P1-Q3, P4-exclusion

- **SHAs 13/13 OK** (`material-preparado.json`); `aceptadas_sha256` declarado
  = calculado `3f960a47…366cd4f8e`; cubre datos/modelo/shapes + 2 pins.
- **Cruces byte-exactos**: datos = P1 v003 verbatim (tildes, sujetos v003);
  filas = fixtures v003; normativa = W v002; base/cobertura = vivas;
  shape = P4 v001 (`fc301d85…`); modelo ≠ vocab v003 solo por
  `rdf:Property` corregido (término válido; `rdfs:Property` no existe).
- **Loader estructural** (sin normalización, sin PROHIBIDO-substring):
  `_modelo` 26 triples OK, `_datos` 24 triples OK, resumen R8 exacto,
  `cargar()+construir()` en tmp anclado a real: OK, 14 fuentes, R9,
  62 triples, **cero joins**.
- **Mutaciones 23/23 rechazadas**: 15 manifiesto/núcleo/auditoría/camino
  (triple/sujeto/predicado/objeto/core/auditoría/camino/normativa/fila/Q2/
  shape) + 8 capa estructural con mensaje preciso (incl. D5/D6 de revisión I
  y literal refugiado en comentario).
- **Modelo**: 9 términos exactos, `rdf:Property` ×8, anotaciones Literales.
- **Hooks mínimos** pinnados: consolidar +6 (cadena R9), ampliar +3/+1.
- **C4 v002** (alcance pedido): sello 4/4, 19/19, 104/104 intactas;
  organismos a metadato API (ND-02 sagarhpa…); 7+7. **versionado-y-lanzamientos.md**
  coherente (format vs release, 2 dictámenes, escritor único).

## Límites

Q1/Q3 literales exactos con tilde e IRIs http; Q2 fuera; base R8 intacta.
SHACL se ejecuta en suite de instalación. Correcciones futuras se auditan
exactas, no heredadas. Auditorías A/B las fija el coordinador al instalar.
