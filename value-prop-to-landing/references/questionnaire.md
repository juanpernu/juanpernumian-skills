# Cuestionario breve (solo si NO hay fuente de la verdad)

Se usa cuando, en el Paso 0, la persona confirmó que no tiene ninguna fuente (ni documentos, ni URL, ni repo, ni notas, ni
brief). Si tiene aunque sea una fuente parcial, se lee esa fuente y este cuestionario se reduce a las preguntas que
queden sin responder. Sirve para armar un brief limpio sin inventar nada.

## Reglas

- Herramienta: `AskUserQuestion`. **Una o dos rondas de máximo 4 preguntas** (8 preguntas en total, que cubren los 10 temas
  porque "producto + problema" y "mercado + idioma + tono" van juntos). Con la persona que ya contestó algo, no se repite.
- Cada pregunta lleva 2 a 4 opciones. La primera es el **default razonable** y termina en "(Recomendado)". La herramienta
  agrega "Otro" (texto libre) por sí sola: ahí la persona cuenta los detalles. Usar `multiSelect` donde se indica.
- Las opciones nombran categorías, no contenido: lo específico del producto lo pone la persona en "Otro". Si eligió solo una
  categoría y falta lo esencial (qué hace el producto), hacer **una** pregunta de seguimiento en el chat, no más.
- Qué se hace con las respuestas:
  - lo que dijo la persona entra al brief sin marca;
  - lo que se tomó del default o se dedujo de otra respuesta se marca **[inferido]**;
  - lo que no existe o no se sabe se marca **[A CONSEGUIR]** (pruebas, precio, equipo, políticas);
  - **nunca** se inventan métricas, clientes, logos ni testimonios. Una pregunta sin respuesta es un hueco, no un dato.
- Al terminar, devolver un resumen de 8 a 10 líneas del brief (con las marcas) y pedir confirmación antes de la Fase 1.
- La pregunta de modo y carpeta de entrega (Paso 0.3, puntos 2 y 3, de `SKILL.md`) NO cuenta dentro de este presupuesto.
- **Qué cuenta como "lo que dijo la persona":** toda opción que la persona eligió activamente (aunque sea la recomendada) y todo texto de
  «Otro» entra al brief sin marca. El **default** solo se usa cuando la persona saltea la pregunta, contesta "no sé" o falta el detalle:
  ahí se aplica y se marca **[inferido]**. En las preguntas `multiSelect` el default es lo que se asume si no marcó nada.
- Exclusividad: la herramienta no puede forzarla. Si marca "Ninguna todavía" (P5) junto con otras opciones, preguntá en el chat cuál
  vale. Si no se necesitan las 8 (la persona ya contó parte en su pedido), saltear esas y hacer una sola ronda si alcanza con 4 o menos.

## Ronda 1 · Qué es y para quién (4 preguntas)

**P1 · Producto y problema** (`header`: "Producto", `multiSelect`: false)
> ¿Qué es tu producto y qué problema resuelve? Elegí el tipo y, en «Otro», contá en 1 o 2 líneas qué hace y qué problema
> resuelve (si no, te lo pregunto en el chat).
- Software o app (Recomendado) · Herramienta que automatiza, mide o gestiona algo
- Servicio o consultoría · Trabajo profesional a medida o por paquete
- Producto físico · Algo que se compra y se recibe
- Contenido, curso o comunidad · Formación, membresía o recurso para aprender

Va al brief en: §1 Qué es, §3 Problema y dolores, §4 Qué hace. Si falta el "qué hace", seguimiento en el chat.

**P2 · Para quién** (`header`: "Para quién", `multiSelect`: false)
> ¿A quién le habla la landing primero (segmento líder)? Si hay un segundo segmento (variante), nombralo en «Otro».
- Empresas chicas y medianas, B2B (Recomendado)
- Equipos o áreas dentro de empresas grandes
- Profesionales independientes, consultores o agencias
- Personas o consumidores finales, B2C

Va al brief en: §2 Para quién (líder, variante, comprador vs. usuario). Si no nombró variante: "sin variante por ahora".

**P3 · Alternativas** (`header`: "Hoy", `multiSelect`: false)
> ¿Qué hace hoy el cliente en lugar de usar tu producto?
- Lo hace a mano: planillas, mails, chat (Recomendado)
- Usa otra herramienta o un competidor directo
- Contrata a alguien: agencia, freelance, consultor
- No lo resuelve o lo ignora

Va al brief en: §7 Alternativas del cliente y a la parte 3 y 6 de la propuesta de valor. Los nombres de competidores solo si
la persona los da; nunca se deducen.

**P4 · Diferenciales y qué los respalda** (`header`: "Diferencial", `multiSelect`: true)
> ¿Qué te diferencia y con qué lo podés demostrar? Marcá lo que aplica y, en «Otro», contá la prueba concreta.
- Método o proceso propio y documentado
- Tecnología o producto que se puede mostrar funcionando
- Experiencia o credenciales del equipo
- Resultados medidos con datos reales

