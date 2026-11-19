"""Рисует флаги по цветам/символам с фона портретов лидеров.
Запуск из папки мода: python tools/make_flags.py
Результат: mortaly_world/gfx/flags/{,medium/,small/}<TAG>.tga (82x52, 41x26, 10x7, 32 бит)."""
from PIL import Image, ImageDraw
import os
S = 4
W, H = 82 * S, 52 * S

def blank(c):
    im = Image.new('RGBA', (W, H), c); return im, ImageDraw.Draw(im)

def bli():  # синий флаг с белым отпечатком лапы (фон портрета Мяуны)
    im, d = blank((52, 88, 170, 255))
    d.rectangle([0, 0, W, 6 * S], fill=(36, 64, 130, 255)); d.rectangle([0, H - 6 * S, W, H], fill=(36, 64, 130, 255))
    cx, cy = W // 2, H // 2 + 5 * S; wh = (245, 248, 255, 255)
    d.ellipse([cx - 11 * S, cy - 7 * S, cx + 11 * S, cy + 9 * S], fill=wh)
    for dx, dy, r in [(-15, -8, 4.5), (-6, -17, 4.5), (6, -17, 4.5), (15, -8, 4.5)]:
        d.ellipse([cx + (dx - r) * S, cy + (dy - r) * S, cx + (dx + r) * S, cy + (dy + r) * S], fill=wh)
    return im

def wwf():  # серый флаг с тёмным кольцом-эмблемой (фон Красной панды)
    im, d = blank((138, 138, 140, 255))
    cx, cy = W // 2, H // 2; dk = (52, 52, 56, 255)
    d.ellipse([cx - 19 * S, cy - 19 * S, cx + 19 * S, cy + 19 * S], fill=dk)
    d.ellipse([cx - 14 * S, cy - 14 * S, cx + 14 * S, cy + 14 * S], fill=(138, 138, 140, 255))
    d.ellipse([cx - 7 * S, cy - 7 * S, cx + 7 * S, cy + 7 * S], fill=dk)
    return im

