import pypsa
import numpy as np


network = pypsa.Network()

busbar = {
    'AC': {
        20: ['City_BB', 'UG_BB_20kV'],
        2: ['UG_BB_2kV'],
        0.4: ['UG_Serv_BB']
    },
    'DC': {
        1.5: ['UG_BB_LVDC', 'UGS_BB'],
        0.75: ['UGS_PV_BB', 'UGS_BESS_Node']
    }
}

for bbtype in busbar:
    for level in busbar[bbtype]:
        for name in busbar[bbtype][level]:
            network.add(
                'Bus',
                name,
                v_nom=level,
                type=bbtype + ' Busbar'
            )
print('\nBusBar e Nodi')
print(network.buses)

network.add("Generator", "External Grid", bus="City_BB", control="Slack")
network.add('Generator', 'UGS_PV1', bus='UGS_PV_BB', control='PQ', p_set=0.015, q_set=0)
network.add('Generator', 'UGS_PV2', bus='UGS_PV_BB', control='PQ', p_set=0.015, q_set=0)

network.add(
    'Line',
    'UG_Line',
    bus0='City_BB',
    bus1='UG_BB_20kV',
    length=3,
    x=0.09,
    r=0.09
)

network.add('Transformer', 'UG_TR1', bus0='UG_BB_20kV', bus1='UG_BB_2kV', s_nom=2, x=0.05916, r=0.01)
network.add('Transformer', 'UG_TR2', bus0='UG_BB_20kV', bus1='UG_BB_2kV', s_nom=2, x=0.05916, r=0.01)
network.add('Transformer', 'UG_Serv_TR', bus0='UG_BB_2kV', bus1='UG_Serv_BB', s_nom=0.4, x=0.05916, r=0.01)
network.add('Transformer', 'UG_PWM', bus0='UG_BB_2kV', bus1='UG_BB_LVDC', s_nom=0.8, x=1e-12, r=1e-12)
network.add('Transformer', 'UGS_PWM', bus0='UG_BB_2kV', bus1='UGS_BB', s_nom=0.8, x=1e-12, r=1e-12)
network.add('Transformer', 'UGS_PV_DC-DC-Conv', bus0='UGS_BB', bus1='UGS_PV_BB', s_nom=0.05, x=1e-12, r=1e-12)
network.add('Transformer', 'UGS_BESS_DC-DC-Conv', bus0='UGS_BB', bus1='UGS_BESS_Node', s_nom=0.05, x=1e-12, r=1e-12)

network.add('Load', 'UG_Serv_AC-Load1', bus='UG_Serv_BB', p_set=0.08, q_set=0.03875)
network.add('Load', 'UG_Serv_AC-Load2', bus='UG_Serv_BB', p_set=0.12, q_set=0.05812)
network.add('Load', 'UG_Load', bus='UG_BB_LVDC', p_set=0.4, q_set=0)
network.add('Load', 'UGS_Load', bus='UGS_BB', p_set=0.4, q_set=0)

network.add('Store', 'UGS_BESS', bus='UGS_BESS_Node', p_set=0.010, q_set=0, sign=-1)

print(network.pf())

print(network.buses_t.v_mag_pu)

for load in ['UG_Serv_AC-Load1', 'UG_Serv_AC-Load2']:
    print( load + ': P = ' + str(network.loads_t['p'][load]['now']) +
           '\tQ = ' + str(network.loads_t['q'][load]['now']) + '\tBus = ' + network.loads['bus'][load])

print('Ext. Grid: P = ' + str(network.generators_t['p']['External Grid']['now']) +
      '\tQ = ' + str(network.generators_t['q']['External Grid']['now']))

print('UGS_PWM: P0 = ' + str(network.transformers_t['p0']['UGS_PWM']['now']) +
      '\tQ0 = ' + str(network.transformers_t['q0']['UGS_PWM']['now']) +
      '\tP1 = ' + str(network.transformers_t['p1']['UGS_PWM']['now']) +
      '\tQ1 = ' + str(network.transformers_t['q1']['UGS_PWM']['now']))
print('UGS_PV_DC-DC-Conv: P0 = ' + str(network.transformers_t['p0']['UGS_PV_DC-DC-Conv']['now']) +
      '\tQ0 = ' + str(network.transformers_t['q0']['UGS_PV_DC-DC-Conv']['now']) +
      '\tP1 = ' + str(network.transformers_t['p1']['UGS_PV_DC-DC-Conv']['now']) +
      '\tQ1 = ' + str(network.transformers_t['q1']['UGS_PV_DC-DC-Conv']['now']))
