#!/usr/bin/env python3
"""pdf_check.py · verifica un PDF generado desde HTML (solo biblioteca estándar + poppler).

Uso:
  pdf_check.py archivo.pdf [--prev anterior.pdf] [--min-lines 5] [--min-fill 0.15]
                           [--sparse-ok 1,9] [--mode text|images] [--paper A4] [--strict]

Qué comprueba (necesita pdfinfo, pdftotext y pdftoppm de poppler):
  - cantidad de páginas y tamaño de cada página (por defecto A4 = 595 x 842 pt);
  - líneas de texto por página (sin contar el pie, el 6% inferior) y hasta dónde llega el contenido (% del alto);
  - páginas "casi vacías": pocas líneas (modo text) o contenido que termina en el primer tramo de la página;
  - desbordes: palabras fuera de la página (a la derecha, a la izquierda o abajo) y tinta pegada al borde;
  - comparación contra una versión previa (páginas y líneas por página), para ver qué bloque se movió.
--mode images: para PDF hechos de capturas (no exige líneas de texto, solo tinta y desbordes).
Código de salida: 0 siempre, salvo --strict (1 si hay avisos).
"""
import argparse
import glob
import html
import os
import re
import subprocess
import sys
import tempfile

PAPERS = {"A4": (595.28, 841.89), "A3": (841.89, 1190.55), "LETTER": (612.0, 792.0)}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr.decode("utf-8", "replace"))
        raise SystemExit("falló: " + " ".join(cmd))
    return r.stdout


def pdfinfo(pdf):
    out = run(["pdfinfo", "-f", "1", "-l", "9999", pdf]).decode("utf-8", "replace")
    pages = int(re.search(r"^Pages:\s+(\d+)", out, re.M).group(1))
    sizes = {}
    for m in re.finditer(r"^Page\s+(\d+)\s+size:\s+([\d.]+) x ([\d.]+) pts", out, re.M):
        sizes[int(m.group(1))] = (float(m.group(2)), float(m.group(3)))
    if not sizes:
        m = re.search(r"^Page size:\s+([\d.]+) x ([\d.]+) pts", out, re.M)
        if m:
            sizes = {i: (float(m.group(1)), float(m.group(2))) for i in range(1, pages + 1)}
    return pages, sizes


def bbox_words(pdf):
    """Devuelve {pagina: [(xmin, ymin, xmax, ymax, texto), ...]} usando pdftotext -bbox."""
    xml = run(["pdftotext", "-bbox", pdf, "-"]).decode("utf-8", "replace")
    pages, cur = {}, None
    for line in xml.splitlines():
        if line.lstrip().startswith("<page "):
            cur = len(pages) + 1
            pages[cur] = []
        m = re.search(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', line)
        if m and cur:
            pages[cur].append((float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)), html.unescape(m.group(5))))
    return pages


def count_lines(words, page_h, footer_frac=0.06):
    """Agrupa palabras en líneas por su posición vertical; ignora el pie (franja inferior)."""
    body = [w for w in words if w[1] < page_h * (1 - footer_frac)]
    body.sort(key=lambda w: (w[1], w[0]))
    lines, ref = 0, None
    for w in body:
        h = max(w[3] - w[1], 1.0)
        if ref is None or abs(w[1] - ref) > 0.55 * h:
            lines += 1
            ref = w[1]
    return lines, (max((w[3] for w in body), default=0.0) / page_h)


def read_pgm(path):
    data = open(path, "rb").read()
    m = re.match(rb"P5\s+(\d+)\s+(\d+)\s+(\d+)\s", data)
    w, h = int(m.group(1)), int(m.group(2))
    return w, h, data[m.end():]


def ink_metrics(pdf, dpi=30):
    """Rasteriza en gris a baja resolución y mide: tinta %, hasta dónde llega el contenido y tinta en los bordes."""
    tmp = tempfile.mkdtemp()
    run(["pdftoppm", "-gray", "-r", str(dpi), pdf, os.path.join(tmp, "p")])
    files = sorted(glob.glob(os.path.join(tmp, "p-*.pgm")), key=lambda f: int(re.search(r"-(\d+)\.pgm$", f).group(1)))
    thr = 235
    table = bytes(1 if b < thr else 0 for b in range(256))
    em = max(1, int(round(dpi / 25.4 * 3)))  # 3 mm
    res = []
    for f in files:
        w, h, px = read_pgm(f)
        dark_map = px.translate(table)          # 1 = tinta, 0 = blanco (a velocidad de C)
        dark = dark_map.count(1)
        last_row = -1
        edge = 0
        for y in range(h):
            row = dark_map[y * w:(y + 1) * w]
            n = row.count(1)
            if n and y < int(h * 0.94):
                last_row = y
            if y < em or y >= h - em:
                edge += n
            else:
                edge += row[:em].count(1) + row[w - em:].count(1)
        res.append({"ink": dark / float(w * h), "bottom": (last_row + 1) / float(h), "edge": edge})
        os.remove(f)
    os.rmdir(tmp)
    return res


def images_per_page(pdf):
    """Cantidad de imágenes por página (pdfimages -list): instantáneo, sirve para PDF hechos de capturas."""
    out = run(["pdfimages", "-list", pdf]).decode("utf-8", "replace").splitlines()
    counts = {}
    for line in out[2:]:
        parts = line.split()
        if parts and parts[0].isdigit():
            counts[int(parts[0])] = counts.get(int(parts[0]), 0) + 1
    return counts


