"""Mirror Cry: clip TikTok 9:16 con letra palabra por palabra sobre el coro (el hook).

Uso: python3 build_tiktok.py AUDIO.mp3 [salida.mp4]

Tiempos por compases (156 BPM) con reparto por silabas dentro de cada verso; no es un
alineado con la voz. Ajusta START_BAR / LINES si algo queda corrido.
"""
import os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
BEAT = 60 / 156
BAR = BEAT * 4
W, H, FPS = 1080, 1920, 30
START_BAR, END_BAR = 74, 92          # 2 compases de entrada + coro completo
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
ACCENT, WHITE, DIM = (255, 92, 120), (255, 255, 255), (120, 124, 140)
LINES = [(76, "It's a mirror cry driving me"), (80, "A ghost that won't let me be"),
         (84, "I won't lose the opportunity"), (88, "And that's why I'll miss it")]
SING = 3.4 * BAR / 4 * 4 / 4         # fraccion del verso (4 compases) donde se canta
SING = BAR * 3.3


def syl(w):
    return max(1, len(re.findall(r"[aeiouy]+", w.lower())))


def words_timed():
    out = []
    for b, text in LINES:
        ws = text.split()
        tot = sum(syl(w) for w in ws)
        t, a = 0.0, b * BAR
        line = []
        for w in ws:
            d = SING * syl(w) / tot
            line.append((w, a + t, a + t + d))
            t += d
        out.append(line)
    return out


def bg():
    im = Image.open(os.path.join(HERE, "portada.png")).convert("RGB")
    s = max(W / im.width, H / im.height) * 1.12
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1))
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width + W) // 2, (im.height + H) // 2))
    return ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(22))).enhance(0.45)


def fit(ws, d, size):
    f = ImageFont.truetype(B, size)
    return f


def frame(base, t, lines):
    ph = (t / BEAT) % 1.0
    pulse = np.exp(-ph * 5)                       # golpe en cada pulso
    z = 1 + 0.035 * pulse
    im = base.resize((int(W * z), int(H * z)))
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width + W) // 2, (im.height + H) // 2))
    im = ImageEnhance.Brightness(im).enhance(0.85 + 0.35 * pulse)
    d = ImageDraw.Draw(im)
    d.text((W / 2, 170), "MIRROR CRY", font=ImageFont.truetype(B, 72), fill=WHITE, anchor="mm")
    d.text((W / 2, 245), "@mirrorcry.music", font=ImageFont.truetype(B, 38), fill=(200, 205, 225), anchor="mm")
    cur = next((l for l in lines if l[0][1] - 0.4 <= t < l[-1][2] + 0.9), None)
    if cur:
        # envuelve en 2-3 filas
        rows, row = [], []
        for w in cur:
            if sum(len(x[0]) + 1 for x in row + [w]) > 15 and row:
                rows.append(row); row = []
            row.append(w)
        rows.append(row)
        y = H * 0.5 - (len(rows) - 1) * 80
        for r in rows:
            f = ImageFont.truetype(B, 104)
            widths = [d.textlength(w[0] + " ", font=f) for w in r]
            x = (W - sum(widths) + d.textlength(" ", font=f)) / 2
            for (w, a, e), wd in zip(r, widths):
                if t < a:
                    col, s = DIM, 1
                else:
                    col = ACCENT if t < e + 0.12 else WHITE
                    k = min(1, (t - a) / 0.12)
                    s = 1 + 0.25 * (1 - k) if t < e else 1
                fw = ImageFont.truetype(B, int(104 * s))
                d.text((x + wd / 2, y), w, font=fw, fill=col, anchor="mm",
                       stroke_width=5, stroke_fill=(0, 0, 0))
                x += wd
            y += 160
    d.text((W / 2, H - 150), "PONTE AUDÍFONOS", font=ImageFont.truetype(B, 40), fill=(200, 205, 225), anchor="mm")
    return im


def main():
    audio = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "mirror_cry_tiktok.mp4")
    t0, dur = START_BAR * BAR, (END_BAR - START_BAR) * BAR
    base, lines = bg(), words_timed()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}",
                          "-i", audio, "-af", f"afade=t=out:st={dur - 0.6:.2f}:d=0.6", "-c:v", "libx264",
                          "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-shortest", out],
                         stdin=subprocess.PIPE)
    for i in range(int(dur * FPS)):
        p.stdin.write(frame(base, t0 + i / FPS, lines).tobytes())
    p.stdin.close(); p.wait()
    print(out)


main()
