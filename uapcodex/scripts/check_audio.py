"""Verifica la locución de un vídeo/audio final: transcripción, marcas de tiempo por palabra y sonoridad.

Uso: python uapcodex/scripts/check_audio.py video.mp4 [--words]
  - Transcribe con faster-whisper small.en SOBRE LA MEZCLA COMPLETA (voz+música+SFX):
    en la mezcla aparecen errores que la frase aislada no tiene (p. ej. "Case 21" -> "Face 21").
  - --words imprime marcas por palabra (útil para sincronizar subtítulos).
  - Imprime LUFS integrados y pico (objetivo redes: -14 LUFS, pico <= -1.5 dBFS).
"""
import subprocess, sys
from faster_whisper import WhisperModel

path = sys.argv[1]; words = "--words" in sys.argv
m = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(path, word_timestamps=words)
for s in segs:
    print(f"{s.start:6.2f}-{s.end:6.2f} {s.text.strip()}")
    if words:
        print("        " + " ".join(f"{w.word.strip()}@{w.start:.2f}" for w in s.words))
out = subprocess.run(["ffmpeg", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
print("\n".join(l.strip() for l in out.splitlines()[-12:] if "I:" in l or "Peak:" in l))
