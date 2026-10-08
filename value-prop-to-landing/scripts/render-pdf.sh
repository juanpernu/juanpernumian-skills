#!/usr/bin/env bash
# render-pdf.sh · HTML -> PDF (A4 por defecto, según el @page del HTML) con Chrome headless + verificación.
#
# Uso:  render-pdf.sh <entrada.html> <salida.pdf> [--prev anterior.pdf] [--min-lines 5] [--min-fill 0.15]
#                     [--sparse-ok 1] [--edge-ok 1] [--strict]
# Variables: CHROME=/ruta/al/chrome
# Qué hace después de generar el PDF (con pdfinfo, pdftotext y pdftoppm):
#   - cuenta páginas y líneas por página, hasta dónde llega el contenido y la tinta de cada una;
#   - avisa de páginas casi vacías (un bloque empujado por una frase más larga), desbordes (texto fuera de la página)
#     y tamaños de página distintos;
#   - con --prev compara contra la versión anterior (páginas y líneas por página) para ver qué se movió.
# Regla del proceso: una página casi vacía se arregla acortando o compactando, no se acepta.
# En el HTML: usá @page { size: A4; margin: ... } y `break-inside: avoid` en tarjetas y filas; en las tablas, evitá columnas
# de páginas/fuentes que se ensanchen (rompen las filas); cada sección grande con `break-before: page`.
# Variable ALLOW_WIDE='.cover': elementos que pueden pasarse del ancho a propósito (portada a página completa).
# Código de salida: 0 (con avisos visibles) · 1 con --strict y avisos · 2 error.

set -u
source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
for t in pdfinfo pdftotext pdftoppm; do
  command -v "$t" >/dev/null 2>&1 || { echo "ERROR: falta $t (poppler). En macOS: brew install poppler" >&2; exit 2; }
done

[ $# -lt 2 ] && { sed -n '2,17p' "$0"; exit 2; }
HTML="$1"; OUT="$2"; shift 2
[ -f "$HTML" ] || { echo "no existe: $HTML" >&2; exit 2; }
HTML="$(abs_path "$HTML")"; OUT="$(abs_path "$OUT")"; mkdir -p "$(dirname "$OUT")"

# Aviso previo: algo más ancho que la página hace que Chrome encoja TODO el documento (no se ve texto afuera: se ve todo más chico).
PW="$(print_width_px "$HTML")"
OVR="$(overflow_report "$HTML" "$PW" "${ALLOW_WIDE:-.cover}")"
if [ -n "$OVR" ]; then
  echo "AVISO: elementos más anchos que el ancho imprimible (${PW} px); Chrome va a encoger todo el documento:" >&2
  echo "$OVR" >&2
  echo "  (excepciones con ALLOW_WIDE='selector', por defecto '.cover')" >&2
fi

chrome_run --virtual-time-budget=10000 --no-pdf-header-footer --print-to-pdf="$OUT" "$(file_url "$HTML")" >/dev/null
[ -s "$OUT" ] || { echo "Chrome no generó $OUT" >&2; exit 2; }

python3 "$(dirname "${BASH_SOURCE[0]}")/pdf_check.py" "$OUT" "$@"