def analyze(pdf, paper, mode="text", ink_on=None):
    pages, sizes = pdfinfo(pdf)
    words = bbox_words(pdf)
    use_ink = (mode == "text") if ink_on is None else ink_on
    ink = ink_metrics(pdf) if use_ink else []
    imgs = images_per_page(pdf) if mode == "images" else {}
    out = []
    heights = sorted((w[3] - w[1]) for ws_ in words.values() for w in ws_ if w[3] > w[1])
    median_h = heights[len(heights) // 2] if heights else 0.0
    for p in range(1, pages + 1):
        w, h = sizes.get(p, paper)
        ws = words.get(p, [])
        lines, text_bottom = count_lines(ws, h)
        over = [x for x in ws if x[2] > w + 1.0 or x[0] < -1.0 or x[3] > h + 1.0]
        im = ink[p - 1] if p - 1 < len(ink) else None
        n_img = imgs.get(p, 0)
        if im is not None:
            fill, inkv, edge = max(im["bottom"], text_bottom), im["ink"], im["edge"]
        else:                                  # sin raster: una página con imagen cuenta como llena
            fill, inkv, edge = (1.0 if n_img else text_bottom), None, 0
        out.append({"page": p, "w": w, "h": h, "lines": lines, "fill": fill, "ink": inkv, "edge": edge,
                    "overflow": len(over), "images": n_img})
    return pages, out, median_h


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--prev")
    ap.add_argument("--min-lines", type=int, default=5)
    ap.add_argument("--min-fill", type=float, default=0.15)
    ap.add_argument("--sparse-ok", default="", help="páginas (1,9) que pueden ser livianas, por ejemplo la portada")
    ap.add_argument("--edge-ok", default="", help="páginas con sangrado a propósito (portada a página completa)")
    ap.add_argument("--mode", choices=["text", "images"], default="text")
    ap.add_argument("--paper", default="A4")
    ap.add_argument("--ink", action="store_true", help="en modo images, rasteriza también (lento con imágenes grandes)")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    paper = PAPERS.get(a.paper.upper(), PAPERS["A4"])
    sparse_ok = {int(x) for x in a.sparse_ok.split(",") if x.strip()}
    edge_ok = {int(x) for x in a.edge_ok.split(",") if x.strip()}
    pages, rows, med = analyze(a.pdf, paper, a.mode, True if a.ink else None)
    prev_rows, prev_pages = None, None
    if a.prev and os.path.exists(a.prev):
        prev_pages, prev_rows, prev_med = analyze(a.prev, paper, a.mode, True if a.ink else None)

    warnings = []
    size_kb = os.path.getsize(a.pdf) / 1024.0
    print("PDF: %s · %d páginas · %.0f KB" % (a.pdf, pages, size_kb))
    hdr = "pág | tamaño pt   | líneas | contenido hasta | tinta  | imág. | desborde"
    if prev_rows:
        hdr += " | prev líneas | Δ"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        flags = []
        if abs(r["w"] - paper[0]) > 2 or abs(r["h"] - paper[1]) > 2:
            if not (abs(r["h"] - paper[0]) <= 2 and abs(r["w"] - paper[1]) <= 2):  # apaisado también vale
                flags.append("tamaño distinto de %s" % a.paper.upper())
        if r["page"] not in sparse_ok:
            if a.mode == "text" and r["lines"] < a.min_lines:
                flags.append("CASI VACÍA (%d líneas)" % r["lines"])
            elif r["fill"] < a.min_fill or (r["ink"] is not None and r["ink"] < 0.002):
                flags.append("CASI VACÍA (contenido hasta %.0f%%)" % (r["fill"] * 100))
        if r["overflow"]:
            flags.append("DESBORDE: %d palabras fuera de la página" % r["overflow"])
        if a.mode == "images" and r["images"] == 0 and r["lines"] == 0 and r["page"] not in sparse_ok:
            flags.append("PÁGINA EN BLANCO (sin texto ni imágenes)")
        if r["page"] not in edge_ok and r["edge"] > 0 and a.mode == "text":
            flags.append("tinta pegada al borde (¿desborde o sangrado?)")
        line = "%3d | %5.0f x %-5.0f | %6d | %14.0f%% | %6s | %5d | %8d" % (
            r["page"], r["w"], r["h"], r["lines"], r["fill"] * 100,
            ("%.1f%%" % (r["ink"] * 100)) if r["ink"] is not None else "-", r["images"], r["overflow"])
        if prev_rows:
            pr = prev_rows[r["page"] - 1] if r["page"] - 1 < len(prev_rows) else None
            line += " | %11s | %s" % (pr["lines"] if pr else "-", ("%+d" % (r["lines"] - pr["lines"])) if pr else "-")
        if flags:
            line += "   <-- " + "; ".join(flags)
            warnings += ["pág %d: %s" % (r["page"], f) for f in flags]
        print(line)
    if prev_rows:
        print("\nComparación: %d págs ahora vs. %d antes (%+d)" % (pages, prev_pages, pages - prev_pages))
        if pages != prev_pages:
            warnings.append("cambió la cantidad de páginas (%d -> %d)" % (prev_pages, pages))
        if prev_med and med and med < prev_med * 0.95:
            msg = "el texto quedó %.0f%% más chico que en la versión anterior (¿Chrome encogió el documento por un desborde horizontal?)" % ((1 - med / prev_med) * 100)
            print(msg)
            warnings.append(msg)
        moved = [r["page"] for r in rows if r["page"] - 1 < len(prev_rows) and abs(r["lines"] - prev_rows[r["page"] - 1]["lines"]) > 8]
        if moved:
            print("Páginas con cambios grandes de líneas (> 8): %s. Un bloque pudo moverse de página." % ", ".join(map(str, moved)))
    print("\nRESULTADO: %s" % ("OK, sin avisos" if not warnings else "%d aviso(s)" % len(warnings)))
    for w in warnings:
        print(" - " + w)
    sys.exit(1 if (warnings and a.strict) else 0)


if __name__ == "__main__":
    main()
