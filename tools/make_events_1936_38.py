# Генератор событий 1936-1938 (этап 20). Запуск из папки mortaly_world: python ../tools/make_events_1936_38.py
import os
E = []  # (namespace, num, tag, trigger, mtth, title, desc, [(label, effect, ai)])
def ev(ns, n, tag, trig, mtth, title, desc, opts): E.append((ns, n, tag, trig, mtth, title, desc, opts))
NOWAR = 'NOT = { has_global_flag = civil_war_started }'
ev('mortaly_crl', 1, 'CRL', 'date > 1936.2.1\ndate < 1936.12.1', 15, 'Казна пуста',
   'Министр финансов докладывает Дворцу власти, что денег хватит максимум на три месяца. Заводы стоят без заказов, а армия ждёт жалованья. Кого спасать первым?',
   [('Направить остатки казны в промышленность', 'add_timed_idea = { idea = CRL_treasury_industry days = 365 }', 1),
    ('Отдать всё армии', 'add_equipment_to_stockpile = { type = infantry_equipment amount = 400 }\nadd_timed_idea = { idea = CRL_treasury_army days = 365 }', 1)])
ev('mortaly_crl', 2, 'CRL', 'date > 1936.4.1\ndate < 1937.1.1', 20, 'Кому принадлежат Голубые острова?',
   'Совет Дворца власти снова вспомнил про Голубые острова. По старым картам они принадлежат Жестокой земле, а сами острова считают себя независимыми. Воевать из-за них сейчас никто не собирается, но молчать тоже нельзя.',
   [('Подтвердить, что острова принадлежат нам', 'add_political_power = 25\nset_country_flag = CRL_islands_claim_declared\nif = { limit = { country_exists = BLI } BLI = { country_event = { id = mortaly_bli.1 days = 2 } } }', 1),
    ('Не поднимать вопрос, пока не кончатся дела поважнее', 'add_stability = 0.02\nif = { limit = { country_exists = BLI } BLI = { country_event = { id = mortaly_bli.1 days = 2 } } }', 1)])
ev('mortaly_bli', 1, 'BLI', None, 0, 'Что думает Дворец власти о наших островах?',
   'Из Жестокой земли пришло напоминание, что острова считаются её территорией. Совет островов должен ответить хотя бы для себя.',
   [('Мы независимы, и это не обсуждается', 'add_stability = 0.03\nset_country_flag = BLI_independence_affirmed', 1),
    ('Делать вид, что письма не было', 'add_political_power = 25', 1)])
ev('mortaly_crl', 3, 'CRL', 'date > 1937.2.1\ndate < 1938.1.1', 15, 'Забастовка северных рабочих',
   'Северные рабочие требуют повысить жалованье и вернуть отнятые выходные. Забастовка уже остановила два завода. Что ответит Дворец власти?',
   [('Пойти на уступки', 'add_timed_idea = { idea = CRL_strike_concessions days = 180 }\nset_country_flag = CRL_north_conceded', 1),
    ('Подавить забастовку силой', 'add_stability = 0.03\nset_country_flag = CRL_north_repressed', 1)])
ev('mortaly_crl', 4, 'CRL', 'date > 1937.6.1\ndate < 1938.4.1', 20, 'Офицерский корпус разделён',
   'Часть офицеров сочувствует северу и открыто говорит об этом. Верные Дворцу власти требуют навести порядок, пока не поздно.',
   [('Убрать сочувствующих из армии', 'add_stability = -0.03\narmy_experience = 10\nset_country_flag = CRL_officers_purged', 1),
    ('Закрыть глаза и не раздувать конфликт', 'add_political_power = 25\nset_country_flag = CRL_officers_tolerated', 1)])
ev('mortaly_crl', 5, 'CRL', 'date > 1938.1.15\ndate < 1938.9.1', 15, 'Скаф и Юри',
   'Агенты сообщают, что северное движение сплотилось вокруг двух имён: Скафа, к которому прислушиваются в городах, и Юри, которому верят в казармах. Пока это только разговоры.',
   [('Взять обоих под наблюдение', 'add_political_power = -25\nadd_stability = 0.02\nset_global_flag = scaf_yuri_movement\nset_country_flag = CRL_watching_scaf_yuri', 1),
    ('Не придавать значения', 'add_political_power = 25\nset_global_flag = scaf_yuri_movement', 1)])
