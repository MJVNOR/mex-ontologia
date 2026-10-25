"""Extrae el texto del Manual SEED 2022 preservado con marcadores de pagina.
Genera evidencia/manual_seed2022_paginas.txt (ya generado; se conserva por provenance).
Uso: uv run python propuestas/investigacion-post-r6/salud-defunciones/temporales/generadores/extraer_manual.py
Requiere: pypdf (solo entorno efimero de extraccion; no agregado al proyecto).
"""
from pathlib import Path

from pypdf import PdfReader

REPO = Path(__file__).resolve().parents[5]
OUT = REPO / "propuestas/investigacion-post-r6/salud-defunciones"


def main() -> None:
    pdf = REPO / "propuestas/pendientes-muse-r6/salud/evidencia/Manual_Llenado_CD_CMF_2022_20220930.pdf"
    r = PdfReader(str(pdf))
    with (OUT / "evidencia/manual_seed2022_paginas.txt").open("w", encoding="utf-8") as f:
        for i, pg in enumerate(r.pages):
            f.write(f"\n\n===== PAGINA {i + 1} =====\n")
            f.write(pg.extract_text() or "")
    print("paginas:", len(r.pages))


if __name__ == "__main__":
    main()
