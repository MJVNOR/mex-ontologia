"""Descarga Hermosillo-educación vía helper CKAN (con User-Agent)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from descargar_ckan import descargar  # ponytail: reusa UA + binario de scripts/descargar_ckan.py

base = Path(__file__).resolve().parent
urls = {
 "total-egresados-2020-2021.xlsx": "https://datos.sonora.gob.mx/dataset/ef7dfb43-a80f-43b6-96c3-e067b8bf7ad1/resource/e6ba941d-c8b9-4392-8725-65e913bf2f22/download/total-de-egresados-2020-2021.xlsx",
 "egresados-2022.xlsx": "https://datos.sonora.gob.mx/dataset/85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f/resource/7422760b-8f99-4774-a436-c7d1f49c2cc0/download/egresados-2022.xlsx",
 "egresados-2023.xlsx": "https://datos.sonora.gob.mx/dataset/85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f/resource/3e3bed3e-db98-45a0-89b3-d07fb57cafe6/download/egresados-2023.xlsx",
 "egresados-2024.xlsx": "https://datos.sonora.gob.mx/dataset/85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f/resource/ae39974c-131d-48f1-bd25-b368d59db4b6/download/egresados-2024.xlsx",
 "egresados-2025.xlsx": "https://datos.sonora.gob.mx/dataset/85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f/resource/ad71c81a-01ac-40f2-821d-0b1efd06b487/download/egresados-2025.xlsx",
 "diccionario-egresados.csv": "https://datos.sonora.gob.mx/dataset/ef7dfb43-a80f-43b6-96c3-e067b8bf7ad1/resource/2b0630a2-dd4f-4b93-a321-d4a6c47a522b/download/diccionario-egresados.csv",
}
for fn, url in urls.items():
    p = base / fn
    if p.exists() and p.stat().st_size > 0:
        print(f"existe {fn} {p.stat().st_size}B")
        continue
    info = descargar(url, p)
    print(f"ok {fn} {info['bytes']}B")
