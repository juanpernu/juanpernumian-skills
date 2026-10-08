#!/usr/bin/env bash
# measure-html.sh · mide el alto y el ancho de contenido de un HTML a uno o más anchos de viewport.
#
# Uso:  measure-html.sh <archivo.html> [ancho ...] [--json]
#   Sin anchos usa 1440. Ejemplo: measure-html.sh landing.html 1440 390
# Salida (una línea por ancho):
#   ancho=390 alto=14520 ancho_contenido=390 desborde=no
# Código de salida: 0 todo bien · 3 hay desborde horizontal en algún ancho · 1 no se pudo medir · 2 uso incorrecto.
#
# Para qué sirve: comparar el largo mobile contra otras propuestas, anticipar el alto de la captura y detectar
# scroll horizontal (ancho_contenido > ancho) antes de mirar nada a ojo.
# Nota: con ancho < 500 se mide dentro de un iframe del ancho pedido (Chrome headless no baja de 500 px de ventana).
# Evitá unidades vh en el wireframe: el alto del iframe de medición (800 px) no es el de una pantalla real.

set -u
source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"

JSON=0; WIDTHS=(); HTML=""
for a in "$@"; do
  case "$a" in
    --json) JSON=1 ;;
    -h|--help) sed -n '2,15p' "$0"; exit 0 ;;
    ''|*[!0-9]*) [ -z "$HTML" ] && HTML="$a" || { echo "argumento inesperado: $a" >&2; exit 2; } ;;
    *) WIDTHS+=("$a") ;;
  esac
done
[ -z "$HTML" ] && { echo "uso: measure-html.sh <archivo.html> [ancho ...] [--json]" >&2; exit 2; }
[ -f "$HTML" ] || { echo "no existe: $HTML" >&2; exit 2; }
[ ${#WIDTHS[@]} -eq 0 ] && WIDTHS=(1440)
HTML="$(abs_path "$HTML")"

rc=0; first=1
[ "$JSON" -eq 1 ] && printf '['
for w in "${WIDTHS[@]}"; do
  if ! m="$(measure_page "$HTML" "$w" 800)"; then echo "no pude medir $HTML a $w px" >&2; rc=1; continue; fi
  set -- $m; h="$1"; cw="$2"
  ov=no; [ "$cw" -gt "$w" ] && { ov=si; [ "$rc" -eq 0 ] && rc=3; }
  if [ "$JSON" -eq 1 ]; then
    [ "$first" -eq 0 ] && printf ','
    printf '{"ancho":%s,"alto":%s,"ancho_contenido":%s,"desborde":%s}' "$w" "$h" "$cw" "$([ "$ov" = si ] && echo true || echo false)"
  else
    echo "ancho=$w alto=$h ancho_contenido=$cw desborde=$ov"
  fi
  first=0
done
[ "$JSON" -eq 1 ] && echo ']'
exit $rc
