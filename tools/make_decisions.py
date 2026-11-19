# Генератор решений CRL/PCL/BLI; запуск из папки mortaly_world: python ../tools/make_decisions.py
import os
NORTH = list(range(169, 185)) + list(range(217, 265))
def bunkers(ids, lvl, tabs=3):
    return ''.join('\t'*tabs + f"{i} = {{ add_building_construction = {{ type = bunker level = {lvl} province = {i} instant_build = yes }} }}\n" for i in ids)
def dec(name, icon, cost, avail, effect, visible='', extra='', fire_once=False, re_enable=0, remove=0, modifier='', ai=1):
    s = f'\t{name} = {{\n\t\ticon = {icon}\n\t\tcost = {cost}\n'
    if visible: s += f'\t\tvisible = {{\n\t\t\t{visible}\n\t\t}}\n'
    if avail: s += f'\t\tavailable = {{\n\t\t\t{avail}\n\t\t}}\n'
    if fire_once: s += '\t\tfire_only_once = yes\n'
    if re_enable: s += f'\t\tdays_re_enable = {re_enable}\n'
    if remove:
        s += f'\t\tdays_remove = {remove}\n'
    if modifier: s += '\t\tmodifier = {\n' + ''.join(f'\t\t\t{l}\n' for l in modifier.split('\n')) + '\t\t}\n'
    s += '\t\tcomplete_effect = {\n' + ''.join(('\t\t\t'+l+'\n') if not l.startswith('\t') else l+'\n' for l in effect.rstrip('\n').split('\n')) + '\t\t}\n'
    s += f'\t\tai_will_do = {{\n\t\t\tfactor = {ai}\n\t\t}}\n\t}}\n'
    return s
