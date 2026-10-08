#!/usr/bin/env python3
"""build_bocetos_pdf.py · arma el PDF de bocetos de landing (portada + por propuesta: resumen, vista general y capturas
desktop y mobile en tramos legibles). Solo biblioteca estándar + Chrome headless + poppler (para verificar).

Uso (normalmente vía build-bocetos-pdf.sh):
  build_bocetos_pdf.py <carpeta> <salida.pdf> [--lang es|en] [--cols 4] [--keep-html ruta.html]
                       [--title T] [--subtitle S] [--date D] [--brand B] [--note N]

Convención de la carpeta:
  bocetos.meta.json            (opcional) portada: titulo, subtitulo, fecha, marca, nota, fuente
  propuesta-<id>.meta.json     una por propuesta: id, nombre, angulo, big_idea, audiencia, conciencia, trafico,
                               cta_primario, cta_secundario, secciones[{n,nombre,proposito}], decision_riesgosa,
                               placeholders[], y opcionalmente desktop / mobile (nombres de los PNG)
  propuesta-<id>-desktop.png   captura de página completa a 1440 px
  propuesta-<id>-mobile.png    captura de página completa a 390 px

Cómo resuelve el problema de las capturas de 8.000 a 20.000 px de alto:
  - Nunca usa una página gigante (los PDF tienen un límite práctico de ~14.400 pt por lado y los lectores se ponen lentos).
    Corta la captura en TRAMOS que entran en una página A4 apaisada, escalados para que el texto se lea.
  - Desktop: un tramo por página, a todo el ancho útil (277 mm; ~0,19 mm por píxel; el texto de 16 px mide ~8,7 pt).
  - Mobile: varias columnas por página (4 por defecto, de 62 mm; el texto de 16 px mide ~7,2 pt), en orden de lectura.
  - Vista general: la captura desktop completa en pocas columnas chicas, para ver el ritmo de la página.
  - Los cortes se hacen en filas "quietas" (sin texto ni bordes) detectadas con un canvas en Chrome, así no se parte una línea;
    si el canvas no puede leer el PNG, cae a cortes parejos y lo avisa.
  - Los tramos son recortes CSS de la misma imagen (no se re-codifica nada) y se verifica el tamaño del PDF.
"""
import argparse
import glob
import html
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

LABELS = {
    "es": {
        "doc": "Bocetos de landing", "cover_kicker": "Documento de trabajo · Bocetos",
        "proposals": "Propuestas", "pages": "págs.", "how": "Cómo leer este PDF",
        "how_text": ("Cada propuesta tiene: una página de resumen (ángulo, estrategia, estructura de secciones y CTA), una vista "
                     "general de la captura desktop completa y las capturas en tramos legibles (desktop 1440 px: un tramo por página; "
                     "mobile 390 px: varias columnas por página, en orden de lectura). Los cortes se hacen en espacios en blanco."),
        "note_default": "Wireframes en escala de grises. Todo texto con sello EJEMPLO es ilustrativo; los huecos marcados [A CONSEGUIR] son decisiones o datos que faltan y no se resuelven inventando.",
        "source": "Fuente de la verdad", "angle": "Ángulo", "big_idea": "Idea central", "audience": "Audiencia",
        "awareness": "Nivel de conciencia", "traffic": "Tráfico supuesto", "cta1": "CTA primario", "cta2": "CTA secundario",
        "sections": "Estructura de secciones", "section": "Sección", "purpose": "Propósito", "risk": "Decisión más arriesgada",
        "gaps": "Huecos [A CONSEGUIR]", "summary": "Resumen", "overview": "Vista general · desktop completo",
        "desktop": "Desktop 1440 px", "mobile": "Mobile 390 px", "slice": "tramo", "of": "de", "px": "px",
        "mobile_cols": "columnas en orden de lectura (de izquierda a derecha)",
    },
    "en": {
        "doc": "Landing sketches", "cover_kicker": "Working document · Sketches",
        "proposals": "Proposals", "pages": "pp.", "how": "How to read this PDF",
        "how_text": ("Each proposal has a summary page (angle, strategy, section structure and CTA), an overview of the full desktop "
                     "capture and the captures in readable slices (desktop 1440 px: one slice per page; mobile 390 px: several columns "
                     "per page, in reading order). Cuts are made on blank rows."),
        "note_default": "Grayscale wireframes. Any text stamped EXAMPLE is illustrative; gaps marked [TO GET] are missing decisions or data and are never filled by inventing.",
        "source": "Source of truth", "angle": "Angle", "big_idea": "Big idea", "audience": "Audience",
        "awareness": "Awareness level", "traffic": "Assumed traffic", "cta1": "Primary CTA", "cta2": "Secondary CTA",
        "sections": "Section structure", "section": "Section", "purpose": "Purpose", "risk": "Riskiest decision",
        "gaps": "Gaps [TO GET]", "summary": "Summary", "overview": "Overview · full desktop",
        "desktop": "Desktop 1440 px", "mobile": "Mobile 390 px", "slice": "slice", "of": "of", "px": "px",
        "mobile_cols": "columns in reading order (left to right)",
    },
}

