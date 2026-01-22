from FlatTreeMod import *

# ----------------------------------------
# Functions to plot Enu_reco bias
# input:
# - plt axis
# - flat tree filename
# - legend label
# - legend colour (see FlatTreeMod for defined colourblind-friendly palette
# output: Plot of Enu_reco bias
# ----------------------------------------

def plot_EnuReco_bias(ax, filename: str, label: str, color: str):

    infile = up.open(filename)
    Enu_t = 1000*infile["FlatTree_VARS;1"]["Enu_true"].array()
    Enu_QE = 1000*infile["FlatTree_VARS;1"]["Enu_QE"].array()
    diff = Enu_t - Enu_QE

    # ----------------------------------------
    # Compute oscillation weights PER EVENT
    # (convert MeV -> GeV for OscProb)
    # ----------------------------------------
    weights = np.array([pmns.Prob(1, 1, E/1000.0, L) for E in Enu_t])  # νμ → νμ survival



    ax.hist(diff, bins=np.arange(-1000, 1000, step=10), histtype='step', weights=np.ones_like(diff), color=color,linewidth=1.5, label = label)
    # Create a matching line handle for legend
    custom_lines.append(Line2D([0], [0], color=color, lw=2, linestyle='-'))
    labels.append(label)

    ax.hist(diff, bins=np.arange(-1000, 1000, step=10), histtype='step', weights=weights, color=color,linewidth=1.5, label = label + " osc", linestyle = '--')
    # Create a matching line handle for legend
    custom_lines.append(Line2D([0], [0], color=color, lw=2, linestyle='--'))
    labels.append(label + " osc")


    return


fig, ax = plt.subplots()
plot_EnuReco_bias(ax, "../flattrees/EDRMF_HK_test.flat.root", r"ED-RMF", dark_blue)
plot_EnuReco_bias(ax, "../flattrees/RPWIA_HK_test.flat.root", r"RPWIA", dark_red)

plt.legend(custom_lines, labels)
plt.title("HK unoscillated Enu reco for CCQE channel")
plt.xlabel(r"$E_{\nu}^{\text{true}} - E_{\nu}^{\text{QE}}$ [MeV]")
plt.ylabel("Number of events")
# plt.savefig("Fig7-test.pdf")
plt.show()



