#!/usr/bin/env bash
# shot.sh · captura de página completa de un HTML a un ancho de viewport (desktop 1440, mobile 390, etc.).
#
# Uso:  shot.sh <archivo.html> <ancho> <salida.png> [--strict]
#   Ejemplos:  shot.sh landing.html 1440 landing-desktop.png
#              shot.sh landing.html 390  landing-mobile.png
# Variables:  CHROME=/ruta/al/chrome  (default: Chrome de macOS; si no está, google-chrome/chromium del PATH)
# Salida: una línea "archivo: alto medido=H · ancho de contenido=W (viewport=V) · pixeles reales WxH".
# Códigos: 0 ok · 3 desborde horizontal con --strict · 1 error de medición/recorte · 2 uso incorrecto.
#
# Cómo evita los problemas conocidos:
#  - Chrome headless no baja de 500 px de ventana: para 390 px captura un iframe de 390 px REALES dentro de una ventana
#    de 500 px y recorta después. Las media queries se evalúan a 390.
#  - Recorte con sips: `sips -c ALTO ANCHO --cropOffset <y> <x>` mide el offset desde la esquina superior izquierda,
#    pero un offset (0,0) se interpreta como "centrar" (cortaba ~55 px de cada borde). Se ancla con x = 1 y el iframe
#    está corrido 1 px a la derecha, así no se pierde ni un píxel.
#  - Mide el alto con dos pasadas (iframe de 800 px y después del alto medido) por si algo depende de la altura.
#  - Verifica que la imagen final tenga exactamente ANCHO x ALTO y avisa si el contenido desborda el viewport.
# Mirá siempre una captura recortada a ojo (Read de la imagen) antes de darla por buena.

set -u
source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"

STRICT=0; ARGS=()
for a in "$@"; do case "$a" in --strict) STRICT=1 ;; -h|--help) sed -n '2,20p' "$0"; exit 0 ;; *) ARGS+=("$a") ;; esac; done
[ ${#ARGS[@]} -ne 3 ] && { echo "uso: shot.sh <archivo.html> <ancho> <salida.png> [--strict]" >&2; exit 2; }
HTML="${ARGS[0]}"; W="${ARGS[1]}"; OUT="${ARGS[2]}"
[ -f "$HTML" ] || { echo "no existe: $HTML" >&2; exit 2; }
case "$W" in ''|*[!0-9]*) echo "el ancho debe ser un entero (px)" >&2; exit 2 ;; esac
HTML="$(abs_path "$HTML")"; OUT="$(abs_path "$OUT")"; mkdir -p "$(dirname "$OUT")"

# 1) Medir (dos pasadas)
m1="$(measure_page "$HTML" "$W" 800)" || { echo "no pude medir $HTML" >&2; exit 1; }
H1="${m1%% *}"
m2="$(measure_page "$HTML" "$W" "$H1")" || { echo "no pude medir $HTML (2da pasada)" >&2; exit 1; }
H="${m2%% *}"; SW="${m2##* }"
[ "$H" != "$H1" ] && echo "AVISO: el alto cambió entre pasadas ($H1 -> $H); ¿hay unidades vh o min-height ligados al viewport?" >&2
[ "$H" -gt 30000 ] && echo "AVISO: alto $H px; Chrome puede fallar sobre ~30.000 px. Considerá partir la captura." >&2

# 2) Capturar
WRAP="$SKILL_TMP/wrap-shot-$W.html"
make_wrap "$HTML" "$W" "$H" "$WRAP"
WIN="$W"; [ "$W" -lt 500 ] && WIN=500
chrome_run --virtual-time-budget=8000 --window-size="$WIN","$H" --screenshot="$OUT" "$(file_url "$WRAP")" >/dev/null
[ -s "$OUT" ] || { echo "Chrome no generó $OUT" >&2; exit 1; }

# 3) Recortar a ancho real (solo si W < 500)
if [ "$W" -lt 500 ]; then
  if command -v sips >/dev/null 2>&1; then
    sips -c "$H" "$W" --cropOffset 0 1 "$OUT" >/dev/null 2>&1
  elif command -v magick >/dev/null 2>&1; then
    magick "$OUT" -crop "${W}x${H}+1+0" +repage "$OUT"
  elif command -v convert >/dev/null 2>&1; then
    convert "$OUT" -crop "${W}x${H}+1+0" +repage "$OUT"
  else
    echo "ERROR: para recortar la captura mobile necesito sips (macOS) o ImageMagick." >&2; exit 1
  fi
fi

# 4) Verificar dimensiones finales
if command -v sips >/dev/null 2>&1; then
  PW="$(sips -g pixelWidth "$OUT" | awk '/pixelWidth/{print $2}')"; PH="$(sips -g pixelHeight "$OUT" | awk '/pixelHeight/{print $2}')"
  if [ "$PW" != "$W" ] || [ "$PH" != "$H" ]; then
    echo "ERROR: la imagen final mide ${PW}x${PH}, se esperaba ${W}x${H}" >&2; exit 1
  fi
else
  PW="$W"; PH="$H"
fi
echo "$(basename "$OUT"): alto medido=$H · ancho de contenido=$SW (viewport=$W) · pixeles reales ${PW}x${PH}"
if [ "$SW" -gt "$W" ]; then
  echo "ADVERTENCIA: desborde horizontal ($SW > $W): hay scroll horizontal a $W px." >&2
  [ "$STRICT" -eq 1 ] && exit 3
fi
exit 0
