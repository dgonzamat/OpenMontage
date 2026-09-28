#!/usr/bin/env bash
# Prepara un contenedor nuevo para producir vídeos de UAP Codex.
# Uso: bash uapcodex/scripts/setup.sh
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

command -v ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg)
pip install -q -r "$ROOT/requirements.txt"
# kokoro (voz local) necesita esta variable para compilar docopt
SETUPTOOLS_USE_DISTUTILS=stdlib pip install -q kokoro soundfile
pip install -q rembg opencv-python-headless faster-whisper

# GSAP no se versiona en el repo: se descarga aquí (misma versión probada)
curl -sSL -o "$ROOT/uapcodex/templates/collage-1x1/assets/gsap.min.js" \
  https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js

echo "OK. HyperFrames: npx hyperframes --help (en la plantilla: npx hyperframes lint/snapshot/render)"
