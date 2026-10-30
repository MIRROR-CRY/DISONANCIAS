"""Mirror Cry: video de lyrics (16:9) con la palabra cantada resaltada, audio de Bandcamp.

Uso: python3 build_lyrics.py AUDIO.mp3 [salida.mp4]

Tiempos reales marcados a mano con lipsync (mirror_cry_timing.json).
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

ACCENT = (255, 92, 120)
TOTAL = 184.04


def wrap_draw(d, text, font, y, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)


def bg():
    im = Image.open(os.path.join(HERE, "portada_bandcamp.jpg")).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1))
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width + W) // 2, (im.height + H) // 2))
    im = im.filter(ImageFilter.GaussianBlur(28))
    return ImageEnhance.Brightness(im).enhance(0.32)


def slide(base, words, n, chorus, title=False):
    im = base.copy()
    d = ImageDraw.Draw(im)
    if title:
        wrap_draw(d, "MIRROR CRY", ImageFont.truetype(B, 150), 400, (255, 255, 255))
        wrap_draw(d, "@mirrorcry.music", ImageFont.truetype(R, 48), 620, (190, 200, 230))
    elif words:
        f = ImageFont.truetype(B, 92 if chorus else 80)
        sp = d.textlength(" ", font=f)
        ws = [d.textlength(w, font=f) for w in words]
        x = (W - sum(ws) - sp * (len(ws) - 1)) / 2
        for i, (w, wd) in enumerate(zip(words, ws)):
            col = ACCENT if i == n else ((255, 255, 255) if i < n else (120, 124, 140))
            d.text((x, 470), w, font=f, fill=col, stroke_width=3, stroke_fill=(0, 0, 0))
            x += wd + sp
    return im


def main():
    audio = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "mirror_cry_lyrics.mp4")
    base = bg()
    data = json.load(open(os.path.join(HERE, "mirror_cry_timing.json")))
    ev = []   # (inicio, fin, palabras, n resaltada, coro, titulo)
    for sec in data["sections"]:
        chorus = sec["section"].startswith("Chorus") or sec["section"] == "Post-Chorus"
        for ln in sec["lines"]:
            ws = [w["text"] for w in ln["words"]]
            for i, w in enumerate(ln["words"]):
                end = ln["words"][i + 1]["start"] if i + 1 < len(ws) else w["end"] + 0.3
                ev.append((w["start"], end, ws, i, chorus, False))
    full, last = [(0, ev[0][0], None, 0, False, True)], 0
    for e in ev:
        if e[0] > last + 1e-6 and last:
            full.append((last, e[0], None, 0, False, False))
        full.append(e); last = e[1]
    full.append((last, TOTAL, None, 0, False, False))
    ev = full
    with tempfile.TemporaryDirectory() as td:
        cat = []
        for i, (a, e, t, n, c, ti) in enumerate(ev):
            p = os.path.join(td, f"s{i}.png")
            slide(base, t, n, c, ti).save(p)
            cat += [f"file '{p}'", f"duration {e - a:.4f}"]
        cat.append(f"file '{p}'")
        lst = os.path.join(td, "l.txt")
        open(lst, "w").write("\n".join(cat))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", audio,
                        "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac",
                        "-b:a", "192k", "-shortest", out], check=True)
    print(out)


main()
