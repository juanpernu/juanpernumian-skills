# Auditoría de conversión · pre-lanzamiento

Una auditoría por propuesta (fase 3) y una re-auditoría de la landing de síntesis (fase 6). Archivo: `auditoria-<id>.md` y
`auditoria-final.md`. Es una auditoría de **wireframe sin lanzar**: no hay URL, tráfico, anuncio ni analítica. Eso cambia qué
se puede concluir y lo primero que el informe tiene que decir.

## Qué cambia en pre-lanzamiento

- No hay datos de sesiones ni de conversión: **todo el ranking es por fricción de primeros principios**. Nunca prometer un
  porcentaje de mejora ("expected direction", orden relativo). Las cifras de casos publicados no se transfieren.
- La **fuente de tráfico es supuesta** (la dice la propuesta y está marcada [inferido]). El "message match" se chequea contra esa
  fuente supuesta y el informe lo aclara.
- Con menos de ~1.000 sesiones y ~30 conversiones por variante, ningún A/B separa señal de ruido: las comparaciones se hacen
  por tanda de envío o por canal y se juzgan por una métrica de decisión que no sea el clic.
- Si el problema es upstream (oferta, mercado, precio), la auditoría lo dice y no lo disfraza de problema de copy: una página
  no arregla una oferta rota.
- Se audita el **md y el html juntos** (el html a 1440 y a 390 px reales, con las capturas a la vista) y se compara lo que dicen.

## Formato fijo del informe

```
# Auditoría de conversión · <Propuesta> · <fecha> · wireframe pre-lanzamiento: sin URL, tráfico, anuncio ni analítica

## Verdict
Un párrafo: ¿el problema es la página o está upstream? Qué hecho de negocio sin definir condiciona el CTA. Qué se asumió
(fuente de tráfico) y que todo el ranking es por primeros principios.

## Fix now (ordered by expected impact)
1. <elemento + dónde (archivo:línea o id)> - <modo de falla> → <cambio concreto> | effort: S/M/L | confidence: high/med/low
   - sub-puntos con la evidencia (qué vio, en qué viewport) y el cambio exacto de copy o de componente
2. ...
(máximo 7; una lista de 30 no se implementa)

## Test, don't guess
Cambios que merecen una prueba y no un reemplazo directo, con la métrica de decisión y cómo se corre con poco tráfico.

## Not a problem
Lo que se revisó y está bien (para que nadie lo vuelva a arreglar).

## Could not check
Lo que no se pudo verificar (tráfico real, velocidad, producto real, destinos que no existen) y qué significa para los hallazgos.

## Qué conservar para la síntesis
Lo mejor de esta propuesta (componentes, frases, estructura) que la landing única debería heredar.
```

Cada ítem de *Fix now* nombra **el elemento, el modo de falla y el cambio**: no vale "agregar más prueba social".
En la re-auditoría se suma, antes de *Fix now*, una sección **Verificación de trazabilidad** (ver más abajo).

## Checks A a G (en este orden: por impacto, no por facilidad)

**A. Message match (fuente supuesta -> página)**
- ¿El titular repite la promesa de la fuente supuesta con sus palabras? Una discordancia acá limita todo lo demás.
- ¿La página entrega lo específico que prometería esa fuente, o una versión general?
- ¿La oferta se ve sin scrollear en 390 x 844?

**B. Above the fold mobile**
- Una promesa, un CTA. Contar los CTA que compiten (más de un primario es una fuga).
- ¿El CTA entra en la primera pantalla o queda debajo de una tarjeta o imagen?
- ¿Algo significativo se pinta antes de ~2,5 s? (en un wireframe: peso, tipografías, nada bloqueante).

**C. Claridad de la oferta**
- Un extraño, en cinco segundos: ¿qué es, para quién, cuánto cuesta, qué pasa si hago clic?
- ¿Precio presente u oculto? Ocultarlo solo es correcto en compras de alto valor con llamada. Si no existe, que sea un hueco
  visible con las opciones reales, no una invención.
- ¿Reducción de riesgo real (prueba, cancelación, garantía) o ninguna? No inventar una.

**D. Fricción del formulario**
- Contar los campos; cada uno extra cuesta. ¿Es necesario ahora o se puede pedir después?
- ¿Validación en línea y errores claros? ¿Se entiende con qué cuenta o dato se va a entrar (login)?
- ¿Hay un paso manual entre el formulario y el producto? Es la fuga oculta más grande: pedir un plazo que el equipo pueda cumplir.

**E. Confianza en el momento del clic**
- Elementos de confianza **al lado del botón** y no en el pie: qué se hace con el dato, quién está detrás, política de datos.
- ¿Los testimonios o logos son específicos y atribuibles, o relleno anónimo? Sin pruebas reales: hueco visible, nunca inventado.

**F. El camino después del botón**
- ¿Qué pasa tras el envío, con qué plazo y por qué canal? ¿Hay un aviso (email, dentro de la app) o el visitante cierra la pestaña esperando
  algo que no llega? ¿Los plazos corren desde el hito correcto?
- ¿El vocabulario del producto está glosado donde aparece?

**G. Medición**
- ¿Hay una clave que cruce landing -> login -> app? ¿Eventos posteriores al formulario (acceso, activación, entrega)?
- ¿La métrica de decisión es algo que no sea el clic? ¿El envío del formulario se cuenta también del lado del servidor
  (bloqueadores)? ¿Pocos eventos (los que separan señal de ruido con poco tráfico)?
- ¿Algún evento queda sesgado por el diseño (preselecciones, una FAQ abierta, clics absolutos con una barra fija siempre visible)?

**H. Chequeos de honestidad (se hacen siempre)**
- ¿Cada afirmación de producto está en el brief con su fuente, y está escrita en el tiempo verbal que corresponde a su estado
  (descripta vs. probada)? ¿Hay absolutos o generalizaciones que la fuente no cubre?
- ¿Cada pieza con cifras tiene el sello EJEMPLO adentro? ¿Las cifras de hero, recorrido y respaldo son las mismas y
  coherentes con su fórmula? ¿Hay marcas reales con puntajes inventados?
- ¿Algún enlace o CTA apunta a un destino que no existe? ¿Algún mecanismo prometido que el ejemplo no muestra?
- ¿Las decisiones que no son del diseño están como `[A CONSEGUIR]` pegadas al punto de uso, con sus opciones?
- ¿Las capturas PNG están actualizadas respecto del md y el html? (una captura vieja puede seguir mostrando un claim corregido)
- ¿La comparación nombra marcas o generaliza a una categoría? ¿Dice dónde gana cada alternativa?

## Re-auditoría de la síntesis: verificación de trazabilidad

Además de los checks, el agente abre la tabla de trazabilidad de la spec (ver `synthesis-and-traceability.md`) y, **fila por fila**,
verifica contra el HTML y las capturas que el cambio dicho está hecho: veredicto por fila **verificada / parcial / falsa** con la
evidencia (id, línea, viewport). Cierra con un resumen ("N de M verificadas, X parciales, Y falsas"). Una fila "Aplicado" que
el HTML no refleja es el hallazgo más grave de esta pasada.

## Reglas del informe

- Nunca un porcentaje de mejora; "dirección esperada" y orden relativo.
- Máximo 7 en *Fix now*; lo demás va a *Test* o se descarta con motivo.
- Citar siempre dónde (archivo y línea, o id del elemento, y el viewport).
- No arreglar nada: la auditoría escribe solo su informe.

## Complemento opcional

Si está instalado el skill `landing-page-conversion-audit`, puede usarse como segunda lista de verificación. Este skill no depende de él.
