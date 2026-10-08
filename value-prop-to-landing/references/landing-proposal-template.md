# Propuesta de landing · plantilla (md + wireframe HTML + capturas)

Cada propuesta es un par de archivos que dicen lo mismo: `propuesta-<id>.md` (estrategia + estructura sección por sección) y
`propuesta-<id>.html` (wireframe en escala de grises, partiendo de `assets/wireframe-base.html`), más
`propuesta-<id>.meta.json` (lo que lee el PDF de bocetos) y las capturas `propuesta-<id>-desktop.png` y `-mobile.png`
(las genera el orquestador con `scripts/shot.sh`, no el agente).

## Los tres ángulos (tienen que ser realmente distintos, no variaciones de titular)

| Id | Ángulo | Idea | Cuándo gana | Estructura que lo expresa |
|---|---|---|---|---|
| **A** | **Dolor primero (PAS)** | Problema, agitación, solución. Abre con la situación que el visitante reconoce y recién después muestra el producto. | El visitante siente el problema pero no conoce la solución. | Hero de dolor, problema, agravantes, solución, prueba, CTA. |
| **B** | **El entregable o la demo es el producto** | La página es un recorrido por lo que se recibe, parada por parada, con mocks sellados "EJEMPLO". | El comprador compara alternativas y quiere ver el resultado antes de leer cómo se hace. | Hero con tarjeta de resultado, recorrido en paradas, método corto, qué incluye. |
| **C** | **Método y credibilidad** | Para el comprador que tiene que defender el resultado ante un tercero (cliente, jefe, comité): cómo se construye el número y por qué aguanta preguntas. | Hay escepticismo y alguien más va a cuestionar el resultado. | Hero con la idea de "defendible", método en tarjetas con "lo que le decís a tu cliente", comparación honesta, límites de frente. |

Cada agente recibe SOLO su ángulo y no ve las otras propuestas (así no se contaminan). Si el producto no encaja con alguno de
los tres, el orquestador puede reemplazarlo por otro ángulo igual de distinto, y lo deja dicho en el informe.

## `propuesta-<id>.md` · estructura obligatoria

```
# Landing · Propuesta <id> · "<nombre del ángulo>"

> Ángulo en una línea. Fuentes: brief y propuesta de valor. (ref. p. N) = fuente. [inferido] = sin respaldo. [A CONSEGUIR] = hueco.
> Las referencias van solo en este documento, no en el wireframe.

## 1. Estrategia
tabla: Audiencia foco · Audiencia secundaria · Nivel de conciencia (Schwartz) y sofisticación de mercado · Big idea ·
Promesa · Objetivo de conversión · CTA primario · CTA secundario · Fuente de tráfico supuesta · KPI principal y de calidad
+ "Por qué el CTA primario es ese y no otro" (3 a 4 razones y el riesgo a monitorear)

## 2. Estructura sección por sección
Para cada sección (00 Nav, 01 Hero, ...):
- Propósito
- Copy (titulares, subtítulos, microcopy, textos de botón; el copy real, no "texto aquí")
- Componente (qué se ve: tarjeta, mock, tabla, acordeón)
- Prueba (qué respalda lo que dice la sección y de dónde sale)
- Objeción que responde

## 3. Mobile        (qué cambia: orden, barra fija, tabla apilada, tipografía mínima, gutter)
## 4. Formulario    (campos exactos, tipo, obligatorio, placeholder, error en línea, mensaje posterior, campos ocultos, qué NO se pide y por qué)
## 5. Eventos de medición  (pocos: evento | cuándo | parámetros | para qué; una clave que cruce landing -> login -> app)
## 6. Por qué esta estructura convierte  (reglas de landing-design-rules.md aplicadas, una por una)
## 7. Desvíos deliberados  (reglas que se rompen a propósito y por qué)
## 8. Placeholders consolidados  ([A CONSEGUIR] con las opciones reales de cada decisión)
## 9. Riesgos y la decisión más arriesgada  (qué se apuesta, qué puede salir mal, cómo medirlo)
```

