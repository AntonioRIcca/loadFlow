
import yaml
# from PIL import Image, ImageDraw, ImageFont
import os
import copy
import numpy as np

path = os.getcwd()
print(path)

# dictionary = dict()
filename = 'network_extended.yml'
print(os.path.join(path, filename))
dictionary = yaml.safe_load(open(os.path.join(path, filename)))
print('ok')

walk_dict = True
level_cat = dict()
level_cat['AC'] = dict()
# levels['AC'][20] = ['City_BB']
level_cat['DC'] = dict()
map_draw = dict()
map_draw['bus'] = dict()

links = dict()

# d = copy.deepcopy(dictionary['External Grid']['node']['City_BB'])       # da correggere
# new_dicts = [d]
# nodes = list(d.keys())
# all_nodes = nodes
# all_buses = dict()
# all_buses['City_BB'] = d
# print(nodes)
elem_nums = [0]

l_num = 0
cat = ('', '')
for bus in dictionary['nodes']:
    level = dictionary['nodes'][bus]['voltage']
    typology = dictionary['nodes'][bus]['typology']
    if level not in list(level_cat[typology].keys()):
        level_cat[typology][level] = []
    level_cat[typology][level].append(bus)

print(level_cat)
levels = dict()

for typology in['AC', 'DC']:
    for level in level_cat[typology]:
        if cat != (typology, level):
            l_num += 1
            cat = (typology, level)
            levels[l_num] = []

        multilevel = False
        for bus in level_cat[typology][level]:
            for link in dictionary['nodes'][bus]['links_down']:
                if dictionary['nodes'][bus]['links_down'][link] == 'Line':
                    multilevel = True
                    pass

        if multilevel:
            buses = level_cat[typology][level]
            done = []

            while buses != []:
                if levels[l_num]:
                    l_num += 1
                    levels[l_num] = []

                to_save = []
                for bus in buses:
                    current = True
                    for link in dictionary['nodes'][bus]['links_up']:
                        if dictionary['nodes'][bus]['links_up'][link] == 'Line' and \
                                dictionary['links'][link]['bus_H'] not in done:
                            current = False

                    if current:
                        to_save.append(bus)

                for bus in to_save:
                    levels[l_num].append(bus)
                    done.append(bus)
                    buses.remove(bus)


        else:
            for bus in level_cat[typology][level]:

            # for link in level_cat[typology][level][bus]['links_up']:
            #     if link == ['Line']:


                levels[l_num].append(bus)

print(levels)

dependencies = dict()

for j in reversed(list(levels.keys())):
    for bus in levels[j]:
        if bus == 'EV-Fast_BB':
            print('stop')
        dependencies[bus] = dict()
        dependencies[bus]['up'] = dict()
        dependencies[bus]['down'] = dict()
        links_up = list(dictionary['nodes'][bus]['links_up'])
        while links_up:
            for link in links_up:
                bus_dep = dictionary['links'][link]['bus_H']
                lev = 0
                for i in levels:
                    if bus_dep in levels[i]:
                        lev = i
                        break
                try:
                    if bus_dep not in dependencies[bus]['up'][lev]:
                        dependencies[bus]['up'][lev].append(bus_dep)
                except:
                    dependencies[bus]['up'][lev] = [bus_dep]

                links_up.remove(link)
                links_up = links_up + list(dictionary['nodes'][bus_dep]['links_up'])
        print('end')

        links_down = list(dictionary['nodes'][bus]['links_down'])
        while links_down:
            for link in links_down:
                bus_dep = dictionary['links'][link]['bus_L']
                lev = 0
                for i in levels:
                    if bus_dep in levels[i]:
                        lev = i
                        break
                try:
                    if bus_dep not in dependencies[bus]['down'][lev]:
                        dependencies[bus]['down'][lev].append(bus_dep)
                except:
                    dependencies[bus]['down'][lev] = [bus_dep]

                links_down.remove(link)
                print(bus_dep)
                links_down = links_down + list(dictionary['nodes'][bus_dep]['links_down'])
                print('done')
print('end')
#
# while walk_dict:
#     dicts = new_dicts
#     new_dicts = []
#     for d in dicts:
#         if d['links_out']:
#             for bus in d['links_out']:
#                 all_buses[bus] = d['links_out'][bus]
#                 new_dicts.append(d['links_out'][bus])
#                 print(bus)
#                 level = d['links_out'][bus]['level']
#                 typology = d['links_out'][bus]['type']
#                 if level not in list(level_cat[typology].keys()):
#                     level_cat[typology][level] = []
#                 level_cat[typology][level].append(bus)
#     if not new_dicts:
#         walk_dict = False
#
# for typology in ['AC', 'DC']:
#     for level in level_cat[typology]:
#         for bus in level_cat[typology][level]:
#             for bus2 in all_buses[bus]['links_out']:
#                 for link in all_buses[bus2]:
#
#                     pass
#
#
# jumps = 0
# jumped = []
# for bus in all_buses:
#     if all_buses[bus]['links_out']:
#         for bus_out in all_buses[bus]['links_out']:
#             if all_buses[bus_out]['level'] == all_buses[bus]['level'] and \
#                     all_buses[bus_out]['type'] == all_buses[bus]['type']:
#                 jumps += 1
#                 jumped.append(jumped)
#                 break
#
# print('end')
#
# print(level_cat['AC'].keys())
# print(sorted(level_cat['DC'].keys(), reverse=True))
#
# levels_order = []
# for typology in ['AC', 'DC']:
#     for level in sorted(level_cat[typology].keys(), reverse=True):
#         levels_order.append((typology, level))
# print(levels_order)
# a = copy.deepcopy(levels_order)
# a.reverse()
# print(levels_order)
# print(a)

