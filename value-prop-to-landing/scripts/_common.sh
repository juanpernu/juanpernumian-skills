#!/usr/bin/env bash
# _common.sh · funciones compartidas por los scripts del skill. No se ejecuta solo: se carga con
#   source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
#
# Chrome: se toma de la variable CHROME; si no existe, el default de macOS y después los nombres
# habituales de Linux. Cada script usa un perfil temporal propio (así no choca con un Chrome abierto).

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
if [ ! -x "$CHROME" ]; then
  for _c in google-chrome google-chrome-stable chromium chromium-browser; do
    if command -v "$_c" >/dev/null 2>&1; then CHROME="$(command -v "$_c")"; break; fi
  done
fi
if [ ! -x "$CHROME" ]; then
  echo "ERROR: no encuentro Chrome. Exportá CHROME=/ruta/al/binario (por ejemplo CHROME=/usr/bin/chromium)." >&2
  exit 2
fi

SKILL_TMP="$(mktemp -d "${TMPDIR:-/tmp}/vpl.XXXXXX")"
cleanup_tmp() { rm -rf "$SKILL_TMP"; }
trap cleanup_tmp EXIT

# Corre Chrome headless con los flags comunes. Uso: chrome_run <flags extra...> <url>
chrome_run() {
  "$CHROME" --headless=new --disable-gpu --allow-file-access-from-files --hide-scrollbars \
    "--host-resolver-rules=MAP * ~NOTFOUND , EXCLUDE localhost" \
    --no-first-run --no-default-browser-check --user-data-dir="$SKILL_TMP/profile" "$@" 2>/dev/null
}

