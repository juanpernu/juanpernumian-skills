# Estructura de la carpeta de entrega

Se crea en el Paso 0 (carpeta que eligió la persona; por defecto `./entrega-landing/`) con `scripts/init-delivery.sh <carpeta>`.
Numerada para que se lea en el orden del proceso. Lo que no corresponde al modo elegido (Rápido) simplemente no se crea.

```
<entrega>/
  00-brief-producto.md                     Fase 0 · brief con referencias a la fuente, [inferido], huecos y datos de demostración
  01-propuesta-de-valor/                   Fase 1
    propuesta-de-valor.md                    fuente del documento
    propuesta-de-valor.html                  maquetado (partiendo de assets/report-pdf-base.html)
    propuesta-de-valor.pdf                   A4, verificado con scripts/render-pdf.sh
  02-bocetos/                              Fase 2 · bocetos de las tres propuestas (una en modo Rápido)
    bocetos.pdf                              PDF de bocetos (portada + por propuesta: resumen, vista general, desktop y mobile en tramos)
    bocetos.meta.json                        datos de la portada del PDF
    propuesta-A.md · propuesta-A.html · propuesta-A.meta.json
    propuesta-A-desktop.png · propuesta-A-mobile.png      (1440 px y 390 px, página completa)
    propuesta-B.* · propuesta-C.*            idem
  03-auditorias/                           Fase 3
    auditoria-A.md · auditoria-B.md · auditoria-C.md
  04-landing-final/                        Fases 5 a 7
    landing.md                               spec con trazabilidad (hallazgo -> cambio) y decisiones del negocio
    landing.html                             wireframe final
    landing-desktop.png · landing-mobile.png
    auditoria-final.md                       Fase 6 (i) conversión + verificación de cada fila de trazabilidad
    verificacion-de-claims.md                Fase 6 (ii) claims contra las fuentes primarias
  _trabajo/                                Ola de validación, lista de cambios y scripts de reemplazo (no se entrega, se conserva)
    validacion-fase-<n>.md                   informe único de la ola de validación (problemas encontrados antes de arreglar)
    cambios-finales.md                       lista exacta de cambios de la fase 7
    reemplazos-*.json                        entradas de apply-replacements.py
```

## Qué es cada archivo

| Archivo | Quién lo escribe | Se verifica con |
|---|---|---|
| `00-brief-producto.md` | orquestador (o agente con la fuente completa) | chequeo del brief (`brief-template.md`) |
| `propuesta-de-valor.*` | orquestador o agente de la Fase 1 | `render-pdf.sh` (páginas, líneas, desbordes) |
| `propuesta-X.md/.html/.meta.json` | agente de la propuesta X | `check-claims.sh`, `measure-html.sh`, capturas |
| `propuesta-X-desktop/mobile.png` | orquestador (`shot.sh`) | mirar un recorte; desborde horizontal |
| `bocetos.pdf` | orquestador (`build-bocetos-pdf.sh`) | páginas esperadas, tamaño, vista de una página |
| `auditoria-X.md` | agente de auditoría X | lectura completa por el orquestador |
| `landing.md` / `landing.html` | orquestador (+ agente de wireframe) | `check-claims.sh`, coherencia de datos del ejemplo |
| `auditoria-final.md` | agente (i) | la tabla de trazabilidad verificada fila por fila |
| `verificacion-de-claims.md` | agente (ii) | los hechos graves los verifica el orquestador |

## Convenciones

- Nombres en minúscula, sin espacios; capturas con el sufijo `-desktop.png` y `-mobile.png`.
- El html y el md de cada pieza dicen lo mismo; si se corrige uno, el mismo día se corrige el otro (y se regenera el PDF y las capturas).
- Cada pieza lleva fecha y estado ("propuesta de proceso, superada por 04-landing-final/landing.md") en su cabecera cuando queda archivada.
- Las propuestas A/B/C quedan archivadas: no se editan después de la síntesis salvo el copy que depende de una corrección de hechos
  (y entonces se deja la nota de estado).

## Checklist de la entrega final

- [ ] Carpeta con la estructura de arriba; nada suelto en la raíz salvo `00-brief-producto.md`.
- [ ] `propuesta-de-valor.pdf` verificado (páginas, sin páginas casi vacías ni desbordes) y `bocetos.pdf` verificado (páginas esperadas).
- [ ] Capturas regeneradas DESPUÉS de la última edición del html (comparar fechas de modificación).
- [ ] `landing.md` y `landing.html` dicen lo mismo; tabla de trazabilidad con estados y motivos; decisiones del negocio como huecos visibles.
- [ ] `auditoria-final.md` y `verificacion-de-claims.md` presentes y sus hallazgos graves resueltos o anotados en la §7b.
- [ ] Resumen final honesto: qué es dato real y qué demostración, qué no se pudo verificar, qué decisiones esperan a la persona.
