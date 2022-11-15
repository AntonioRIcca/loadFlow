import pypsa
import numpy as np
import pandas as pd


network = pypsa.Network()

network.add("Bus", "20kV_BB", v_nom=20)
network.add("Bus", "2kV_BB", v_nom=2)

network.add('TransformerType', 'myTr2',
            f_nom=50,
            s_nom=0.5,
            v_nom_0=20,
            v_nom_1=2,
            vsc=1,
            # vscr=1.2,
            # pfe=0.6,
            i0=0.24,
            # phase_shift=150,
            # tap_side=0,
            # tap_neutral=0,
            # tap_min=-2,
            # tap_max=2,
            # tap_step=2.5,
            )

network.add(
    "Transformer",
    "Tr",
    # type="0.4 MVA 20/0.4 kV",
    type='myTr2',
    bus0="20kV_BB",
    bus1="2kV_BB",
    # x=0.05916,
    # r=0.01,
    # model='t',
    # s_nom=0.5,
)

network.add(
    "Transformer",
    "Tr2",
    # type="0.4 MVA 20/0.4 kV",
    # type='myTr2',
    bus0="20kV_BB",
    bus1="2kV_BB",
    x=0.05916,
    r=0.01,
    model='t',
    s_nom=0.5,
)
#
# network.add(
#     'Link',
#     'mylink',
#     bus0='MV bus',
#     bus1='LV1 bus',
#     p_nom_extendable=False,
#     capital_cost=1400,
#     efficiency=0.3,
# )

network.add('Generator', 'ExternalGrid', bus='20kV_BB', control='Slack')
network.add("Load", "LV load", bus="2kV_BB", p_set=0.1, q_set=0.05)

# print(network.pf())
#

network.pf()

print(network.buses_t.v_ang * 180 / np.pi)
print(network.buses_t.p)
print(network.buses_t.v_mag_pu)

print('\n\nP Generatore = ' + str(network.generators_t['p']['ExternalGrid']['now']) +
      '\nQ Generatore = ' + str(network.generators_t['q']['ExternalGrid']['now']))

p0 = network.transformers_t['p0']['Tr']['now']
p1 = network.transformers_t['p1']['Tr']['now']
q0 = network.transformers_t['q0']['Tr']['now']
q1 = network.transformers_t['q1']['Tr']['now']
s0 = (p0**2 + q0**2)**0.5
s1 = (p1**2 + q1**2)**0.5
bus0 = network.transformers['bus0']['Tr']
bus1 = network.transformers['bus1']['Tr']
v0 = network.buses_t['v_mag_pu'][bus0]['now'] * network.buses['v_nom'][bus0]
v1 = network.buses_t['v_mag_pu'][bus1]['now'] * network.buses['v_nom'][bus1]
i0 = s0 / v0 / (3**0.5)
i1 = s1 / v1 / (3**0.5)
print('Trasformatore 1' + ':\tP0 = %.2f MW\tP1 = %.2f MW\tQ0 = %.2f MVA\tQ1 = %.2f MVA\tV0 = %.3f kV\tV1 = %.3f kV'
      '\ti0 = %.3f kA\ti1 = %.3f kA' % (p0*1000, p1*1000, q0*1000, q1*1000, v0, v1, i0*1000, i1*1000))

p0 = network.transformers_t['p0']['Tr2']['now']
p1 = network.transformers_t['p1']['Tr2']['now']
q0 = network.transformers_t['q0']['Tr2']['now']
q1 = network.transformers_t['q1']['Tr2']['now']
s0 = (p0**2 + q0**2)**0.5
s1 = (p1**2 + q1**2)**0.5
bus0 = network.transformers['bus0']['Tr2']
bus1 = network.transformers['bus1']['Tr2']
v0 = network.buses_t['v_mag_pu'][bus0]['now'] * network.buses['v_nom'][bus0]
v1 = network.buses_t['v_mag_pu'][bus1]['now'] * network.buses['v_nom'][bus1]
i0 = s0 / v0 / (3**0.5)
i1 = s1 / v1 / (3**0.5)
print('Trasformatore 2' + ':\tP0 = %.2f MW\tP1 = %.2f MW\tQ0 = %.2f MVA\tQ1 = %.2f MVA\tV0 = %.3f kV\tV1 = %.3f kV'
      '\ti0 = %.3f kA\ti1 = %.3f kA' % (p0*1000, p1*1000, q0*1000, q1*1000, v0, v1, i0*1000, i1*1000))

p = network.loads_t['p']['LV load']['now']
q = network.loads_t['q']['LV load']['now']
s = (p**2 + q**2)**0.5
bus = network.loads['bus']['LV load']
v = network.buses_t['v_mag_pu'][bus]['now'] * network.buses['v_nom'][bus]
i = s / v / (3**0.5)

print('LV load' + ':\tP = %.2f kW\tQ = %.2f kVA\tV = %.3f kV\ti = %.3f A' % (p * 1000, q * 1000, v, i * 1000))
