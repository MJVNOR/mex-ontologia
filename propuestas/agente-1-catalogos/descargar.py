"""Descarga los 6 catalogos + 6 diccionarios a fuentes/, con manifiesto (URL, fecha, SHA-256). Solo stdlib para descarga+hash."""
import json, urllib.request, hashlib, datetime, os, time

CONJ = json.load(open('propuestas/agente-1-catalogos/conjuntos_objetivo.json', encoding='utf-8'))
os.makedirs('propuestas/agente-1-catalogos/fuentes', exist_ok=True)
manifiesto = {'fecha_consulta_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'archivos': []}
for ds in CONJ:
    for r in ds.get('resources', []):
        if r.get('name') not in ('Catalogo', 'Diccionario'):
            continue
        url = r.get('url')
        fname = f"{ds['id']}_{r['id']}_{r['name']}.bin"
        dest = f"propuestas/agente-1-catalogos/fuentes/{fname}"
        info = {'conjunto': ds['id'], 'titulo_conjunto': ds.get('title'),
                'recurso': r.get('id'), 'nombre_recurso': r.get('name'),
                'formato': r.get('format'), 'url': url, 'archivo_local': dest}
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'MEX-Ontologi agente-1-catalogos'})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
                info['http_status'] = resp.status
                info['content_type'] = resp.headers.get('Content-Type')
            info['bytes'] = len(data)
            info['sha256'] = hashlib.sha256(data).hexdigest()
            info['fecha_descarga_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            info['ok'] = True
            with open(dest, 'wb') as f:
                f.write(data)
        except Exception as e:
            info['ok'] = False
            info['error'] = f"{type(e).__name__}: {e}"
        manifiesto['archivos'].append(info)
        print(('OK ' if info.get('ok') else 'FALLO ') + info['recurso'] + ' ' + info['nombre_recurso'] + ' ' + str(info.get('sha256', info.get('error'))))
        time.sleep(0.5)
with open('propuestas/agente-1-catalogos/manifiesto_descargas.json', 'w', encoding='utf-8') as f:
    json.dump(manifiesto, f, ensure_ascii=False, indent=2)
print('manifiesto escrito')