# Geometría (A4 apaisado con 10 mm de margen)
PAGE_W, PAGE_H, MARGIN = 297.0, 210.0, 10.0
CONTENT_W = PAGE_W - 2 * MARGIN          # 277 mm
PG_H = PAGE_H - 2 * MARGIN - 1.0         # 189 mm (1 mm de holgura contra el redondeo)
HD_H = 8.0 + 2.5                         # cabecera + separación
GAP = 6.0


def die(msg):
    sys.stderr.write("ERROR: " + msg + "\n")
    sys.exit(1)


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        die("no es un PNG: " + path)
    return struct.unpack(">II", head[16:24])


def g(meta, *keys, default=""):
    for k in keys:
        if k in meta and meta[k] not in (None, ""):
            return meta[k]
    return default


def esc(s):
    return html.escape(str(s), quote=True)


def paras(s):
    return "".join("<p>%s</p>" % esc(x) for x in str(s).split("\n") if x.strip())


def find_chrome():
    c = os.environ.get("CHROME")
    cands = [c] if c else []
    cands += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        p = shutil.which(n)
        if p:
            cands.append(p)
    for p in cands:
        if p and os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    die("no encuentro Chrome; exportá CHROME=/ruta/al/binario")


def chrome(args, timeout=240):
    prof = tempfile.mkdtemp(prefix="bocetos-chrome-")
    cmd = [find_chrome(), "--headless=new", "--disable-gpu", "--allow-file-access-from-files", "--hide-scrollbars",
           "--host-resolver-rules=MAP * ~NOTFOUND , EXCLUDE localhost",
           "--no-first-run", "--no-default-browser-check", "--user-data-dir=" + prof] + args
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout)
    finally:
        shutil.rmtree(prof, ignore_errors=True)
    return r


def file_url(p):
    from pathlib import Path
    return Path(p).resolve().as_uri()


