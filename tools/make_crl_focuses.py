"""Генерирует дерево фокусов Жестокой земли (CRL), духи фокусов и локализацию.
Запуск из папки мода: python tools/make_crl_focuses.py"""
import os
base = os.path.dirname(os.path.abspath(__file__))
mod = os.path.join(base, '..', 'mortaly_world')
NORTH = list(range(169, 185)) + list(range(217, 265))  # северные стейты (как в mortaly_cruel_land_split)

def bunkers(ids):
    return ''.join(f"\t\t\t{i} = {{ add_building_construction = {{ type = bunker level = 1 province = {i} instant_build = yes }} }}\n" for i in ids)

ICON = {'eco': 'GFX_goal_generic_production', 'build': 'GFX_goal_generic_construction', 'army': 'GFX_goal_generic_army_doctrines',
        'sf': 'GFX_goal_generic_special_forces', 'arms': 'GFX_goal_generic_small_arms', 'press': 'GFX_goal_generic_propaganda',
        'unity': 'GFX_goal_generic_national_unity', 'pol': 'GFX_goal_generic_political_pressure', 'mob': 'GFX_goal_generic_forced_march'}
INF = "every_owned_state = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }"
CIV = "random_owned_state = { add_building_construction = { type = industrial_complex level = 1 instant_build = yes } }"
MIL = "random_owned_state = { add_building_construction = { type = arms_factory level = 1 instant_build = yes } }"
AFTER = "has_country_flag = CRL_won_civil_war"