ev('mortaly_crl', 6, 'CRL', 'date > 1938.8.1\ndate < 1939.1.1', 15, 'Последний приказ Дворца власти',
   'Дворец власти решает навести порядок на севере раз и навсегда. Приказ сулит прочную оборону, но северяне уже недовольны.',
   [('Усилить контроль над севером', 'add_timed_idea = { idea = CRL_last_order_defence days = 365 }\nset_country_flag = CRL_north_tightened', 1),
    ('Выслушать северных старейшин', 'add_stability = 0.05\nset_country_flag = CRL_north_heard', 1)])
ev('mortaly_bli', 2, 'BLI', 'date > 1938.6.1\ndate < 1939.1.1', 20, 'Вести с севера',
   'На острова приходят слухи, что на севере Жестокой земли готовят выступление. Совет островов должен решить, на чьей он стороне, если оно начнётся.',
   [('Готовиться помочь северянам', 'set_country_flag = BLI_prepared_to_help\nadd_political_power = 25', 1),
    ('Остаться в стороне', 'add_stability = 0.02\nset_country_flag = BLI_prepared_neutral', 0)])

out = ''
ru = 'l_russian:\n'; en = 'l_english:\n'
for ns in sorted({e[0] for e in E}): out += f'add_namespace = {ns}\n'
out += '\n'
for ns, n, tag, trig, mtth, title, desc, opts in E:
    eid = f'{ns}.{n}'
    out += f'country_event = {{\n\tid = {eid}\n\ttitle = {eid}.t\n\tdesc = {eid}.d\n'
    if trig is None:
        out += '\tis_triggered_only = yes\n'
    else:
        out += f'\tfire_only_once = yes\n\ttrigger = {{\n\t\toriginal_tag = {tag}\n\t\t{NOWAR}\n' + ''.join(f'\t\t{l}\n' for l in trig.split('\n')) + f'\t}}\n\tmean_time_to_happen = {{\n\t\tdays = {mtth}\n\t}}\n'
    for i, (label, eff, ai) in enumerate(opts):
        k = 'ab'[i]
        out += f'\toption = {{\n\t\tname = {eid}.{k}\n' + ''.join(f'\t\t{l}\n' for l in eff.split('\n')) + f'\t\tai_chance = {{ factor = {max(ai,0) if ai else 0} }}\n\t}}\n'
        ru += f' {eid}.{k}:0 "{label}"\n'; en += f' {eid}.{k}:0 "{label}"\n'
    out += '}\n\n'
    ru += f' {eid}.t:0 "{title}"\n {eid}.d:0 "{desc}"\n'; en += f' {eid}.t:0 "{title}"\n {eid}.d:0 "{desc}"\n'
open('events/mortaly_events_1936_38.txt', 'w', encoding='utf-8').write(out)
open('localisation/russian/mortaly_events_1936_38_l_russian.yml', 'w', encoding='utf-8-sig').write(ru)
open('localisation/english/mortaly_events_1936_38_l_english.yml', 'w', encoding='utf-8-sig').write(en)
M = {'CRL_treasury_industry': ('Казна в промышленность', 'Остатки казны вложены в заводы.', 'industrial_capacity_factory = 0.05'),
 'CRL_treasury_army': ('Казна в армию', 'Армия получила деньги, заводы остались без заказов.', 'industrial_capacity_factory = -0.05'),
 'CRL_strike_concessions': ('Уступки рабочим', 'Рабочие довольны, но выпуск упал.', 'industrial_capacity_factory = -0.04'),
 'CRL_last_order_defence': ('Последний приказ', 'Север укреплён и охраняется усиленно.', 'army_defence_factor = 0.10')}
t = 'ideas = {\n\tcountry = {\n'
l_ru = ''; l_en = ''
for k, (nm, d, m) in M.items():
    t += f'\t\t{k} = {{\n\t\t\tallowed = {{ always = no }}\n\t\t\tremoval_cost = -1\n\t\t\tmodifier = {{\n\t\t\t\t{m}\n\t\t\t}}\n\t\t}}\n'
    l_ru += f' {k}:0 "{nm}"\n {k}_desc:0 "{d}"\n'
open('common/ideas/mortaly_event_ideas.txt', 'w', encoding='utf-8').write(t + '\t}\n}\n')
open('localisation/russian/mortaly_events_1936_38_l_russian.yml', 'a', encoding='utf-8-sig').write(l_ru)
open('localisation/english/mortaly_events_1936_38_l_english.yml', 'a', encoding='utf-8-sig').write(l_ru)
print(len(E), 'events')
