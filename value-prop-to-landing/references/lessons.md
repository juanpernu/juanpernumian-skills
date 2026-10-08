# Lecciones aprendidas (generalizadas)

Cada lección salió de un error real del proceso. Están agrupadas por tema; las reglas duras de `SKILL.md` son su versión corta.
Contenido: [1. Datos reales y de demostración](#1-datos-reales-y-de-demostración) · [2. Leer las fuentes](#2-leer-las-fuentes) ·
[3. Qué se puede afirmar](#3-qué-se-puede-afirmar) · [4. Decisiones del negocio, CTA y enlaces](#4-decisiones-del-negocio-cta-y-enlaces) ·
[5. Largo y comparaciones](#5-largo-y-comparaciones) · [6. Medición y pruebas](#6-medición-y-pruebas) ·
[7. Subagentes y orquestación](#7-subagentes-y-orquestación) · [8. Herramientas: capturas, PDF y reemplazos](#8-herramientas-capturas-pdf-y-reemplazos).

## 1. Datos reales y de demostración

- **Declarar siempre qué es dato real y qué es demostración.** El sello "EJEMPLO · cifras ilustrativas" va DENTRO de cada pieza con
  cifras (en el encabezado del marco), no en una nota debajo: el número se lee antes que la nota.
- **Datos de ejemplo: una sola fuente de verdad** (una tabla en la spec) con chequeos de coherencia:
  - el total es el promedio ponderado de las partes visibles;
  - una métrica descripta no puede contradecir su fórmula (pisos, techos, casos límite);
  - las mismas cifras en hero, recorrido y respaldo;
  - no atribuir a una entidad una cifra que en la fuente es de otra;
  - usar etiquetas genéricas ("Plataforma A/B", "Marca A–D", "dominio-N.com") en vez de marcas reales con puntajes inventados.
- **Un mecanismo declarado debe poder verse en el ejemplo.** Si el texto promete "se rechaza y queda listado", el ejemplo lo
  muestra o la página no se apoya en eso.
- Cuando el set de ejemplo del documento es distinto del que produciría el producto real, la spec lo dice (qué cifras son del dato
  y cuáles se armaron para ilustrar).

## 2. Leer las fuentes

- **No copiar cifras ni textos de miniaturas de PDF.** Leer a resolución completa (renderizar a 300 dpi y recortar) o contra el dato
  crudo (fixture, resultado de referencia, código). Un número mal leído de una miniatura se propagó a tres documentos.
- **La fuente puede estar desactualizada** respecto de decisiones posteriores. Buscar lo que supera al documento (changelogs,
  tareas, README, código, historial) y marcar el documento como superado donde corresponda. Si una afirmación de marketing
  depende de una decisión superada, se corrige en TODOS los archivos derivados: brief, propuestas, HTML, PDF y capturas (una
  captura vieja puede seguir mostrando el claim corregido).
- **Un documento de diseño no es un producto en producción.** Separar "el documento lo describe" de "está probado o construido".
  No prometer lo que no está confirmado (re-correr mediciones, exportaciones, integraciones, SLA).
- Si el producto existe, leer el código: una constante o una fórmula contradice una frase de marketing con más autoridad que
  cualquier documento.

## 3. Qué se puede afirmar

- **Afirmar solo lo que cubre la fuente:** "una muestra auditada" no es "cada elemento auditado"; "algunas herramientas" no es "la
  categoría"; plazos y áreas son ejemplos, no listas cerradas; cuidado con los absolutos ("nunca", "no hay forma", "sigue
  circulando").
- **Plazos:** decir "en horas" y no un número de horas hasta medir; contar el tiempo desde el hito correcto (no desde el clic si
  hay un paso manual, un login y una entrevista en el medio).
- **Hacer lo que dice el verbo:** si algo es una solicitud de acceso, el botón no dice "pedir"; si la oferta no está definida, el
  CTA no dice "primera" ni "gratis".

## 4. Decisiones del negocio, CTA y enlaces

- **Decisiones que NO son del diseño** (oferta y precio, mercado e idioma, quién está detrás, marca blanca, calendario, aviso por
  email, informe de ejemplo real) quedan como `[A CONSEGUIR]` visibles y pegadas al punto de uso, con las opciones verdaderas
  posibles. Nunca se resuelven inventando.
- **CTA neutro** cuando la oferta no está definida.
- **Un CTA no puede ser un scroll desnudo de miles de píxeles:** repetir el mismo componente (campo + botón) cerca, o llevar al
  formulario más cercano y poner el foco en el campo.
- **Barra fija mobile:** aparece solo cuando el formulario del hero salió de pantalla y se oculta con cualquier formulario en pantalla;
  mientras está activa, el botón del header se oculta.
- **Nunca enlazar a destinos que no existen** (un "ver informe de ejemplo" que apunta a la misma sección): usar un ancla al
  recorrido dentro de la página hasta que el destino exista.

## 5. Largo y comparaciones

- **Largo:** auditar la duplicación (la misma prueba repetida en barra de respaldo, hero y método), medir la altura mobile contra
  las propuestas y cortar lo que repite.
- **Comparaciones con competidores:** no nombrar marcas ni generalizar a una categoría entera a partir de un solo producto; los
  contrastes van en la celda propia; dejar "dónde gana cada alternativa"; revisión legal si se nombra a alguien. Las celdas "no
  aplica" no se muestran en el layout apilado mobile.

## 6. Medición y pruebas

- **FAQ cerradas por defecto:** la primera abierta sesga la medición de objeciones. Y abrir una pregunta no es tener la objeción.
- **Medición:** una clave que cruce landing -> login -> app (por ejemplo el `state` de OAuth), eventos posteriores al formulario
  (entrevista, activación, entrega), una métrica de decisión que no sea el clic y **pocos eventos**. Contar el envío también del
  lado del servidor (los bloqueadores subestiman). Cuidado con los clics absolutos cuando hay una barra fija siempre visible:
  comparar contra la exposición de la sección.
- **Pruebas de 5 segundos** necesitan una versión limpia (sin banner ni etiquetas de wireframe; los sellos y los huecos se quedan).
- **Con poco tráfico no hay A/B** que separe señal de ruido (~1.000 sesiones y ~30 conversiones por variante): comparar por tanda
  de envío o por canal y juzgar por una métrica de decisión.

## 7. Subagentes y orquestación

- **Una tarea por agente.** Cada uno escribe SOLO su archivo. Los de un mismo paso van en paralelo (un solo mensaje).
- **El orquestador no se queda con el resumen:** lee el informe completo y verifica por su cuenta los hechos graves antes de apoyarse
  en ellos (código, fuente a resolución completa).
- Los subagentes **NO cambian de rama ni hacen commit**; se confirma la rama antes de editar y se repite en el prompt.
- **Ola de validación obligatoria** tras trabajo en paralelo: confirmar qué tocó cada agente (`git status`, fechas de modificación),
  leer los informes completos, verificar los hechos graves y **resumir todos los problemas en un solo informe ANTES de arreglar
  nada**. Nunca saltar de "agentes terminaron" a "arreglando": el resumen obliga a ver el daño completo y evita arreglar de a una cosa.
- Las correcciones masivas las hace **un agente con una lista exacta** (origen, archivo, texto viejo, texto nuevo) para que HTML y
  spec digan lo mismo; después el orquestador verifica por su cuenta (claims prohibidos, conteos, aritmética del ejemplo, render,
  capturas).

## 8. Herramientas: capturas, PDF y reemplazos

- **Mobile en Chrome headless:** el ancho mínimo de ventana es 500 px. Capturar un iframe de 390 px reales y recortar con
  `sips -c ALTO ANCHO --cropOffset <y> <x>`: el offset es desde la esquina superior izquierda y un offset (0,0) se interpreta como
  "centrar" (usar 1, no 0, para anclar a la izquierda; ese error cortó ~55 px a las capturas). Verificar visualmente una captura
  recortada. `scripts/shot.sh` ya lo resuelve (el iframe se corre 1 px para no perder ni un píxel).
- **PDF desde Chrome headless:** contar páginas y líneas por página con `pdfinfo`/`pdftotext` y comparar contra la versión anterior
  (`scripts/render-pdf.sh --prev`). Una frase más larga puede empujar un bloque a una página casi vacía: acortar o compactar antes
  que aceptarlo. Una columna de "páginas/fuentes" que se ensancha rompe filas de tabla (mantenerla `nowrap` y angosta).
- **PDF de capturas largas** (8.000 a 20.000 px): no usar una página gigante (límite práctico de ~14.400 pt por lado). Cortar en
  tramos que entran en una página y escalarlos para que el texto se lea (`scripts/build-bocetos-pdf.sh`).
- **Reemplazos de texto masivos:** con un script que exige el **conteo exacto** de cada reemplazo y no escribe nada si uno falla;
  primero ensayo y después `--apply` (`scripts/apply-replacements.py`).
