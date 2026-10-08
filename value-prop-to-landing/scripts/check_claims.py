#!/usr/bin/env python3
"""check_claims.py · patrones prohibidos y conteos estructurales sobre el TEXTO VISIBLE de un HTML (o un .md).

Uso (normalmente vía check-claims.sh):
  check_claims.py archivo.html [--forbid 'regex|regex'] [--forbid-file patrones.txt] [--require 'regex']
                  [--count 'regex=N'] [--max-words N] [--attrs] [--show-text] [--no-structural]
                  [--mock-class mock] [--stamp-class stamp]

Qué hace:
  1. Extrae el texto visible (sin <script>, <style>, <head> ni comentarios; con los textos de los <details> cerrados).
  2. --forbid / --forbid-file: patrones prohibidos (regex, sin distinguir mayúsculas). Cada coincidencia se imprime con su
     línea y contexto. Ejemplos: promesas que la fuente no respalda, palabras de oferta no definida ("gratis", "primera"),
     absolutos ("nunca", "siempre"), marcas que no se pueden nombrar, rastros de un claim superado.
  3. --require: patrones que tienen que aparecer. --count 'regex=N': cantidad exacta de coincidencias.
  4. Chequeos estructurales del HTML (se pueden apagar con --no-structural):
       - exactamente un <h1> · ningún <details open> · ids duplicados · anclas internas (#x) que apuntan a un id inexistente ·
         recursos externos (src, <link>, url(), @import) · imágenes sin alt · enlaces "#" vacíos (aviso) ·
         cada elemento .mock contiene un .stamp (el sello EJEMPLO va ADENTRO de cada pieza con cifras).
  5. Resumen de conteos (h2, secciones, formularios, botones, FAQ, huecos [A CONSEGUIR], sellos, palabras) para comparar
     el largo de una propuesta con otra o antes/después de una pasada de recortes.
Código de salida: 0 sin problemas · 1 hay problemas · 2 uso incorrecto.
"""
import argparse
import re
import sys
from html.parser import HTMLParser

BLOCK = {"p", "div", "section", "article", "header", "footer", "main", "nav", "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5",
         "h6", "table", "tr", "td", "th", "details", "summary", "blockquote", "form", "label", "br", "dl", "dt", "dd", "figure",
         "figcaption", "button", "a"}
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "area", "base", "col", "embed", "param", "track", "wbr"}
TEXT_ATTRS = ("alt", "title", "aria-label", "placeholder", "value")