CUT_HTML = """<!doctype html><meta charset="utf-8"><body><pre id="out">pending</pre>
<script>
const JOBS = %JOBS%;
function load(src){return new Promise((res,rej)=>{const i=new Image();i.onload=()=>res(i);i.onerror=()=>rej(new Error('no carga '+src));i.src=src;});}
async function run(j){
  const img=await load(j.src);
  const W=img.naturalWidth,H=img.naturalHeight;
  let tainted=false;
  // Transiciones de color por fila en [y0,y1): una fila "quieta" (sin texto ni bordes verticales) tiene casi 0.
  function scores(y0,y1){
    const rows=y1-y0;
    const cv=document.createElement('canvas');cv.width=W;cv.height=rows;
    const ctx=cv.getContext('2d',{willReadFrequently:true});
    ctx.drawImage(img,0,y0,W,rows,0,0,W,rows);
    let d;
    try{d=ctx.getImageData(0,0,W,rows).data;}catch(e){tainted=true;return null;}
    const sc=new Array(rows);
    for(let r=0;r<rows;r++){let t=0;const o=r*W*4;
      for(let x=1;x<W;x++){const a=o+x*4,b=a-4;
        if(Math.abs(d[a]-d[b])+Math.abs(d[a+1]-d[b+1])+Math.abs(d[a+2]-d[b+2])>40)t++;}
      sc[r]=t;}
    return sc;
  }
  // Elige dónde cortar en [lo,hi): el último de los tramos quietos más largos (los espacios entre secciones
  // ganan a los interlineados); si no hay ninguno, la fila con menos transiciones.
  function pick(lo,hi){
    lo=Math.max(1,Math.floor(lo));hi=Math.min(H-1,Math.floor(hi));
    if(hi-lo<6)return hi;
    const sc=scores(lo,hi);
    if(!sc)return hi;
    const runs=[];let st=-1;
    for(let r=0;r<=sc.length;r++){
      const q=r<sc.length&&sc[r]<=2;
      if(q){if(st<0)st=r;}else if(st>=0){runs.push([st,r-st]);st=-1;}
    }
    let longest=0;for(const u of runs)longest=Math.max(longest,u[1]);
    if(longest>=3){
      const min=Math.max(3,longest*0.6);
      let chosen=null;for(const u of runs){if(u[1]>=min)chosen=u;}
      return lo+chosen[0]+Math.floor(chosen[1]/2);
    }
    let m=Infinity,mr=sc.length-1;
    for(let r=0;r<sc.length;r++){if(sc[r]<=m){m=sc[r];mr=r;}}
    return lo+mr;
  }
  const cuts=[0];
  if(j.n){                                   // n tramos parejos (vista general)
    const step=H/j.n;
    for(let k=1;k<j.n;k++){const t=Math.round(k*step);cuts.push(pick(t-j.win,t));}
  }else{                                     // llenar cada página hasta maxh, cortando lo más tarde posible
    let y=0;
    while(H-y>j.maxh){const c=pick(y+j.maxh*0.6,y+j.maxh);cuts.push(c);y=c;}
    const L=cuts.length;
    if(L>=2&&(H-cuts[L-1])<0.3*j.maxh){  // cola muy corta: repartir los dos últimos tramos
      const a=cuts[L-2],mid=Math.round((a+H)/2);
      cuts[L-1]=pick(mid-0.15*j.maxh,mid+0.15*j.maxh);
    }
  }
  cuts.push(H);
  return{W:W,H:H,cuts:cuts,mode:tainted?'fixed':'quiet'};
}
async function main(){
  const out={};
  for(const j of JOBS){try{out[j.key]=await run(j);}catch(e){out[j.key]={error:String(e)};}}
  document.getElementById('out').textContent=JSON.stringify(out);
}
main();
</script></body>"""


def compute_cuts(jobs, workdir):
    """jobs: [{key, src(url), maxh, win}] -> {key: {cuts, mode}} usando Chrome para buscar filas quietas."""
    page = os.path.join(workdir, "cuts.html")
    with open(page, "w", encoding="utf-8") as f:
        # "<" escapado: el JSON va dentro de un <script> y un "</script>" en un id lo cerraría.
        f.write(CUT_HTML.replace("%JOBS%", json.dumps(jobs).replace("<", "\\u003c")))
    r = chrome(["--virtual-time-budget=60000", "--dump-dom", file_url(page)])
    m = re.search(r'<pre id="out">(.*?)</pre>', r.stdout.decode("utf-8", "replace"), re.S)
    res = {}
    if m and m.group(1) != "pending":
        try:
            res = json.loads(html.unescape(m.group(1)))
        except ValueError:
            res = {}
    out = {}
    for j in jobs:
        v = res.get(j["key"])
        if not v or "error" in v:
            sys.stderr.write("AVISO: no pude analizar %s con Chrome (%s); uso cortes parejos.\n" % (j["key"], (v or {}).get("error", "sin respuesta")))
            H = j["H"]
            n = j.get("n") or max(1, math.ceil(H / j["maxh"]))
            out[j["key"]] = {"cuts": [round(i * H / n) for i in range(n)] + [H], "mode": "fixed"}
        else:
            out[j["key"]] = v
    return out


