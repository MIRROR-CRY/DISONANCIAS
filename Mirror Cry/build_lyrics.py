"""Mirror Cry: video de lyrics (16:9) con el audio de Bandcamp o un mix local.

Uso: python3 build_lyrics.py AUDIO.mp3 [salida.mp4]

Los tiempos salen de la estructura de build_song.py (156 BPM, 1 compas = 1.538 s): son una
estimacion por compases, no un alineado con la voz. Ajusta LINES si algo queda corrido.
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
BAR = 60 / 156 * 4
W, H = 1920, 1080
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# (compas de inicio, duracion en compases, texto)
LINES = [(8, 4, "Why should I stay AS-IS?"), (12, 4, "If I can be TO-BE?"),
         (16, 4, "From years ago, the Miss"), (20, 4, "Taught me the verb To Be"),
         (24, 4, "Trapped in an iron cage"), (28, 4, "Sisyphus wasn't like this"),
         (32, 4, "Just knowing what to do"), (36, 4, "Won't happen any day"),
         (48, 4, "In front of the perfect girl"), (52, 4, "Faking a perfect day"),
         (56, 4, "No way I won't say hello"), (60, 4, "Watching me ruin it again")]
for s in (76, 92):
    LINES += [(s, 4, "It's a mirror cry driving me"), (s + 4, 4, "A ghost that won't let me be"),
              (s + 8, 4, "I won't lose the opportunity"), (s + 12, 4, "And that's why I'll miss it")]
LINES += [(108, 2, "I thought I was in front of her"), (110, 2, "I thought it was the great chance"),
          (112, 2.4, "I look through the glass..."), (114.5, 4, "...BUT I'M IN FRONT OF ME AGAIN!")]
CHORUS = {76, 80, 84, 88, 92, 96, 100, 104}
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


def slide(base, text, chorus, title=False):
    im = base.copy()
    d = ImageDraw.Draw(im)
    if title:
        wrap_draw(d, "MIRROR CRY", ImageFont.truetype(B, 150), 400, (255, 255, 255))
        wrap_draw(d, "@mirrorcry.music", ImageFont.truetype(R, 48), 620, (190, 200, 230))
    elif text:
        f = ImageFont.truetype(B, 92 if chorus else 80)
        wrap_draw(d, text, f, 470, (255, 255, 255) if chorus else (225, 230, 245))
    return im


def main():
    audio = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "mirror_cry_lyrics.mp4")
    base = bg()
    ev = [(0, LINES[0][0] * BAR, None, False, True)]
    for i, (b, n, t) in enumerate(LINES):
        a, e = b * BAR, (b + n) * BAR
        if ev and ev[-1][1] < a - 1e-6:
            ev.append((ev[-1][1], a, None, False, False))
        ev.append((a, e, t, int(b) in CHORUS, False))
    ev.append((ev[-1][1], TOTAL, None, False, False))
    with tempfile.TemporaryDirectory() as td:
        cat = []
        for i, (a, e, t, c, ti) in enumerate(ev):
            p = os.path.join(td, f"s{i}.png")
            slide(base, t, c, ti).save(p)
            cat += [f"file '{p}'", f"duration {e - a:.4f}"]
        cat.append(f"file '{p}'")
        lst = os.path.join(td, "l.txt")
        open(lst, "w").write("\n".join(cat))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", audio,
                        "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac",
                        "-b:a", "192k", "-shortest", out], check=True)
    print(out)


main()
