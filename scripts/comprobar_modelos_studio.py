"""Consulta y prueba brevemente los modelos de texto, sin enviar datos del grafo."""
import concurrent.futures
import datetime
import json
import pathlib
import re
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    settings = {}
    for line in (ROOT / '.env').read_text(encoding='utf-8-sig').splitlines():
        if line.startswith('ONTO_') and '=' in line:
            key, value = line.split('=', 1)
            settings[key] = value.strip().strip('"').strip("'")
    base = settings['ONTO_LLM_BASE_URL'].rstrip('/')
    headers = {'Authorization': 'Bearer ' + settings['ONTO_LLM_API_KEY'], 'Content-Type': 'application/json'}
    with urllib.request.urlopen(urllib.request.Request(base + '/models', headers=headers), timeout=25) as response:
        catalog = json.load(response)['data']
    models = [item['id'].removeprefix('models/') for item in catalog]
    models = [m for m in models if re.search(r'^(gemma-|gemini-(?:\d|flash|pro))', m)
              and not re.search(r'image|tts|audio|live|transcrib|embedding|robotics|computer-use|translate|omni', m, re.I)]

    def probe(model):
        result = {'model': model}
        body = json.dumps({'model': model, 'messages': [{'role': 'user', 'content': 'Reply with only OK.'}], 'max_tokens': 512, 'stream': False}).encode()
        try:
            with urllib.request.urlopen(urllib.request.Request(base + '/chat/completions', data=body, headers=headers), timeout=30) as response:
                data = json.load(response)
            text = data.get('choices', [{}])[0].get('message', {}).get('content', '') or ''
            text = re.sub(r'<think>.*?</think>', '', text, flags=re.S).strip()
            result.update(status='available' if text else 'empty_response', http=200)
        except urllib.error.HTTPError as error:
            result.update(status='quota' if error.code == 429 else 'denied' if error.code in (401, 403, 404) else 'error', http=error.code)
        except Exception:
            result.update(status='timeout_or_network_error')
        print(json.dumps(result), flush=True)
        return result

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(probe, models))
    report = {'checked_at_utc': datetime.datetime.now(datetime.UTC).isoformat(),
              'default_model': settings['ONTO_LLM_MODEL'], 'catalog_count': len(catalog),
              'scope': 'Una prueba breve de texto por candidato, sin grafo ni herramientas. No acredita cuota futura, llamadas a herramientas ni análisis complejo.',
              'results': results}
    (ROOT / 'reports/modelos-studio.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')


if __name__ == '__main__':
    main()
