# Síntesis y trazabilidad

La fase 5 produce **UNA** landing a partir de las tres propuestas y las tres auditorías: `landing.md` (spec con trazabilidad),
`landing.html` (wireframe) y las capturas desktop y mobile. Contenido: [Elegir la base](#elegir-la-base) ·
[Estructura de la spec](#estructura-de-la-spec) · [Datos del ejemplo](#datos-del-ejemplo-una-sola-fuente-de-verdad) ·
[Tabla de trazabilidad](#tabla-de-trazabilidad-hallazgo--cambio) · [Decisiones del negocio](#decisiones-del-negocio) ·
[Largo y duplicación](#largo-y-duplicación) · [Cierre](#cierre-de-la-síntesis).

## Elegir la base

No se promedian las tres propuestas. Se **elige una base con criterio** y se injertan piezas de las otras:

- Base = la propuesta cuya estrategia coincide con el segmento líder y el nivel de conciencia de la propuesta de valor.
- Se toma de cada propuesta lo que la auditoría marcó en "Qué conservar para la síntesis".
- **Si la propuesta de valor dice que un segmento va primero** (por ejemplo, profesionales independientes antes que equipos dentro de empresas),
  el copy completo le habla a ese segmento; el secundario se atiende con una variante mínima, no con una página partida.
- Se anotan las decisiones de síntesis en un párrafo: qué se tomó de A, de B y de C y por qué, y qué se descartó.
- Todos los hallazgos de las tres auditorías se mapean uno por uno en la tabla de trazabilidad.

## Estructura de la spec (`landing.md`)

```
# Landing · <Producto> · versión de síntesis
> estado, fuentes (brief, propuesta de valor, propuestas A/B/C, auditorías), convenciones de marcas.

## 1. Estrategia                 (como en la propuesta; segmento líder y base elegida)
## 2. Datos del ejemplo          (UNA tabla de verdad + chequeos de coherencia; fuente de cada cifra)
## 3. Estructura sección por sección   (propósito, copy, componente, prueba, objeción; referencias (p. N) solo acá)
## 4. Formulario y flujo
## 5. Mobile
## 6. Eventos de medición
## 7. Trazabilidad: hallazgo -> cambio
## 7b. Hallazgos de la verificación final   (se agrega en la fase 7: filas nuevas con su estado)
## 8. Decisiones del negocio y placeholders
## 9. Qué testear (cuando haya tráfico)
## 10. Riesgos y la decisión más arriesgada
## 11. No verificado
```

## Datos del ejemplo: una sola fuente de verdad

Todas las cifras de los mocks salen de **una tabla** en la §2 de la spec; el HTML las copia de ahí, nunca al revés ni "de memoria".
La tabla tiene: cifra | valor | fuente exacta (página, línea del dato crudo, código) | cómo se obtuvo (literal, promedio, derivada).

Chequeos de coherencia (se escriben en la spec y se verifican en la ola de la fase 6, con aritmética a la vista):

1. **El total es el promedio ponderado de las partes visibles.** Si el hero muestra 10,0 y las barras 12,0 y 8,0 con el mismo peso,
   cierra; si los pesos son otros, se muestran.
2. **Una métrica descripta no contradice su fórmula.** Si la fórmula tiene un piso, un techo o un caso límite, la frase del ejemplo
   no puede ignorarlo (una descripción en palabras que implica un valor imposible según la fórmula es un error).
3. **Las mismas cifras en el hero, el recorrido y el respaldo.** Un número que cambia entre secciones destruye la credibilidad.
4. **No atribuir a una entidad una cifra que en la fuente es de otra** (ni mover un valor de una plataforma o marca a otra).
5. **Etiquetas genéricas:** "Plataforma A/B", "Marca A–D", "dominio-N.com", en vez de marcas reales con puntajes inventados. El
   texto de marketing real (qué plataformas o marcas soporta el producto) puede nombrarlas; los mocks no.
6. **Un mecanismo declarado se ve en el ejemplo** (si se promete "se rechaza y queda listado", el ejemplo lo muestra).
7. **Sello EJEMPLO dentro de cada pieza con cifras** (verificable con `scripts/check-claims.sh`: cada `.mock` contiene `.stamp`).
8. **Origen honesto de cada cifra:** distinguir "del dato crudo", "del documento de diseño" y "armada para el ejemplo". Las cifras
   armadas se rotulan como ilustrativas y la spec dice cuáles son.

Cuidado con leer cifras de imágenes: renderizar el PDF a 300 dpi y recortar, o contrastar con el dato crudo (ver `claims-verification.md`).

## Tabla de trazabilidad (hallazgo -> cambio)

Una fila por cada hallazgo de las auditorías (y, en la fase 7, por cada hallazgo de la re-auditoría y de la verificación de claims).

| # | Origen | Hallazgo | Cambio en la landing | Estado | Dónde | Motivo (si no es Aplicado) |
|---|---|---|---|---|---|---|
| 1 | Auditoría A, fix 2 | <qué fallaba> | <cambio concreto> | Aplicado | spec §3.01 · `#hero` | — |

**Estados:**
- **Aplicado:** está hecho y se puede ver en el HTML (id o sección en "Dónde").
- **Parcial:** se hizo una parte; el motivo dice qué falta y por qué.
- **Negocio:** depende de una decisión que no es del diseño; queda un `[A CONSEGUIR]` visible y la fila apunta a la decisión.
- **Descartado:** se decidió no hacerlo, con el motivo (cuesta más de lo que rinde, contradice otra decisión, la fuente no lo respalda).

Cada fila "Aplicado" tiene que poder verificarse por un tercero abriendo el HTML y las capturas; la re-auditoría de la fase 6 lo hace.

## Decisiones del negocio

Tabla en la §8 de la spec: **# | decisión | opciones reales | quién decide | dónde está el hueco | ¿bloquea la publicación?**
Entran siempre: oferta y precio, mercado e idioma, quién está detrás y la política de datos, marca blanca o marca propia en el
entregable, calendario de llamadas, aviso por email de entrega, informe de ejemplo real generado con el producto, revisión legal
de la comparación. Cada una queda como `[A CONSEGUIR: ...]` en el punto de uso del HTML, con las opciones reales. Resolverlas
inventando una respuesta es un error de proceso.

## Largo y duplicación

- Medir la altura mobile de la síntesis contra las tres propuestas (`scripts/measure-html.sh landing.html 390`). Una síntesis
  mucho más larga que la más larga de las propuestas casi siempre repite pruebas.
- Auditar la duplicación: la misma prueba en la barra de respaldo, en el hero y en el método se deja en un solo lugar.
- Cada CTA repetido es el mismo componente; ningún CTA como scroll desnudo.

## Cierre de la síntesis

1. `landing.html` pasa `scripts/check-claims.sh` (estructura limpia) y se mide a 1440 y 390.
2. Capturas con `scripts/shot.sh` y revisión visual de una captura recortada.
3. La spec dice lo mismo que el HTML en cada pieza de copy (cuando se corrige uno, se corrige el otro; ver `apply-replacements.py`).
4. Pasa a la fase 6 (re-auditoría independiente). No se entrega como "lista" antes de eso.
