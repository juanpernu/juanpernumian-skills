#!/usr/bin/env bash
# check-claims.sh · grep parametrizable de patrones prohibidos y conteos estructurales sobre el texto visible de un HTML.
#
# Uso:  check-claims.sh <archivo.html|.md> [opciones]
#   --forbid 'gratis|primera|nunca'     patrones prohibidos (regex; sin distinguir mayúsculas; varios con |)
#   --forbid-file patrones.txt          un patrón por línea ("#" = comentario)
#   --require 'EJEMPLO'                 tiene que aparecer al menos una vez
#   --count 'EJEMPLO=4'                 cantidad exacta de coincidencias (repetible)
#   --max-words 2500                    falla si el texto visible supera ese largo
#   --attrs                             suma alt/title/aria-label/placeholder/value al texto
#   --show-text                         imprime el texto visible y sale
#   --no-structural                     sin los chequeos estructurales (h1, details open, anclas, recursos externos, sellos)
# Qué es "texto visible": sin script, style, head ni comentarios; incluye los <details> cerrados.
# Cuándo correrlo: en la ola de validación y tras cada pasada de correcciones (claims prohibidos que la fuente no respalda,
# rastros de una decisión superada, palabras de oferta no definida, sellos EJEMPLO, conteos que la spec promete).
# Código de salida: 0 sin problemas · 1 hay problemas · 2 uso incorrecto.

set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[ $# -lt 1 ] && { sed -n '2,17p' "$0"; exit 2; }
case "$1" in -h|--help) sed -n '2,17p' "$0"; exit 0 ;; esac
command -v python3 >/dev/null 2>&1 || { echo "ERROR: falta python3" >&2; exit 2; }
python3 "$HERE/check_claims.py" "$@"
exit $?
