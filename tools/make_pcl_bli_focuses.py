"""Генерирует деревья фокусов Мирной земли (PCL) и Голубых островов (BLI), духи и локализацию.
Запуск из папки мода: python tools/make_pcl_bli_focuses.py"""
import os
base = os.path.dirname(os.path.abspath(__file__))
mod = os.path.join(base, '..', 'mortaly_world')
ICON = {'eco': 'GFX_goal_generic_production', 'build': 'GFX_goal_generic_construction', 'army': 'GFX_goal_generic_army_doctrines',
        'arms': 'GFX_goal_generic_small_arms', 'unity': 'GFX_goal_generic_national_unity', 'pol': 'GFX_goal_generic_political_pressure',
        'mob': 'GFX_goal_generic_forced_march', 'navy': 'GFX_goal_generic_build_navy', 'trade': 'GFX_goal_generic_trade', 'ally': 'GFX_goal_generic_alliance', 'air': 'GFX_goal_generic_air_fighter'}
INF = "every_owned_state = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }"
CIV = "random_owned_state = { add_building_construction = { type = industrial_complex level = 1 instant_build = yes } }"
EQ = lambda n: f"add_equipment_to_stockpile = {{ type = infantry_equipment amount = {n} }}"

PCL = []; BLI = []
def p(*a): PCL.append(a)
def b(*a): BLI.append(a)
W = 'has_country_flag = PCL_won_civil_war'
# ---- Мирная земля: id, x, y, cost, prereqs, available, icon, reward, name, desc
p('PCL_provisional_council', 3, 0, 5, [], '', 'pol', 'add_political_power = 50\nset_country_flag = PCL_council_formed', 'Временный совет', 'Север отделился. Временный совет собирается в Североград, чтобы принимать решения, пока нет ни конституции, ни армии.')
p('PCL_scaf_declaration', 1, 1, 5, ['PCL_provisional_council'], '', 'unity', 'add_stability = 0.05\nadd_political_power = 25', 'Декларация Скафа', 'Скаф и Юри объявляют, что власть принадлежит людям, а не Дворцу власти.')
p('PCL_yuri_command', 5, 1, 5, ['PCL_provisional_council'], '', 'army', 'army_experience = 25\nadd_war_support = 0.03', 'Объединённое командование', 'Скаф и Юри вдвоём возглавляют и страну, и армию Мирной земли.')
p('PCL_restore_civil_rights', 1, 2, 5, ['PCL_scaf_declaration'], '', 'unity', 'add_ideas = PCL_civil_rights', 'Вернуть гражданские права', 'Свобода слова и собраний возвращается первым же указом.')
p('PCL_northern_administration', 5, 2, 5, ['PCL_yuri_command'], '', 'pol', 'add_ideas = PCL_northern_admin', 'Администрация Севера', 'Старые чиновники остаются на местах, но теперь отвечают перед советом.')
p('PCL_call_the_militia', 10, 0, 5, [], '', 'mob', 'add_manpower = 5000\n' + EQ(400), 'Призыв ополчения', 'Тысячи добровольцев приходят в военкоматы с собственными ружьями.')
p('PCL_capture_the_depots', 8, 1, 5, ['PCL_call_the_militia'], 'controls_state = 169', 'arms', EQ(600), 'Северные склады', 'Армейские склады на севере теперь принадлежат Мирной земле.')
p('PCL_people_army', 12, 1, 5, ['PCL_call_the_militia'], '', 'army', 'add_ideas = PCL_people_army', 'Народная армия', 'Ополченцев сводят в дивизии и учат воевать по-настоящему.')
p('PCL_field_command', 12, 2, 5, ['PCL_people_army'], '', 'army', 'add_ideas = PCL_field_command', 'Полевое командование', 'Штабы Юри учатся быстро принимать решения.')
p('PCL_defend_the_north', 10, 3, 10, ['PCL_capture_the_depots', 'PCL_field_command'], '', 'army', 'add_ideas = PCL_northern_defence', 'Удержать Север', 'Рубежи севера укрепляют: отступать некуда.')
p('PCL_appeal_to_the_isles', 18, 0, 5, [], '', 'ally', 'set_country_flag = PCL_appealed_to_isles\nadd_political_power = 25', 'Обращение к Голубым островам', 'Скаф и Юри отправляют послание Голубым островам: Мирной земле нужны друзья.')
p('PCL_supply_corridor', 17, 1, 5, ['PCL_appeal_to_the_isles'], '', 'trade', 'add_ideas = PCL_supply_corridor', 'Морской коридор снабжения', 'Суда с островов привозят грузы в северные порты.')
p('PCL_joint_command', 19, 1, 5, ['PCL_appeal_to_the_isles'], 'BLI = { has_country_flag = BLI_joined_peace_alliance }', 'ally', 'army_experience = 25\nadd_war_support = 0.03', 'Совместное командование', 'Штабы Мирной земли и Голубых островов работают вместе.')
p('PCL_constitution', 24, 0, 10, [], W, 'unity', 'remove_ideas = PCL_provisional_government\nadd_stability = 0.05', 'Конституция Мирной земли', 'Страна принимает конституцию, и временное правительство уходит в историю.')
p('PCL_rebuild_the_country', 22, 1, 5, ['PCL_constitution'], W, 'build', INF + '\n' + CIV, 'Восстановление страны', 'Фабрики, дороги и мосты строят заново.')
p('PCL_civilian_control', 26, 1, 5, ['PCL_constitution'], W, 'pol', 'add_ideas = PCL_civilian_control', 'Гражданский контроль над армией', 'Генералы подчиняются избранным властям.')
p('PCL_amnesty', 24, 2, 5, ['PCL_rebuild_the_country', 'PCL_civilian_control'], W, 'unity', 'add_stability = 0.03\nadd_ideas = PCL_amnesty', 'Общее примирение', 'Бывшим врагам предлагают вернуться домой.')
p('PCL_new_republic', 24, 3, 10, ['PCL_amnesty'], W, 'unity', 'remove_ideas = PCL_popular_uprising\nadd_ideas = PCL_new_republic', 'Новая республика', 'Мирная земля больше не мятеж, а государство.')
# ---- Голубые острова
b('BLI_island_council', 3, 0, 5, [], '', 'pol', 'add_political_power = 50\nadd_stability = 0.03', 'Совет островов', 'Старейшины и капитаны островов собираются, чтобы решить, как жить дальше.')
b('BLI_define_our_status', 1, 1, 5, ['BLI_island_council'], '', 'unity', 'set_country_flag = BLI_status_defined\nadd_political_power = 25', 'Определить наш статус', 'Острова фактически независимы, но Жестокая земля не признаёт этого. Совет решает, что отвечать.')
b('BLI_expand_the_ports', 5, 1, 5, ['BLI_island_council'], '', 'build', INF + '\n' + CIV, 'Расширить гавани', 'Причалы углубляют, склады достраивают.')
b('BLI_coastal_guard', 0, 2, 5, ['BLI_define_our_status'], '', 'navy', 'add_ideas = BLI_coastal_guard', 'Береговая охрана', 'Дозорные катера и береговые батареи охраняют проливы.')
b('BLI_island_militia', 2, 2, 5, ['BLI_define_our_status'], '', 'army', 'add_ideas = BLI_island_militia\n' + EQ(150), 'Островное ополчение', 'Жители островов учатся держать оружие.')
b('BLI_trade_routes', 5, 2, 5, ['BLI_expand_the_ports'], '', 'trade', 'add_ideas = BLI_trade_routes', 'Морские торговые пути', 'Острова торгуют со всем миром, кроме враждебных соседей.')
b('BLI_island_defence_network', 1, 3, 10, ['BLI_coastal_guard', 'BLI_island_militia'], '', 'army', 'swap_ideas = { remove_idea = BLI_island_defence add_idea = BLI_island_defence_2 }', 'Единая система обороны островов', 'Береговая охрана, гарнизоны и маяки связаны в одну сеть.')
b('BLI_open_the_ports', 5, 3, 5, ['BLI_trade_routes'], 'has_global_flag = civil_war_started', 'trade', 'set_country_flag = BLI_ports_open\nif = { limit = { country_exists = PCL } PCL = { add_ideas = BLI_open_harbours } }', 'Открыть порты Севера', 'Гавани островов открыты для кораблей Мирной земли.')
b('BLI_volunteer_detachment', 5, 4, 5, ['BLI_open_the_ports'], '', 'mob', 'set_country_flag = BLI_sent_volunteers\nif = { limit = { country_exists = PCL } PCL = { ' + EQ(200) + ' } }', 'Добровольческий отряд', 'Островные добровольцы отплывают на север.')
b('BLI_join_the_peace_alliance', 7, 4, 5, ['BLI_open_the_ports'], 'country_exists = PCL', 'ally', 'mortaly_bli_join_war = yes\ngive_guarantee = PCL', 'Союз с Мирной землёй', 'Острова и север заключают союз.')
b('BLI_international_recognition', 5, 5, 10, ['BLI_volunteer_detachment', 'BLI_join_the_peace_alliance'], 'has_global_flag = civil_war_ended', 'pol', 'remove_ideas = BLI_disputed_status\nadd_ideas = BLI_recognition', 'Международное признание', 'После войны острова добиваются признания.')
b('BLI_status_treaty', 5, 6, 10, ['BLI_international_recognition'], 'has_global_flag = pcl_won_civil_war', 'pol', 'add_political_power = 50\nadd_stability = 0.05\nset_country_flag = BLI_status_treaty_signed', 'Договор о статусе островов', 'Мирная земля признаёт независимость островов и подписывает договор о торговле и ненападении.')

