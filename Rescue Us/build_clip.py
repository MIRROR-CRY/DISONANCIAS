"""Rescue Us: clip vertical (9:16) para Reels / TikTok / Stories, generado desde el audio de la canción.

Uso:
    python3 build_clip.py --start 95 --seconds 30 --layout stories   # final del puente y último coro

Qué hace:
  1. Corta el tramo del mix (audio/backing_track_with_intro.wav) por segundo, con fundidos y -14 LUFS.
  2. Compone el video: portada con fondo desenfocado y zoom lento, onda de audio,
     "PONTE AUDÍFONOS" al inicio y luego el nombre de la banda.
Requiere ffmpeg en el PATH y portada.png (recorte de la portada, junto a este script).
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
FONTS = {  # (negrita, normal) en el primer sistema donde existan
    "bold": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "/Library/Fonts/Arial Bold.ttf", r"C:\Windows\Fonts\arialbd.ttf"],
    "regular": ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/Library/Fonts/Arial.ttf", r"C:\Windows\Fonts\arial.ttf"],
}
BAND, HANDLE = "RESCUE US", "@mirrorcry.music"
INTRO_TEXT, INTRO_SECONDS = "MIRROR CRY", 3.5  # artista primero, luego el tema

# Posiciones en px sobre un lienzo de 1080x1920. "stories" deja libres la parte alta
# (~270 px) y la baja (~380 px), que tapan la interfaz de Stories / Reels / TikTok.
LAYOUTS = {
    "full":    dict(photo=1080, cy=880, wave_y=1450, wave_h=240, intro_y=150, band_y=120, handle_y=205),
    "stories": dict(photo=900,  cy=870, wave_y=1380, wave_h=150, intro_y=300, band_y=285, handle_y=365),
}


def find_font(kind):
    for p in FONTS[kind]:
        if os.path.isfile(p):
            return p
    sys.exit(f"No se encontró una fuente {kind}. Edita FONTS en build_clip.py.")


def esc(path):  # ffmpeg: ':' y '\' en rutas dentro de filtros
    return path.replace("\\", "/").replace(":", r"\:")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg falló:\n{r.stderr}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--start", type=float, default=95.0, help="segundo de inicio (default 95)")
    ap.add_argument("--seconds", type=float, default=15.0, help="duración (default 15)")
    ap.add_argument("--layout", choices=sorted(LAYOUTS), default="full",
                    help="'stories' respeta las zonas seguras de la interfaz (default: full)")
    ap.add_argument("--cover", default=os.path.join(PROJECT_DIR, "portada.png"))
    args = ap.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("No se encontró ffmpeg en el PATH.")
    if not os.path.isfile(args.cover):
        sys.exit(f"Falta la portada: {args.cover}")
    wav = os.path.join(PROJECT_DIR, "audio", "backing_track_with_intro.wav")
    if not os.path.isfile(wav):
        sys.exit(f"No existe {wav}")

    start = args.start
    dur = args.seconds
    L = LAYOUTS[args.layout]
    suffix = "" if args.layout == "full" else f"_{args.layout}"
    out = os.path.join(PROJECT_DIR, f"rescue_us_clip_{dur:g}s{suffix}.mp4")
    bold, regular = esc(find_font("bold")), esc(find_font("regular"))
    print(f"Clip: {start:.2f} s a {start + dur:.2f} s -> {os.path.basename(out)}")

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
[b]scale=w='{L['photo']}*(1+0.04*t/{dur:g})':h=-1:eval=frame[fg];
[1:a]asplit[a1][a2];
[a2]showwaves=s=1080x{L['wave_h']}:mode=cline:colors=white:rate=30,format=rgba,colorchannelmixer=aa=0.85[wv];
[bg][fg]overlay=x=(W-w)/2:y={L['cy']}-h/2[v1];
[v1][wv]overlay=0:{L['wave_y']}[v2];
[v2]drawtext=fontfile={bold}:text='{INTRO_TEXT}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y={L['intro_y']}:alpha='if(lt(t,0.3),t/0.3,if(gt(t,{t_in}),max(0,1-(t-{t_in})/0.5),1))'[v3];
[v3]drawtext=fontfile={bold}:text='{BAND}':fontcolor=white:fontsize=64:x=(w-text_w)/2:y={L['band_y']}:alpha='{fade_in}'[v4];
[v4]drawtext=fontfile={regular}:text='{HANDLE}':fontcolor=white@0.85:fontsize=36:x=(w-text_w)/2:y={L['handle_y']}:alpha='{fade_in}'[v]
"""
        run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-t", f"{dur:g}",
             "-i", args.cover, "-i", audio, "-filter_complex", graph,
             "-map", "[v]", "-map", "[a1]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
             "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k",
             "-movflags", "+faststart", "-t", f"{dur:g}", out])
    print(f"Listo: {out}")


if __name__ == "__main__":
    main()
