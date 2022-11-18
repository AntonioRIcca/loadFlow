import yaml
# from PIL import Image, ImageDraw, ImageFont
import os
import copy
import numpy as np

path = os.getcwd()
print(path)

# dictionary = dict()
filename = 'network.yml'
print(os.path.join(path, filename))
dictionary = yaml.safe_load(open(os.path.join(path, filename)))
print('ok')

walk_dict = True
levels = dict()
levels['AC'] = dict()
levels['DC'] = dict()
d = copy.deepcopy(dictionary['External Grid']['node']['City_BB'])       # da correggere
new_dicts = [d]
nodes = list(d.keys())
all_nodes = nodes
all_buses = dict()
all_buses['City_BB'] = d
print(nodes)

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


for l in sorted(levels['DC'].keys(), reverse=True):

    print(l)



size_h = (len(list(levels['AC'].keys())) + len(list(levels['DC'].keys())) + jumps) * 2 + 1
print(size_h)

frame = np.zeros((size_h, 100))
# frame[5][4] = 'prova'

print(frame)

# for b in sorted(levels['DC'].keys(), reverse=True):
#     if b not in jumped:
