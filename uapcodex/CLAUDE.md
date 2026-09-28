# Vídeos de UAP Codex — guía para futuras sesiones

Guía para producir vídeos promocionales de **uapcodex.org**, un sitio de investigación sobre evidencia UAP, con OpenMontage. Recoge lo que funcionó y lo que el usuario rechazó en los vídeos del caso 396, Nimitz (36), Colares (20), Release 06 y Manises (21). Tiene prioridad sobre las rutas genéricas de `AGENT_GUIDE.md` en lo relativo a estos vídeos.

**Idioma:** hablar con el usuario en español. Los vídeos van en inglés.

## 0. Reglas del usuario (obligatorias)
- Ser correcto antes que sonar seguro. Si algo no está verificado, decirlo ("no estoy seguro", "deberías verificarlo").
- **Nunca inventar fuentes, citas, cifras ni eslóganes.** Todo dato del vídeo sale de la ficha del caso en `uapcodex.org/cases/<slug>/` o de una fuente primaria nombrada.
  - Ejemplo de error cometido: se escribió "EVIDENCE · NOT BELIEF" como lema del sitio y hubo que quitarlo.
- Separar hechos de interpretación. Incluir siempre la **visión escéptica** del caso si la ficha la tiene; da credibilidad.
- Toda imagen que no sea documental lleva en pantalla **"AI-GENERATED ILLUSTRATIONS · RECONSTRUCTION, NOT FOOTAGE"**, o "ILLUSTRATION, NOT FOOTAGE".
- Para fotos con licencia CC-BY, atribución en pantalla. En SCRIPT.md, anotar la licencia de cada recurso.
- Avisar de lo que no se pudo verificar al entregar.

## 1. Formato por defecto
- **1:1, 1080×1080, 30 s, locución en inglés**, pensado para Instagram. El 9:16 "se cortaba" en su feed.
- Nombre del entregable: `projects/<caso>/renders/<caso>-1x1-30s-ig.mp4`. Debe pesar **menos de 30 MB**, porque `SendUserFile` rechaza archivos mayores.

## 2. Flujo de trabajo (en este orden)
1. **Investigar** la ficha del caso **en el momento de producir**; no fiarse de notas de sesiones anteriores. Escribir `projects/<caso>/SCRIPT.md` con una tabla de escenas, datos con su fuente y fecha de consulta, y una sección "Pendiente de verificar".
   - ⚠️ Lección de Manises: las notas antiguas decían 78%, "intense red lights", "radar contact" y Palma → Las Palmas. La ficha del 2026-09-28 dice **50%**, "two steady red lights, without flashing", "**no** radar contact" y JK-297 Palma → Tenerife; además, Mach 1.4 es una declaración posterior del piloto, no un dato del expediente.
   - Pide a WebFetch el **texto literal**, no un resumen. Vuelve a comprobar cada cifra del vídeo **justo antes de renderizar**.
   - Distingue en pantalla lo que dice el expediente de lo que son declaraciones posteriores (p. ej. "PILOT'S LATER CLAIM · NOT IN THE FILE").
2. **Guion:** unas 60–65 palabras para 30 s, en unas 6 frases.
   - Estructura: gancho → incidente → escalada → dato clave → visión escéptica → CTA.
   - Frase final: **"Read case <N>, at U A P Codex dot org."** Con "Case <N>." a secas, la mezcla se oía como "Face 21".
3. **Imágenes: enseñar primero al usuario** una hoja de contactos y esperar su visto bueno antes de producir. Ver §3.
4. **Capas:** recortar sujetos con `scripts/cutout.py` y borrar luces u objetos pintados que se vayan a animar.
5. **Locución** con `scripts/tts.py` (voz `bm_george`). Ver §4.
6. **Audio:** música de Pixabay, efectos y mezcla. Ver §5.
7. **Composición HyperFrames** a partir de `templates/collage-1x1/index.html`. Ver §6.
8. **Verificar y entregar.** Ver §7.

## 3. Imágenes (lo que el usuario acepta y rechaza)
- ❌ **Rechazado:** fotos de archivo o de Wikimedia de museo ("muy malas, poco artísticas y de baja calidad") y el 3D hecho con código en Three.js ("muy pobre la calidad").
- ✅ **Aceptado:** ilustraciones de IA en estilo **collage de papel recortado de los años 70 (tipo Terry Gilliam)**, generadas con Canva (`mcp__Canva__generate-image`, `aspectRatio: SQUARE_1_1`).
  - Sufijo de prompt que funcionó:
    > `Vintage 1970s cut-paper collage illustration, Terry Gilliam style: <escena>. Halftone print grain, torn paper edges, muted cream, navy and crimson palette, dramatic cinematic composition, high detail. No people, no faces, no text.`
  - Quita "No people, no faces" si la escena necesita personas, como la cabina.
  - Si falta, añade al prompt los detalles de exactitud: escarapelas españolas rojo-amarillo-rojo, tipo de avión, etc.
