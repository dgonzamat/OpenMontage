"""Separa un sujeto (avión, persona…) de una ilustración para animarlo como recorte de papel.

Genera:
  <out>_cut.png : sujeto con alfa binaria + borde de papel crema (look collage)
  <out>_bg.jpg  : fondo sin el sujeto (hueco relleno con el color del entorno)

Uso:
  python uapcodex/scripts/cutout.py scene.png out/s1 --box 0,270,1080,780 \
      [--poly "0,498 0,540 425,648 440,588"] [--erase "104,362,125" "832,578,140"]

  --box    recorte donde buscar el sujeto (rembg funciona mejor con el sujeto grande en el recorte)
  --poly   polígonos extra (x,y separados por espacio) para piezas finas que rembg pierde (alas, colas);
           dentro del polígono solo se añaden píxeles más claros que el cielo (luminancia > --lum)
  --erase  círculos cx,cy,r a borrar del fondo (p. ej. luces pintadas que luego se animan en CSS)

Notas aprendidas:
  - Modelo 'isnet-general-use' > 'u2net' para estas ilustraciones.
  - Si el recorte sale semitransparente o roto (pasó con un Mirage), no forzarlo: dejar esa escena plana.
  - El relleno queda liso; mover el recorte poco (±60–100 px) para no enseñar el hueco.
"""
import argparse
import numpy as np, cv2
from PIL import Image
from rembg import remove, new_session

ap = argparse.ArgumentParser()
ap.add_argument("image"); ap.add_argument("out")
ap.add_argument("--box", required=True)
ap.add_argument("--poly", nargs="*", default=[])
ap.add_argument("--erase", nargs="*", default=[])
ap.add_argument("--lum", type=float, default=55)
ap.add_argument("--edge", type=int, default=7)
a = ap.parse_args()

img = np.array(Image.open(a.image).convert("RGB"))
H, W = img.shape[:2]
box = tuple(int(v) for v in a.box.split(","))
cut = remove(Image.fromarray(img).crop(box), session=new_session("isnet-general-use"))
alpha = np.zeros((H, W), np.uint8)
alpha[box[1]:box[3], box[0]:box[2]] = np.array(cut)[..., 3]
alpha = (alpha > 100).astype(np.uint8) * 255
if a.poly:
    pm = np.zeros((H, W), np.uint8)
    for p in a.poly:
        pts = np.array([[int(v) for v in xy.split(",")] for xy in p.split()], np.int32)
        cv2.fillPoly(pm, [pts], 255)
    alpha = np.maximum(alpha, ((pm > 0) & (img.mean(axis=2) > a.lum)).astype(np.uint8) * 255)
alpha = cv2.medianBlur(cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)), 5)

# recorte con borde de papel
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (a.edge * 2 + 1,) * 2)
outline = cv2.dilate(alpha, k)
rgba = np.zeros((H, W, 4), np.uint8); rgba[..., :3] = (239, 229, 207); rgba[..., 3] = outline
m = alpha > 0; rgba[m, :3] = img[m]
Image.fromarray(rgba).save(a.out + "_cut.png")

# fondo: relleno por desenfoque normalizado (mejor que cv2.inpaint en huecos grandes)
mk = cv2.dilate(outline, np.ones((25, 25), np.uint8))
for e in a.erase:
    cx, cy, r = (int(v) for v in e.split(",")); cv2.circle(mk, (cx, cy), r, 255, -1)
valid = (mk == 0).astype(np.float32); f = img.astype(np.float32)
sm = cv2.GaussianBlur(f * valid[..., None], (0, 0), 45) / (cv2.GaussianBlur(valid, (0, 0), 45)[..., None] + 1e-4)
sm += np.random.default_rng(1).normal(0, 6, f.shape)
soft = cv2.GaussianBlur(mk.astype(np.float32) / 255, (0, 0), 6)[..., None]
Image.fromarray(np.clip(f * (1 - soft) + sm * soft, 0, 255).astype(np.uint8)).save(a.out + "_bg.jpg", quality=92)
print("ok:", a.out + "_cut.png", a.out + "_bg.jpg")
