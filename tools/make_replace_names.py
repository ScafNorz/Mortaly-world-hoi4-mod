"""Переносит названия стейтов и очков победы в localisation/replace, чтобы они перекрывали ванильные (Москва, Хубэй и т. п.).
Запуск из папки mortaly_world: python ../tools/make_replace_names.py (повторный запуск безопасен)"""
import re, os
for lang in ('russian', 'english'):
    main = f'localisation/{lang}/mortaly_world_l_{lang}.yml'
    t = open(main, encoding='utf-8-sig').read()
    rep = f'localisation/replace/mortaly_names_l_{lang}.yml'
    names = {}; vps = {}
    if os.path.exists(rep):
        r = open(rep, encoding='utf-8-sig').read()
        names = {int(a): b for a, b in re.findall(r' STATE_(\d+):\d* "(.*)"', r)}
        vps = {int(a): b for a, b in re.findall(r' VICTORY_POINTS_(\d+):\d* "(.*)"', r)}
    names.update({int(a): b for a, b in re.findall(r' STATE_(\d+):\d* "(.*)"', t)})
    vps.update({int(a): b for a, b in re.findall(r' VICTORY_POINTS_(\d+):\d* "(.*)"', t)})
    for n in range(1, 621): vps.setdefault(n, names.get(n, f'Province {n}'))
    out = f'l_{lang}:\n' + ''.join(f' STATE_{n}:0 "{names[n]}"\n' for n in sorted(names)) + ''.join(f' VICTORY_POINTS_{n}:0 "{vps[n]}"\n' for n in sorted(vps))
    os.makedirs('localisation/replace', exist_ok=True)
    open(rep, 'w', encoding='utf-8-sig').write(out)
    t2 = re.sub(r'^ (STATE_\d+|VICTORY_POINTS_\d+):\d* ".*"\n', '', t, flags=re.M)
    open(main, 'w', encoding='utf-8-sig').write(t2)
    print(lang, len(names), 'states', len(vps), 'vp')