- **Revisar cada imagen** en busca de errores: tipo de aeronave, escarapelas de otro país o caras sueltas que no vienen a cuento. Regenerar si hace falta.
- **Descargar en 1080 px** (la miniatura que devuelve generate-image es de solo 200 px):
  1. `create-design` (formato "Instagram Post (Square)").
  2. `read-design` con `open_transaction`.
  3. `edit-design` con `update_fill` en el fondo de cada página y `add_page` para las siguientes.
  4. `commit` (con el permiso del usuario para crear el diseño).
  5. `export-design {type:"png"}` **sin width/height**; con tamaño personalizado devolvió "Not allowed".
- Material documental real, cuando lo haya:
  - DVIDS (`dvidshub.net/video/<id>` expone los mp4; war.gov da 403).
  - Wikimedia: la API da 429, así que usar la URL de miniatura `thumb/{md5[0]}/{md5[:2]}/{name}/1280px-{name}`.
  - Verificar la licencia en la página del archivo.

## 4. Voz
- **Actual:** Kokoro **`bm_george`** (británica, tipo documental), elegida por el usuario entre 6 muestras.
  - Usar `--speed 1.0` y recortar silencios; eso lo hace `tts.py`.
- Descartadas:
  - Piper ("robótica").
  - `am_fenrir` sin tratamiento ("poco profesional").
- **Higgsfield "Jasper"** (`text2speech_v2`, variante `seed_speech`, preset `a7b8abe9-47f1-553e-a9df-87945a7e5bc8`) le gustó.
  - Cuesta unos 0,8 créditos por 30 s y el plan gratuito tenía 0,28.
  - Comprobar el coste con `get_cost:true` y ofrecérselo solo si hay saldo.
- **Tratamiento de locutor** (aplicar a la pista de voz completa):
  ```
  highpass=f=70,equalizer=f=150:t=q:w=1:g=3,equalizer=f=3000:t=q:w=1.5:g=2.5,equalizer=f=7500:t=q:w=2:g=-2,
  acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=4,aecho=0.8:0.5:28:0.07,loudnorm=I=-16:TP=-1.5
  ```
- Pistas de 30 s con `adelay` por frase, `amix=normalize=0`, `apad=whole_dur=30` y `-t 30`. Todas deben durar exactamente 30 s.

## 5. Música y efectos
- **Música:** Pixabay, con la herramienta `pixabay_music` de OpenMontage; anotar título, autor y licencia.
  - Hay que darle **estructura** con una expresión `volume` de ffmpeg:
    - subida en la persecución o la escalada;
    - golpe (efecto `hit`) en el dato clave, como "Mach 1.4";
    - **bajada casi a silencio unos 0,5 s antes del cierre**;
    - fade final.
  - Nivel en la composición: unos 0,34.
  - **Ducking obligatorio** con la voz como clave de sidechain: `[music][vo]sidechaincompress=threshold=0.012:ratio=10:attack=15:release=350`.
  - Objetivo: música unos 12 LU por debajo de la voz mientras se habla. Sin ducking quedaba solo unos 3,6 LU por debajo y restaba claridad a la voz.
- **Efectos** sintetizados con `ffmpeg aevalsrc` (boom, ping, riser, hit, whoosh, papel).
  - No deben pisar palabras clave de la voz. Adelantar el efecto y verificar con Whisper.
- **Máster final:** `loudnorm=I=-14:TP=-1.5`.

## 6. Composición (HyperFrames + GSAP)
- Partir de `templates/collage-1x1/index.html`: es el vídeo de Manises v2 y sirve de ejemplo completo. Hay que cambiar:
  - las escenas (`s1…s7`);
  - `CAPS`, los subtítulos;
  - los textos y las posiciones de luces y halos;
  - los tiempos.
- `bash uapcodex/scripts/setup.sh` descarga GSAP en `assets/gsap.min.js`. GSAP y las fuentes deben ser **locales**: la CDN falla en Chrome headless por el certificado.
- Reglas técnicas:
  - La estructura exige `data-composition-id` / `data-start` / `data-duration` / `data-track-index`, la clase `clip` y la línea de tiempo pausada en `window.__timelines["main"]`.
  - Estados iniciales en CSS. `immediateRender:false` en los `fromTo` posteriores.
  - **Nada de tweens relativos (`"-=10"`) sobre una propiedad que otro tween esté animando**: el linter lo marca como error. Usar un div envoltorio.
  - Easing `steps(n)` para el efecto stop-motion.
  - Solo fuentes con `@font-face`. Para el ▲, usar "DejaVu Sans Mono".
  - Playwright/Chromium: `executable_path='/opt/pw-browsers/chromium'`.
