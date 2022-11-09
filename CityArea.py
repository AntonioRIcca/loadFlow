import pypsa
import numpy as np


elements = dict()
categories = ['AC-Bus', 'DC-Bus', 'PV', 'AC-Load', 'DC-Load', 'ExtGrid', 'BESS', 'Transformer', 'AC-Line', 'DC-Line']
for cat in categories:
    elements[cat] = dict()

conv = dict()
conv['AC-Bus'] = 'buses'
conv['DC-Bus'] = 'buses'
conv['PV'] = 'generators'
conv['AC-Load'] = 'loads'
conv['DC-Load'] = 'loads'
conv['ExtGrid'] = 'generators'
conv['BESS'] = 'stores'
conv['Transformer'] = 'transformers'
conv['AC-Line'] = 'lines'
conv['DC-Line'] = 'lines'


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
                type=bbtype + ' Busbar',
                carrier=bbtype
            )

            if bbtype == 'AC':
                elements['AC-Bus'][name] = dict()
            else:
                elements['DC-Bus'][name] = dict()
print('\nBusBar e Nodi')
print(network.buses)

network.add("Generator", "External Grid", bus="City_BB", control="Slack")
elements['ExtGrid']['External Grid'] = dict()
network.add('Generator', 'UGS_PV1', bus='UGS_PV_BB', control='PQ', p_set=0.015, q_set=0)
elements['PV']['UGS_PV1'] = dict()
network.add('Generator', 'UGS_PV2', bus='UGS_PV_BB', control='PQ', p_set=0.015, q_set=0)
elements['PV']['UGS_PV2'] = dict()

network.add(
    'Line',
    'UG_Line',
    bus0='City_BB',
    bus1='UG_BB_20kV',
    length=3,
    x=0.09,
    r=0.09
)
elements['AC-Line']['UG_Line'] = dict()

network.add('Transformer', 'UG_TR1', bus0='UG_BB_20kV', bus1='UG_BB_2kV', s_nom=2, x=0.05916, r=0.01)
network.add('Transformer', 'UG_TR2', bus0='UG_BB_20kV', bus1='UG_BB_2kV', s_nom=2, x=0.05916, r=0.01)
network.add('Transformer', 'UG_Serv_TR', bus0='UG_BB_2kV', bus1='UG_Serv_BB', s_nom=0.4, x=0.05916, r=0.01)
network.add('Transformer', 'UG_PWM', bus0='UG_BB_2kV', bus1='UG_BB_LVDC', s_nom=0.8, x=1e-12, r=1e-12)
network.add('Transformer', 'UGS_PWM', bus0='UG_BB_2kV', bus1='UGS_BB', s_nom=0.8, x=1e-12, r=1e-12)
network.add('Transformer', 'UGS_PV_DC-DC-Conv', bus0='UGS_BB', bus1='UGS_PV_BB', s_nom=0.05, x=1e-12, r=1e-12)
network.add('Transformer', 'UGS_BESS_DC-DC-Conv', bus0='UGS_BB', bus1='UGS_BESS_Node', s_nom=0.05, x=1e-12, r=1e-12)
for e in ['UG_TR1', 'UG_TR2', 'UG_Serv_TR', 'UG_PWM', 'UGS_PWM', 'UGS_PV_DC-DC-Conv', 'UGS_BESS_DC-DC-Conv']:
    elements['Transformer'][e] = dict()

network.add('Load', 'UG_Serv_AC-Load1', bus='UG_Serv_BB', p_set=0.08, q_set=0.03875)
elements['AC-Load']['UG_Serv_AC-Load1'] = dict()
network.add('Load', 'UG_Serv_AC-Load2', bus='UG_Serv_BB', p_set=0.12, q_set=0.05812)
elements['AC-Load']['UG_Serv_AC-Load2'] = dict()
network.add('Load', 'UG_Load', bus='UG_BB_LVDC', p_set=0.4, q_set=0)
elements['DC-Load']['UG_Load'] = dict()
network.add('Load', 'UGS_Load', bus='UGS_BB', p_set=0.4, q_set=0)
elements['DC-Load']['UGS_Load'] = dict()

network.add('Store', 'UGS_BESS', bus='UGS_BESS_Node', p_set=0.010, q_set=0, sign=-1)
elements['BESS']['UGS_BESS'] = dict()

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


print('\n\n\n')
for cat in categories:
    if cat in ['PV', 'AC-Load', 'DC-Load', 'ExtGrid', 'BESS']:
        for e in elements[cat].keys():
            bus = network.__getattribute__(conv[cat])['bus'][e]
            p = network.__getattribute__(conv[cat] + '_t')['p'][e]['now']
            q = network.__getattribute__(conv[cat] + '_t')['q'][e]['now']
            s = (p**2 + q**2)**0.5
            v = network.__getattribute__('buses_t')['v_mag_pu'][bus]['now'] *\
                network.__getattribute__('buses')['v_nom'][bus]
            if cat in ['AC-Load', 'ExtGrid']:
                i = s / v / (3**0.5)
            else:
                i = s / v
            print(e + ':\tP = %.4f MW\tQ = %.4f MVA\tV = %.3f kV\ti = %.4f kA' % (p, q, v, i))

    if cat in ['Transformer', 'AC-Line', 'DC-Line']:
        for e in elements[cat].keys():
            bus0 = network.__getattribute__(conv[cat])['bus0'][e]
            p0 = network.__getattribute__(conv[cat] + '_t')['p0'][e]['now']
            q0 = network.__getattribute__(conv[cat] + '_t')['q0'][e]['now']
            s0 = (p0**2 + q0**2)**0.5
            v0 = network.__getattribute__('buses_t')['v_mag_pu'][bus0]['now'] *\
                network.__getattribute__('buses')['v_nom'][bus0]
            if cat in ['AC-Load', 'ExtGrid']:
                i0 = s0 / v0 / (3**0.5)
            else:
                i0 = s0 / v0

            bus1 = network.__getattribute__(conv[cat])['bus1'][e]
            p1 = network.__getattribute__(conv[cat] + '_t')['p1'][e]['now']
            q1 = network.__getattribute__(conv[cat] + '_t')['q1'][e]['now']
            s1 = (p1**2 + q1**2)**0.5
            v1 = network.__getattribute__('buses_t')['v_mag_pu'][bus1]['now'] *\
                network.__getattribute__('buses')['v_nom'][bus1]
            if cat in ['AC-Load', 'ExtGrid']:
                i1 = s1 / v1 / (3**0.5)
            else:
                i1 = s1 / v1

            print(e + ':\tP0 = %.4f MW\tP1 = %.4f MW\tQ0 = %.4f MVA\tQ1 = %.4f MVA\tV0 = %.3f kV\tV1 = %.3f kV'
                      '\ti0 = %.4f kA\ti1 = %.4f kA' % (p0, p1, q0, q1, v0, v1, i0, i1))
