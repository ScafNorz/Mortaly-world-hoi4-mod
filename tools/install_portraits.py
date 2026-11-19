"""Раскладывает портреты лидеров по странам.
Заполни MAPPING (тег страны -> номер портрета) и запусти из папки мода: python tools/install_portraits.py
Результат: mortaly_world/gfx/leaders/<TAG>/<TAG>_leader.tga (156x210, 32 бит)."""
from PIL import Image
import os
MAPPING = {
    'YOZ': 3,
    'VMP': 5,
    'WWF': 7,
    'CRL': 4,
    'BLI': 2,
    'FOX': 1,
    'SVB': 6,
    'OVS': 8,
}
base = os.path.dirname(os.path.abspath(__file__))
for tag, n in MAPPING.items():
    im = Image.open(os.path.join(base, 'portraits', f'portrait_{n}.png')).convert('RGBA')
    d = os.path.join(base, '..', 'mortaly_world', 'gfx', 'leaders', tag); os.makedirs(d, exist_ok=True)
    im.save(os.path.join(d, f'{tag}_leader.tga'))
    print(tag, '<- portrait', n)