- **Checklist de edición**, de la crítica que el usuario pidió como "experto editor":
  1. **Gancho en el primer segundo:** pregunta grande en papel, p. ej. "What were the / *red lights?*".
  2. **Recortes animados por capas.** No hacer un pase de diapositivas con zoom: el sujeto se mueve sobre su fondo, las luces entran y se van.
  3. **Subtítulos** grandes en tiras de papel (Inter 600, 46 px, palabras clave en rojo), sincronizados con `check_audio.py --words`. No duplicar texto que ya esté en pantalla.
  4. **Transiciones variadas:** empujón de papel, corte seco con destello, rasgado (clip-path dentado), corte a negro, golpe de escala en el cierre.
  5. **Coherencia imagen-texto:** si dice "it slips away", la luz tiene que irse. Borrar la luz pintada y animarla.
  6. **Tamaños mínimos para móvil:** crédito 17 px, etiquetas 26 px, sellos 30 px o más.
  7. **Ritmo:** ninguna escena estática de más de unos 3 s sin algo que cambie.
  8. **Portada = fotograma 0:** el gancho y el elemento clave (p. ej. las luces) ya visibles en t=0, sin animación de entrada. Instagram usa ese fotograma como portada si no se elige otra.
  9. **Nada cruza los subtítulos:** las piezas entran por arriba o por los lados, nunca desde abajo mientras hay un subtítulo en pantalla.
  10. **Sin fotogramas vacíos:** ni notas vacías antes del texto tecleado ni fondos sin elementos al empezar una escena.
  11. **Los recortes no deben salirse del cuadro** (deriva del avión, alas); movimiento moderado para no enseñar el hueco del fondo.
  12. **Pronunciación de nombres propios:** `bm_george` dijo "Manny's" por Manises. Usar `[Manises](/manˈisɛs/)` y verificar con Whisper.

## 7. Marca UAP Codex
- Colores:
  - fondo `#171717` / `#0a0e1a`
  - rojo `#c41e3a`
  - rosa `#ee6075` ("Codex" sobre fondo oscuro)
  - crema `#f7f2e8` / papel `#efe5cf`
  - tinta `#1a1a1a`
- Fuentes: **Fraunces** (display; variable, con eje `opsz`) e **Inter** (sans). Las etiquetas van en monoespaciada.
- **Logo (fiel al marcado de la web):**
  - cuadrado rojo con "▲" en monoespaciada (32 px / 14 px en la web);
  - "UAP" + "*Codex*" en Fraunces 500, `letter-spacing:-0.025em`;
  - "Codex" en cursiva roja sobre fondo claro, o `#ee6075` sobre fondo oscuro.
  - Al escalarlo, fijar **`font-variation-settings:"opsz" 30`**; si no, sale con demasiado contraste.
  - Hay una tarjeta de cierre con logo, CTA y etiquetas en la plantilla (escena `s7`).
- **Datos del cierre:** usar solo lo que diga la ficha (Tier, "Probability: NN%", fecha de desclasificación). Las fichas usan la etiqueta "Probability" (comprobado en Manises, 2026-09-28).

## 8. Verificar y entregar
1. `npx hyperframes lint` con 0 errores. Luego `npx hyperframes snapshot --at <t1,t2,…> -o snaps .` y **mirar las hojas de contactos**.
2. `npx hyperframes render -o ../renders/<caso>-master.mp4 .`
3. Recomprimir: `ffmpeg -i master.mp4 -c:v libx264 -crf 20 -preset slow -pix_fmt yuv420p -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -movflags +faststart <caso>-1x1-30s-ig.mp4`
4. `python uapcodex/scripts/check_audio.py <ig.mp4>`: la transcripción debe coincidir con el guion, con unos -14 LUFS.
5. Enviar con `SendUserFile` y resumir qué se verificó y qué queda pendiente.

## 9. Entorno (avisos)
- **`projects/` está en `.gitignore`.** Los renders y recursos de cada vídeo **no se guardan en git**, y el contenedor en la nube es temporal: entregar siempre los archivos con `SendUserFile`. Las ilustraciones quedan además en el Canva del usuario.
- Lo reutilizable (esta guía, plantilla y scripts) vive en `uapcodex/` y sí se versiona.
- La cuota de ZeroGPU de Hugging Face y los créditos de Higgsfield suelen estar agotados. Para vídeo con IA hace falta fal.ai (unos 2 $ por 30 s, dato estimado en su momento, **sin verificar**), créditos o una GPU local.
