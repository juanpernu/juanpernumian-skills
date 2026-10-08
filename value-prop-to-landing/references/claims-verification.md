# Verificación de claims contra las fuentes primarias

La re-auditoría independiente (fase 6, frente ii) abre las fuentes de verdad y compara, afirmación por afirmación, lo que dice la
landing con lo que dice la fuente. Se hace aparte de la auditoría de conversión porque son dos preguntas distintas: "¿convierte?"
y "¿es verdad?". Archivo: `verificacion-de-claims.md`. Un documento de diseño no es un producto en producción, y una landing
suele hablar en presente de cosas que el documento solo describe.

## Procedimiento

1. **Inventario.** Sacar el texto visible del HTML (`scripts/check-claims.sh landing.html --show-text`) y las afirmaciones de la
   spec §3. Numerar cada afirmación de producto tal como figura (con la sección donde está). Incluir los textos de los mocks
   y las cifras del ejemplo.
2. **Abrir las fuentes primarias completas**, no resúmenes: cada PDF o documento de la fuente de la verdad, entero; el sitio; y
   **el código y los tests del producto si existe** (constantes, fórmulas, límites, configuración). El brief y la propuesta de
   valor son derivados: se usan de contexto, nunca como prueba.
3. **Buscar decisiones que superan a la fuente** (changelog, lista de tareas, README, issues, `git log`). Si una afirmación
   depende de una decisión superada, es un hallazgo aunque la fuente original la respalde.
4. **Veredicto por afirmación**, con evidencia exacta (fuente, página o línea, cita corta).
5. **Revisar las referencias de página** de la spec y del brief: página citada vs. página que lo dice de verdad.
6. **Comparar los datos del ejemplo** con el dato crudo y con el documento (tabla aparte).
7. **Cerrar** con el resumen de conteos, lo más grave y "No pude verificar".

## Si la base fue el cuestionario (no hay documento ni código)

No hay fuente primaria contra la cual verificar. El frente (ii) verifica contra el brief y sus marcas: cada afirmación de producto de la
landing tiene que mapear a una respuesta `(cuestionario P#)` y lo que no mapea es **SOLO INFERIDA** (o **SIN RESPALDO** si es una cifra,
un cliente o un testimonio). El informe lo dice en la primera línea y el resumen final se lo recuerda a la persona: hay que confirmar
cada afirmación con quien conoce el producto antes de publicar.

## Veredictos

| Veredicto | Significa |
|---|---|
| **RESPALDADA** | La fuente lo dice, con las mismas condiciones. |
| **RESPALDADA CON MATIZ** | La fuente lo dice, pero con un alcance, condición o estado distinto (es un objetivo de diseño, no una medición; vale para una muestra, no para todo; es un ejemplo, no una lista cerrada). Se propone el texto ajustado. |
| **SOLO INFERIDA** | La fuente no lo dice; es una interpretación razonable. Se marca como tal o se saca. |
| **SIN RESPALDO** | Una cifra o dato que no está en ninguna fuente. Se saca o se reemplaza. |
| **CONTRADICE LA FUENTE** | La fuente dice otra cosa. Es el hallazgo más grave. |

## Formato del informe

```
# Verificación de claims · <landing> · <fecha>
Verificador independiente. Fuentes primarias abiertas por mí: <lista exacta, con páginas leídas>. Convención: Doc A p. N · L = línea.

## Resumen
N afirmaciones: RESPALDADA a · CON MATIZ b · SOLO INFERIDA c · SIN RESPALDO d · CONTRADICE e (conteo hecho con un script sobre la tabla).
Lo más grave: (3 a 5 puntos, cada uno con su evidencia). Contexto que cruza todo (documento de trabajo vs. producto).

## Afirmaciones
| # | Afirmación (como figura en la landing) | Veredicto | Evidencia exacta | Cambio propuesto |

## Referencias de página mal citadas
| Dónde | Cita | Qué dice realmente esa página | Página o fuente correcta |

## Datos del ejemplo
| Cifra de la landing | Dato crudo | Documento | Veredicto |   (+ qué se presenta como "armado desde el dato" y no lo es)

## Decisiones que superan a la fuente
(qué se encontró, dónde está, qué afirmaciones afecta)

## No pude verificar
(lo que no existe para probar: flujo en producción, integraciones reales, tiempos medidos, UI pública; qué quedó abierto)
```

## Cómo leer una cifra sin equivocarse

- **No copiar cifras ni textos de miniaturas de PDF.** Renderizar la página a 300 dpi y recortar la zona:
  `pdftoppm -r 300 -f N -l N -png doc.pdf /tmp/pag` y después `sips -c ALTO ANCHO --cropOffset Y X /tmp/pag-N.png --out /tmp/recorte.png`
  (el offset es desde la esquina superior izquierda; un offset 0 en ambos ejes se interpreta como "centrar": usar 1) y mirar el
  recorte. O contrastar con el **dato crudo** (fixture, resultado de referencia, código, tabla de origen). Un número mal leído de
  una miniatura se propagó a tres documentos en el proceso original.
- Texto: `pdftotext -layout -f N -l N doc.pdf -` para citar literal; `pdfinfo` para el total de páginas; buscar con `grep` sobre el texto.
- Código: leer la constante o fórmula en el archivo y citar archivo y línea; correr los tests si existen y no cuesta.
- Si dos fuentes se contradicen, mostrar la contradicción y no elegir en silencio.

## Qué buscar (patrones que fallan)

- **Una muestra no es el total:** "una muestra auditada" no es "cada elemento auditado".
- **Un producto no es la categoría:** "algunas herramientas" no es "las herramientas".
- **Ejemplos no son listas cerradas:** plazos, áreas, tipos, límites que la fuente da "por ejemplo".
- **Absolutos:** "nunca", "siempre", "no hay forma", "sigue circulando", "nadie".
- **Objetivo de diseño dicho como hecho:** plazos, tiempos de entrega, "re-correr", exportaciones, integraciones, SLA.
- **El hito de un plazo:** el tiempo corre desde que ocurre qué; si hay pasos manuales o esperas, no se cuentan desde el clic.
- **Cifras armadas que se presentan como del dato:** valores reasignados de una entidad a otra, promedios que no están en la fuente.
- **Una descripción de una métrica que contradice su fórmula** (pisos, techos, casos límite).
- **Mecanismos prometidos que el ejemplo no muestra.**
- **Documento superado** por una decisión posterior (changelog, tareas, código).
- **Estado de implementación:** "construido" vs. "descripto en un documento" vs. "sin probar contra el servicio real".

## Qué hace el orquestador con el informe

No se queda con el resumen del agente. **Lee el informe completo** y **verifica por su cuenta los hechos más pesados** (los 3 a 5
hallazgos graves) contra el código y las fuentes antes de apoyarse en ellos: un agente puede equivocarse o sobreafirmar. Lo
verificado y lo corregido se anota en la spec (§7b) y, si afecta al brief o a la propuesta de valor, se corrige AGUAS ARRIBA
(brief, propuesta de valor md/html/pdf, propuestas archivadas, capturas) en la misma pasada.
