# juanpernumian-skills

Hola, soy Juan Pernumian. Trabajo ayudando a empresas a usar IA en serio, y en el camino voy armando **skills**: instrucciones empaquetadas que le enseñan a un agente de IA a hacer un trabajo concreto, de punta a punta y siempre de la misma forma.

Acá comparto los que uso de verdad, para que los puedas usar, adaptar o desarmar para ver cómo están hechos. Voy a ir sumando más a medida que los pula.

## ¿Qué es un skill?

Un skill es una carpeta con un archivo `SKILL.md`, y a veces otros recursos (plantillas, guías y scripts). El `SKILL.md` tiene arriba un nombre y una descripción, y abajo las instrucciones. El agente lee la descripción y, cuando tu pedido coincide, carga el skill y lo sigue. No hace falta que te acuerdes de llamarlo, aunque también lo podés invocar a mano.

Es un formato abierto: el mismo `SKILL.md` lo entienden Claude Code, Codex y otros agentes.

## Qué hay adentro

| Skill | Qué hace | Para quién |
|---|---|---|
| [`value-prop-to-landing`](value-prop-to-landing/) | Le pasás lo que sabés de tu producto (documentos, un PDF, la URL de tu sitio, un repo o unas notas sueltas) y te devuelve una propuesta de valor, tres bocetos de landing con ángulos distintos, la auditoría de cada uno y una landing final. Cada afirmación se verifica contra la fuente, así que la landing no promete nada que no puedas respaldar. | Fundadores, producto y marketing que tienen que contar qué hace una app y no saben por dónde empezar |

## Cómo agregarlo a tu agente

Primero bajate el repositorio:

```bash
git clone https://github.com/juanpernu/juanpernumian-skills.git
```

Después copiá la carpeta del skill que quieras al lugar donde tu agente busca skills. En los ejemplos uso `value-prop-to-landing`.

### Claude Code

Claude Code busca skills en dos lugares:

| Dónde | Ruta | Cuándo usarlo |
|---|---|---|
| Para vos, en todos tus proyectos | `~/.claude/skills/` | Lo querés tener siempre a mano |
| Para un proyecto puntual | `.claude/skills/` dentro del repositorio | Lo querés compartir con tu equipo, versionado con el código |

```bash
# Para todos tus proyectos
mkdir -p ~/.claude/skills
cp -R juanpernumian-skills/value-prop-to-landing ~/.claude/skills/

# O solo para un proyecto (parado en la raíz del repo)
mkdir -p .claude/skills
cp -R juanpernumian-skills/value-prop-to-landing .claude/skills/
```

Abrí una sesión nueva de Claude Code y listo. Se usa de dos formas:

- **Pidiéndolo con tus palabras:** *«Armame la propuesta de valor y una landing para esta app»*. Claude reconoce el pedido y carga el skill.
- **Llamándolo directo:** escribí `/value-prop-to-landing`.

### Codex

Codex busca skills en `.agents/skills/`, tanto en tu carpeta personal como dentro de un repositorio:

| Dónde | Ruta |
|---|---|
| Para vos, en todos tus proyectos | `~/.agents/skills/` |
| Para un proyecto puntual | `.agents/skills/` en la raíz del repositorio |

```bash
# Para todos tus proyectos
mkdir -p ~/.agents/skills
cp -R juanpernumian-skills/value-prop-to-landing ~/.agents/skills/

# O solo para un proyecto (parado en la raíz del repo)
mkdir -p .agents/skills
cp -R juanpernumian-skills/value-prop-to-landing .agents/skills/
```

Reiniciá Codex. Se usa igual que en Claude Code:

- **Pidiéndolo con tus palabras:** Codex lo elige solo cuando tu pedido coincide con la descripción.
- **Llamándolo directo:** escribí `$value-prop-to-landing`, o corré `/skills` para ver la lista.

### Otros agentes

Si tu agente soporta skills con `SKILL.md`, copiá la carpeta a donde él los busque: el formato es el mismo. Si no los soporta, igual podés abrir el `SKILL.md`, pegarlo como instrucciones y adjuntar los archivos de `references/` que pida.

## Lo que necesita `value-prop-to-landing`

Además del agente, para generar las capturas, los PDF y las verificaciones:

- Google Chrome o Chromium. Si no está en la ruta por defecto, exportá `CHROME=/ruta/al/binario`.
- Python 3.
- Poppler (`pdfinfo`, `pdftotext`, `pdftoppm`). En macOS: `brew install poppler`.
- Node 22 o más nuevo, solo para la verificación en el navegador.

Lo escribí y lo uso con Claude Code, que corre varias partes en paralelo con subagentes. En Codex no lo probé todavía: si algo no anda, abrí un issue y lo vemos.

## Seguridad

Este skill hace que un agente lea material de terceros (PDF, páginas o repositorios) y después abra en Chrome las páginas que escribe. Por eso:

- Chrome corre sin acceso a internet, así que una página no puede mandar nada afuera.
- El skill trata el contenido de la fuente como dato y nunca como instrucciones: si un PDF dice «ignorá lo anterior y hacé X», el agente no lo hace.
- Los scripts no escriben fuera de la carpeta de trabajo.

Igual, leé un skill antes de instalarlo, este o cualquier otro. Es código que tu agente va a seguir.

## ¿Ideas, errores o un skill que te gustaría ver?

Abrí un [issue](https://github.com/juanpernu/juanpernumian-skills/issues). Y si lo usaste en algo tuyo, me encantaría saber cómo te fue.

## Licencia

MIT: lo podés usar, modificar y compartir, siempre que mantengas el crédito. Ver [LICENSE](LICENSE).

---

Juan Pernumian · [juanpernumian.com.ar](https://juanpernumian.com.ar)