PRE = 'NOT = { has_global_flag = civil_war_started }'
# ---- категории ----
cats = '''CRL_economic_recovery = {
	icon = generic_industry
	allowed = { original_tag = CRL }
	visible = { NOT = { has_global_flag = civil_war_started } }
}
CRL_prepare_for_split = {
	icon = generic_military
	allowed = { original_tag = CRL }
	visible = { NOT = { has_global_flag = civil_war_started } }
}
PCL_provisional_gov_cat = {
	icon = generic_political_actions
	allowed = { original_tag = PCL }
}
BLI_support_the_north = {
	icon = generic_prepare_civil_war
	allowed = { original_tag = BLI }
}
'''
open('common/decisions/categories/mortaly_categories.txt','w',encoding='utf-8').write(cats)
# ---- решения CRL ----
c1 = 'CRL_economic_recovery = {\n'
c1 += dec('CRL_check_state_enterprises','generic_industry',25,'','add_timed_idea = { idea = CRL_enterprise_audit days = 180 }',re_enable=120)
c1 += dec('CRL_launch_the_mines','generic_industry',50,'','add_timed_idea = { idea = CRL_mines_running days = 120 }',re_enable=180)
c1 += dec('CRL_restore_workshops','generic_industry',50,'','add_timed_idea = { idea = CRL_workshops_output days = 120 }\nadd_equipment_to_stockpile = { type = infantry_equipment amount = 100 }',re_enable=180)
c1 += dec('CRL_resource_rationing','generic_industry',35,'','add_timed_idea = { idea = CRL_rationing days = 90 }',re_enable=240)
c1 += dec('CRL_redirect_army_orders','generic_industry',35,'','add_timed_idea = { idea = CRL_army_orders days = 90 }\nadd_equipment_to_stockpile = { type = infantry_equipment amount = 200 }',re_enable=240)
c1 += '}\nCRL_prepare_for_split = {\n'
c1 += dec('CRL_fortify_northern_line','generic_military',75,'has_country_flag = CRL_northern_question_raised',bunkers(NORTH,1).rstrip('\n')+'\nset_country_flag = CRL_north_fortified',fire_once=True)
c1 += dec('CRL_evacuate_army_depots','generic_military',50,'has_country_flag = CRL_northern_question_raised','add_equipment_to_stockpile = { type = infantry_equipment amount = 500 }\nset_country_flag = CRL_depots_evacuated',fire_once=True)
c1 += dec('CRL_check_the_officers','generic_military',40,'','add_timed_idea = { idea = CRL_officer_checks days = 365 }\nset_country_flag = CRL_officers_loyal',fire_once=True)
c1 += dec('CRL_prepare_the_capital','generic_military',50,'','210 = { add_building_construction = { type = bunker level = 2 province = 210 instant_build = yes } }\nset_country_flag = CRL_capital_prepared',fire_once=True)
c1 += dec('CRL_form_the_reserve','generic_military',40,'','add_equipment_to_stockpile = { type = infantry_equipment amount = 300 }\nadd_manpower = 4000',re_enable=120)
c1 += '}\n'
open('common/decisions/mortaly_crl_decisions.txt','w',encoding='utf-8').write(c1)
# ---- PCL ----
p = 'PCL_provisional_gov_cat = {\n'
p += dec('PCL_urgent_mobilisation','generic_military',50,'','add_manpower = 6000\nadd_equipment_to_stockpile = { type = infantry_equipment amount = 300 }',re_enable=120)
p += dec('PCL_requisition_depots','generic_military',40,'controls_state = 169','add_equipment_to_stockpile = { type = infantry_equipment amount = 600 }',fire_once=True)
p += dec('PCL_field_hospitals','generic_political_actions',35,'','add_timed_idea = { idea = PCL_field_hospitals_idea days = 120 }',re_enable=180)
p += dec('PCL_protect_rail_hub','generic_construction',35,'','add_timed_idea = { idea = PCL_rail_hub days = 120 }',re_enable=180)
p += '}\n'
open('common/decisions/mortaly_pcl_decisions.txt','w',encoding='utf-8').write(p)
# ---- BLI ----
b = 'BLI_support_the_north = {\n'
b += dec('BLI_supply_volunteer_arms','generic_military',25,'country_exists = PCL\nhas_global_flag = civil_war_started','PCL = { add_equipment_to_stockpile = { type = infantry_equipment amount = 200 } }',re_enable=90)
b += dec('BLI_send_volunteer_division','generic_military',75,'country_exists = PCL\nhas_global_flag = civil_war_started','mortaly_spawn_bli_volunteers = yes\nset_country_flag = BLI_division_sent',fire_once=True)
b += dec('BLI_open_the_harbours','generic_construction',25,'country_exists = PCL\nhas_global_flag = civil_war_started','PCL = { add_timed_idea = { idea = BLI_open_harbours days = 120 } }',re_enable=150)
b += dec('BLI_sea_convoy','generic_naval',50,'country_exists = PCL\nhas_global_flag = civil_war_started','PCL = { add_equipment_to_stockpile = { type = infantry_equipment amount = 150 } }\nadd_timed_idea = { idea = BLI_convoy_effort days = 90 }',re_enable=120)
b += '}\n'
open('common/decisions/mortaly_bli_decisions.txt','w',encoding='utf-8').write(b)
# ---- духи решений ----
M = {
 'CRL_enterprise_audit': ('Проверка предприятий', 'Проверенные государственные предприятия работают лучше.', 'industrial_capacity_factory = 0.04'),
 'CRL_mines_running': ('Работающие шахты', 'Шахты временно дают больше сырья для заводов.', 'industrial_capacity_factory = 0.06'),
 'CRL_workshops_output': ('Мастерские на подъёме', 'Мастерские выпускают продукцию быстрее.', 'production_factory_efficiency_gain_factor = 0.15'),
 'CRL_rationing': ('Нормирование ресурсов', 'Промышленность получает приоритет, население затягивает пояса.', 'industrial_capacity_factory = 0.10\nstability_factor = -0.05'),
 'CRL_army_orders': ('Армейские заказы', 'Гражданские заводы временно работают на армию.', 'industrial_capacity_factory = -0.05\nproduction_speed_industrial_complex_factor = -0.10'),
 'CRL_officer_checks': ('Проверка офицеров', 'Офицеры лояльны, но доверие в войсках упало.', 'army_morale_factor = 0.05\nstability_factor = -0.03'),
 'PCL_field_hospitals_idea': ('Полевые госпитали', 'Раненые быстрее возвращаются в строй.', 'land_reinforce_rate = 0.10\narmy_morale_factor = 0.05'),
 'PCL_rail_hub': ('Железнодорожный узел под охраной', 'Снабжение севера стало надёжнее.', 'land_reinforce_rate = 0.05\narmy_defence_factor = 0.05'),
 'BLI_convoy_effort': ('Морской конвой', 'Конвои идут на север, и островам приходится затянуть пояса.', 'political_power_gain = -0.05'),
}
t = 'ideas = {\n\tcountry = {\n'
for k,(n,d,m) in M.items():
    t += f'\t\t{k} = {{\n\t\t\tallowed = {{ always = no }}\n\t\t\tremoval_cost = -1\n\t\t\tmodifier = {{\n' + ''.join(f'\t\t\t\t{l}\n' for l in m.split('\n')) + '\t\t\t}\n\t\t}\n'