# ---- Голубые острова: базовые фокусы армии, авиации и флота (этап 24)
b('BLI_army_foundation', 10, 0, 5, [], '', 'army', 'add_ideas = BLI_army_foundation\narmy_experience = 10', 'Основы армии', 'Островные гарнизоны сводят в единую армию с общим уставом и учебными лагерями.')
b('BLI_army_training', 10, 1, 5, ['BLI_army_foundation'], '', 'mob', 'army_experience = 20\nadd_manpower = 2000', 'Учебные лагеря', 'Новобранцев учат на каждом острове, чтобы резерв был всегда под рукой.')
b('BLI_army_equipment', 10, 2, 5, ['BLI_army_training'], '', 'arms', EQ(250) + '\nset_technology = { infantry_weapons1 = 1 tech_support = 1 }', 'Вооружение армии', 'Склады островов пополняют винтовками, а ремонтные мастерские учатся делать больше.')
b('BLI_air_foundation', 14, 0, 5, [], '', 'air', 'set_technology = { early_fighter = 1 }\nrandom_owned_state = { add_building_construction = { type = air_base level = 1 instant_build = yes } }', 'Основы авиации', 'На главном острове строят первый аэродром и учат первых лётчиков.')
b('BLI_air_squadrons', 14, 1, 5, ['BLI_air_foundation'], '', 'air', 'add_ideas = BLI_air_squadrons\nadd_equipment_to_stockpile = { type = fighter_equipment_1 amount = 30 producer = BLI }', 'Островные эскадрильи', 'Первые истребители прикрывают небо над островами и проливами.')
b('BLI_air_defence', 14, 2, 5, ['BLI_air_squadrons'], '', 'air', 'air_experience = 25', 'Воздушная оборона', 'Посты наблюдения и зенитные точки связывают с аэродромом общей сетью оповещения.')
b('BLI_navy_foundation', 18, 0, 5, [], '', 'navy', 'add_ideas = BLI_navy_foundation\nset_technology = { early_ship_hull_light = 1 early_ship_hull_submarine = 1 basic_battery = 1 basic_torpedo = 1 basic_depth_charges = 1 }', 'Основы флота', 'Рыбацкие и торговые суда переоборудуют в боевые, а капитанов учат воевать.')
b('BLI_navy_harbours', 18, 1, 5, ['BLI_navy_foundation'], '', 'build', 'random_owned_state = { limit = { is_coastal = yes } add_building_construction = { type = dockyard level = 1 instant_build = yes } }\nadd_equipment_to_stockpile = { type = convoy_1 amount = 20 }', 'Верфи островов', 'Достраивают верфи и пополняют запас транспортных судов.')
b('BLI_navy_fleet', 18, 2, 5, ['BLI_navy_harbours'], '', 'navy', 'add_ideas = BLI_navy_fleet\nnavy_experience = 25', 'Флот островов', 'Эсминцы и подводные лодки несут дозор между островами.')

