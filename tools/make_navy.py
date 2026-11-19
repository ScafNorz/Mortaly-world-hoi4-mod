# Порты, верфи, технологии флота, конвои и проектировка эсминца для CRL, PCL (бывший север CRL), BLI; небольшая армия BLI.
# Запуск из папки mortaly_world: python ../tools/make_navy.py (повторный запуск безопасен)
import re, glob, os
rows = {int(r.split(';')[0]): r.strip().split(';') for r in open('map/definition.csv', encoding='utf-8').readlines()[1:] if r.split(';')[0].isdigit()}
def owner_of(path):
    t = open(path, encoding='utf-8').read(); return re.search(r'owner\s*=\s*(\w+)', t).group(1), t
# Порты: мало, но мощные. Сначала снимаем старые верфи/базы, потом ставим по плану (повторный запуск безопасен).
PLAN = {197: (4, 8), 202: (4, 8), 275: (3, 6),            # Жестокая земля: Тяжёлый порт, Стальная гавань, Литейная гавань
        221: (4, 8), 229: (3, 6), 218: (2, 5),            # север (Мирная земля): Ясная гавань, Северный причал, Светлый берег
        605: (3, 6), 613: (1, 4), 616: (1, 4), 619: (1, 4)}  # Голубые острова: ровно один порт на каждый из 4 островов
done = 0
for f in glob.glob('history/states/*.txt'):
    n = int(os.path.basename(f).split('-')[0])
    own, t = owner_of(f)
    t0 = t
    t = re.sub(r'\t\t\tdockyard = \d+\n', '', t)
    t = re.sub(r'\t\t\t%d = \{\n\t\t\t\tnaval_base = \d+\n\t\t\t\}\n' % n, '', t)
    if own == 'BLI': t = t.replace('\t\tadd_claim_by = CRL\n', '')
    if n in PLAN and rows[n][5] == 'true':
        dock, base = PLAN[n]
        ins = (f'\t\t\tdockyard = {dock}\n' if dock else '') + f'\t\t\t{n} = {{\n\t\t\t\tnaval_base = {base}\n\t\t\t}}\n'
        t = t.replace('\t\tbuildings = {\n', '\t\tbuildings = {\n' + ins, 1); done += 1
    if t != t0: open(f, 'w', encoding='utf-8').write(t)
print('ports:', done)

TECH = 'early_ship_hull_light = 1\n\tearly_ship_hull_cruiser = 1\n\tearly_ship_hull_submarine = 1\n\tbasic_battery = 1\n\tbasic_medium_battery = 1\n\tbasic_torpedo = 1\n\tbasic_depth_charges = 1\n'
NAVY = '''
# --- флот (этап 22) ---
add_equipment_to_stockpile = {
	type = convoy_1
	amount = %d
}
create_equipment_variant = {
	name = "Destroyer 1936"
	type = ship_hull_light_1
	parent_version = 0
	modules = {
		fixed_ship_battery_slot = ship_light_battery_1
		fixed_ship_anti_air_slot = empty
		fixed_ship_fire_control_system_slot = empty
		fixed_ship_radar_slot = empty
		fixed_ship_engine_slot = light_ship_engine_1
		fixed_ship_torpedo_slot = ship_torpedo_1
		mid_1_custom_slot = ship_depth_charge_1
		rear_1_custom_slot = empty
	}
}
'''
for name, amount in (('CRL - Cruel Land', 40), ('PCL - Peace Land', 25), ('BLI - Blue Isles', 60)):
    p = f'history/countries/{name}.txt'; t = open(p, encoding='utf-8-sig').read()
    if '# --- флот (этап 22)' in t: continue
    if 'set_technology = {' in t:
        t = t.replace('set_technology = {\n', 'set_technology = {\n\t' + TECH, 1)
    else:
        t += '\nset_technology = {\n\t' + TECH + '}\n'
    t += NAVY % amount
    if name.startswith('BLI'): t += '\noob = "BLI_1936"\n'
    open(p, 'w', encoding='utf-8').write(t)

# армия BLI
oob = 'units = {\n\tdivision_template = {\n\t\tname = "BLI Island Garrison"\n\t\tregiments = {\n'
for x, y in [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)]: oob += f'\t\t\tinfantry = {{ x = {x} y = {y} }}\n'
oob += '\t\t}\n\t}\n\tunits = {\n'
for i, loc in enumerate([610, 611, 613, 616]):
    oob += f'\t\tdivision = {{\n\t\t\tname = "{i+1} Island Garrison"\n\t\t\tlocation = {loc}\n\t\t\tdivision_template = "BLI Island Garrison"\n\t\t\tstart_experience_factor = 0.2\n\t\t\tstart_equipment_factor = 0.8\n\t\t}}\n'
oob += '\t}\n}\n'
open('history/units/BLI_1936.txt', 'w', encoding='utf-8').write(oob)
