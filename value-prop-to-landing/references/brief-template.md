# Brief de producto (plantilla)

El brief es la única puerta entre la fuente de la verdad y todo lo demás. Cada propuesta, auditoría y verificación se apoya
en él, así que un error acá se multiplica. Archivo: `00-brief-producto.md`. Lo escribe el orquestador (o un agente con la
fuente completa) y lo confirma la persona antes de la Fase 1.

## Reglas de escritura

- **Referencias a la fuente.** Cada afirmación lleva `(p. N)`, `(§ X)` o `(URL corta)`. Con más de una fuente, la etiqueta
  nombra la fuente: `(Doc. B p. 4)`. Con cuestionario: `(cuestionario P#)`.
- **[inferido]** es toda interpretación que ninguna fuente dice. No se esconde ni se suaviza.
- **[A CONSEGUIR]** es un hueco: un dato o una decisión que la landing necesita y no existe.
- **Descripto no es construido.** Para cada capacidad, anotar el estado: *descripta en el documento*, *diseñada*,
  *construida*, *probada*, *en producción*. La landing solo habla en presente de lo que está probado o confirmado. Si el
  producto existe, leer el código y los tests (constantes, fórmulas, límites) y citarlos.
- **Decisiones posteriores.** Buscar lo que supera a la fuente (changelog, lista de tareas, README, issues, código, `git log`)
  y anotarlo arriba del brief: "donde el documento dice X, prevalece Y (fecha, dónde está)". Todo lo que dependa de la
  decisión superada se corrige en los derivados.
- **Datos de demostración.** Si la fuente trae cifras de una marca de ejemplo, el brief las lista aparte y dice que NO son
  resultados de clientes. Cifras de imágenes o miniaturas de PDF: leerlas a resolución completa (ver `claims-verification.md`).
- Lenguaje de cliente en las capacidades; vocabulario propio en una sección aparte con su glosa.

## Estructura

```
# Brief de producto · <Producto>

> Fuente de la verdad: <documento / sitio / repo / cuestionario>, fecha. Qué parte es definitiva y qué parte es borrador.
> Referencias (p. N) = <fuente>. [inferido] = interpretación sin respaldo directo. [A CONSEGUIR] = hueco.
> Actualización <fecha>: <decisiones que superan a la fuente, con dónde están>.

**Advertencia para quien diseñe la landing:** <qué datos son de demostración y que no son resultados de clientes>.

## 1. Qué es                      (una definición en 2-3 líneas + categoría)
## 2. Para quién                  (segmento líder, variante, comprador vs. usuario)
## 3. Problema y dolores          (trabajo a resolver; dolores con su consecuencia)
## 4. Qué hace                    (capacidades en lenguaje de cliente, con estado: descripta / diseñada / construida / probada)
## 5. Qué entrega                 (salidas, pantallas, informes, tiempos; qué se ve y qué se recibe)
## 6. Diferenciales verificables  (tabla: diferencial | prueba concreta | fuente)
## 7. Alternativas del cliente    (qué usa hoy, dónde falla, dónde gana cada una)
## 8. Pruebas disponibles         (solo lo que está en la fuente)
   8.1 Pruebas de método y de ingeniería
   8.2 Datos operativos (diseño, no resultados)
   8.3 Costos internos (insumo para precio, NO para la landing)
   8.4 Datos de ejemplo o demostración (ilustrativos, marca demo)
## 9. Vocabulario propio          (término | glosa en una línea | dónde se usa)
## 10. Huecos                     (lo que la landing necesita y la fuente no dice)
   Comerciales · Prueba social y resultados · Producto y promesa · Marca y legales
## 11. Decisiones que superan a la fuente
## 12. Límites declarados         (qué NO se puede prometer; riesgos de copy)
```

## Qué suele aparecer en "Huecos" (revisar uno por uno)

- **Comerciales:** precio, oferta de entrada (qué es gratis), cobro y moneda, oferta para el segmento líder (volumen, marca blanca).
- **Prueba social y resultados:** testimonios, logos, casos, métricas de resultado; el primer hito de prueba que dice la fuente.
- **Producto y promesa:** tiempos de entrega (¿medidos o de diseño?), avisos y notificaciones, forma de acceso (login),
  mercados e idiomas disponibles, límites técnicos declarados (la medición puede no reflejar lo que ve el usuario), alcance
  real de las comparaciones, diferencias entre el set de ejemplo y el que entrega el producto.
- **Marca y legales:** nombre y arquitectura de marca, dominio definitivo, política de datos y privacidad, términos, quién
  está detrás (equipo, empresa), permisos para nombrar terceros.

## Chequeo antes de entregar el brief

- [ ] Toda cifra está en la fuente a resolución completa o contra el dato crudo (no copiada de una miniatura).
- [ ] Ningún "descripto" quedó escrito como "construido".
- [ ] Las decisiones posteriores a la fuente están arriba y marcadas donde corresponde.
- [ ] Los datos de demostración están separados y rotulados como tales.
- [ ] Cada hueco tiene su opción real (qué se puede decidir), no una invención.
