"""Genera resultado.md desde propuestas.json (trazable, sin tocar el motor)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
prop = json.loads((HERE / "propuestas.json").read_text(encoding="utf-8"))
r = prop["resumen"]

L = []
L.append("# Agente-3 — Revisión de 47 interpretaciones candidatas")
L.append("")
L.append("Aislamiento: solo se leyó `data/semantica/cobertura.json`, `ontologia/semantica.json` y `docs/nucleo-semantico.md`.")
L.append("Todas las escrituras están en `propuestas/agente-3-significados/`. No se modificó el motor, no se sincronizó Studio, no se usaron propuestas de otros agentes.")
L.append("Unidad de trabajo: variable documentada y su definición. No se declaran correspondencias con columnas físicas. No se amplía a las 1,308 fuera del núcleo.")
L.append("Propuestas no aplicadas al vocabulario central.")
L.append("")
L.append(f"Total: {r['total']} = proponer {r['proponer']} + mantener pendiente {r['mantener_pendiente']}.")
L.append(f"Motivos pendiente: pendiente explícita {r['motivos_pendiente'].get('descripcion_pendiente_explicita',0)}, genérica insuficiente {r['motivos_pendiente'].get('descripcion_generica_insuficiente',0)}, truncada {r['motivos_pendiente'].get('descripcion_truncada',0)}.")
L.append("Verificación: `uv run python propuestas/agente-3-significados/scripts/verificar.py`.")
L.append("")
L.append("## Criterio aplicado")
L.append("- «Pendiente de especificar» o vacía → siempre pendiente, sin deducir por el nombre.")
L.append("- Genérica/truncada/ambigua (`Clave geográfica`, `perido…`, `Trimestre del estrato`, `Registro cronológico…`, `Fecha del registro.`, `Municipio donde el alumno`) → pendiente; el texto no precisa evento, papel, unidad o representación.")
L.append("- Propuesta solo si la descripción + contexto respaldan evento/objeto; si la población no está declarada se conserva la limitación en la definición del concepto.")
L.append("- Clínica: toma/recepción/resultado separan muestra (suero/sangre), prueba (ser1/RT-PCR) y secuencia (primera); inicio/fin tratamiento e ingreso son eventos distintos e intercambiables entre sí queda prohibido.")
L.append("")
L.append("## Decisiones por variable")
for x in prop["variables"]:
    L.append(f"### {x['titulo_conjunto']} — `{x['variable']}`")
    L.append(f"- Decisión: **{x['decision']}**" + (f" ({x['motivo_pendiente']}: {x['motivo_detalle']})" if x["decision"]=="mantener_pendiente" else ""))
    if x["concepto_propuesto"]:
        L.append(f"- Concepto propuesto (nuevo): `{x['concepto_propuesto']['id']}` — {x['concepto_propuesto']['definicion']}")
        L.append(f"- Regla propuesta: `{x['regla_propuesta']['id']}` (representación `{x['regla_propuesta']['representacion']}`)")
    else:
        L.append(f"- Concepto/regla: ninguno (pista previa `{x['concepto_pista_previo']}` no promocionada)")
    L.append(f"- Evidencia: descripción literal {repr(x['descripcion_literal'])}, def `{x['definicion_iri']}`, diccionario `{x['diccionario']}`, conjunto `{x['conjunto']}`, huella `{x['huella_fila_diccionario']}`, catálogo declarado {repr(x['catalogo_declarado'])}")
    L.append(f"- Alcance: {x['alcance']}")
    L.append(f"- Limitaciones: {'; '.join(x['limitaciones'])}")
    L.append(f"- Documentado vs inferencia: {x['documentado_vs_inferencia']}")
    if x["decision"]=="proponer":
        L.append(f"- Ejemplo positivo: {x['ejemplos_positivos'][0]}; contraejemplo: {x['contraejemplos'][0]}")
    L.append("")
L.append("## Reglas nuevas (20) — ejemplos y contraejemplos")
for g in prop["reglas_nuevas"]:
    L.append(f"- `{g['id']}` ({g['representacion']}): +{g['ejemplos_positivos'][0]} / −{g['contraejemplos'][0]}")
L.append("")
L.append("No aplicado a `ontologia/semantica.json` ni a `data/semantica/*`.")
(HERE / "resultado.md").write_text("\n".join(L), encoding="utf-8")
print(f"resultado.md: {len(prop['variables'])} fichas")