# id, x, y, cost, [AND-prereqs], available, icon, reward, name, desc
F = []
def f(i, x, y, cost, pre, avail, icon, reward, name, desc): F.append((i, x, y, cost, pre, avail, icon, reward, name, desc))
# --- Ветка A: экономика ---
f('CRL_audit_the_treasury', 3, 0, 5, [], '', 'eco', 'add_political_power = 50\nadd_stability = 0.02', 'Ревизия казны', 'Дворец власти наконец пересчитал, что у страны осталось. Цифры неутешительны, но теперь они хотя бы честные.')
f('CRL_reopen_the_mines', 1, 1, 5, ['CRL_audit_the_treasury'], '', 'build', 'random_owned_state = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }\nadd_political_power = 25', 'Вернуть шахты к работе', 'Заброшенные шахты расчищают, укрепляют и снова пускают в дело.')
f('CRL_repair_railways', 5, 1, 5, ['CRL_audit_the_treasury'], '', 'build', INF, 'Ремонт железных дорог', 'Рельсы между столицей и промышленными районами перекладывают заново.')
f('CRL_small_workshops', 1, 2, 5, ['CRL_reopen_the_mines'], '', 'eco', CIV, 'Малые мастерские', 'Небольшие частные мастерские получают разрешение работать на государство.')
f('CRL_state_contracts', 5, 2, 5, ['CRL_repair_railways'], '', 'arms', MIL + '\nadd_stability = -0.02', 'Государственные заказы', 'Армия размещает заказы на заводах. Рабочие недовольны, но станки крутятся.')
f('CRL_local_industry', 3, 3, 5, ['CRL_small_workshops', 'CRL_state_contracts'], '', 'eco', 'add_ideas = CRL_local_industry', 'Опора на внутреннее производство', 'Всё, что можно сделать дома, делается дома.')
f('CRL_economic_stabilisation', 3, 4, 10, ['CRL_local_industry'], '', 'eco', 'swap_ideas = { remove_idea = CRL_dead_economy add_idea = CRL_dead_economy_weak }', 'Стабилизация экономики', 'Мёртвая экономика не воскресла, но уже дышит.')
f('CRL_war_industry', 3, 5, 5, ['CRL_economic_stabilisation'], '', 'arms', 'add_ideas = CRL_war_industry\nadd_equipment_to_stockpile = { type = infantry_equipment amount = 300 }', 'Промышленность на случай войны', 'Заводы заранее переводят на военные рельсы.')
# --- Ветка B: армия ---
f('CRL_professional_army', 15, 0, 5, [], '', 'army', 'army_experience = 25', 'Профессиональная армия', 'Дворец власти ставит на армию из профессионалов, а не на толпу призывников.')
f('CRL_infantry_regulations', 13, 1, 5, ['CRL_professional_army'], '', 'army', 'add_ideas = CRL_infantry_regulations', 'Единый пехотный устав', 'Один устав для всех частей, от Дворца власти до самых дальних застав.')
f('CRL_training_centres', 17, 1, 5, ['CRL_professional_army'], '', 'army', 'add_ideas = CRL_training_centres', 'Учебные центры', 'Новобранцев готовят быстрее и жёстче.')
f('CRL_special_forces_school', 13, 2, 5, ['CRL_infantry_regulations'], '', 'sf', 'add_ideas = CRL_special_forces_school', 'Школа спецназа', 'Лучших из лучших отбирают в школу штурмовых частей.')
f('CRL_standardised_weapons', 17, 2, 5, ['CRL_training_centres'], '', 'arms', 'add_ideas = CRL_standard_weapons', 'Стандартизация вооружения', 'Один калибр, одни запчасти, один выпуск.')
f('CRL_elite_command', 13, 3, 5, ['CRL_special_forces_school'], '', 'sf', 'army_experience = 25\nadd_war_support = 0.03', 'Единое командование элитой', 'Штурмовые части подчиняются одному штабу.')
f('CRL_northern_garrisons', 15, 4, 10, ['CRL_elite_command', 'CRL_standardised_weapons'], '', 'army', 'add_ideas = CRL_northern_garrisons\n' + bunkers(NORTH).rstrip('\n'), 'Северные гарнизоны', 'На севере строят доты и ставят гарнизоны: Дворец власти знает, откуда ждать беды.')
f('CRL_general_mobilisation', 15, 5, 10, ['CRL_northern_garrisons'], '', 'mob', 'add_ideas = CRL_general_mobilisation\nadd_war_support = 0.05\nset_country_flag = CRL_mobilisation_unlocked', 'Общая мобилизация', 'Страна готова встать под ружьё по первому приказу.')
# --- Ветка C: изоляция и политика ---
f('CRL_closed_borders', 27, 0, 5, [], '', 'pol', 'swap_ideas = { remove_idea = CRL_closed_country add_idea = CRL_closed_country_2 }', 'Закрыть границы', 'Иностранцев больше не пускают. Тех, кто уже внутри, берут на учёт.')
f('CRL_internal_security', 25, 1, 5, ['CRL_closed_borders'], '', 'pol', 'add_ideas = CRL_internal_security', 'Служба внутренней безопасности', 'Тайная служба Дворца власти следит за всеми, и в первую очередь за своими.')
f('CRL_control_the_press', 29, 1, 5, ['CRL_closed_borders'], '', 'press', 'add_stability = 0.05\nadd_political_power = -25', 'Единая государственная пресса', 'Газеты пишут то, что нужно Дворцу власти. Читателей это радует меньше.')
f('CRL_loyal_officers', 25, 2, 5, ['CRL_internal_security'], '', 'army', 'add_ideas = CRL_loyal_officers\narmy_experience = 15\nset_country_flag = CRL_officers_checked', 'Проверка офицерского корпуса', 'Ненадёжных офицеров снимают с должностей. Остальные внимательно учатся молчать.')
f('CRL_the_northern_question', 29, 2, 5, ['CRL_control_the_press'], '', 'pol', 'set_country_flag = CRL_northern_question_raised\nadd_political_power = 25', 'Северный вопрос', 'Север недоволен всё громче. Дворец власти больше не может делать вид, что ничего не слышит.')
f('CRL_secure_the_palace', 27, 3, 5, ['CRL_loyal_officers'], '', 'build', '210 = { add_building_construction = { type = bunker level = 2 province = 210 instant_build = yes } }\nadd_equipment_to_stockpile = { type = infantry_equipment amount = 300 }', 'Защитить Дворец власти', 'Вокруг Дворца власти поднимаются бетонные стены.')
f('CRL_prepare_for_the_split', 27, 4, 10, ['CRL_secure_the_palace', 'CRL_the_northern_question'], '', 'unity', 'set_country_flag = CRL_prepared_for_split\nadd_war_support = 0.05\nadd_equipment_to_stockpile = { type = infantry_equipment amount = 300 }', 'Подготовиться к расколу', 'Раскол неизбежен. Остаётся выбрать, что успеть вывезти до его начала.')
# --- Ветка D: после победы в гражданской войне ---
f('CRL_restore_order', 39, 0, 5, [], AFTER, 'pol', 'add_stability = 0.05\nadd_political_power = 50', 'Восстановить порядок', 'Мятеж подавлен. Теперь надо снова научить страну слушаться.')
f('CRL_rebuild_the_north', 37, 1, 5, ['CRL_restore_order'], AFTER, 'build', INF + '\nadd_stability = 0.03', 'Восстановить север', 'Разрушенный север отстраивают заново.')
f('CRL_reconcile_or_punish', 41, 1, 5, ['CRL_restore_order'], AFTER, 'pol', 'set_country_flag = CRL_reconcile_choice_open', 'Судьба мятежников', 'Амнистия или расправа: Дворец власти должен решить, как поступить с побеждёнными.')
f('CRL_new_economic_plan', 37, 2, 10, ['CRL_rebuild_the_north'], AFTER, 'eco', 'swap_ideas = { remove_idea = CRL_dead_economy_weak add_idea = CRL_new_plan }', 'Новый хозяйственный план', 'Пятилетка восстановления: на этот раз по-настоящему.')
f('CRL_unified_state', 39, 3, 10, ['CRL_new_economic_plan', 'CRL_reconcile_or_punish'], AFTER, 'unity', 'if = { limit = { has_country_flag = CRL_amnesty } swap_ideas = { remove_idea = CRL_smoldering_split add_idea = CRL_united_nation } }\nif = { limit = { NOT = { has_country_flag = CRL_amnesty } } remove_ideas = CRL_smoldering_split }', 'Единое государство', 'Раскол позади. Что останется на его месте, зависит от того, как с ним обошлись.')

