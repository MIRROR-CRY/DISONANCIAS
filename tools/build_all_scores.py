#!/usr/bin/env python3
"""Regenerate every score in the album with one command."""

import os
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONGS = ["Kicking Stones v2", "Rescue Us", "Medio Limón", "sin titulo (indie-folk)"]

def main():
    failed = []
    print("Partituras del album\n")
    for song in SONGS:
        script = os.path.join(BASE, song, "generate_score.py")
        if not os.path.exists(script):
            print(f"  {song}: sin generate_score.py"); failed.append(song); continue
        r = subprocess.run([sys.executable, script], capture_output=True, text=True,
                           cwd=os.path.join(BASE, song))
        if r.returncode != 0:
            print(f"  {song}: FALLO\n{r.stderr[-1200:]}"); failed.append(song)
        else:
            print(r.stdout.rstrip())
    print()
    if failed:
        print(f"Fallaron: {', '.join(failed)}"); return 1
    print(f"{len(SONGS)} partituras generadas.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