size_h = 2 * len(levels) + 1
print(size_h)

frame = np.zeros((size_h, 300))
# frame[5][4] = 15

print(frame)

elem_nums = elem_nums + list(dictionary['nodes'].keys())
r = size_h
# order = list(levels.keys())
# order.reverse()

bus_drawn = []
all_buses = list(dictionary['nodes'])

for bus in dependencies:

    # Definizione della lista dei bus da cui "BUS" dipende
    buses = [bus]
    for i in dependencies[bus]['up']:
        buses += dependencies[bus]['up'][i]

    while buses:
        b = buses[0]
        # if b == 'EV-Fast_BB':
        #     print('stop')

        # Ricerca del livello di appartenenza del bus "b"
        lev = 0
        for i in levels:
            if b in levels[i]:
                lev = i
                break
        line = 2 * lev - 1  # Posizionamento del bus "b" sulla griglia

        # Ricerca dell'ultima posizione occupata nella griglia nella linea "line"
        x0 = 0
        for i in range(0, np.size(frame, axis=0)):
            if frame[line, i] != 0:
                x0 = i
        if x0 != 0:
            x0 += 2

        # La lunghezza minima della busbar è data dal numero di collegamenti inferiori + gli elementi
        # o superiori + laterali
        length = max(len(list(dictionary['nodes'][b]['links_up'].keys())) +
                len(list(dictionary['nodes'][b]['links_side'].keys())),
                len(list(dictionary['nodes'][b]['links_down'].keys())) +
                len(list(dictionary['nodes'][b]['elements'].keys()))) + 1

        # si determina l'occupazione nella griglia delle busbar dipendendi dalla busbar in oggetto
        x1 = 0
        for i in dependencies[b]['down']:
            for bus_down in dependencies[b]['down'][i]:
                if bus_down in list(map_draw['bus'].keys()):
                    x = map_draw['bus'][bus_down]['l'] + map_draw['bus'][bus_down]['c']
                    x1 = max(x, x1)

        # La lunghezza della busbar deve adeguarsi all'occupazione e posizione delle busbar dipendenti
        length = max(length, x1)

        # Ricerca della posizione libera nella linea di appartenenza e in quelle inferiori
        x2 = 0
        if x1 == 0:
            for j in range(line + 1, size_h):
                for i in range(0, np.size(frame, axis=0)):
                    if frame[j, i] != 0:
                        x2 = max(x2, i)
            if x2 != 0:
                x2 += 2
        col = max(x2, x0)

        # Se però l'elemento già è stato mappato, si utlilizza il suo punto di partenza
        if b in list(map_draw['bus'].keys()):
            col = map_draw['bus'][b]['c']
        else:   # Altrimenti si crea la voce nel dizionario
            map_draw['bus'][b] = dict()

        map_draw['bus'][b]['l'] = length
        map_draw['bus'][b]['c'] = col
        map_draw['bus'][b]['r'] = line
        e = elem_nums.index(b)
        for i in range(col, col + length):
            frame[line, i] = e
        bus_drawn.append(b)
        buses.remove(b)

        # Aggiunta per considerare i links laterali e inferiori
        for link in dictionary['nodes'][b]['links_down']:
            buses = [dictionary['links'][link]['bus_L']] + buses
        print(str(e) + ': ' + b + ' done')
        pass

print('done')

# for j in reversed(list(levels.keys())):
#     print('Level = ' + str(j), levels[j])
#     c = 0
#     r -= 2
#     for bus in levels[j]:
#         map_draw['bus'][bus] = dict()
#         l = max(len(list(dictionary['nodes'][bus]['links_up'].keys())) +
#                 len(list(dictionary['nodes'][bus]['links_side'].keys())),
#                 len(list(dictionary['nodes'][bus]['links_down'].keys())),
#                 len(list(dictionary['nodes'][bus]['elements'].keys()))) + 1
#         map_draw['bus'][bus]['l'] = l
#         map_draw['bus'][bus]['c'] = c
#         map_draw['bus'][bus]['r'] = r
#         e = elem_nums.index(bus)
#         for i in range(c, c+l):
#             frame[r, i] = e
#         bus_drawn = []
#         c = c + l + 1
#         # print(frame)
#     print('end line')
#
# print('next')
# # for b in sorted(levels['DC'].keys(), reverse=True):
# #     if b not in jumped:
