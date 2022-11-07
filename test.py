import pypsa
import numpy as np
import pandas as pd

network = pypsa.Network()

network.add("Bus", "MV bus", v_nom=20,
            # v_mag_pu_set=1.02
            )
network.add("Bus", "LV1 bus", v_nom=0.4)
network.add("Bus", "LV2 bus", v_nom=0.4)

network.add(
    "Transformer",
    "MV-LV trafo",
    # type="0.4 MVA 20/0.4 kV",
    bus0="MV bus",
    bus1="LV1 bus",
    x=0.0000000001,
    r=0.000000001,
    model='t',
    s_nom=10,
)
network.add(
    "Line", "LV cable", type="NAYY 4x50 SE", bus0="LV1 bus", bus1="LV2 bus", length=0.1
)
network.add("Generator", "External Grid", bus="MV bus", control="Slack")
network.add("Load", "LV load", bus="LV2 bus", p_set=0.1, q_set=0.05)

# print(network.pf())
#



def run_pf():
    network.lpf()
    network.pf(use_seed=True)
    return pd.DataFrame(
        {
            "Voltage Angles": network.buses_t.v_ang.loc["now"] * 180.0 / np.pi,
            "Volate Magnitude": network.buses_t.v_mag_pu.loc["now"],
        }
    )

run_pf()
print(network.buses_t.v_ang * 180 / np.pi)
print(network.buses_t.p)
print(network.buses_t.v_mag_pu)

print('\n\nP Generatore = ' + str(network.generators_t['p']['External Grid']['now']))