def svb():  # тёмно-красный флаг, чёрный крест, фиолетовая диагональ (фон Медоеда)
    im, d = blank((138, 38, 52, 255))
    d.polygon([(W, 0), (W, H), (W // 3, H)], fill=(96, 56, 128, 255))
    k = (22, 14, 20, 255); cx = 22 * S
    d.rectangle([cx - 3 * S, 8 * S, cx + 3 * S, 44 * S], fill=k); d.rectangle([cx - 10 * S, 17 * S, cx + 10 * S, 23 * S], fill=k)
    return im

def ovs():  # фиолетовый флаг с бледной полосой и ромбом (фон Эндергуся)
    im, d = blank((104, 62, 160, 255))
    d.rectangle([0, 0, W, 8 * S], fill=(70, 40, 112, 255)); d.rectangle([0, H - 8 * S, W, H], fill=(70, 40, 112, 255))
    cx, cy = W // 2, H // 2
    d.polygon([(cx, cy - 15 * S), (cx + 15 * S, cy), (cx, cy + 15 * S), (cx - 15 * S, cy)], fill=(214, 190, 235, 255))
    d.polygon([(cx, cy - 8 * S), (cx + 8 * S, cy), (cx, cy + 8 * S), (cx - 8 * S, cy)], fill=(34, 20, 52, 255))
    return im

def crl():  # багровый флаг с чёрной эмблемой-рогами (фон Альцергара)
    im, d = blank((142, 36, 40, 255)); k = (20, 16, 18, 255); cx, cy = W // 2, H // 2
    d.ellipse([cx - 12 * S, cy - 10 * S, cx + 12 * S, cy + 14 * S], fill=k)
    d.polygon([(cx - 12 * S, cy - 2 * S), (cx - 26 * S, cy - 18 * S), (cx - 8 * S, cy - 8 * S)], fill=k)
    d.polygon([(cx + 12 * S, cy - 2 * S), (cx + 26 * S, cy - 18 * S), (cx + 8 * S, cy - 8 * S)], fill=k)
    d.rectangle([cx - 7 * S, cy + 1 * S, cx - 2 * S, cy + 5 * S], fill=(230, 60, 60, 255)); d.rectangle([cx + 2 * S, cy + 1 * S, cx + 7 * S, cy + 5 * S], fill=(230, 60, 60, 255))
    return im

def fox():  # оранжевый флаг с чёрной и белой диагональными полосами (фон Роберта)
    im, d = blank((220, 118, 30, 255))
    d.polygon([(0, H * 0.55), (0, H * 0.85), (W, H * 0.25), (W, -H * 0.05)], fill=(24, 20, 20, 255))
    d.polygon([(0, H * 0.85), (0, H * 1.0), (W, H * 0.4), (W, H * 0.25)], fill=(238, 232, 220, 255))
    return im


def pcl():  # розово-белый флаг с сердцем в лавровом венке (портрет Скафа и Юри)
    im, d = blank((236, 214, 220, 255))
    pk = (216, 108, 128, 255)
    d.polygon([(0, 0), (W, 0), (W, 14 * S), (0, 20 * S)], fill=pk); d.polygon([(0, H), (W, H), (W, H - 14 * S), (0, H - 20 * S)], fill=pk)
    cx, cy = W // 2, H // 2; heart = (222, 70, 96, 255)
    d.ellipse([cx - 13 * S, cy - 12 * S, cx, cy + 2 * S], fill=heart); d.ellipse([cx, cy - 12 * S, cx + 13 * S, cy + 2 * S], fill=heart)
    d.polygon([(cx - 13 * S, cy - 4 * S), (cx + 13 * S, cy - 4 * S), (cx, cy + 14 * S)], fill=heart)
    for sgn in (-1, 1):  # лавровый венок
        for i in range(5):
            x = cx + sgn * (20 * S + i * 2 * S); y = cy - 6 * S + i * 4 * S
            d.ellipse([x - 2 * S, y - 3 * S, x + 2 * S, y + 3 * S], fill=(200, 120, 135, 255))
    return im

def hms():  # тёмно-зелёный флаг с бледным крылатым мечом (портрет Мото)
    im, d = blank((44, 70, 56, 255)); cx, cy = W // 2, H // 2; pale = (196, 192, 176, 255)
    d.rectangle([cx - 2 * S, cy - 16 * S, cx + 2 * S, cy + 16 * S], fill=pale)
    d.polygon([(cx, cy - 20 * S), (cx - 4 * S, cy - 14 * S), (cx + 4 * S, cy - 14 * S)], fill=pale)
    for sgn in (-1, 1):
        d.polygon([(cx + sgn * 3 * S, cy - 6 * S), (cx + sgn * 26 * S, cy - 12 * S), (cx + sgn * 22 * S, cy - 4 * S), (cx + sgn * 3 * S, cy + 2 * S)], fill=pale)
        d.polygon([(cx + sgn * 3 * S, cy + 3 * S), (cx + sgn * 20 * S, cy - 1 * S), (cx + sgn * 15 * S, cy + 6 * S), (cx + sgn * 3 * S, cy + 8 * S)], fill=pale)
    return im

FLAGS = {'PCL': pcl, 'HMS': hms, 'BLI': bli, 'WWF': wwf, 'SVB': svb, 'OVS': ovs, 'CRL': crl, 'FOX': fox}
base = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(base, '..', 'mortaly_world', 'gfx', 'flags')
for tag, fn in FLAGS.items():
    big = fn()
    for sub, size in [('', (82, 52)), ('medium', (41, 26)), ('small', (10, 7))]:
        d = os.path.join(out, sub); os.makedirs(d, exist_ok=True)
        big.resize(size, Image.LANCZOS).save(os.path.join(d, tag + '.tga'))
    print(tag, 'ok')