### Estrategia: cómo completar cada fila

- **Nivel de conciencia (Schwartz):** inconsciente, consciente del problema, de la solución, del producto o totalmente consciente.
  Decide el titular: cuanto menos consciente, más se abre con el problema y menos con el producto. Con mercado saturado
  (la promesa genérica ya circula) se gana con el mecanismo, no con repetir la promesa.
- **Fuente de tráfico supuesta:** sin URL ni anuncio real, se **supone** una fuente (contenido orgánico, mensajes directos,
  comunidades, búsqueda, anuncio pago) y se marca [inferido]. Es la base del chequeo de "message match" en la auditoría.
- **CTA:** un solo primario en toda la página; el secundario es un enlace de texto. Con oferta sin definir, el texto es
  neutro ("Dejá tus datos", "Quiero que me contacten"): nada de "pedir", "primera" ni "gratis".
- **KPI:** uno principal (tasa de envío del formulario) y uno de calidad (lo que pasa después del formulario: entrevista,
  activación, entrega). Un clic no es una decisión.

### Formulario

- Los campos mínimos que el producto necesita para arrancar (a veces un dominio, a veces un email); no pedir nada que se pueda
  obtener después. Validación en línea al salir del campo. Mensaje posterior que dice qué pasa y cuándo, con la espera real.
- Si hay un paso manual entre el formulario y el producto, decirlo: es la mayor fuga oculta.
- Campos ocultos para atribución (utm y ubicación del CTA) no cuentan como fricción.

### Eventos de medición (pocos)

Quedarse con: vista de página + atribución, clic en CTA primario por ubicación, inicio y envío del formulario (el envío contado
también del lado del servidor), y los eventos posteriores al formulario (acceso, entrevista o activación, entrega).
Una **clave que cruce** landing -> login -> app (por ejemplo un identificador en el `state` del login con OAuth) y una
**métrica de decisión que no sea el clic** (por ejemplo, formularios que llegan a la activación dentro de 7 días).
Muchos tipos de evento x muchas ubicaciones no separan señal de ruido con poco tráfico.

## `propuesta-<id>.meta.json` (lo lee `scripts/build-bocetos-pdf.sh`)

```json
{
  "id": "A",
  "nombre": "Dolor primero",
  "angulo": "Una o dos frases: qué ángulo es.",
  "big_idea": "La idea central.",
  "audiencia": "A quién le habla.",
  "conciencia": "Nivel de Schwartz.",
  "trafico": "Fuente de tráfico supuesta.",
  "cta_primario": "Texto del botón y componente.",
  "cta_secundario": "Texto del enlace.",
  "secciones": [{"n": "01", "nombre": "Hero", "proposito": "Qué hace esta sección."}],
  "decision_riesgosa": "La apuesta más arriesgada de esta propuesta.",
  "placeholders": ["Hueco 1", "Hueco 2"]
}
```

## `propuesta-<id>.html` · reglas del wireframe

- Partir de `assets/wireframe-base.html` y adaptar; un solo archivo, CSS y JS inline, **sin recursos externos**, escala de grises.
- Mocks hechos con HTML/CSS (no imágenes). Cada mock con cifras lleva su sello "EJEMPLO · cifras ilustrativas" **adentro**.
- Un solo `<h1>`; FAQ con todas las preguntas cerradas; ningún enlace a un destino que no existe.
- El copy del wireframe es el copy del md, palabra por palabra.
- Datos de ejemplo salidos de UNA tabla de verdad (ver `synthesis-and-traceability.md`) y con etiquetas genéricas.
- Mobile real a 390 px: sin scroll horizontal, tabla de comparación apilada, barra fija con la lógica del wireframe base.

## Cómo termina cada agente de propuesta

Escribe los 3 archivos (md, html y meta.json; las capturas las saca el orquestador) y responde en menos de 200 palabras: archivos,
tres decisiones propias que conviene revisar y dudas abiertas.