import re
FIDS = {r[0] for r in F}
def SP(k): return k + '_spirit' if k in FIDS else k
def block(text, tabs):
    text = re.sub(r'(add_ideas|remove_ideas|add_idea|remove_idea) = (\w+)', lambda m: m.group(1) + ' = ' + SP(m.group(2)), text)
    return ''.join('\t' * tabs + l + '\n' for l in text.split('\n') if l.strip())

out = ['focus_tree = {\n\tid = mortaly_crl_tree\n\tcountry = {\n\t\tfactor = 0\n\t\tmodifier = {\n\t\t\tadd = 20\n\t\t\ttag = CRL\n\t\t}\n\t}\n\tdefault = no\n\tinitial_show_position = { focus = CRL_audit_the_treasury }\n']
for i, x, y, cost, pre, avail, icon, reward, name, desc in F:
    s = f'\n\tfocus = {{\n\t\tid = {i}\n\t\ticon = {ICON[icon]}\n\t\tx = {x}\n\t\ty = {y}\n\t\tcost = {cost}\n'
    for p in pre: s += f'\t\tprerequisite = {{ focus = {p} }}\n'
    if avail: s += f'\t\tavailable = {{ {avail} }}\n'
    s += '\t\tai_will_do = {\n\t\t\tfactor = 10\n\t\t}\n\t\tcompletion_reward = {\n' + block(reward, 3) + '\t\t}\n\t}\n'
    out.append(s)
out.append('}\n')
open(os.path.join(mod, 'common/national_focus/mortaly_crl_focuses.txt'), 'w', encoding='utf-8').write(''.join(out))

