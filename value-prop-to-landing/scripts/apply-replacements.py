#!/usr/bin/env python3
"""apply-replacements.py · reemplazos de texto masivos con conteo exacto de cada reemplazo.

Regla: cada reemplazo declara cuántas veces debe aparecer el texto viejo. Si UNO solo no coincide, no se escribe NADA.
Sin --apply es un ensayo (muestra qué haría). Con --apply escribe (de forma atómica) y verifica el resultado.
Sirve para que HTML y spec digan EXACTAMENTE lo mismo y para corregir una afirmación en todos los archivos derivados.

Uso:
  apply-replacements.py cambios.json            # ensayo
  apply-replacements.py cambios.json --apply    # escribe
  opciones: --root DIR (base de las rutas; default: carpeta del JSON) · --backup (deja archivo.bak) · --quiet
            --allow-outside (permite archivos fuera de la base; por defecto se rechazan)

Formato de cambios.json:
{
  "root": "ruta/base",                    // opcional; relativa al JSON si no es absoluta
  "replacements": [
    {"file": "propuesta.md",   "old": "texto viejo", "new": "texto nuevo", "count": 1, "note": "por qué"},
    {"file": ["a.md", "a.html"], "old": "frase", "new": "frase corregida", "count": 1}
  ]
}
- "file" puede ser una lista: el mismo reemplazo en cada archivo, con su propio conteo (por defecto 1 en cada uno).
- Los reemplazos se aplican en orden sobre el texto ya modificado en memoria; el orden importa y el ensayo avisa si un
  "old" aparece dentro del "new" de un reemplazo anterior sobre el mismo archivo.
- Texto literal, no regex. Se respetan espacios, saltos de línea y mayúsculas.
Códigos: 0 ok · 1 algún conteo no coincide (nada escrito) · 2 error de uso o de archivo.
"""
import json
import os
import sys


def die(msg, code=2):
    sys.stderr.write(msg + "\n")
    sys.exit(code)


def resolve(root, f, allow_outside):
    """Ruta real del archivo. Sin --allow-outside, rechaza todo lo que caiga fuera de la base: el JSON lo escribe
    un agente que leyó fuentes ajenas, y una ruta absoluta o con ../ no puede terminar editando otro archivo."""
    path = os.path.realpath(f if os.path.isabs(f) else os.path.join(root, f))
    if not allow_outside and os.path.commonpath([path, os.path.realpath(root)]) != os.path.realpath(root):
        die("%s queda fuera de la base %s; si es a propósito, usá --allow-outside" % (f, root))
    return path


def preview(s, n=70):
    s = s.replace("\n", "\\n")
    return s if len(s) <= n else s[: n - 1] + "…"


def main():
    args = [a for a in sys.argv[1:]]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if args else 2)
    apply_ = "--apply" in args
    backup = "--backup" in args
    quiet = "--quiet" in args
    allow_outside = "--allow-outside" in args
    root_opt = None
    if "--root" in args:
        i = args.index("--root")
        try:
            root_opt = args[i + 1]
        except IndexError:
            die("--root necesita una carpeta")
        del args[i:i + 2]
    positional = [a for a in args if not a.startswith("--")]
    if len(positional) != 1:
        die("uso: apply-replacements.py cambios.json [--apply] [--root DIR] [--backup] [--quiet] [--allow-outside]")
    spec_path = os.path.abspath(positional[0])
    try:
        spec = json.load(open(spec_path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        die("no pude leer %s: %s" % (spec_path, e))

    base = os.path.dirname(spec_path)
    root = root_opt or spec.get("root") or base
    if not os.path.isabs(root):
        root = os.path.abspath(os.path.join(base if not root_opt else os.getcwd(), root))
    items = spec.get("replacements")
    if not isinstance(items, list) or not items:
        die('el JSON necesita una lista "replacements" no vacía')

    # Expandir a pares (índice, archivo, old, new, count, note)
    pairs = []
    for i, it in enumerate(items, 1):
        for key in ("file", "old", "new"):
            if key not in it:
                die("reemplazo #%d: falta la clave '%s'" % (i, key))
        if not isinstance(it["old"], str) or it["old"] == "":
            die("reemplazo #%d: 'old' tiene que ser un texto no vacío" % i)
        files = it["file"] if isinstance(it["file"], list) else [it["file"]]
        for f in files:
            pairs.append((i, f, it["old"], it["new"], int(it.get("count", 1)), it.get("note", "")))

    texts, errors, warnings, log = {}, [], [], []
    news_by_file = {}
    for (i, f, old, new, n, note) in pairs:
        path = resolve(root, f, allow_outside)
        if f not in texts:
            if not os.path.isfile(path):
                errors.append("#%d: no existe el archivo %s" % (i, path))
                texts[f] = None
                continue
            texts[f] = open(path, encoding="utf-8").read()
        if texts[f] is None:
            continue
        found = texts[f].count(old)
        if found != n:
            errors.append("#%d %s: esperaba %d aparición(es) y encontré %d de %r" % (i, f, n, found, preview(old)))
            continue
        if old in new:
            warnings.append("#%d %s: el texto nuevo CONTIENE al viejo; aplicarlo dos veces lo duplicaría" % (i, f))
        for prev_new in news_by_file.get(f, []):
            if old in prev_new:
                warnings.append("#%d %s: el texto viejo aparece dentro del 'new' de un reemplazo anterior (el orden importa)" % (i, f))
                break
        news_by_file.setdefault(f, []).append(new)
        texts[f] = texts[f].replace(old, new)
        log.append("  OK #%d %s ×%d  %s -> %s%s" % (i, f, n, preview(old, 45), preview(new, 45), ("   (" + note + ")") if note else ""))

    if not quiet:
        print("\n".join(log))
    for w in warnings:
        print("AVISO: " + w)
    if errors:
        print("\nFALLA, no se escribió nada:")
        for e in errors:
            print("  - " + e)
        sys.exit(1)

    files = [f for f, t in texts.items() if t is not None]
    print("\n%d reemplazo(s) en %d archivo(s): conteos exactos." % (len(pairs), len(files)))
    if not apply_:
        print("Ensayo: no se escribió nada. Volvé a correr con --apply.")
        return

    for f in files:
        path = resolve(root, f, allow_outside)
        if backup:
            with open(path, "rb") as src, open(path + ".bak", "wb") as dst:
                dst.write(src.read())
        tmp = path + ".tmp-apply"
        with open(tmp, "w", encoding="utf-8") as out:
            out.write(texts[f])
        os.replace(tmp, path)
    # Verificación posterior: el texto viejo no debería quedar (salvo que el nuevo lo contenga)
    leftovers = []
    for (i, f, old, new, n, note) in pairs:
        if old in new:
            continue
        path = resolve(root, f, allow_outside)
        if open(path, encoding="utf-8").read().count(old):
            leftovers.append("#%d %s: el texto viejo sigue presente %r" % (i, f, preview(old)))
    if leftovers:
        print("AVISO tras escribir:")
        for l in leftovers:
            print("  - " + l)
    print("Escrito.%s" % (" Backups: *.bak" if backup else ""))


if __name__ == "__main__":
    main()
