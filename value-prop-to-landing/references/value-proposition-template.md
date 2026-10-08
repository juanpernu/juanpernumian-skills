# Propuesta de valor · plantilla JTBD de 6 partes

Se arma a partir del brief (nunca de memoria ni de lo que "suena bien"). Un segmento por pasada: el segmento líder va completo
y el secundario en versión corta. Entrega en tres formatos: `propuesta-de-valor.md` (fuente), `propuesta-de-valor.html`
(maquetado con `assets/report-pdf-base.html`) y `propuesta-de-valor.pdf` (`scripts/render-pdf.sh`).

## Estructura del documento

1. **Portada** (A4, a página completa): producto, "Propuesta de valor", una línea que dice qué hace, las 6 partes como etiquetas,
   fuente de la verdad, segmento principal, estado ("borrador para validar").
2. **En una página:** statement + cuatro tarjetas (quién, problema, cómo, resultado) y la nota de datos de demostración.
3. **Segmento principal · las 6 partes** (cada una con su cabecera numerada y sus fuentes):
4. **Statements para marketing:** statement (1 a 2 frases) y posicionamiento.
5. **Segmento secundario** (versión corta de las 6 partes).
6. **Mensajes clave y su prueba:** de 4 a 6, cada uno con su evidencia, su fuente y su estado.
7. **Supuestos a validar:** qué se da por cierto, cómo se valida y qué pasa si es falso.

## Las 6 partes (qué responde cada una y qué errores evitar)

| # | Parte | Responde | Errores comunes |
|---|---|---|---|
| 1 | **Quién** | Para quién es, con sus características y restricciones. Quién compra y quién usa, si son distintos. | Describir demografía en vez de situación; mezclar dos segmentos. |
| 2 | **Por qué** | El problema o trabajo a resolver (JTBD): "Cuando [situación], quiero [motivación] para poder [resultado]". Los dolores con su consecuencia. | Escribir el feature como si fuera el problema. |
| 3 | **Qué hacen hoy** | La situación actual: qué usan, dónde duele cada alternativa actual (incluida "no hacer nada"). | Inventar un "antes" que la fuente no respalda. |
| 4 | **Cómo lo resuelve** | El mecanismo, en lenguaje de cliente: capacidades, qué resuelve cada una y su **estado** (descripta, diseñada, construida, probada). | Prometer lo que solo está descripto en un documento. |
| 5 | **Qué pasa después** | El estado futuro: qué cambia y qué se vuelve posible. Sin cifras de mejora salvo que existan y estén en la fuente. | Porcentajes, plazos exactos o resultados no medidos. |
| 6 | **Alternativas** | Qué otras soluciones hay, dónde gana cada una hoy y dónde gana el producto, y el costo de cambiarse. | Nombrar marcas o generalizar a una categoría entera a partir de un solo producto. |

## Statement y posicionamiento

- **Statement:** "Para [quién] que necesita [trabajo a resolver], [Producto] es [categoría] que [beneficio principal]. A diferencia
  de [alternativa principal], [diferencial verificable]." Sin cifras inventadas; el diferencial tiene que tener prueba en el brief.
- **Posicionamiento:** la misma idea en una frase que se pueda pegar en un titular, y la lista de palabras que el producto SÍ puede
  decir y las que NO (límites del brief §12).

## Mensajes clave

Tabla de 4 a 6 filas: **mensaje | prueba concreta | fuente | estado** (respaldada / con matiz / solo inferida / a conseguir).
Un mensaje sin prueba no se descarta: se marca como inferido o a conseguir, y la landing lo trata como tal.

## Supuestos a validar

Siempre incluir, con su método de validación y el riesgo si es falso: el segmento líder correcto, el problema que más duele,
el plazo prometido (medirlo en producción antes de publicarlo), la oferta de entrada, y cualquier decisión que no es del diseño
(precio, mercado e idioma). Un supuesto a validar es una conversación con clientes reales, no una opinión del equipo.

## Reglas de la entrega

- Etiquetas de fuente `<span class="src">p. N</span>` en cada afirmación; `<span class="inf">inferido</span>` en cada deducción.
- Cada dato de demostración rotulado como ejemplo dentro de la pieza donde aparece.
- PDF: A4, portada a página completa y secciones que empiezan en página nueva. Verificar con `scripts/render-pdf.sh`
  (páginas, líneas por página, páginas casi vacías, desbordes) y comparar con la versión anterior con `--prev`.
- Si se corrige una afirmación en el md, se corrige en el html y se regenera el PDF en la misma pasada
  (usar `scripts/apply-replacements.py` para que los tres digan lo mismo).

## Complemento opcional

Si está instalado el skill `value-proposition`, puede consultarse como segunda mirada de la plantilla. Este skill no depende de él.
