import pypsa
import numpy as np
#
#
# network = pypsa.Network()
#
# network.add('Bus', 'AC_Bus', v_nom=20)
# network.add('Bus', 'DC_Bus', v_nom=2)
#
# network.add('Generator', 'ExtGrid', bus='AC_Bus', control='Slack')
#
# network.add('Load', 'DC_Load', bus='DC_Bus', p_set=0.1, q_set=0)
#
# # network.add('Line', 'PWM', bus0='AC_Bus', bus1='DC_Bus', x=1e-12, r=1e-12)
#
# network.add('Link', 'PWM', bus0='AC_Bus', bus1='DC_Bus', efficiency=1)
#
# print(network.pf())
#
# print(network.buses_t.v_mag_pu)


# override_component_attrs = pypsa.descriptors.Dict(
#     {k: v.copy() for k, v in pypsa.components.component_attrs.items()}
# )
# override_component_attrs["Link"].loc["bus2"] = [
#     "string",
#     np.nan,
#     np.nan,
#     "2nd bus",
#     "Input (optional)",
# ]
# override_component_attrs["Link"].loc["efficiency2"] = [
#     "static or series",
#     "per unit",
#     1.0,
#     "2nd bus efficiency",
#     "Input (optional)",
# ]
# override_component_attrs["Link"].loc["p2"] = [
#     "series",
#     "MW",
#     0.0,
#     "2nd bus output",
#     "Output",
# ]


# network = pypsa.Network(override_component_attrs=override_component_attrs)
network = pypsa.Network()

network.add('Bus', 'AC_Bus', carrier='AC', v_nom=20)
network.add('Bus', 'DC_Bus', carrier='DC', v_nom=2)

network.add('Generator', 'ExtGrid', bus='AC_Bus', control='PV')

network.add('Load', 'DC_Load', bus='DC_Bus', p_set=0.1, q_set=0)

# network.add('Line', 'PWM', bus0='AC_Bus', bus1='DC_Bus', x=1e-12, r=1e-12)

network.add('Link', 'PWM', bus0='AC_Bus', bus1='DC_Bus', efficiency=1,
            marginal_cost=0, p_min_pu=-1, p_nom=1000, p_set=100)

# print(network.pf())
#
# print(network.buses_t.v_mag_pu)

#
#
#
# network.add("Bus", "Frankfurt", carrier="AC")
# network.add("Load", "Frankfurt", bus="Frankfurt", p_set=5)
#
#
# # network.add("Bus", "Frankfurt heat", carrier="heat")
# # network.add("Load", "Frankfurt heat", bus="Frankfurt heat", p_set=3)
#
#
# network.add("Bus", "Frankfurt gas", carrier="gas")
# network.add("Store", "Frankfurt gas", e_initial=1e6, e_nom=1e6, bus="Frankfurt gas")
#
# network.add(
#     "Link",
#     "OCGT",
#     bus0="Frankfurt gas",
#     bus1="Frankfurt",
#     p_nom_extendable=True,
#     capital_cost=600,
#     efficiency=0.4,
# )
#
#
# network.add(
#     "Link",
#     "CHP",
#     bus0="Frankfurt gas",
#     bus1="Frankfurt",
#     bus2="Frankfurt heat",
#     p_nom_extendable=True,
#     capital_cost=1400,
#     efficiency=0.3,
#     efficiency2=0.3,
# )

network.lpf()

print(network.buses_t.v_mag_pu)

print(network.buses_t.p)

print(network.loads_t.p)

print(network.generators_t.p)

# print(network.links_t.p0)