Va al brief en: §6 Diferenciales verificables (tabla diferencial | prueba | fuente). Un diferencial sin prueba concreta se
anota como **[inferido]** y su prueba como **[A CONSEGUIR]**. Default si no marca nada: un diferencial deducido de P1, marcado [inferido].

## Ronda 2 · Qué existe de verdad y qué se ofrece (4 preguntas)

**P5 · Pruebas que existen** (`header`: "Pruebas", `multiSelect`: true)
> ¿Qué pruebas existen DE VERDAD hoy? Todo lo que no marques se publica como hueco [A CONSEGUIR]; nada se inventa.
- Ninguna todavía (Recomendado; excluye a las demás)
- Clientes o logos que puedo nombrar, con permiso
- Testimonios o métricas de resultado medidas
- Demos o casos reales que se pueden mostrar

Va al brief en: §8 Pruebas disponibles y §10 Huecos (prueba social y resultados). Si marcó "ninguna", la landing no lleva
logos, testimonios ni métricas, y la franja de prueba queda como hueco visible.

**P6 · Oferta, precio y CTA** (`header`: "Oferta", `multiSelect`: false)
> ¿Cuál es la oferta y el CTA principal?
- Sin definir: CTA neutro, dejar datos o pedir contacto (Recomendado)
- Prueba o demo gratuita
- Compra o suscripción con precio publicado
- Llamada o reunión con ventas

Va al brief en: §10 Huecos (comerciales) y a la estrategia de cada propuesta. Con "sin definir", el CTA no dice "pedir",
"primera" ni "gratis", y el precio queda como **[A CONSEGUIR]** con las opciones reales (piloto, pago único, suscripción,
gratis hasta X) en el punto de uso.

**P7 · Mercado, idioma y tono** (`header`: "Mercado/tono", `multiSelect`: false; los `header` miden como máximo 12 caracteres)
> ¿Mercado, idioma y tono de la marca?
- El mismo mercado e idioma de esta conversación, tono cercano y directo (Recomendado)
- Español neutro para varios países, tono profesional
- Inglés, mercado global, tono profesional y técnico

(Cualquier otra combinación de país, idioma y tono la escribe la persona en «Otro».)

Va al brief en: §9 Vocabulario y a la regla de copy (voseo, decimales, separador de miles, moneda). Si falta, **[inferido]**
con el idioma en que escribe la persona.

**P8 · Límites: qué NO se puede prometer** (`header`: "Límites", `multiSelect`: true)
> ¿Qué NO se puede prometer? Marcá lo que aplica y, en «Otro», cualquier otro límite.
- Resultados o porcentajes de mejora (Recomendado)
- Plazos de entrega o disponibilidad
- Cobertura: mercados, integraciones, plataformas
- Temas regulados: salud, finanzas, datos personales

Va al brief en: §12 Límites declarados y a las reglas duras de cada propuesta. Sin respuesta: se asume que no se promete
ningún resultado cuantificado ni plazo exacto (**[inferido]**). Un límite se respeta en todo el copy (simplemente no se promete) y los
que ayudan a decidir al visitante se dicen de frente en las preguntas o en la letra chica de la landing.

## Lo que no se pregunta y se resuelve con reglas

| Dato del brief | Cómo se resuelve sin preguntar |
|---|---|
| Nombre del producto | Del texto de P1 si lo dio; si no, "Producto X" y **[A CONSEGUIR: nombre]**. |
| Madurez (descripto, diseñado, construido, probado) | Por defecto "descripto por la persona, sin confirmar construido" **[inferido]**: la landing no habla en presente de lo que no está confirmado; se pregunta en el chat solo si cambia el copy. |
| Qué entrega y tiempos | De P1; tiempos **[A CONSEGUIR]** ("en horas" o "en días" hasta medirlos). |
| Comprador vs. usuario | De P2, marcado **[inferido]** si la persona no lo dijo. |
| Quién está detrás, equipo, política de datos, términos | Siempre **[A CONSEGUIR]**. |

## Mapa temas -> preguntas (para comprobar cobertura)

| Tema que el brief necesita | Pregunta |
|---|---|
| Qué es el producto y qué hace | P1 |
| Para quién (líder y variante) | P2 |
| Problema o trabajo a resolver | P1 (+ seguimiento si falta) |
| Qué hace hoy el cliente en su lugar | P3 |
| Diferenciales y la prueba que los respalda | P4 |
| Qué pruebas existen y cuáles no | P5 |
| Oferta, precio, CTA (o sin definir) | P6 |
| Mercado e idioma | P7 |
| Tono de marca | P7 |
| Límites: qué no se puede prometer | P8 |

## Después del cuestionario

1. Armar el brief con `references/brief-template.md`, marcando [inferido] y [A CONSEGUIR].
2. Mostrar el resumen de 8 a 10 líneas y pedir confirmación.
3. En el brief, la "fuente" es "Cuestionario del <fecha>" y cada dato lleva `(cuestionario P#)`. Dejar anotado que no hay
   documento detrás: cualquier cifra, cliente o testimonio que aparezca después es un error.
