# Этап 24: тех-стартовый набор CRL/PCL, лидер PCL «Скаф и Юри», ресурсы, ИИ.
# Запуск из папки mortaly_world: python ../tools/make_stage24.py [путь к ai_strategy ванили]  (повторный запуск безопасен)
import re, os, sys, glob
AI_SRC = sys.argv[1] if len(sys.argv) > 1 else '../tools/vanilla_ai_strategy'
def rd(p): return open(p, encoding='utf-8-sig').read()
def wr(p, t): open(p, 'w', encoding='utf-8').write(t)

# ---------- технологии
INF = 'infantry_weapons infantry_weapons1 infantry_weapons2 infantry_weapons3 infantry_weapons4 tech_support tech_recon tech_engineers tech_military_police tech_mountaineers tech_marines tech_paratroopers tech_field_hospital tech_logistics_company tech_maintenance_company tech_signal_company tech_special_forces gw_artillery basic_train'.split()
NAVY = 'early_ship_hull_light early_ship_hull_cruiser early_ship_hull_heavy early_ship_hull_submarine basic_battery basic_medium_battery basic_heavy_battery basic_torpedo basic_depth_charges fire_control_methods mtg_transport'.split()
AIR = 'early_fighter CAS1 tactical_bomber1 naval_bomber1 early_bomber'.split()
def set_tech(path):
    t = rd(path); m = re.search(r'set_technology = \{([^}]*)\}', t)
    have = dict(re.findall(r'(\w+)\s*=\s*(\d)', m.group(1))) if m else {}
    for k in INF + NAVY + AIR: have[k] = '1'
    block = 'set_technology = {\n' + ''.join(f'\t{k} = {v}\n' for k, v in have.items()) + '}'
    t = t.replace(m.group(0), block) if m else t + '\n' + block + '\n'
    return t
for name in ('CRL - Cruel Land', 'PCL - Peace Land'):
    p = f'history/countries/{name}.txt'; wr(p, set_tech(p))

# ---------- PCL: единый лидер «Скаф и Юри», генерала Юри нет
p = 'history/countries/PCL - Peace Land.txt'; t = rd(p)
t = re.sub(r'create_corps_commander = \{.*?\n\}\n', '', t, flags=re.S)
t = t.replace('# Скаф: политический лидер. Юри: главнокомандующий.', '# Скаф и Юри: один общий лидер (2 в 1), отдельного генерала Юри нет.')
wr(p, t)
for lang, name in (('russian', 'Скаф и Юри'), ('english', 'Scaf and Yuri')):
    f = f'localisation/{lang}/mortaly_world_l_{lang}.yml'; s = rd(f)
    s = re.sub(r' PCL_LEADER_NAME:0 "[^"]*"', f' PCL_LEADER_NAME:0 "{name}"', s)
    open(f, 'w', encoding='utf-8-sig').write(s)

# ---------- ресурсы (по 3 источника каждого ресурса в южной и северной половине; все на железной дороге)
SOUTH = {'oil': [190, 199, 269], 'steel': [191, 204, 274], 'aluminium': [201, 211, 277], 'chromium': [213, 269, 190], 'rubber': [199, 204, 211], 'tungsten': [274, 277, 201]}
NORTH = {'oil': [169, 225, 254], 'steel': [175, 181, 257], 'aluminium': [172, 217, 259], 'chromium': [178, 227, 262], 'rubber': [183, 234, 258], 'tungsten': [249, 254, 257]}
AMT = {'oil': (30, 12), 'steel': (60, 15), 'aluminium': (30, 8), 'chromium': (22, 6), 'rubber': (28, 8), 'tungsten': (20, 6)}
res = {}
for grp in (SOUTH, NORTH):
    for r, sts in grp.items():
        for i, n in enumerate(sts): res.setdefault(n, {})[r] = AMT[r][0] + AMT[r][1] * (i - 1)
for f in glob.glob('history/states/*.txt'):
    n = int(os.path.basename(f).split('-')[0])
    if not (169 <= n <= 280): continue
    t = rd(f); t = re.sub(r'\tresources = \{[^}]*\}\n', '', t)
    if n in res:
        t = re.sub(r'(\tstate_category = \w+\n)', lambda m: m.group(1) + '\tresources = {\n' + ''.join(f'\t\t{k} = {v}\n' for k, v in res[n].items()) + '\t}\n', t, 1)
    wr(f, t)