def best_overview(H, W):
    """Elige la cantidad de columnas k de la vista general que maximiza la escala.
    Cada tramo puede alargarse hasta 1/8 del paso al buscar una fila quieta, de ahí el 1,125."""
    avail_h = PG_H - HD_H - 5.0
    best = None
    for k in range(1, 9):
        s_h = avail_h * k / (1.125 * float(H))
        s_w = (CONTENT_W - (k - 1) * GAP) / (k * float(W))
        s = min(s_h, s_w)
        if best is None or s > best[1] + 1e-9:
            best = (k, s)
    return best


CSS = """
@page { size: A4 landscape; margin: %(m)smm;
  @bottom-left { content: "%(foot)s"; font-family: Helvetica, Arial, sans-serif; font-size: 7pt; color: #777; }
  @bottom-right { content: counter(page) " / " counter(pages); font-family: Helvetica, Arial, sans-serif; font-size: 7pt; color: #777; } }
@page :first { margin: 0; @bottom-left { content: none; } @bottom-right { content: none; } }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif; color: #1a1a1a; font-size: 9pt; line-height: 1.4; }
p { margin: 0 0 1.6mm; }
.cover { width: 297mm; height: 209mm; background: #262626; color: #f2f2f2; padding: 22mm 24mm 16mm; display: flex; flex-direction: column; break-after: page; overflow: hidden; }
.cover .kicker { font: 600 8.5pt/1 Menlo, monospace; letter-spacing: .2em; text-transform: uppercase; color: #bdbdbd; }
.cover h1 { font-size: 40pt; line-height: 1.05; margin: 14mm 0 0; letter-spacing: -.02em; font-weight: 700; }
.cover .sub { font-size: 16pt; color: #d6d6d6; margin-top: 3mm; }
.cover .list { margin-top: 12mm; display: grid; gap: 2.2mm; font-size: 10.5pt; max-width: 230mm; }
.cover .list div { display: grid; grid-template-columns: 9mm 1fr 22mm; gap: 4mm; border-top: .25mm solid #4a4a4a; padding-top: 2mm; }
.cover .list b { font-family: Menlo, monospace; }
.cover .list span.pgs { text-align: right; color: #aaa; font-size: 8.5pt; }
.cover .how { margin-top: auto; display: grid; grid-template-columns: 1.4fr 1fr; gap: 10mm; font-size: 8.5pt; color: #cfcfcf; border-top: .25mm solid #4a4a4a; padding-top: 4mm; }
.cover .how b { color: #fff; display: block; margin-bottom: 1mm; }
.pg { width: %(cw)smm; height: %(pgh)smm; overflow: hidden; break-after: page; display: flex; flex-direction: column; }
.flow { width: %(cw)smm; break-after: page; }
.last { break-after: auto; }
.hd { height: 8mm; margin-bottom: 2.5mm; display: flex; justify-content: space-between; align-items: baseline; border-bottom: .3mm solid #bbb; font-size: 8pt; color: #555; padding-bottom: 1.4mm; flex: none; }
.hd b { color: #111; font-size: 9.5pt; }
.hd .id { display: inline-block; background: #1a1a1a; color: #fff; font: 700 8pt/1 Menlo, monospace; padding: 1.2mm 2mm; border-radius: 1mm; margin-right: 2mm; }
.sl { overflow: hidden; outline: .2mm solid #aaa; flex: none; }
.sl img { display: block; max-width: none; }
.cols { display: flex; gap: %(gap)smm; align-items: flex-start; }
.col .cap { font: 7pt/1 Menlo, monospace; color: #777; margin-bottom: 1.2mm; height: 3mm; }
.summary h2 { font-size: 22pt; line-height: 1.1; margin: 0 0 2mm; letter-spacing: -.01em; }
.summary .angle { font-size: 11.5pt; color: #333; margin-bottom: 4mm; max-width: 150mm; }
.summary .grid { display: grid; grid-template-columns: 1fr 1.25fr; gap: 8mm; }
.summary dl { margin: 0; display: grid; grid-template-columns: 30mm 1fr; gap: 1.6mm 3mm; font-size: 8.6pt; }
.summary dt { font: 600 7pt/1.5 Menlo, monospace; text-transform: uppercase; letter-spacing: .06em; color: #666; padding-top: .3mm; }
.summary dd { margin: 0; }
.summary table { width: 100%%; border-collapse: collapse; font-size: 8pt; }
.summary th { text-align: left; font: 600 6.8pt/1.3 Menlo, monospace; text-transform: uppercase; letter-spacing: .06em; color: #666; background: #eee; padding: 1.2mm 2mm; }
.summary td { padding: 1.1mm 2mm; border-bottom: .2mm solid #ddd; vertical-align: top; }
.summary td.n { font-family: Menlo, monospace; color: #666; width: 8mm; }
.summary h3 { font: 600 7.5pt/1 Menlo, monospace; letter-spacing: .08em; text-transform: uppercase; color: #555; margin: 4mm 0 1.6mm; }
.summary .risk { border-left: 1.2mm solid #1a1a1a; background: #f1f1f1; padding: 2.4mm 3.5mm; font-size: 8.6pt; margin-top: 3mm; break-inside: avoid; }
.summary .gaps { font: 7.6pt/1.45 Menlo, monospace; border: .3mm dashed #888; background: #f6f6f6; padding: 2.4mm 3.5mm; margin-top: 3mm; break-inside: avoid; }
.summary .gaps li { margin-bottom: .8mm; }
.summary ul { margin: 0; padding-left: 4mm; }
"""


