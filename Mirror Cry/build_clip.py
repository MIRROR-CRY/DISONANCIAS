"""Mirror Cry: clip vertical (9:16) para Reels / TikTok, generado desde el mix de una versión.

Uso:
    python3 build_clip.py                      # última versión, 15 s desde el compás 38,5
    python3 build_clip.py --version 13 --start-bar 38.5 --seconds 15

Qué hace:
  1. Corta el tramo del mix (mirror_cry_base_vN.wav) por compás, con fundidos y -14 LUFS.
  2. Compone el video: portada con fondo desenfocado y zoom lento, onda de audio,
     "PONTE AUDÍFONOS" al inicio y luego el nombre de la banda.
Requiere ffmpeg en el PATH y portada.png (foto, junto a este script).
"""
import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BPM = 156
FONTS = {  # (negrita, normal) en el primer sistema donde existan
    "bold": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "/Library/Fonts/Arial Bold.ttf", r"C:\Windows\Fonts\arialbd.ttf"],
    "regular": ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/Library/Fonts/Arial.ttf", r"C:\Windows\Fonts\arial.ttf"],
}
BAND, HANDLE = "MIRROR CRY", "@mirrorcry.music"
INTRO_TEXT, INTRO_SECONDS = "PONTE AUDÍFONOS", 3.5  # el 3D es el gancho: se avisa al inicio


def find_font(kind):
    for p in FONTS[kind]:
        if os.path.isfile(p):
            return p
    sys.exit(f"No se encontró una fuente {kind}. Edita FONTS en build_clip.py.")


def esc(path):  # ffmpeg: ':' y '\' en rutas dentro de filtros
    return path.replace("\\", "/").replace(":", r"\:")


def latest_version():
    nums = [int(m.group(1)) for f in glob.glob(os.path.join(PROJECT_DIR, "mirror_cry_base_v*.wav"))
            if (m := re.search(r"_v(\d+)\.wav$", f))]
    if not nums:
        sys.exit("No hay mirror_cry_base_vN.wav. Ejecuta build_song.py primero.")
    return max(nums)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg falló:\n{r.stderr}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--version", type=int, default=None, help="versión del mix (por defecto, la última)")
    ap.add_argument("--start-bar", type=float, default=38.5, help="compás de inicio (default 38,5)")
    ap.add_argument("--seconds", type=float, default=15.0, help="duración (default 15)")
    ap.add_argument("--cover", default=os.path.join(PROJECT_DIR, "portada.png"))
    args = ap.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("No se encontró ffmpeg en el PATH.")
    if not os.path.isfile(args.cover):
        sys.exit(f"Falta la portada: {args.cover}")
    v = args.version or latest_version()
    wav = os.path.join(PROJECT_DIR, f"mirror_cry_base_v{v}.wav")
    if not os.path.isfile(wav):
        sys.exit(f"No existe {wav}")

    start = args.start_bar * 4 * 60.0 / BPM
    dur = args.seconds
    out = os.path.join(PROJECT_DIR, f"mirror_cry_clip_{dur:g}s_v{v}.mp4")
    bold, regular = esc(find_font("bold")), esc(find_font("regular"))
    print(f"Clip v{v}: {start:.2f} s a {start + dur:.2f} s (compás {args.start_bar:g}) -> {os.path.basename(out)}")

    with tempfile.TemporaryDirectory() as tmp:
        audio = os.path.join(tmp, "clip_audio.wav")
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{start:.4f}", "-t", f"{dur:g}", "-i", wav,
             "-af", f"afade=t=in:d=0.2,afade=t=out:st={dur - 0.6:g}:d=0.6,loudnorm=I=-14:TP=-1.5:LRA=11",
             "-ar", "44100", audio])

        t_in = INTRO_SECONDS
        fade_in = "if(lt(t,3.8),0,min(1,(t-3.8)/0.5))"
        graph = f"""
[0:v]split[a][b];
[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:5,eq=brightness=-0.25[bg];
[b]scale=w='1080*(1+0.04*t/{dur:g})':h=-1:eval=frame[fg];
[1:a]asplit[a1][a2];
[a2]showwaves=s=1080x240:mode=cline:colors=white:rate=30,format=rgba,colorchannelmixer=aa=0.85[wv];
[bg][fg]overlay=x=(W-w)/2:y=(H-h)/2-80[v1];
[v1][wv]overlay=0:H-h-230[v2];
[v2]drawtext=fontfile={bold}:text='{INTRO_TEXT}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=150:alpha='if(lt(t,0.3),t/0.3,if(gt(t,{t_in}),max(0,1-(t-{t_in})/0.5),1))'[v3];
[v3]drawtext=fontfile={bold}:text='{BAND}':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=120:alpha='{fade_in}'[v4];
[v4]drawtext=fontfile={regular}:text='{HANDLE}':fontcolor=white@0.85:fontsize=36:x=(w-text_w)/2:y=205:alpha='{fade_in}'[v]
"""
        run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-t", f"{dur:g}",
             "-i", args.cover, "-i", audio, "-filter_complex", graph,
             "-map", "[v]", "-map", "[a1]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
             "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k",
             "-movflags", "+faststart", "-t", f"{dur:g}", out])
    print(f"Listo: {out}")


if __name__ == "__main__":
    main()
