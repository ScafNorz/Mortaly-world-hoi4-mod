#!/usr/bin/env python3
"""Превращает картинки друзей во флаги и портреты лидеров.
Положи картинки в папку avatars/ рядом со скриптом, назвав по тегу страны:
  YOZ.png  VMP.jpg  WWF.png ...   (теги: YOZ VMP WWF CRL PCL BLI ORD FOX HMS SVB DLD OVS)
Запуск:  python convert_avatars.py "C:\\путь\\к\\папке\\mortaly_world"
Нужен Python 3 и Pillow:  pip install pillow
"""
import sys, os, glob
from PIL import Image

mod = sys.argv[1] if len(sys.argv) > 1 else 'mortaly_world'
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'avatars')

def fit(im, size):
    """обрезка по центру под нужное соотношение сторон"""
    w, h = im.size; tw, th = size
    k = max(tw / w, th / h)
    im = im.resize((max(tw, round(w * k)), max(th, round(h * k))), Image.LANCZOS)
    x, y = (im.width - tw) // 2, (im.height - th) // 2
    return im.crop((x, y, x + tw, y + th))

n = 0
for f in glob.glob(os.path.join(src, '*')):
    tag, ext = os.path.splitext(os.path.basename(f))
    if ext.lower() not in ('.png', '.jpg', '.jpeg', '.webp', '.bmp'): continue
    tag = tag.upper(); im = Image.open(f).convert('RGBA')
    for d, sz in (('', (82, 52)), ('medium/', (41, 26)), ('small/', (10, 7))):
        p = os.path.join(mod, 'gfx', 'flags', d, tag + '.tga'); os.makedirs(os.path.dirname(p), exist_ok=True)
        fit(im, sz).save(p)
    p = os.path.join(mod, 'gfx', 'leaders', tag, tag + '_leader.tga'); os.makedirs(os.path.dirname(p), exist_ok=True)
    fit(im, (156, 210)).save(p)
    print('ok', tag); n += 1
print('готово, обработано:', n)