class Doc(HTMLParser):
    def __init__(self, with_attrs, mock_class, stamp_class):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0                      # profundidad dentro de script/style/head
        self.stack = []                    # (tag, clases, tiene_sello)
        self.with_attrs = with_attrs
        self.mock_class, self.stamp_class = mock_class, stamp_class
        self.ids, self.hrefs, self.dup_ids = {}, [], []
        self.external, self.noalt, self.empty_hash = [], 0, 0
        self.tags = {}
        self.details_open = 0
        self.mocks, self.mocks_without_stamp, self.stamps = 0, 0, 0
        self.placeholders = 0

    def handle_starttag(self, tag, attrs):
        a = dict((k, v if v is not None else "") for k, v in attrs)
        self.tags[tag] = self.tags.get(tag, 0) + 1
        if tag in ("script", "style", "head"):
            self.skip += 1
        if tag == "link" and a.get("href", "").lower().startswith(("http://", "https://", "//")):
            self.external.append("<link href=%s>" % a["href"])
        if tag in ("script", "img", "iframe", "source", "video", "audio") and a.get("src", "").lower().startswith(("http://", "https://", "//")):
            self.external.append("<%s src=%s>" % (tag, a["src"]))
        if "style" in a and re.search(r"url\(\s*['\"]?(https?:)?//", a["style"]):
            self.external.append("style url(...) externo")
        if tag == "style":
            self._in_style = True
        if "id" in a and a["id"]:
            if a["id"] in self.ids:
                self.dup_ids.append(a["id"])
            self.ids[a["id"]] = True
        if tag == "a" and "href" in a:
            h = a["href"]
            if h == "#":
                self.empty_hash += 1
            elif h.startswith("#"):
                self.hrefs.append(h[1:])
        if tag == "img" and not a.get("alt", "").strip() and "alt" not in a:
            self.noalt += 1
        if tag == "details" and "open" in a:
            self.details_open += 1
        classes = a.get("class", "").split()
        if tag not in VOID:
            self.stack.append([tag, classes, False, self.mock_class in classes])
        if self.stamp_class in classes:
            self.stamps += 1
            for fr in self.stack:
                if fr[3]:
                    fr[2] = True
        if self.mock_class in classes:
            self.mocks += 1
        if self.skip == 0:
            if tag in BLOCK:
                self.parts.append("\n")
            if self.with_attrs:
                for k in TEXT_ATTRS:
                    if a.get(k):
                        self.parts.append(" " + a[k] + " ")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head") and self.skip:
            self.skip -= 1
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                fr = self.stack[i]
                if fr[3] and not fr[2]:
                    self.mocks_without_stamp += 1
                del self.stack[i:]
                break
        if self.skip == 0 and tag in BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip == 0:
            self.parts.append(data)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def text(self):
        t = "".join(self.parts)
        t = re.sub(r"[ \t\r\f\v ]+", " ", t)
        t = re.sub(r" *\n *", "\n", t)
        t = re.sub(r"\n{2,}", "\n", t)
        return t.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--forbid", action="append", default=[], help="regex o varios separados por |")
    ap.add_argument("--forbid-file")
    ap.add_argument("--require", action="append", default=[])
    ap.add_argument("--count", action="append", default=[], help="regex=N")
    ap.add_argument("--max-words", type=int)
    ap.add_argument("--attrs", action="store_true")
    ap.add_argument("--show-text", action="store_true")
    ap.add_argument("--no-structural", action="store_true")
    ap.add_argument("--mock-class", default="mock")
    ap.add_argument("--stamp-class", default="stamp")
    a = ap.parse_args()

    try:
        raw = open(a.file, encoding="utf-8").read()
    except OSError as e:
        sys.stderr.write("no pude leer %s: %s\n" % (a.file, e))
        sys.exit(2)
    is_html = a.file.lower().endswith((".html", ".htm"))
    doc = None
    if is_html:
        doc = Doc(a.attrs, a.mock_class, a.stamp_class)
        doc.feed(raw)
        doc.close()
        text = doc.text()
    else:
        text = raw
    if a.show_text:
        print(text)
        return

    problems = []
    forbid = []
    for f in a.forbid:
        forbid += [p for p in f.split("|") if p.strip()] if "(" not in f else [f]
    if a.forbid_file:
        try:
            for line in open(a.forbid_file, encoding="utf-8"):
                line = line.strip()
                if line and not line.startswith("#"):
                    forbid.append(line)
        except OSError as e:
            sys.stderr.write("no pude leer %s: %s\n" % (a.forbid_file, e))
            sys.exit(2)

    lines = text.split("\n")
    print("Archivo: %s · %s · %d palabras visibles" % (a.file, "HTML" if is_html else "texto", len(re.findall(r"\w+", text))))
    if forbid:
        print("\nPatrones prohibidos:")
    for pat in forbid:
        try:
            rx = re.compile(pat, re.I)
        except re.error as e:
            sys.stderr.write("regex inválida %r: %s\n" % (pat, e))
            sys.exit(2)
        hits = []
        for n, ln in enumerate(lines, 1):
            for m in rx.finditer(ln):
                s = max(0, m.start() - 35)
                hits.append("    L%d: …%s…" % (n, ln[s:m.end() + 35].strip()))
        if hits:
            problems.append("prohibido %r: %d coincidencia(s)" % (pat, len(hits)))
            print("  X %r -> %d" % (pat, len(hits)))
            print("\n".join(hits[:6]) + ("\n    … y %d más" % (len(hits) - 6) if len(hits) > 6 else ""))
        else:
            print("  ok %r -> 0" % pat)
    for pat in a.require:
        n = len(re.findall(pat, text, re.I))
        if n == 0:
            problems.append("falta lo requerido %r" % pat)
        print("%s requerido %r -> %d" % ("  ok" if n else "  X ", pat, n))
    for spec in a.count:
        if "=" not in spec:
            sys.stderr.write("--count espera 'regex=N', recibí %r\n" % spec)
            sys.exit(2)
        pat, n_exp = spec.rsplit("=", 1)
        n = len(re.findall(pat, text, re.I))
        ok = n == int(n_exp)
        if not ok:
            problems.append("conteo %r: esperaba %s y encontré %d" % (pat, n_exp, n))
        print("%s conteo %r: esperado %s, encontrado %d" % ("  ok" if ok else "  X ", pat, n_exp, n))
    words = len(re.findall(r"\w+", text))
    if a.max_words is not None and words > a.max_words:
        problems.append("%d palabras visibles (máximo %d)" % (words, a.max_words))
        print("  X palabras visibles %d > %d" % (words, a.max_words))

    if is_html and not a.no_structural:
        print("\nEstructura:")
        h1 = doc.tags.get("h1", 0)
        checks = [
            (h1 == 1, "un solo <h1> (hay %d)" % h1),
            (doc.details_open == 0, "ningún <details open> (hay %d): una pregunta abierta sesga la medición de objeciones" % doc.details_open),
            (not doc.dup_ids, "ids duplicados: %s" % (", ".join(sorted(set(doc.dup_ids))) or "ninguno")),
        ]
        broken = sorted({h for h in doc.hrefs if h not in doc.ids})
        checks.append((not broken, "anclas internas rotas: %s" % (", ".join("#" + b for b in broken) or "ninguna")))
        checks.append((not doc.external, "recursos externos: %s" % ("; ".join(sorted(set(doc.external))[:5]) or "ninguno")))
        checks.append((doc.noalt == 0, "imágenes sin alt: %d" % doc.noalt))
        checks.append((doc.mocks_without_stamp == 0, "piezas .%s sin sello .%s ADENTRO: %d de %d" % (a.mock_class, a.stamp_class, doc.mocks_without_stamp, doc.mocks)))
        for ok, msg in checks:
            print("  %s %s" % ("ok" if ok else "X ", msg))
            if not ok:
                problems.append(msg)
        if doc.empty_hash:
            print("  ! %d enlace(s) a '#' vacío: confirmá que no sean CTA que no llevan a ningún lado" % doc.empty_hash)
        ph = len(re.findall(r"\[A CONSEGUIR", text, re.I))
        print("\nConteos: h2=%d · h3=%d · section=%d · form=%d · button=%d · details=%d · .%s=%d · .%s=%d · [A CONSEGUIR]=%d · palabras=%d" % (
            doc.tags.get("h2", 0), doc.tags.get("h3", 0), doc.tags.get("section", 0), doc.tags.get("form", 0), doc.tags.get("button", 0),
            doc.tags.get("details", 0), a.mock_class, doc.mocks, a.stamp_class, doc.stamps, ph, words))

    print("\nRESULTADO: %s" % ("OK, sin problemas" if not problems else "%d problema(s)" % len(problems)))
    for p in problems:
        print(" - " + p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
