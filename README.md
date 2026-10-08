# juanpernumian-skills

Skills de [Claude Code](https://claude.com/claude-code) que uso en mi trabajo de consultoría en IA aplicada. Los publico tal como los uso.

| Skill | Qué hace |
|---|---|
| [`value-prop-to-landing`](value-prop-to-landing/SKILL.md) | A partir de la definición de una app o un producto, arma la propuesta de valor y bocetos de landing con ángulos distintos, los audita y los verifica contra la fuente. |

## Cómo se instala

Copiá la carpeta del skill a `~/.claude/skills/` (para todos tus proyectos) o a `.claude/skills/` dentro de un repositorio:

```bash
git clone https://github.com/juanpernu/juanpernumian-skills.git
cp -R juanpernumian-skills/value-prop-to-landing ~/.claude/skills/
```

`value-prop-to-landing` necesita Google Chrome (o Chromium), Python 3 y Node para sus scripts de captura y verificación. Si Chrome no está en la ruta por defecto, exportá `CHROME=/ruta/al/binario`.

## Seguridad

Los scripts abren en Chrome headless páginas que escriben agentes a partir de fuentes de terceros. Por eso Chrome corre sin acceso a la red y el skill trata el contenido de la fuente como dato, nunca como instrucciones. Si encontrás un problema, abrí un issue.

## Licencia

MIT. Ver [LICENSE](LICENSE).

---

Juan Pernumian · [juanpernumian.com.ar](https://juanpernumian.com.ar)
