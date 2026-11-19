# Местность Жестокой земли (юг: пустыни и равнины; север: холмы и горы), Голубых островов (холмы, леса); города разнесены.
# Запуск из папки mortaly_world: python ../tools/make_terrain.py  (нужны numpy, Pillow)
import numpy as np, random
from PIL import Image
random.seed(1939)
P = Image.open('map/provinces.bmp').convert('RGB'); a = np.array(P).astype(np.int64)
rows = [l.rstrip('\n').split(';') for l in open('map/definition.csv', encoding='utf-8')]
lut = {int(r[1])*65536+int(r[2])*256+int(r[3]): int(r[0]) for r in rows if r[0] != '0'}
code = a[..., 0]*65536 + a[..., 1]*256 + a[..., 2]
u, inv = np.unique(code.ravel(), return_inverse=True)
pid = np.array([lut.get(x, 0) for x in u])[inv].reshape(code.shape)
NORTH = list(range(169, 185)) + list(range(217, 265))
SOUTH = [n for n in range(169, 281) if n not in NORTH]
cen = {}
for n in list(range(169, 281)) + list(range(605, 621)):
    ys, xs = np.nonzero(pid == n); cen[n] = (xs.mean(), ys.mean())
T = {}
def by_y(group, plan):  # plan: [(доля, местность)] с юга на север, с небольшим шумом
    order = sorted(group, key=lambda n: -cen[n][1] + random.uniform(-18, 18))
    i = 0
    for share, ter in plan:
        k = round(share*len(group)); 
        for n in order[i:i+k]: T[n] = ter
        i += k
    for n in order[i:]: T[n] = plan[-1][1]
by_y(SOUTH, [(0.60, 'desert'), (0.40, 'plains')])            # юг: пустыни и равнины
by_y(NORTH, [(0.30, 'plains'), (0.42, 'hills'), (0.28, 'mountain')])  # север: равнины, холмы, горы (на самом севере)
# города: столицы + разнесённые по стране (дальняя выборка), чтобы не стояли кучкой
def fps(group, first, k):
    pick = list(first)
    while len(pick) < k:
        best = max([n for n in group if n not in pick], key=lambda n: min((cen[n][0]-cen[m][0])**2 + (cen[n][1]-cen[m][1])**2 for m in pick))
        pick.append(best)
    return pick
for n in fps(SOUTH, [210], 4) + fps(NORTH, [242], 4): T[n] = 'urban'
# Голубые острова: холмы и леса, города — Лазурная гавань и остров Мир
for n in range(605, 621): T[n] = 'forest' if (n % 2 == 0) else 'hills'
for n in (605, 610): T[n] = 'urban'
IDX = {'plains': 0, 'forest': 1, 'hills': 2, 'desert': 3, 'mountain': 6, 'urban': 13}
for r in rows:
    if r[0].isdigit() and int(r[0]) in T: r[6] = T[int(r[0])]
open('map/definition.csv', 'w', encoding='utf-8', newline='').write('\n'.join(';'.join(r) for r in rows) + '\n')
tb = Image.open('map/terrain.bmp'); ta = np.array(tb)
for n, t in T.items(): ta[pid == n] = IDX[t]
nb = Image.fromarray(ta, 'P'); nb.putpalette(tb.getpalette()); nb.save('map/terrain.bmp')
# карта деревьев (375x300): леса Голубых островов
tr = Image.open('map/trees.bmp'); tra = np.array(tr)
small = np.array(Image.fromarray(pid.astype(np.int32)).resize(tra.shape[::-1], Image.NEAREST))
for n, t in T.items():
    if t == 'forest': tra[small == n] = 3
nt = Image.fromarray(tra, 'P'); nt.putpalette(tr.getpalette()); nt.save('map/trees.bmp')
import collections
print(collections.Counter(T[n] for n in SOUTH+NORTH), collections.Counter(T[n] for n in range(605, 621)))
print('urban', [n for n, t in T.items() if t == 'urban'])