M = {
 'PCL_civil_rights': ('Гражданские права', 'Свобода слова и собраний укрепляет поддержку нового государства.', 'stability_factor = 0.05'),
 'PCL_northern_admin': ('Администрация Севера', 'Местные чиновники подчиняются Временному совету.', 'stability_factor = 0.03\npolitical_power_gain = 0.05'),
 'PCL_people_army': ('Народная армия', 'Ополчение превращается в регулярные дивизии.', 'army_infantry_attack_factor = 0.08\narmy_infantry_defence_factor = 0.08'),
 'PCL_field_command': ('Полевое командование', 'Штабы быстро реагируют на изменения на фронте.', 'army_morale_factor = 0.05\nplanning_speed = 0.10'),
 'PCL_northern_defence': ('Удержать Север', 'Рубежи севера укреплены.', 'max_dig_in_factor = 0.15\narmy_defence_factor = 0.05'),
 'PCL_supply_corridor': ('Морской коридор снабжения', 'Грузы с островов идут в северные порты.', 'land_reinforce_rate = 0.05'),
 'PCL_civilian_control': ('Гражданский контроль над армией', 'Армия подчиняется выборным властям.', 'stability_factor = 0.05\npolitical_power_gain = 0.10'),
 'PCL_amnesty': ('Общее примирение', 'Бывшие противники возвращаются к мирной жизни.', 'stability_factor = 0.03\nwar_support_factor = 0.02'),
 'BLI_coastal_guard': ('Береговая охрана', 'Катера и батареи прикрывают острова.', 'army_defence_factor = 0.05\nmax_dig_in_factor = 0.10'),
 'BLI_island_militia': ('Островное ополчение', 'Жители островов готовы защищать их.', 'army_infantry_defence_factor = 0.05\nconscription_factor = 0.05'),
 'BLI_trade_routes': ('Морские торговые пути', 'Торговля приносит островам деньги и влияние.', 'industrial_capacity_factory = 0.05\npolitical_power_gain = 0.10'),
 'BLI_island_defence_2': ('Единая оборона островов', 'Все острова защищены общей системой обороны.', 'army_defence_factor = 0.25\nmax_dig_in_factor = 0.25'),
 'BLI_open_harbours': ('Гавани Голубых островов', 'Корабли островов подвозят припасы.', 'land_reinforce_rate = 0.05'),
 'BLI_army_foundation': ('Основы армии', 'Общий устав и учебные лагеря на всех островах.', 'army_infantry_attack_factor = 0.05\ntraining_time_factor = -0.10'),
 'BLI_air_squadrons': ('Островные эскадрильи', 'Истребители прикрывают острова и проливы.', 'air_attack_factor = 0.05\nair_superiority_efficiency = 0.05'),
 'BLI_navy_foundation': ('Основы флота', 'Островные капитаны знают каждый пролив.', 'naval_speed_factor = 0.05'),
 'BLI_navy_fleet': ('Флот островов', 'Дозорные корабли охраняют морские пути.', 'convoy_escort_efficiency = 0.10'),
 'BLI_recognition': ('Международное признание', 'Мир признал острова независимыми.', 'stability_factor = 0.05\npolitical_power_gain = 0.10'),
}
import re
FIDS = {r[0] for r in PCL + BLI}
def SP(k): return k + '_spirit' if (k in FIDS or k == 'PCL_new_republic') else k
def block(text, tabs):
    text = re.sub(r'(add_ideas|remove_ideas|add_idea|remove_idea) = (\w+)', lambda m: m.group(1) + ' = ' + SP(m.group(2)), text)
    return ''.join('\t' * tabs + l + '\n' for l in text.split('\n') if l.strip())
