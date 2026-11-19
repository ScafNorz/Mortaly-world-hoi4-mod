# Генератор гражданской войны (этап 21). Запуск из папки mortaly_world: python ../tools/make_civil_war.py
import os
NORTH = list(range(169, 185)) + list(range(217, 265))
SOUTH = [n for n in range(169, 281) if n not in NORTH]  # CRL после раскола
def spread(lst, k): return [lst[int(i * len(lst) / k)] for i in range(k)]
def oob(tname, dname, provs, n, eq, exp):
    t = 'units = {\n\tdivision_template = {\n\t\tname = "' + tname + '"\n\t\tregiments = {\n'
    for x in range(3):
        for y in range(3 if x < 2 else 1): t += f'\t\t\tinfantry = {{ x = {x} y = {y} }}\n'
    t += '\t\t}\n\t}\n\tunits = {\n'
    for i in range(n):
        t += f'\t\tdivision = {{\n\t\t\tname = "{i+1}-я {dname}"\n\t\t\tlocation = {provs[i % len(provs)]}\n\t\t\tdivision_template = "{tname}"\n\t\t\tstart_experience_factor = {exp}\n\t\t\tstart_equipment_factor = {eq}\n\t\t}}\n'
    return t + '\t}\n}\n'
os.makedirs('history/units', exist_ok=True)
files = {
 'PCL_civilwar_base': oob('Народная пехота', 'народная дивизия', spread(NORTH, 8), 7, 0.8, 0.2),
 'PCL_civilwar_defectors': oob('Перешедшие на сторону Мирной земли', 'дивизия перебежчиков', spread(NORTH, 4), 2, 0.9, 0.5),
 'PCL_civilwar_rebels': oob('Повстанческая пехота', 'повстанческая дивизия', spread(NORTH, 4), 2, 0.6, 0.1),
 'CRL_civilwar_army': oob('Пехота Дворца власти', 'дивизия Дворца власти', [210] + spread(SOUTH, 8), 10, 0.85, 0.3),
 'CRL_civilwar_guard': oob('Гвардия Дворца власти', 'гвардейская дивизия', [210, 210, 211], 2, 0.9, 0.5),
}
pass  # армии создаются эффектами mortaly_spawn_* (tools/make_spawn.py)

E = []
def ev(eid, title, desc, trig, hidden, immediate, opts): E.append((eid, title, desc, trig, hidden, immediate, opts))
TRANSFER_BLI = 'if = {\n\tlimit = { country_exists = BLI BLI = { has_country_flag = BLI_joined_peace_alliance } }\n' + ''.join(f'\ttransfer_state = {i}\n' for i in range(605, 621)) + '}'
TRANSFER_ALL = '\n'.join(f'transfer_state = {i}' for i in range(169, 281))
GUARD = 'NOT = { has_global_flag = civil_war_started }'
ev('mortaly_war.1', 'Раскол Жестокой земли',
   'Терпение севера кончилось. Города и гарнизоны северных стейтов отказались подчиняться Дворцу власти и объявили о создании Мирной земли. Скаф и Юри провозгласили республику и возглавили северные войска. Начинается гражданская война.',
   'original_tag = CRL\n' + GUARD + '\ndate > 1939.1.1', False,
   '''set_global_flag = civil_war_started
mortaly_cruel_land_split = yes
PCL = {
	add_ideas = PCL_popular_uprising
	add_ideas = PCL_provisional_government
	add_ideas = PCL_northern_volunteers
	add_manpower = 20000
	if = { limit = { CRL = { has_country_flag = CRL_depots_evacuated } } add_equipment_to_stockpile = { type = infantry_equipment amount = 500 } }
	if = { limit = { CRL = { NOT = { has_country_flag = CRL_depots_evacuated } } } add_equipment_to_stockpile = { type = infantry_equipment amount = 900 } }
	mortaly_spawn_pcl_base = yes
	if = { limit = { CRL = { has_country_flag = CRL_officers_tolerated } } mortaly_spawn_pcl_defectors = yes }
	if = { limit = { OR = { CRL = { has_country_flag = CRL_north_repressed } CRL = { has_country_flag = CRL_north_tightened } } } mortaly_spawn_pcl_rebels = yes }
}
add_equipment_to_stockpile = { type = infantry_equipment amount = 500 }
mortaly_spawn_crl_army = yes
if = { limit = { OR = { has_country_flag = CRL_officers_loyal has_country_flag = CRL_officers_purged } } mortaly_spawn_crl_guard = yes }
CRL = { declare_war_on = { target = PCL type = annex_everything } }
if = { limit = { country_exists = BLI } BLI = { country_event = { id = mortaly_war.3 days = 1 } } }
if = { limit = { is_ai = no } country_event = { id = mortaly_war.2 days = 1 } }
country_event = { id = mortaly_war.20 days = 30 }''',
   [('Начинается война', '')])
