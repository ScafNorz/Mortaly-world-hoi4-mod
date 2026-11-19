# Генератор common/scripted_effects/mortaly_spawn.txt. Запуск из папки mortaly_world: python ../tools/make_spawn.py
def tmpl(name, n=9):
    t = f'\t\tdivision_template = {{\n\t\t\tname = "{name}"\n\t\t\tregiments = {{\n'
    cells = [(x, y) for x in range(3) for y in range(3)][:n]
    for x, y in cells: t += f'\t\t\t\tinfantry = {{ x = {x} y = {y} }}\n'
    return t + '\t\t\t}\n\t\t}\n'
def eff(key, tag, tname, dname, count, loc, exp, eq, n=9):
    # create_unit работает в области состояния (state): оборачиваем в "<номер стейта> = { ... }"
    return (f'{key} = {{\n\t{tag} = {{\n' + tmpl(tname, n) + '\t}\n' +
            f'\t{loc} = {{\n\t\tcreate_unit = {{\n\t\t\tdivision = "name = \\"{dname}\\" division_template = \\"{tname}\\" start_experience_factor = {exp} start_equipment_factor = {eq}"\n'
            f'\t\t\towner = {tag}\n\t\t\tcount = {count}\n\t\t\tallow_spawning_on_enemy_provs = yes\n\t\t}}\n\t}}\n}}\n\n')
out = '# Появление дивизий через create_unit (генератор: tools/make_spawn.py)\n\n'
out += eff('mortaly_spawn_pcl_base', 'PCL', 'PCL Peoples Infantry', 'Peoples Division', 7, 242, 0.2, 0.8)
out += eff('mortaly_spawn_pcl_defectors', 'PCL', 'PCL Defectors', 'Defector Division', 2, 242, 0.5, 0.9)
out += eff('mortaly_spawn_pcl_rebels', 'PCL', 'PCL Rebels', 'Rebel Division', 2, 242, 0.1, 0.6)
out += eff('mortaly_spawn_crl_army', 'CRL', 'CRL Palace Infantry', 'Palace Division', 10, 210, 0.3, 0.85)
out += eff('mortaly_spawn_crl_guard', 'CRL', 'CRL Guard', 'Guard Division', 2, 210, 0.5, 0.9)
out += eff('mortaly_spawn_bli_volunteers', 'PCL', 'BLI Volunteers', 'Island Volunteers', 1, 242, 0.3, 0.7)
open('common/scripted_effects/mortaly_spawn.txt', 'w', encoding='utf-8').write(out)
print('spawn ok')