def build_html(folder, args, L, cuts, geom, props, cover):
    lang_footer = cover["title"]
    css = CSS % {"m": MARGIN, "foot": lang_footer.replace('"', "'"), "cw": CONTENT_W, "pgh": PG_H, "gap": GAP}
    out = ["<!doctype html><html lang=\"%s\"><head><meta charset=\"utf-8\"><title>%s</title><style>%s</style></head><body>" % (args.lang, esc(cover["title"]), css)]

    # Portada
    out.append('<div class="cover"><div class="kicker">%s%s</div><h1>%s</h1>%s' % (
        esc(L["cover_kicker"]), (" · " + esc(cover["date"])) if cover["date"] else "", esc(cover["title"]),
        ('<div class="sub">%s</div>' % esc(cover["subtitle"])) if cover["subtitle"] else ""))
    out.append('<div class="list">')
    for p in props:
        out.append('<div><b>%s</b><span>%s</span><span class="pgs">%s %d–%d</span></div>' % (
            esc(p["id"]), esc(p["name"] + (" · " + p["angle"] if p["angle"] else "")), L["pages"], p["first"], p["last"]))
    out.append("</div>")
    out.append('<div class="how"><div><b>%s</b>%s</div><div>%s%s</div></div></div>' % (
        esc(L["how"]), esc(L["how_text"]),
        ("<b>%s</b>%s<br><br>" % (esc(L["source"]), esc(cover["source"]))) if cover["source"] else "",
        esc(cover["note"] or L["note_default"])))

    for pi, p in enumerate(props):
        meta = p["meta"]
        # Resumen
        out.append('<div class="flow summary%s"><div class="hd"><span><span class="id">%s</span><b>%s</b> · %s</span><span>%s</span></div>' % (
            "", esc(p["id"]), esc(p["name"]), esc(L["summary"]), esc(cover["title"])))
        out.append("<h2>%s</h2>" % esc(p["name"]))
        if p["angle"]:
            out.append('<p class="angle">%s</p>' % esc(p["angle"]))
        out.append('<div class="grid"><div><dl>')
        for lab, val in ((L["big_idea"], g(meta, "big_idea", "idea_central")), (L["audience"], g(meta, "audiencia", "audience")),
                         (L["awareness"], g(meta, "conciencia", "awareness")), (L["traffic"], g(meta, "trafico", "traffic")),
                         (L["cta1"], g(meta, "cta_primario", "cta_primary")), (L["cta2"], g(meta, "cta_secundario", "cta_secondary"))):
            if val:
                out.append("<dt>%s</dt><dd>%s</dd>" % (esc(lab), esc(val)))
        out.append("</dl>")
        risk = g(meta, "decision_riesgosa", "riskiest")
        if risk:
            out.append('<div class="risk"><b>%s.</b> %s</div>' % (esc(L["risk"]), esc(risk)))
        gaps = g(meta, "placeholders", "gaps", default=[])
        if gaps:
            out.append('<div class="gaps"><b>%s</b><ul>%s</ul></div>' % (esc(L["gaps"]), "".join("<li>%s</li>" % esc(x) for x in gaps[:8])))
        out.append("</div><div>")
        secs = g(meta, "secciones", "sections", default=[])
        if secs:
            out.append("<h3 style=\"margin-top:0\">%s</h3><table><thead><tr><th>#</th><th>%s</th><th>%s</th></tr></thead><tbody>" % (
                esc(L["sections"]), esc(L["section"]), esc(L["purpose"])))
            for s in secs:
                out.append('<tr><td class="n">%s</td><td><b>%s</b></td><td>%s</td></tr>' % (
                    esc(g(s, "n")), esc(g(s, "nombre", "name")), esc(g(s, "proposito", "purpose"))))
            out.append("</tbody></table>")
        out.append("</div></div></div>")

        # Vista general
        k, s_o = p["overview"]["k"], p["overview"]["scale"]
        W, H = p["d_size"]
        cuts_o = p["overview"]["cuts"]
        out.append('<div class="pg"><div class="hd"><span><span class="id">%s</span><b>%s</b> · %s</span><span>%s · %d %s</span></div><div class="cols">' % (
            esc(p["id"]), esc(p["name"]), esc(L["overview"]), esc(L["desktop"]), H, L["px"]))
        for i in range(len(cuts_o) - 1):
            y0, y1 = cuts_o[i], cuts_o[i + 1]
            out.append('<div class="col"><div class="cap">%d–%d %s</div><div class="sl" style="width:%.3fmm;height:%.3fmm"><img src="%s" style="width:%.3fmm;margin-top:-%.3fmm"></div></div>' % (
                y0, y1, L["px"], W * s_o, (y1 - y0) * s_o, p["d_url"], W * s_o, y0 * s_o))
        out.append("</div></div>")

        # Desktop: un tramo por página
        s_d = CONTENT_W / float(W)
        cd = p["d_cuts"]
        for i in range(len(cd) - 1):
            y0, y1 = cd[i], cd[i + 1]
            out.append('<div class="pg"><div class="hd"><span><span class="id">%s</span><b>%s</b> · %s · %s %d %s %d</span><span>%d–%d %s %s %d</span></div><div class="sl" style="width:%.3fmm;height:%.3fmm"><img src="%s" style="width:%.3fmm;margin-top:-%.3fmm"></div></div>' % (
                esc(p["id"]), esc(p["name"]), esc(L["desktop"]), L["slice"], i + 1, L["of"], len(cd) - 1,
                y0, y1, L["px"], L["of"], H, CONTENT_W, (y1 - y0) * s_d, p["d_url"], CONTENT_W, y0 * s_d))

        # Mobile: columnas por página
        mW, mH = p["m_size"]
        colw = (CONTENT_W - (args.cols - 1) * GAP) / args.cols
        s_m = colw / float(mW)
        cm = p["m_cuts"]
        n_sl = len(cm) - 1
        pages_m = int(math.ceil(n_sl / float(args.cols)))
        for pg in range(pages_m):
            last = (pi == len(props) - 1 and pg == pages_m - 1)
            out.append('<div class="pg%s"><div class="hd"><span><span class="id">%s</span><b>%s</b> · %s · %s</span><span>%d %s</span></div><div class="cols">' % (
                " last" if last else "", esc(p["id"]), esc(p["name"]), esc(L["mobile"]), esc(L["mobile_cols"]), mH, L["px"]))
            for j in range(pg * args.cols, min(n_sl, (pg + 1) * args.cols)):
                y0, y1 = cm[j], cm[j + 1]
                out.append('<div class="col"><div class="cap">%d–%d %s</div><div class="sl" style="width:%.3fmm;height:%.3fmm"><img src="%s" style="width:%.3fmm;margin-top:-%.3fmm"></div></div>' % (
                    y0, y1, L["px"], colw, (y1 - y0) * s_m, p["m_url"], colw, y0 * s_m))
            out.append("</div></div>")
    out.append("</body></html>")
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("out")
    ap.add_argument("--lang", default="es", choices=sorted(LABELS))
    ap.add_argument("--cols", type=int, default=4, help="columnas mobile por página (default 4)")
    ap.add_argument("--keep-html")
    ap.add_argument("--title")
    ap.add_argument("--subtitle")
    ap.add_argument("--date")
    ap.add_argument("--brand")
    ap.add_argument("--note")
    args = ap.parse_args()
    L = LABELS[args.lang]
    folder = os.path.abspath(args.folder)
    if not os.path.isdir(folder):
        die("no existe la carpeta " + folder)

    cmeta = {}
    cp = os.path.join(folder, "bocetos.meta.json")
    if os.path.exists(cp):
        cmeta = json.load(open(cp, encoding="utf-8"))
    cover = {
        "title": args.title or g(cmeta, "titulo", "title", default=L["doc"]),
        "subtitle": args.subtitle or g(cmeta, "subtitulo", "subtitle"),
        "date": args.date or g(cmeta, "fecha", "date"),
        "brand": args.brand or g(cmeta, "marca", "brand"),
        "note": args.note or g(cmeta, "nota", "note"),
        "source": g(cmeta, "fuente", "source"),
    }

    metas = sorted(glob.glob(os.path.join(folder, "propuesta-*.meta.json")))
    if not metas:
        die("no encontré propuesta-*.meta.json en " + folder)
    props = []
    for mp in metas:
        meta = json.load(open(mp, encoding="utf-8"))
        pid = str(g(meta, "id", default=re.search(r"propuesta-(.+)\.meta\.json$", os.path.basename(mp)).group(1)))
        if not re.match(r"^[A-Za-z0-9_-]+$", pid):
            die("id de propuesta inválido en %s: solo letras, números, - y _" % mp)
        dpng = os.path.join(folder, g(meta, "desktop", default="propuesta-%s-desktop.png" % pid))
        mpng = os.path.join(folder, g(meta, "mobile", default="propuesta-%s-mobile.png" % pid))
        for pth in (dpng, mpng):
            if not os.path.exists(pth):
                die("falta la captura " + pth)
        props.append({"id": pid, "name": str(g(meta, "nombre", "name", default="Propuesta " + pid)),
                      "angle": str(g(meta, "angulo", "angle")), "meta": meta,
                      "d_png": dpng, "m_png": mpng, "d_url": file_url(dpng), "m_url": file_url(mpng),
                      "d_size": png_size(dpng), "m_size": png_size(mpng)})

    # Geometría y cortes
    jobs = []
    for p in props:
        dW, dH = p["d_size"]
        mW, mH = p["m_size"]
        s_d = CONTENT_W / float(dW)
        maxh_d = int((PG_H - HD_H - 1.5) / s_d)
        colw = (CONTENT_W - (args.cols - 1) * GAP) / args.cols
        s_m = colw / float(mW)
        maxh_m = int((PG_H - HD_H - 4.5) / s_m)
        k, s_o = best_overview(dH, dW)
        p["overview"] = {"k": k, "scale": s_o}
        jobs += [{"key": p["id"] + ":d", "src": p["d_url"], "maxh": maxh_d, "H": dH},
                 {"key": p["id"] + ":m", "src": p["m_url"], "maxh": maxh_m, "H": mH},
                 {"key": p["id"] + ":o", "src": p["d_url"], "n": k, "maxh": 0, "win": max(20, dH // k // 8), "H": dH}]
    work = tempfile.mkdtemp(prefix="bocetos-")
    cuts = compute_cuts(jobs, work)
    modes = set()
    for p in props:
        p["d_cuts"] = cuts[p["id"] + ":d"]["cuts"]
        p["m_cuts"] = cuts[p["id"] + ":m"]["cuts"]
        p["overview"]["cuts"] = cuts[p["id"] + ":o"]["cuts"]
        modes |= {cuts[p["id"] + ":d"]["mode"], cuts[p["id"] + ":m"]["mode"]}

    # Páginas esperadas (1 por resumen) para el índice de la portada
    page = 2
    for p in props:
        n_d = len(p["d_cuts"]) - 1
        n_m = int(math.ceil((len(p["m_cuts"]) - 1) / float(args.cols)))
        p["first"] = page
        p["last"] = page + 1 + 1 + n_d + n_m - 1   # resumen + general + desktop + mobile
        p["expected"] = 1 + 1 + n_d + n_m
        page = p["last"] + 1
    expected_total = page - 1

    doc = build_html(folder, args, L, cuts, None, props, cover)
    hp = os.path.join(work, "bocetos.html")
    with open(hp, "w", encoding="utf-8") as f:
        f.write(doc)
    if args.keep_html:
        shutil.copy(hp, args.keep_html)

    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    r = chrome(["--virtual-time-budget=60000", "--no-pdf-header-footer", "--print-to-pdf=" + out, file_url(hp)], timeout=600)
    if not os.path.exists(out) or os.path.getsize(out) == 0:
        sys.stderr.write(r.stderr.decode("utf-8", "replace")[-800:])
        die("Chrome no generó el PDF")
    shutil.rmtree(work, ignore_errors=True)

    print("Cortes: %s" % ("en filas quietas (sin partir líneas de texto)" if modes == {"quiet"} else "AVISO: al menos una captura quedó con cortes parejos (%s)" % ",".join(sorted(modes))))
    for p in props:
        print("  %s · desktop %dx%d px -> %d tramos · mobile %dx%d px -> %d tramos (%d págs) · vista general en %d columnas" % (
            p["id"], p["d_size"][0], p["d_size"][1], len(p["d_cuts"]) - 1, p["m_size"][0], p["m_size"][1],
            len(p["m_cuts"]) - 1, int(math.ceil((len(p["m_cuts"]) - 1) / float(args.cols))), len(p["overview"]["cuts"]) - 1))
    print("Páginas esperadas: %d" % expected_total)

    # Verificación
    pc = os.path.join(HERE, "pdf_check.py")
    ver = subprocess.run([sys.executable, pc, out, "--mode", "images", "--paper", "A4", "--sparse-ok", "1"],
                         capture_output=True, text=True)
    sys.stdout.write(ver.stdout)
    m = re.search(r"· (\d+) páginas", ver.stdout)
    real = int(m.group(1)) if m else -1
    status = 0
    if real != expected_total:
        print("AVISO: el PDF tiene %d páginas y se esperaban %d (¿se desbordó una página de resumen?)." % (real, expected_total))
        status = 1
    # El tamaño del PDF no debería multiplicarse por la cantidad de tramos
    total_png = sum(os.path.getsize(p["d_png"]) + os.path.getsize(p["m_png"]) for p in props)
    size = os.path.getsize(out)
    print("Tamaño: PDF %.1f MB · PNG de origen %.1f MB (relación %.1fx)" % (size / 1048576.0, total_png / 1048576.0, size / float(max(total_png, 1))))
    if size > 6 * total_png + 2 * 1048576:
        print("AVISO: el PDF pesa mucho más que las capturas; Chrome pudo duplicar las imágenes por tramo.")
        status = 1
    sys.exit(status)


if __name__ == "__main__":
    main()