ev('mortaly_war.2', 'На чьей вы стороне?',
   'Север восстал, и вы можете остаться верным Дворцу власти или перейти к Скафу. Если выберете Скафа, вы возьмёте управление Мирной землёй, а Жестокая земля продолжит воевать под управлением ИИ.',
   None, False, '',
   [('Остаться с Дворцом власти', 'set_country_flag = CRL_player_stayed'), ('Встать под знамёна Скафа и Юри', 'set_country_flag = CRL_player_to_scaf\nPCL = { change_tag_from = CRL }', 'ai0')])
ev('mortaly_war.3', 'Решение Голубых островов',
   'Север Жестокой земли восстал против Дворца власти. Совет островов должен решить, поможет ли он Мирной земле или останется в стороне.',
   None, False, '',
   [('Вступить в союз с Мирной землёй',
     '''mortaly_bli_join_war = yes
if = { limit = { country_exists = PCL } PCL = { add_equipment_to_stockpile = { type = infantry_equipment amount = 300 } add_timed_idea = { idea = BLI_open_harbours days = 180 } } }
if = { limit = { NOT = { has_country_flag = BLI_division_sent } } set_country_flag = BLI_division_sent set_country_flag = BLI_sent_volunteers mortaly_spawn_bli_volunteers = yes }''', 'ai1'),
    ('Остаться нейтральными', 'add_stability = 0.02\nset_country_flag = BLI_neutral_in_war', 'ai0')])
ev('mortaly_war.11', 'Победа Дворца власти',
   'Мятеж подавлен. Северные стейты возвращены, а Мирная земля перестала существовать. Голубые острова, вставшие на сторону севера, тоже вошли в состав Жестокой земли. Теперь Дворец власти решает, как поступить с побеждёнными.',
   None, False,
   '''set_global_flag = civil_war_ended
set_global_flag = crl_won_civil_war
set_country_flag = CRL_won_civil_war
''' + TRANSFER_ALL + '\n' + TRANSFER_BLI,
   [('Объявить амнистию', 'set_country_flag = CRL_amnesty\nadd_stability = 0.05', 'ai1'), ('Начать репрессии', 'add_political_power = 50\nset_country_flag = CRL_repression', 'ai1')])
ev('mortaly_war.12', 'Провозглашение Мирной земли',
   'Дворец власти пал. Мирная земля объединила обе половины страны и стала единой демократической республикой. Голубые острова сохранили независимость: Мирная земля гарантирует её и остаётся с островами в союзе. Впереди восстановление и новая конституция.',
   None, False,
   '''set_global_flag = civil_war_ended
set_global_flag = pcl_won_civil_war
set_country_flag = PCL_won_civil_war
''' + TRANSFER_ALL + '''
if = {
	limit = { country_exists = BLI }
	give_guarantee = BLI
	if = { limit = { is_in_faction = no } create_faction = PCL_peace_union }
	BLI = { country_event = { id = mortaly_war.13 days = 3 } }
}''',
   [('Да здравствует Мирная земля!', 'add_stability = 0.05\nadd_political_power = 50', 'ai1')])
ev('mortaly_war.13', 'Договор с Голубыми островами',
   'Война окончена. Мирная земля не тронула острова: она гарантирует их независимость и предлагает остаться в союзе.',
   None, False, '',
   [('Подтвердить союз и гарантии', 'add_political_power = 50\nadd_stability = 0.03\nset_country_flag = BLI_treaty_signed\nif = { limit = { country_exists = PCL NOT = { is_in_faction_with = PCL } } add_to_faction = PCL }', 'ai1'), ('Ограничиться торговым соглашением', 'add_political_power = 25', 'ai0')])
ev('mortaly_war.30', 'Дворец власти пал', 'Жестокая земля капитулировала. Вы можете принять поражение или продолжить борьбу, взяв управление другой страной.', None, False, '',
   [('Продолжить за Мирную землю', 'PCL = { change_tag_from = CRL }\nPCL = { country_event = { id = mortaly_war.12 days = 1 } }', 'ai0', 'country_exists = PCL'),
    ('Продолжить за Голубые острова', 'BLI = { change_tag_from = CRL }\nPCL = { country_event = { id = mortaly_war.12 days = 1 } }', 'ai0', 'country_exists = BLI'),
    ('Принять поражение', 'PCL = { country_event = { id = mortaly_war.12 days = 1 } }', 'ai1')])