# ---------- ИИ: общие стратегии из ванили (без привязки к чужим странам) + стратегии наших стран
os.makedirs('common/ai_strategy', exist_ok=True)
for f in os.listdir('common/ai_strategy'): os.remove('common/ai_strategy/' + f)
t = rd(AI_SRC + '/default.txt'); blocks = []; i = 0
while True:
    m = re.search(r'^([A-Za-z_0-9]+) = \{', t[i:], re.M)
    if not m: break
    s = i + m.start(); j = i + m.end(); d = 1
    while d: c = t[j]; d += (c == '{') - (c == '}'); j += 1
    blocks.append((m.group(1), t[s:j])); i = j
out = '# Общие стратегии ИИ из ванили (только блоки без привязки к ванильным странам); этап 24\n\n'
for name, b in blocks:
    if name == 'default_unit_production':
        b = re.sub(r'\tenable = \{.*?\n\t\}\n(?=\tabort_when_not_enabled)', '\tenable = {\n\t\talways = yes\n\t}\n', b, flags=re.S)
    elif re.search(r'(?:tag|original_tag|id|target) = "?[A-Z]{3}"?\b', b): continue
    out += b + '\n\n'
wr('common/ai_strategy/mortaly_default.txt', out)
for f in ('doctrines.txt', 'operatives_default.txt', 'generic_operation_strats.txt'):
    if os.path.exists(AI_SRC + '/' + f): wr('common/ai_strategy/' + f, rd(AI_SRC + '/' + f))
WAR = 'has_global_flag = civil_war_started\n\t\tNOT = { has_global_flag = civil_war_ended }'
def strat(typ, id_, val): return f'\tai_strategy = {{\n\t\ttype = {typ}\n\t\tid = "{id_}"\n\t\tvalue = {val}\n\t}}\n'
ai = '# Стратегии ИИ стран Mortaly world (этап 24)\n\n'
ai += f'''MORTALY_crl_civil_war = {{
\tallowed = {{ original_tag = CRL }}
\tenable = {{
\t\t{WAR}
\t}}
\tabort_when_not_enabled = yes
{strat('conquer', 'PCL', 400)}{strat('antagonize', 'PCL', 400)}{strat('conquer', 'BLI', 150)}{strat('antagonize', 'BLI', 200)}}}

MORTALY_pcl_civil_war = {{
\tallowed = {{ original_tag = PCL }}
\tenable = {{
\t\t{WAR}
\t}}
\tabort_when_not_enabled = yes
{strat('conquer', 'CRL', 400)}{strat('antagonize', 'CRL', 400)}{strat('alliance', 'BLI', 300)}{strat('protect', 'BLI', 200)}}}

MORTALY_bli_civil_war = {{
\tallowed = {{ original_tag = BLI }}
\tenable = {{
\t\t{WAR}
\t\tPCL = {{ exists = yes }}
\t}}
\tabort_when_not_enabled = yes
{strat('alliance', 'PCL', 300)}{strat('protect', 'PCL', 200)}{strat('antagonize', 'CRL', 100)}}}

# До войны Жестокая земля не трогает острова, а острова не лезут в чужие дела
MORTALY_crl_leaves_islands = {{
\tallowed = {{ original_tag = CRL }}
\tenable = {{
\t\tNOT = {{ has_global_flag = civil_war_started }}
\t}}
\tabort_when_not_enabled = yes
{strat('conquer', 'BLI', -1000)}}}

MORTALY_bli_peaceful = {{
\tallowed = {{ original_tag = BLI }}
\tenable = {{
\t\tNOT = {{ has_global_flag = civil_war_started }}
\t}}
\tabort_when_not_enabled = yes
\tai_strategy = {{
\t\ttype = avoid_starting_wars
\t\tvalue = -300
\t}}
}}

# После победы Мирная земля держится за острова
MORTALY_pcl_keeps_islands = {{
\tallowed = {{ original_tag = PCL }}
\tenable = {{
\t\thas_global_flag = pcl_won_civil_war
\t}}
\tabort_when_not_enabled = yes
{strat('protect', 'BLI', 300)}{strat('alliance', 'BLI', 300)}}}
'''
wr('common/ai_strategy/mortaly_countries.txt', ai)
print('stage24 ok')
