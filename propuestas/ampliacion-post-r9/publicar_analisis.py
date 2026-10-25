"""Publica tres fichas analíticas separadas del grafo, con fuentes exactas."""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
EXP = Path('propuestas/ampliacion-post-r9/ejecucion-20261024')
CASOS = [
    ('911', 'Llamadas procedentes e improcedentes', 'A1-911/v002/resultados.json', 'ficha',
     'El Q1 etiquetado como improcedentes es un duplicado de procedentes; el Q2 de improcedentes carece de MUNICIPIO. Las muestras disponibles no permiten calcular la comparación municipal y mensual ni una proporción del universo.',
     ['Recurso correcto de improcedentes Q1 y esquema territorial aplicable a Q2.', 'Archivos completos, periodos verificados y estrategia de agregación validada.', 'Para proporciones, documento que acredite partición del mismo universo.']),
    ('registro-civil', 'Matrimonios y nacimientos registrados', 'A2-registro-civil/v002/resultados.json', 'ejes',
     'Los datos disponibles tienen distinto grano y las validaciones detectan totales incompatibles con hombres + mujeres y meses ausentes. Una comparación de agregados requiere validar su preparación y cobertura; la diferencia de grano por sí sola no la impide. No se interpretan tasas poblacionales ni causalidad.',
     ['Archivos completos y cobertura por municipio y mes.', 'Aclaración o corrección de totales y meses ausentes.', 'Regla documentada para agregar matrimonios y comparar periodos de registro.']),
    ('itama', 'Internamiento y externamiento ITAMA', 'A3-itama/v002/resultados/analisis-a3-itama-v002.json', 'ficha_8_ejes',
     'Faltan copias locales completas de los recursos ITAMA y respaldo del periodo observado y de escolaridad. Los trimestres son metadatos; las muestras de 29 y 16 registros no acreditan el universo completo. Comparar distribuciones agregadas será posible si se documentan grano, categorías, periodo y cobertura; aquí no se suman universos ni se vinculan personas.',
     ['Copias completas de los recursos del par y alcance de cada hoja.', 'Grano y periodo documentados; catálogo de sexo y definición de escolaridad aplicables.', 'Comprobaciones de cobertura y recuentos reproducibles por población.']),
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def generar(outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for key, title, rel, field, conclusion, conditions in CASOS:
        source = ROOT / EXP / rel
        data = json.loads(source.read_text(encoding='utf-8'))
        axes = data[field]
        assert len(axes) == 8, (key, axes.keys())
        rows.append({'id':key, 'titulo':title, 'par':data['par'], 'pregunta':data['pregunta'],
                     'estado':'bloqueado_por_evidencia_y_validacion_pendiente',
                     'volumenes_comparados':None, 'join_grafo':False, 'conclusion':conclusion,
                     'ficha_8_ejes':axes, 'condiciones_reapertura':conditions,
                     'fuente':{'ruta':source.relative_to(ROOT).as_posix(),'sha256':sha(source)}})
    result = {'format_version':1,'release_base':'R9','corte_documental':'2026-10-24',
              'analisis':rows,'limites':['No se ejecutaron joins ni se añadieron relaciones analíticas al grafo.',
              'Una muestra no demuestra unicidad ni cobertura integral; ausencia no equivale a cero.',
              'El ranking prioriza revisiones; no aprueba comparabilidad.'],
              'nota_editorial':'Las fichas fuente se conservan íntegras. Las conclusiones publicadas precisan el bloqueo actual; no expresan imposibilidades universales de comparación agregada.'}
    (outdir/'analisis-pares-post-r9.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    md=['# Tres análisis de pares posteriores a R9','','Los tres análisis quedan bloqueados por la evidencia y validaciones disponibles. No se calcularon comparaciones de volúmenes, proporciones o distribuciones ni se ejecutaron joins. El [top 50](top50-oportunidades-r9.html) solo prioriza revisiones.','']
    for row in rows:
        md += ['## '+row['titulo'],'', '**Pregunta:** '+row['pregunta'],'',row['conclusion'],'',
               '| Comprobación | Estado en la ficha fuente |','| --- | --- |']
        for name, axis in row['ficha_8_ejes'].items():
            state=axis.get('estado',axis.get('veredicto','ver fuente')) if isinstance(axis,dict) else str(axis)
            md.append('| '+name.replace('_',' ')+' | '+state.replace('|','/')+' |')
        md += ['', '### Condiciones de reapertura','']+['- '+s for s in row['condiciones_reapertura']]
        source=row['fuente']
        md += ['',f"[Ficha y evidencia originales](../{source['ruta']}); SHA256 `{source['sha256']}`.",'']
    md += ['## Límites','']+['- '+s for s in result['limites']]+['','El JSON publicado conserva las ocho comprobaciones completas y su evidencia, junto con el vínculo y huella del original. Las conclusiones precisan el alcance del bloqueo sin modificar los originales.','']
    (outdir/'analisis-pares-post-r9.md').write_text('\n'.join(md),encoding='utf-8')
    print(json.dumps({'analisis':len(rows),'ejes_por_analisis':[len(r['ficha_8_ejes']) for r in rows],'salida':str(outdir)}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir',required=True)
    generar(parser.parse_args().out_dir)
