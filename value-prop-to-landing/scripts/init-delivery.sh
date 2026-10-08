#!/usr/bin/env bash
# init-delivery.sh · crea la estructura de la carpeta de entrega (ver references/delivery-layout.md).
#
# Uso:  init-delivery.sh <carpeta> [--quick]
#   --quick  modo Rápido: una sola propuesta de landing (A) y una sola auditoría; no crea lo de B y C.
# No pisa nada: si la carpeta ya existe, solo agrega lo que falta. No crea archivos de contenido (los escriben las fases).

set -eu
[ $# -lt 1 ] && { sed -n '2,6p' "$0"; exit 2; }
DEST="$1"; QUICK=0
[ "${2:-}" = "--quick" ] && QUICK=1
mkdir -p "$DEST/01-propuesta-de-valor" "$DEST/02-bocetos" "$DEST/03-auditorias" "$DEST/04-landing-final" "$DEST/_trabajo"
cat > "$DEST/_trabajo/LEEME.txt" <<EOT
Carpeta de trabajo (no se entrega): informes de la ola de validación, lista de cambios finales y JSON de reemplazos.
Estructura completa y qué escribe cada fase: references/delivery-layout.md del skill.
EOT
echo "Carpeta de entrega lista en: $DEST"
if [ "$QUICK" -eq 1 ]; then
  echo "Modo Rápido: 00-brief-producto.md · 01-propuesta-de-valor/ · 02-bocetos/ (propuesta A) · 03-auditorias/ (auditoria-A.md) · 04-landing-final/ (landing + verificacion-de-claims.md)"
else
  echo "Modo Completo: 00-brief-producto.md · 01-propuesta-de-valor/ · 02-bocetos/ (A, B, C + bocetos.pdf) · 03-auditorias/ (A, B, C) · 04-landing-final/ · _trabajo/"
fi
