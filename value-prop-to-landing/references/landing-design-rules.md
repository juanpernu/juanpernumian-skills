# Reglas de diseño de landing (en palabras propias)

Reglas de conversión para armar y juzgar una landing, con las reglas de honestidad que este proceso agrega. Sirven tanto para
escribir las propuestas como para la síntesis y la auditoría. Contenido:
[Above the fold](#above-the-fold) · [Titulares](#titulares) · [CTA](#cta) · [Orden de secciones](#orden-de-secciones) ·
[Prueba social](#prueba-social-cuando-no-hay) · [Formularios](#formularios) · [Mobile](#mobile) · [Velocidad](#velocidad) ·
[Reglas de honestidad](#reglas-de-honestidad-de-este-proceso) · [Errores comunes](#errores-comunes)

## Above the fold

Lo que se ve sin scrollear tiene que comunicar el valor en cinco segundos. Cinco elementos, en este orden de importancia:

1. **Titular de 6 a 12 palabras que dice el resultado**, no la categoría ni el nombre de la tecnología.
2. **Subtítulo de 15 a 25 palabras que explica el cómo** (el mecanismo), sin adjetivos vacíos.
3. **Un visual que muestra el resultado** (una tarjeta de ejemplo, un fragmento del entregable), no un adorno ni una captura
   ilegible de toda la interfaz. Si el producto es el entregable, el visual es una pieza real del entregable, sellada como ejemplo.
4. **CTA primario** con verbo de acción + valor, visible sin scroll en 390 x 844.
5. **Prueba o su hueco visible.** Sin clientes ni métricas, la prueba disponible es el método; el hueco de logos queda marcado.

## Titulares

Fórmulas útiles: "[Resultado] sin [dolor]" · "[Resultado] en [plazo]" (solo con plazo medido) · "Dejá de [dolor], empezá a
[resultado]" · "El [camino mejor] para [tarea común]" · titulares de contraste ("no te van a preguntar cuánto dio, te van a
preguntar de dónde sale").
Fallan: los que no dicen nada ("Bienvenido a nuestra plataforma"), los de buzzwords ("solución de nueva generación impulsada por
IA"), los vagos ("ayudamos a crecer") y los que prometen lo que el visitante no controla.

## CTA

- **Texto:** verbo de acción + valor + reductor de riesgo opcional. Nunca "Enviar" ni "Más información".
- **Oferta sin definir:** texto neutro. Prohibido "pedir", "primera" y "gratis" hasta que la oferta exista, porque cada una
  promete algo concreto.
- **Diseño:** el elemento de mayor contraste de la página, alto mínimo de 48 px, aire alrededor, un solo primario; el
  secundario es un enlace de texto.
- **Un CTA no puede ser un scroll desnudo de miles de píxeles:** repetir el mismo componente (campo + botón) cerca, o llevar al
  formulario más cercano y poner el foco en el campo.
- **Barra fija mobile:** aparece solo cuando el formulario del hero salió de pantalla y se oculta cuando CUALQUIER formulario
  está a la vista. El botón del header se oculta mientras la barra está activa.
- **No enlazar a destinos que no existen.** Un "ver informe de ejemplo" que apunta a la misma sección engaña: usar un ancla al
  recorrido dentro de la página hasta que el destino exista.

## Orden de secciones

Secuencia probada: hero -> prueba -> problema -> solución o recorrido -> método -> cómo funciona -> comparación -> qué incluye /
precio -> preguntas -> cierre con formulario. Se ajusta con razón, no por gusto:

- Sin testimonios, la franja de prueba se reduce al hueco y no se publica hasta que haya algo real.
- El precio vive donde tenga sentido (por ejemplo junto a "qué incluye"); si no existe, es un hueco con sus opciones.
- Antes de la comparación va la solución: el comprador compara contra lo que ya usa.
- **Longitud:** auditar la duplicación (la misma prueba repetida en barra de respaldo, hero y método), medir la altura mobile
  contra las otras propuestas con `scripts/measure-html.sh` y cortar lo que repite.

## Prueba social (cuando no hay)

Sin logos ni testimonios reales, usar lo más cercano que sea verdadero: datos de un entregable de demostración **rotulados**,
el método declarado y los límites dichos de frente. Inventar clientes, citas o métricas está prohibido. El hueco queda visible
con la meta real (por ejemplo "las primeras N marcas reales con entregable") y la franja no se publica hasta tenerlos.

## Formularios

Cada campo extra cuesta conversión: pedir solo lo que el producto necesita para arrancar ahora, una columna, validación en
línea al salir del campo, errores en lenguaje claro ("Revisá el email: falta la @"), botón con la acción, mensaje posterior que
dice qué pasa y cuándo. Si hay un paso manual o un login entre el formulario y el producto, decirlo antes del clic. Los
campos ocultos de atribución no cuentan como fricción.

## Mobile

CTA a ancho completo, barra fija, sin scroll horizontal, cuerpo y campos de 16 px como mínimo (si no, iOS hace zoom), áreas de
toque de 48 x 48 px, tablas que se apilan en una tarjeta por criterio (las celdas "no aplica" no se muestran apiladas), titular y
CTA primero, gutter de 16 px, FAQ como acordeón nativo con toda la fila clickeable. Probar a 390 px reales.

## Velocidad

Visual del hero hecho con HTML/CSS (el LCP es el titular), peso total < 2 MB, JS mínimo, nada que bloquee el render, imágenes
diferidas debajo del pliegue.

## Reglas de honestidad de este proceso

1. **Dato real o demostración, siempre declarado.** El sello "EJEMPLO · cifras ilustrativas" va DENTRO de cada pieza con cifras
   (en el encabezado del marco), no en una nota al pie.
2. **Una mecánica prometida debe verse en el ejemplo** (si se dice "se rechaza y queda listado", el ejemplo lo muestra, o no se
   apoya en eso).
3. **Afirmar solo lo que cubre la fuente:** "una muestra auditada" no es "cada elemento auditado"; "algunas herramientas" no es
   "la categoría"; plazos y áreas son ejemplos, no listas cerradas; cuidado con los absolutos ("nunca", "no hay forma").
4. **Diseño no es producción:** no prometer lo que no está confirmado (volver a medir, exportar, integrar, SLA). "En horas" y
   no un número de horas hasta medir; contar el tiempo desde el hito correcto.
5. **Decisiones que no son del diseño** (oferta y precio, mercado e idioma, quién está detrás, marca blanca, calendario, avisos por
   email, informe de ejemplo real) quedan como `[A CONSEGUIR]` visibles y pegadas al punto de uso, con las opciones verdaderas.
6. **Comparaciones:** no nombrar marcas ni generalizar a una categoría entera a partir de un solo producto; los contrastes van en
   la celda propia; dejar "dónde gana cada alternativa"; revisión legal si se nombra a alguien.
7. **FAQ cerradas por defecto.** Una abierta sesga la medición de objeciones.
8. **Versión limpia para pruebas de 5 segundos** (sin banner ni etiquetas de wireframe; los sellos y los huecos se quedan). Con
   poco tráfico no hay A/B que separe señal de ruido (~1.000 sesiones y ~30 conversiones por variante).

## Errores comunes

| Error | Por qué falla | Arreglo |
|---|---|---|
| Titular que no dice el resultado | El visitante no sabe qué hacés | 6 a 12 palabras, orientado al resultado |
| "Más información" como CTA | Compromiso bajo, sin valor | Verbo + valor |
| Visual que es una captura de la interfaz | Difícil de leer de un vistazo | Una pieza del entregable, sellada |
| Varios CTA que compiten | Parálisis | Un primario, un secundario de texto |
| Prueba social inventada | Se nota y destruye la confianza | Hueco visible o método declarado |
| Formulario largo | Cada campo cuesta conversión | Solo lo necesario ahora |
| Promesa de plazo sin medición | Se rompe en el primer cliente | "En horas" hasta medir |
| Diseñar solo desktop | La mayoría del tráfico es mobile | Mobile primero, probar a 390 px |
