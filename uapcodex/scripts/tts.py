"""Locución con Kokoro (local, gratis) + recorte de silencios.

Uso:
  python uapcodex/scripts/tts.py lines.json out_dir [--voice bm_george] [--speed 1.0]

lines.json: {"l1": "November, nineteen seventy-nine. ...", "l2": "..."}
  - Una entrada por frase; se colocan luego con adelay en la mezcla.
  - Pronunciación: override con fonemas, p. ej. "[Colares](/kolˈɑɹəs/)".
  - Números y siglas escritos como se dicen ("nineteen seventy-nine", "U A P Codex dot org").
Imprime la duración de cada frase (ya sin silencios) para encajar la línea de tiempo.
"""
import argparse, json, os, subprocess
import numpy as np, soundfile as sf
from kokoro import KPipeline

ap = argparse.ArgumentParser()
ap.add_argument("lines"); ap.add_argument("out")
ap.add_argument("--voice", default="bm_george")  # voz elegida por el usuario (británica, documental)
ap.add_argument("--speed", type=float, default=1.0)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
L = json.load(open(a.lines))
pipe = KPipeline(lang_code="b" if a.voice.startswith("b") else "a")
for k, t in L.items():
    audio = np.concatenate([np.asarray(x[2]) for x in pipe(t, voice=a.voice, speed=a.speed)])
    raw = f"{a.out}/raw_{k}.wav"; sf.write(raw, audio, 24000)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                    f"{a.out}/{k}.wav"], check=True)
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                       "-of", "csv=p=0", f"{a.out}/{k}.wav"]))
    print(f"{k}\t{d:.2f}s\t{t}")
