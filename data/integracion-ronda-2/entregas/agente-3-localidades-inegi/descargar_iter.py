import urllib.request, os, hashlib, sys, datetime
BASE = os.path.join("propuestas", "ronda-2", "agente-3-localidades-inegi", "fuentes")
ESPERADOS = {
 "iter_26_cpv2020_csv.zip": ("https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_26_cpv2020_csv.zip",
                             "4ad9380527c248bb236bd90eefed760b0f8796eaeab7c469f95ead033e96dee2"),
 "fd_iter_cpv2020.pdf": ("https://www.inegi.org.mx/contenidos/programas/ccpv/2020/doc/fd_iter_cpv2020.pdf",
                         "1b7ea20fb8f00b9ed248da725a43bda0c7bab6c96d4fe77d6ddf51b1876525eb"),
}
os.makedirs(BASE, exist_ok=True)
for name, (url, sha_ok) in ESPERADOS.items():
    dest = os.path.join(BASE, name)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    h = hashlib.sha256()
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            f.write(b)
            h.update(b)
    digest = h.hexdigest()
    print("saved", dest, digest, datetime.datetime.now(datetime.timezone.utc).isoformat())
    if digest != sha_ok:
        print(f"FALLA SHA {name}: esperado {sha_ok}, obtenido {digest}")
        sys.exit(1)
print("SHA OK")
