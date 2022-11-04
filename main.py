import pypsa
import numpy as np

network = pypsa.Network()

n_buses = 3

for i in range(n_buses):
    network.add('Bus', 'My bus {}'.format(i), v_nom=20.0)
print('\nBusBar e Nodi')
print(network.buses)


for i in range(n_buses):
    network.add(
        'Line',
        'My line {}'.format(i),
        bus0='My bus {}'.format(i),
        bus1='My bus {}'.format((i+1) % n_buses),
        x=0.1,
        r=0.01,
        length=1
    )
print('\nLinee')
print(network.lines)

network.add('Generator', 'My gen', bus='My bus 0', p_set=100, control='PQ')
print('\nGeneratori')
print(network.generators)

network.add('Load', 'My load', bus='My bus 1', p_set=100)
print('\nCarichi')
print(network.loads)

network.loads.q_set = 100

print('\n\n----------- LOADFLOW ------------')
print(network.pf())

print('\n\nP Generatore = ' + str(network.generators_t['p']['My gen']['now']))
print('P Carico = ' + str(network.loads_t['p']['My load']['now']))
for i in range (0, 3):
    print('P0 My line ' + str(i) + ' = ' + str(network.lines_t['p0']['My line ' + str(i)]['now']))

# print(network.lines_t.p0)
#
# print(network.buses_t.v_ang * 180 / np.pi)
#
print(network.buses_t.v_mag_pu)
#
# print('valore = ' + str(network.buses_t['p']['My bus 1']['now']))
#
# print(network.loads['p_set']['My load'])
#
# print(network.components.Load.keys())
# print(network.loads['p_set']['My load'])
#
# # network.loads_t['p_set']['My load']['now'] = 10

