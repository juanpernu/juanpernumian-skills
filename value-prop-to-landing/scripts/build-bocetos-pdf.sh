#!/usr/bin/env bash
# build-bocetos-pdf.sh · arma el PDF de bocetos (portada + por propuesta: resumen, vista general y capturas) desde metadatos + PNG.
#
# Uso:  build-bocetos-pdf.sh <carpeta-de-bocetos> <salida.pdf> [opciones de build_bocetos_pdf.py]
#   --lang es|en · --cols 4 · --keep-html ruta.html · --title T · --subtitle S · --date D · --brand B · --note N
# La carpeta contiene, por propuesta: propuesta-<id>.meta.json, propuesta-<id>-desktop.png y propuesta-<id>-mobile.png
# (y opcionalmente bocetos.meta.json para la portada). Ver el encabezado de build_bocetos_pdf.py para el esquema del JSON.
# Variables: CHROME=/ruta/al/chrome
#
# Diseño (probado con capturas de hasta 20.000 px de alto): las capturas largas se cortan en tramos que entran en una página
# A4 apaisada, escalados para que el texto se lea; desktop un tramo por página, mobile varias columnas por página, más una
# vista general. Los cortes caen en filas sin contenido. Al final verifica páginas, tamaños, desbordes, páginas en blanco
# y que el PDF no pese mucho más que las capturas de origen.
# Código de salida: 0 ok · 1 con avisos · 2 error.

set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/_common.sh"
export CHROME
for t in pdfinfo pdftotext pdftoppm; do
  command -v "$t" >/dev/null 2>&1 || { echo "ERROR: falta $t (poppler). En macOS: brew install poppler" >&2; exit 2; }
done
[ $# -lt 2 ] && { sed -n '2,15p' "$0"; exit 2; }
python3 "$HERE/build_bocetos_pdf.py" "$@"
exit $?