def tree(tid, tag, rows, first):
    out = [f'focus_tree = {{\n\tid = {tid}\n\tcountry = {{\n\t\tfactor = 0\n\t\tmodifier = {{\n\t\t\tadd = 20\n\t\t\ttag = {tag}\n\t\t}}\n\t}}\n\tdefault = no\n\tinitial_show_position = {{ focus = {first} }}\n']
    for i, x, y, cost, pre, avail, icon, reward, name, desc in rows:
        s = f'\n\tfocus = {{\n\t\tid = {i}\n\t\ticon = {ICON[icon]}\n\t\tx = {x}\n\t\ty = {y}\n\t\tcost = {cost}\n'
        for q in pre: s += f'\t\tprerequisite = {{ focus = {q} }}\n'
        if avail: s += f'\t\tavailable = {{ {avail} }}\n'
        s += '\t\tai_will_do = {\n\t\t\tfactor = 10\n\t\t}\n\t\tcompletion_reward = {\n' + block(reward, 3) + '\t\t}\n\t}\n'
        out.append(s)
    out.append('}\n'); return ''.join(out)
open(os.path.join(mod, 'common/national_focus/mortaly_pcl_focuses.txt'), 'w', encoding='utf-8').write(tree('mortaly_pcl_tree', 'PCL', PCL, 'PCL_provisional_council'))
open(os.path.join(mod, 'common/national_focus/mortaly_bli_focuses.txt'), 'w', encoding='utf-8').write(tree('mortaly_bli_tree', 'BLI', BLI, 'BLI_island_council'))
t = 'ideas = {\n\tcountry = {\n'
for k, (n, d, m) in M.items():
    t += f'\t\t{SP(k)} = {{\n\t\t\tallowed = {{ always = no }}\n\t\t\tremoval_cost = -1\n\t\t\tmodifier = {{\n' + block(m, 4) + '\t\t\t}\n\t\t}\n'
open(os.path.join(mod, 'common/ideas/mortaly_pcl_bli_focus_ideas.txt'), 'w', encoding='utf-8').write(t + '\t}\n}\n')
ru = 'l_russian:\n'; en = 'l_english:\n'
for r in PCL + BLI:
    ru += f' {r[0]}:0 "{r[8]}"\n {r[0]}_desc:0 "{r[9]}"\n'; en += f' {r[0]}:0 "{r[8]}"\n {r[0]}_desc:0 "{r[8]}"\n'
for k, (n, d, m) in M.items():
    ru += f' {SP(k)}:0 "{n}"\n {SP(k)}_desc:0 "{d}"\n'; en += f' {SP(k)}:0 "{n}"\n {SP(k)}_desc:0 "{d}"\n'
open(os.path.join(mod, 'localisation/russian/mortaly_pcl_bli_focus_l_russian.yml'), 'w', encoding='utf-8-sig').write(ru)
open(os.path.join(mod, 'localisation/english/mortaly_pcl_bli_focus_l_english.yml'), 'w', encoding='utf-8-sig').write(en)
print(len(PCL), len(BLI), len(M))
