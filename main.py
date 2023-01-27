import pypsa
import numpy as np

network = pypsa.Network()

n_buses = 3

for i in range(n_buses):
    network.add('Bus', 'My bus {}'.format(i), v_nom=20.0)

# Inserimento BUS DC
network.add('Bus', 'DC-bus', v_nom=6)

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
print(network.lines)

# Inserimento PWM
# network.add('Line', 'PWM', bus0='My bus 2', bus1='DC-bus', x=0.00000, r=0.0000000000000, length=10)
# network.add('Link', 'PWM', bus0='My bus 2', bus1='DC-bus', p_nom=1000, efficiency=1, marginal_cos=0, p_min_pu=-1)
network.add('TransformerType', 'Tr2', v_nom_0=20, v_nom_1=6.0622, s_nom=300, f_nom=50, vsc=1e-12)
network.add('Transformer', 'PWM', bus0='My bus 2', bus1='DC-bus', x=0.01, r=0.01, model='t', type='Tr2')

print('\nLinee')
print(network.links)

network.add('Generator', 'My gen', bus='My bus 0', p_set=100, control='PQ')
print('\nGeneratori')
print(network.generators)

network.add('Load', 'My load', bus='My bus 1', p_set=100, q_set=100)
network.add('Load', 'DC-load', bus='DC-bus', p_set=50, q_set=0)
print('\nCarichi')
print(network.loads)

# network.loads.q_set = 100

print('\n\n----------- LOADFLOW ------------')
print(network.pf())

print('\n\nP Generatore = ' + str(network.generators_t['p']['My gen']['now']))
print('P Carico = ' + str(network.loads_t['p']['My load']['now']))
print('DC-bus: P = ' + str(network.buses_t['p']['DC-bus']['now']) + '\tQ = ' + str(network.buses_t['q']['DC-bus']['now']))
print('DC-bus: V (p.u.): ' + str(network.buses_t['v_mag_pu']['DC-bus']['now']))

print('\n')
for i in range (0, 3):
    print('P0 My line ' + str(i) + ' = ' + str(network.lines_t['p0']['My line ' + str(i)]['now']))

# print(network.lines_t.p0)
#
# print(network.buses_t.v_ang * 180 / np.pi)
#
print(network.buses_t.v_mag_pu)
print('END')
#
# print('valore = ' + str(network.buses_t['p']['My bus 1']['now']))
#
# print(network.loads['p_set']['My load'])
#
# print(network.components.Load.keys())
# print(network.loads['p_set']['My load'])
#
# # network.loads_t['p_set']['My load']['now'] = 10