# духи фокусов
M = {
 'CRL_dead_economy_weak': ('Ослабленная мёртвая экономика', 'Экономика всё ещё слаба, но уже работает.', 'production_speed_industrial_complex_factor = -0.07\nindustrial_capacity_factory = -0.07\nstability_factor = -0.02'),
 'CRL_local_industry': ('Опора на внутреннее производство', 'Страна полагается на собственные заводы.', 'industrial_capacity_factory = 0.10'),
 'CRL_war_industry': ('Промышленность на случай войны', 'Заводы готовы быстро перейти на военные заказы.', 'industrial_capacity_factory = 0.05\nproduction_factory_efficiency_gain_factor = 0.10'),
 'CRL_infantry_regulations': ('Единый пехотный устав', 'Пехота действует по общему уставу.', 'army_infantry_attack_factor = 0.05\narmy_infantry_defence_factor = 0.05'),
 'CRL_training_centres': ('Учебные центры', 'Дивизии готовятся быстрее.', 'training_time_factor = -0.15'),
 'CRL_special_forces_school': ('Школа спецназа', 'Штурмовые части получают лучшую подготовку.', 'special_forces_cap = 0.05\nspecial_forces_attack_factor = 0.05'),
 'CRL_standard_weapons': ('Стандартизация вооружения', 'Единые образцы упрощают выпуск пехотного снаряжения.', 'production_factory_efficiency_gain_factor = 0.10'),
 'CRL_northern_garrisons': ('Северные гарнизоны', 'На северных рубежах стоят постоянные гарнизоны.', 'max_dig_in_factor = 0.10'),
 'CRL_general_mobilisation': ('Общая мобилизация', 'Страна готова к войне, ценой спокойствия.', 'war_support_factor = 0.05\nconscription_factor = 0.10'),
 'CRL_closed_country_2': ('Полностью закрытая страна', 'Границы закрыты наглухо.', 'foreign_subversive_activites = -0.2\ntrade_opinion_factor = -0.35'),
 'CRL_internal_security': ('Служба внутренней безопасности', 'Диверсантам трудно работать под её надзором.', 'foreign_subversive_activites = -0.15\nstability_factor = 0.03'),
 'CRL_loyal_officers': ('Лояльное офицерство', 'Офицерский корпус проверен и надёжен.', 'army_morale_factor = 0.05'),
 'CRL_new_plan': ('Новый хозяйственный план', 'Экономика восстанавливается по плану.', 'industrial_capacity_factory = 0.10\nproduction_speed_industrial_complex_factor = 0.15'),
 'CRL_united_nation': ('Единая нация', 'Север и юг снова вместе.', 'stability_factor = 0.10\nwar_support_factor = 0.05'),
}
t = 'ideas = {\n\tcountry = {\n'
for k, (n, d, m) in M.items():
    t += f'\t\t{SP(k)} = {{\n\t\t\tallowed = {{ always = no }}\n\t\t\tremoval_cost = -1\n\t\t\tmodifier = {{\n' + block(m, 4) + '\t\t\t}\n\t\t}\n'
t += '\t}\n}\n'
open(os.path.join(mod, 'common/ideas/mortaly_crl_focus_ideas.txt'), 'w', encoding='utf-8').write(t)

# локализация
ru = 'l_russian:\n'; en = 'l_english:\n'
for i, x, y, cost, pre, avail, icon, reward, name, desc in F:
    ru += f' {i}:0 "{name}"\n {i}_desc:0 "{desc}"\n'; en += f' {i}:0 "{name}"\n {i}_desc:0 "{name}"\n'
for k, (n, d, m) in M.items():
    ru += f' {SP(k)}:0 "{n}"\n {SP(k)}_desc:0 "{d}"\n'; en += f' {SP(k)}:0 "{n}"\n {SP(k)}_desc:0 "{d}"\n'
open(os.path.join(mod, 'localisation/russian/mortaly_crl_focus_l_russian.yml'), 'w', encoding='utf-8-sig').write(ru)
open(os.path.join(mod, 'localisation/english/mortaly_crl_focus_l_english.yml'), 'w', encoding='utf-8-sig').write(en)
print(len(F), 'focuses,', len(M), 'ideas')