# Ruta absoluta de un archivo (existente).
abs_path() { python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$1"; }

# URL file:// bien codificada (soporta espacios y tildes en la ruta).
file_url() { python3 -c 'import sys,pathlib; print(pathlib.Path(sys.argv[1]).resolve().as_uri())' "$1"; }

# Arma una página envoltorio con el HTML dentro de un iframe del ancho pedido.
#   Se usa un iframe porque Chrome headless no baja de 500 px de ventana: el iframe es el que mide 390 px reales
#   (y por eso se evalúan bien las media queries mobile).
#   Con ancho < 500 el iframe se corre 1 px a la derecha: el recorte posterior (sips) arranca en x = 1,
#   porque un offset 0 se interpreta como "centrar" y cortaba ~55 px del borde izquierdo.
# Uso: make_wrap <html> <ancho> <alto del iframe> <salida.html>
make_wrap() {
  local url left=0
  url="$(file_url "$1")"
  [ "$2" -lt 500 ] && left=1
  cat > "$4" <<EOT
<!doctype html><html><body style="margin:0;background:#fff"><iframe id="f" src="$url" style="display:block;margin-left:${left}px;width:${2}px;height:${3}px;border:0"></iframe>
<script>var f=document.getElementById('f');f.onload=function(){setTimeout(function(){var d=f.contentDocument;
document.body.setAttribute('data-h',Math.max(d.documentElement.scrollHeight,d.body.scrollHeight));
document.body.setAttribute('data-w',d.documentElement.scrollWidth)},700)}</script></body></html>
EOT
}

# Mide un HTML a un ancho dado. Imprime "ALTO ANCHO_CONTENIDO" (px). Devuelve 1 si no pudo medir.
# Uso: measure_page <html> <ancho> [alto inicial del iframe=800]
measure_page() {
  local html="$1" w="$2" h0="${3:-800}" wrap out
  wrap="$SKILL_TMP/wrap-measure-$w.html"
  make_wrap "$html" "$w" "$h0" "$wrap"
  out="$(chrome_run --virtual-time-budget=8000 --dump-dom "$(file_url "$wrap")" | grep -o 'data-h="[0-9]*" data-w="[0-9]*"' | head -1)"
  [ -z "$out" ] && return 1
  echo "$(echo "$out" | sed -E 's/.*data-h="([0-9]+)".*/\1/') $(echo "$out" | sed -E 's/.*data-w="([0-9]+)".*/\1/')"
}

# Ancho imprimible (px) de un HTML según su primer @page (size y margin); sirve para detectar desbordes antes de imprimir.
# Chrome reduce TODO el documento ("shrink to fit") cuando algo es más ancho que la página: no se ve texto afuera, se ve todo más chico.
print_width_px() {
  python3 - "$1" <<'PY'
import re, sys
css = open(sys.argv[1], encoding="utf-8", errors="replace").read()
m = re.search(r"@page\s*\{", css)
seg = css[m.end():m.end() + 800] if m else ""
sizes = {"a5": (148, 210), "a4": (210, 297), "a3": (297, 420), "letter": (215.9, 279.4), "legal": (215.9, 355.6)}
w, h = sizes["a4"]
sm = re.search(r"size\s*:\s*([^;}]+)", seg)
if sm:
    t = sm.group(1).lower().split()
    for k in t:
        if k in sizes:
            w, h = sizes[k]
    nums = [x for x in t if re.match(r"[\d.]+(mm|cm|in|px|pt)$", x)]
    if len(nums) == 2:
        def mm(x):
            v = float(re.match(r"[\d.]+", x).group()); u = x[-2:]
            return v * {"mm": 1, "cm": 10, "in": 25.4, "px": 25.4 / 96, "pt": 25.4 / 72}[u]
        w, h = mm(nums[0]), mm(nums[1])
    if "landscape" in t:
        w, h = max(w, h), min(w, h)
left = right = 10.16  # 0.4 in: margen por defecto de Chrome
mg = re.search(r"margin\s*:\s*([^;}]+)", seg)
if mg:
    def mm1(x):
        v = float(re.match(r"-?[\d.]+", x).group()); u = re.search(r"(mm|cm|in|px|pt)$", x)
        return v * {"mm": 1, "cm": 10, "in": 25.4, "px": 25.4 / 96, "pt": 25.4 / 72}[u.group(1)] if u else 0.0
    v = [mm1(x) for x in mg.group(1).split()]
    if len(v) == 1: left = right = v[0]
    elif len(v) == 2: left = right = v[1]
    elif len(v) == 3: left = right = v[1]
    elif len(v) == 4: left, right = v[3], v[1]
print(int((w - left - right) * 96 / 25.4))
PY
}

# Lista los elementos que se pasan del ancho dado (excepto los que cumplen el selector permitido, p. ej. una portada a página completa).
# Imprime una línea por elemento ("tag.clase borde-derecho-px: texto") o nada si no hay desborde.
# Uso: overflow_report <html> <ancho px> [selector permitido, default ".cover"]
overflow_report() {
  local html="$1" w="$2" allow="${3:-.cover}" wrap out url
  wrap="$SKILL_TMP/wrap-overflow.html"
  url="$(file_url "$html")"
  cat > "$wrap" <<EOT
<!doctype html><html><body style="margin:0"><iframe id="f" src="$url" style="display:block;width:${w}px;height:1200px;border:0"></iframe>
<script>var f=document.getElementById('f');f.onload=function(){setTimeout(function(){
var d=f.contentDocument,W=$w,allow='$allow',res=[];
[].forEach.call(d.querySelectorAll('body *'),function(e){
  if(allow&&e.closest(allow))return;
  var r=e.getBoundingClientRect(),own=f.contentWindow.getComputedStyle(e);
  var right=r.left+(own.overflowX==='visible'?Math.max(r.width,e.scrollWidth):r.width);
  if(r.width===0||right<=W+1)return;
  for(var a=e.parentElement;a&&a!==d.body;a=a.parentElement){var ar=a.getBoundingClientRect(),cs=f.contentWindow.getComputedStyle(a); if(ar.right<=W+1&&cs.overflowX!=='visible')return;}
  res.push([Math.round(right),e.tagName.toLowerCase()+(e.className&&typeof e.className==='string'?'.'+e.className.trim().split(/\s+/)[0]:''),(e.textContent||'').trim().replace(/\s+/g,' ').slice(0,50)]);
});
res.sort(function(a,b){return b[0]-a[0]});
document.body.setAttribute('data-ov',encodeURIComponent(JSON.stringify(res.slice(0,5))));
},700)}</script></body></html>
EOT
  out="$(chrome_run --virtual-time-budget=8000 --dump-dom "$(file_url "$wrap")" | grep -o 'data-ov="[^"]*"' | head -1 | sed -E 's/data-ov="([^"]*)"/\1/')"
  [ -z "$out" ] && return 0
  python3 - "$out" <<'PY'
import json, sys, urllib.parse
for right, tag, txt in json.loads(urllib.parse.unquote(sys.argv[1])):
    print("  %s llega a %d px: %s" % (tag, right, txt))
PY
}