ev('mortaly_war.31', 'Мирная земля побеждена', 'Мирная земля капитулировала. Вы можете принять поражение или продолжить борьбу, взяв управление другой страной.', None, False, '',
   [('Продолжить за Жестокую землю', 'CRL = { change_tag_from = PCL }\nCRL = { country_event = { id = mortaly_war.11 days = 1 } }', 'ai0', 'country_exists = CRL'),
    ('Продолжить за Голубые острова', 'BLI = { change_tag_from = PCL }\nCRL = { country_event = { id = mortaly_war.11 days = 1 } }', 'ai0', 'country_exists = BLI BLI = { NOT = { has_country_flag = BLI_joined_peace_alliance } }'),
    ('Принять поражение', 'CRL = { country_event = { id = mortaly_war.11 days = 1 } }', 'ai1')])
ev('mortaly_war.20', '', '', None, True,
   '''if = {
	limit = { NOT = { has_global_flag = civil_war_ended } NOT = { has_global_flag = civil_war_ending } PCL = { has_capitulated = yes } }
	set_global_flag = civil_war_ending
	if = { limit = { PCL = { is_ai = no } } PCL = { country_event = { id = mortaly_war.31 days = 1 } } }
	if = { limit = { PCL = { is_ai = yes } } country_event = { id = mortaly_war.11 days = 1 } }
}
else_if = {
	limit = { NOT = { has_global_flag = civil_war_ended } NOT = { has_global_flag = civil_war_ending } has_capitulated = yes }
	set_global_flag = civil_war_ending
	if = { limit = { is_ai = no } country_event = { id = mortaly_war.30 days = 1 } }
	if = { limit = { is_ai = yes } PCL = { country_event = { id = mortaly_war.12 days = 1 } } }
}
else_if = {
	limit = { NOT = { has_global_flag = civil_war_ended } NOT = { has_global_flag = civil_war_ending } }
	country_event = { id = mortaly_war.20 days = 5 }
}''', [])

out = 'add_namespace = mortaly_war\n\n'; ru = 'l_russian:\n'; en = 'l_english:\n'
for eid, title, desc, trig, hidden, imm, opts in E:
    out += f'country_event = {{\n\tid = {eid}\n'
    if hidden: out += '\thidden = yes\n'
    else: out += f'\ttitle = {eid}.t\n\tdesc = {eid}.d\n'
    if trig:
        out += '\tfire_only_once = yes\n\ttrigger = {\n' + ''.join(f'\t\t{l}\n' for l in trig.split('\n')) + '\t}\n\tmean_time_to_happen = {\n\t\tdays = 2\n\t}\n'
    else: out += '\tis_triggered_only = yes\n'
    if imm: out += '\timmediate = {\n' + ''.join(f'\t\t{l}\n' for l in imm.split('\n')) + '\t}\n'
    for i, o in enumerate(opts):
        label, eff = o[0], o[1]; ai = o[2] if len(o) > 2 else 'ai1'; otrig = o[3] if len(o) > 3 else ''
        k = 'abc'[i]
        out += f'\toption = {{\n\t\tname = {eid}.{k}\n' + (f'\t\ttrigger = {{ {otrig} }}\n' if otrig else '') + ''.join(f'\t\t{l}\n' for l in eff.split('\n') if l) + f'\t\tai_chance = {{ factor = {0 if ai == "ai0" else 1} }}\n\t}}\n'
        ru += f' {eid}.{k}:0 "{label}"\n'; en += f' {eid}.{k}:0 "{label}"\n'
    out += '}\n\n'
    if not hidden:
        ru += f' {eid}.t:0 "{title}"\n {eid}.d:0 "{desc}"\n'; en += f' {eid}.t:0 "{title}"\n {eid}.d:0 "{desc}"\n'
open('common/scripted_effects/mortaly_war_effects.txt', 'w', encoding='utf-8').write('''# Вступление Голубых островов в союз с Мирной землёй (фракция + война с Жестокой землёй). Область: BLI.
mortaly_bli_join_war = {
\tset_country_flag = BLI_joined_peace_alliance
\tset_country_flag = BLI_ports_open
\tif = {
\t\tlimit = { country_exists = PCL NOT = { is_in_faction_with = PCL } }
\t\tif = {
\t\t\tlimit = { PCL = { is_in_faction = no } }
\t\t\tPCL = { create_faction = PCL_peace_union }
\t\t}
\t\tadd_to_faction = PCL
\t}
\tif = {
\t\tlimit = { country_exists = CRL has_global_flag = civil_war_started NOT = { has_war_with = CRL } }
\t\tdeclare_war_on = { target = CRL type = annex_everything }
\t}
}
''')
open('events/mortaly_civil_war.txt', 'w', encoding='utf-8').write(out)
ru += ' PCL_peace_union:0 "Мирный союз"\n'; en += ' PCL_peace_union:0 "Peace Union"\n'
open('localisation/russian/mortaly_civil_war_l_russian.yml', 'w', encoding='utf-8-sig').write(ru)
open('localisation/english/mortaly_civil_war_l_english.yml', 'w', encoding='utf-8-sig').write(en)
print('ok')
