"""Descarga una muestra de datos por conjunto (un archivo de datos) y extrae valores del campo objetivo."""
import urllib.request, hashlib, datetime, os, json
import openpyxl

MUESTRAS = [
 ('e5aad52d-5760-481c-ba65-db0ba4a5315e', '05bf66fb-6539-43ef-ae23-9369b678abac',
  'https://datos.sonora.gob.mx/dataset/e5aad52d-5760-481c-ba65-db0ba4a5315e/resource/05bf66fb-6539-43ef-ae23-9369b678abac/download/matricula-enero-abril-2022.xlsx',
  'Campo de Formaci\u00f3n Acad\u00e9mica'),
 ('403912fd-5853-4e18-8256-f77206f855bd', 'd62602e7-a059-4c34-a300-057ec4eb98f0',
  'https://datos.sonora.gob.mx/dataset/403912fd-5853-4e18-8256-f77206f855bd/resource/d62602e7-a059-4c34-a300-057ec4eb98f0/download/indicadores-academicos-enero-abril-2022.xlsx',
  'CAMPO DE FORMACI\u00d3N ACAD\u00c9MICA'),
 ('e7a3d62f-4ace-479c-aa52-1c9e384dc429', '79362ac6-c6ad-4231-aa41-f23ab92d1ae1',
  'https://datos.sonora.gob.mx/dataset/e7a3d62f-4ace-479c-aa52-1c9e384dc429/resource/79362ac6-c6ad-4231-aa41-f23ab92d1ae1/download/titulados-2022.xlsx',
  'Campo de Formaci\u00f3n Acad\u00e9mica'),
 ('85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f', '7422760b-8f99-4774-a436-c7d1f49c2cc0',
  'https://datos.sonora.gob.mx/dataset/85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f/resource/7422760b-8f99-4774-a436-c7d1f49c2cc0/download/egresados-2022.xlsx',
  'Campo de Formaci\u00f3n Acad\u00e9mica'),
 ('ee8f639f-5e89-46ae-93b9-934b05fc6233', 'ffe3c845-1fc7-4a6c-ab21-3a1db1740fdd',
  'https://datos.sonora.gob.mx/dataset/ee8f639f-5e89-46ae-93b9-934b05fc6233/resource/ffe3c845-1fc7-4a6c-ab21-3a1db1740fdd/download/hidrico_sonora_1980-1989.xlsx',
  'Clave'),
 ('5494daa1-09ca-4750-aeac-2558553700e1', '4121cf57-1e4a-4fb0-b175-3805edffca2c',
  'https://datos.sonora.gob.mx/dataset/5494daa1-09ca-4750-aeac-2558553700e1/resource/4121cf57-1e4a-4fb0-b175-3805edffca2c/download/fiebre-manchada-2022.xlsx',
  'servic_atencion'),
]
os.makedirs('propuestas/agente-1-catalogos/fuentes', exist_ok=True)
res = {'fecha_muestra_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'muestras': []}
for cj, rc, url, campo in MUESTRAS:
    dest = f'propuestas/agente-1-catalogos/fuentes/muestra_{cj}_{rc}.bin'
    info = {'conjunto': cj, 'recurso': rc, 'url': url, 'campo_objetivo': campo, 'archivo_local': dest}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'MEX-Ontologi agente-1'})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
            info['http_status'] = resp.status
            info['content_type'] = resp.headers.get('Content-Type')
        info['bytes'] = len(data)
        info['sha256'] = hashlib.sha256(data).hexdigest()
        with open(dest, 'wb') as f:
            f.write(data)
        # lee valores del campo objetivo (primeras 25 filas de datos)
        tmp = dest + '.xlsx'
        import shutil
        shutil.copyfile(dest, tmp)
        wb = openpyxl.load_workbook(tmp, data_only=True, read_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        hdr = [str(c) if c is not None else '' for c in rows[0]]
        # correspondencia no literal: normaliza minusculas/sin acentos/espacios
        import unicodedata
        def norm(s):
            s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode()
            return ' '.join(s.lower().split())
        ncol = None
        for i, h in enumerate(hdr):
            if norm(h) == norm(campo):
                ncol = i; break
        info['hoja'] = ws.title
        info['encabezado_real'] = hdr[:20]
        info['indice_columna'] = ncol
        vals = []
        if ncol is not None:
            for r in rows[1:26]:
                v = r[ncol] if ncol < len(r) else None
                vals.append('' if v is None else str(v))
        info['primeros_valores'] = vals
        from collections import Counter
        info['distribucion_muestra_25'] = dict(Counter(vals)) if vals else {}
        info['ok'] = True
    except Exception as e:
        info['ok'] = False
        info['error'] = f'{type(e).__name__}: {e}'
    res['muestras'].append(info)
    print(('OK ' if info.get('ok') else 'FALLO ') + cj[:8] + ' ' + str(info.get('primeros_valores', info.get('error'))))
with open('propuestas/agente-1-catalogos/muestras_datos.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print('escrito')
