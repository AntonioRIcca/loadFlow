import yaml
from PIL import Image, ImageDraw, ImageFont
import os
import copy

path = os.getcwd()
print(path)

# dictionary = dict()
filename = 'network.yml'
print(os.path.join(path, filename))
dictionary = yaml.safe_load(open(os.path.join(path, filename)))
print('ok')

walk_dict = True
d = copy.deepcopy(dictionary['External Grid']['node']['City_BB'])       # da correggere
new_dicts = [d]
nodes = list(d.keys())
allnodes = nodes
print(nodes)

while walk_dict:
    dicts = new_dicts
    new_dicts = []
    for d in dicts:
        if d['links_out']:
            for bus in d['links_out']:
                new_dicts.append(d['links_out'][bus])
                print(bus)
                if bus == 'UG_Serv_BB':
                    print('end')
    if not new_dicts:
        walk_dict = False

