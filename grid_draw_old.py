import yaml
# from PIL import Image, ImageDraw, ImageFont
import os
import copy
import numpy as np

path = os.getcwd()
print(path)

# dictionary = dict()
filename = 'network_old.yml'
print(os.path.join(path, filename))
dictionary = yaml.safe_load(open(os.path.join(path, filename)))
print('ok')

walk_dict = True
levels = dict()
levels['AC'] = dict()
levels['AC'][20] = ['City_BB']
levels['DC'] = dict()
map_draw = dict()
map_draw['bus'] = dict()

links = dict()

d = copy.deepcopy(dictionary['External Grid']['node']['City_BB'])       # da correggere
new_dicts = [d]
nodes = list(d.keys())
all_nodes = nodes
all_buses = dict()
all_buses['City_BB'] = d
print(nodes)
elem_nums = []


while walk_dict:
    dicts = new_dicts
    new_dicts = []
    for d in dicts:
        if d['links_out']:
            for bus in d['links_out']:
                all_buses[bus] = d['links_out'][bus]
                new_dicts.append(d['links_out'][bus])
                print(bus)
                level = d['links_out'][bus]['level']
                typology = d['links_out'][bus]['type']
                if level not in list(levels[typology].keys()):
                    levels[typology][level] = []
                levels[typology][level].append(bus)
    if not new_dicts:
        walk_dict = False

for typology in ['AC', 'DC']:
    for level in levels[typology]:
        for bus in levels[typology][level]:
            for bus2 in all_buses[bus]['links_out']:
                for link in all_buses[bus2]:

                    pass


jumps = 0
jumped = []
for bus in all_buses:
    if all_buses[bus]['links_out']:
        for bus_out in all_buses[bus]['links_out']:
            if all_buses[bus_out]['level'] == all_buses[bus]['level'] and \
                    all_buses[bus_out]['type'] == all_buses[bus]['type']:
                jumps += 1
                jumped.append(jumped)
                break

print('end')

print(levels['AC'].keys())
print(sorted(levels['DC'].keys(), reverse=True))

levels_order = []
for typology in ['AC', 'DC']:
    for level in sorted(levels[typology].keys(), reverse=True):
        levels_order.append((typology, level))
print(levels_order)
a = copy.deepcopy(levels_order)
a.reverse()
print(levels_order)
print(a)

size_h = (len(list(levels['AC'].keys())) + len(list(levels['DC'].keys())) + jumps) * 2 + 1
print(size_h)

frame = np.zeros((size_h, 16))
frame[5][4] = 15

print(frame)

elem_nums = elem_nums + list(all_buses.keys())
r = size_h
order = copy.deepcopy(levels_order)
order.reverse()
for (typology, level) in order:
    c = 0
    r -= 2
    for bus in levels[typology][level]:
        map_draw['bus'][bus] = dict()
        l = max(len(list(all_buses[bus]['links_in'].keys())), len(list(all_buses[bus]['links_out'].keys()))) + 2
        map_draw['bus'][bus]['l'] = l
        map_draw['bus'][bus]['c'] = c
        map_draw['bus'][bus]['r'] = r
        e = elem_nums.index(bus)
        for i in range(c, c+l):
            frame[r, i] = e
        c = c + l + 1
        print(frame)

print('next')
# for b in sorted(levels['DC'].keys(), reverse=True):
#     if b not in jumped:
