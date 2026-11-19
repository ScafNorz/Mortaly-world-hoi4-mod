"""Портреты ORD, DLD, HMS, PCL из tools/avatars (этап 23). Запуск из папки mortaly_world: python ../tools/install_new_portraits.py
Результат: gfx/leaders/<TAG>/<TAG>_leader.tga (156x210, 32 бит)."""
from PIL import Image
import os
base = os.path.dirname(os.path.abspath(__file__))
SRC = {'DLD': ('Dead land leader teba(Теба).png', None), 'HMS': ('Hippomotoswamp leader Moto(Мото).png', 0.12),
       'ORD': ('Order empire leader Gena(Гена).png', None), 'PCL': ('Peace land leader Scaf&Yuri(Скаф и Юри).png', 0.20)}
for tag, (f, fx) in SRC.items():
    im = Image.open(os.path.join(base, 'avatars', f)).convert('RGBA'); w, h = im.size
    m = int(min(w, h) * 0.012)  # срезать тёмную рамку по краям
    im = im.crop((m, m, w - m, h - m)); w, h = im.size
    cw = int(h * 156 / 210)
    x0 = int((w - cw) / 2) if fx is None else int(w * fx)
    x0 = max(0, min(w - cw, x0))
    out = im.crop((x0, 0, x0 + cw, h)).resize((156, 210), Image.LANCZOS)
    d = os.path.join(base, '..', 'mortaly_world', 'gfx', 'leaders', tag); os.makedirs(d, exist_ok=True)
    out.save(os.path.join(d, f'{tag}_leader.tga')); print(tag, 'ok')