open('common/ideas/mortaly_decision_ideas.txt','w',encoding='utf-8').write(t + '\t}\n}\n')
# ---- OOB добровольцев ----
oob = '''units = {
	division_template = {
		name = "Добровольческая дивизия островов"
		regiments = {
			infantry = { x = 0 y = 0 }
			infantry = { x = 0 y = 1 }
			infantry = { x = 0 y = 2 }
			infantry = { x = 1 y = 0 }
			infantry = { x = 1 y = 1 }
			infantry = { x = 1 y = 2 }
			infantry = { x = 2 y = 0 }
			infantry = { x = 2 y = 1 }
			infantry = { x = 2 y = 2 }
		}
	}
	units = {
		division = {
			name = "1-я островная добровольческая"
			location = 169
			division_template = "Добровольческая дивизия островов"
			start_experience_factor = 0.3
			start_equipment_factor = 0.7
		}
	}
}
'''
pass
# ---- локализация ----
D = {
 'CRL_economic_recovery': ('Экономическое восстановление', ''), 'CRL_prepare_for_split': ('Подготовка к расколу', ''),
 'PCL_provisional_gov_cat': ('Временное правительство', ''), 'BLI_support_the_north': ('Поддержка Севера', ''),
 'CRL_check_state_enterprises': ('Проверить государственные предприятия', 'Ревизоры проверяют заводы и шахты. Это немного смягчает последствия мёртвой экономики.'),
 'CRL_launch_the_mines': ('Запустить шахты', 'Шахты на время дают дополнительное сырьё.'),
 'CRL_restore_workshops': ('Восстановить мастерские', 'Мастерские возобновляют выпуск, и армия получает немного снаряжения.'),
 'CRL_resource_rationing': ('Нормирование ресурсов', 'Промышленность получает бонус, а жителям это не нравится.'),
 'CRL_redirect_army_orders': ('Перенаправить заказы армии', 'Гражданские фабрики временно работают на армию.'),
 'CRL_fortify_northern_line': ('Укрепить Северный рубеж', 'В северных стейтах строят дополнительные укрепления.'),
 'CRL_evacuate_army_depots': ('Вывезти армейские склады', 'Часть снаряжения вывозят из северных складов, пока их не заняли.'),
 'CRL_check_the_officers': ('Проверить офицеров', 'Ненадёжных офицеров убирают, а в войсках растёт напряжение.'),
 'CRL_prepare_the_capital': ('Подготовить столицу', 'Вокруг Дворца власти строят новые укрепления.'),
 'CRL_form_the_reserve': ('Сформировать резерв', 'Создаётся запас людей и оружия.'),
 'PCL_urgent_mobilisation': ('Срочная мобилизация', 'Призывают людей и выдают им оружие со складов.'),
 'PCL_requisition_depots': ('Реквизировать склады', 'Армейские склады севера переходят к Мирной земле.'),
 'PCL_field_hospitals': ('Организовать полевые госпитали', 'Раненые быстрее возвращаются в строй.'),
 'PCL_protect_rail_hub': ('Защитить железнодорожный узел', 'Охраняют железнодорожный узел, чтобы снабжение шло без перебоев.'),
 'BLI_supply_volunteer_arms': ('Поставить оружие добровольцам', 'Острова передают Мирной земле часть пехотного снаряжения.'),
 'BLI_send_volunteer_division': ('Отправить добровольческий отряд', 'Одна островная дивизия отплывает на север.'),
 'BLI_open_the_harbours': ('Открыть гавани', 'Мирная земля временно получает доступ к островным портам.'),
 'BLI_sea_convoy': ('Морской конвой', 'Конвой везёт припасы на север.'),
}
ru = 'l_russian:\n'; en = 'l_english:\n'
for k,(n,d) in D.items():
    ru += f' {k}:0 "{n}"\n'; en += f' {k}:0 "{n}"\n'
    if d: ru += f' {k}_desc:0 "{d}"\n'; en += f' {k}_desc:0 "{d}"\n'
for k,(n,d,m) in M.items():
    ru += f' {k}:0 "{n}"\n {k}_desc:0 "{d}"\n'; en += f' {k}:0 "{n}"\n {k}_desc:0 "{d}"\n'
open('localisation/russian/mortaly_decisions_l_russian.yml','w',encoding='utf-8-sig').write(ru)
open('localisation/english/mortaly_decisions_l_english.yml','w',encoding='utf-8-sig').write(en)
