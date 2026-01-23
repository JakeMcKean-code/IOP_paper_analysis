from FlatTreeMod import *

custom_lines = []
labels = []

def plot_EnuReco_bias_dune(ax, filename: str, label: str, color: str):

    infile = up.open(filename)
    Enu_t  = 1000*infile["FlatTree_VARS;1"]["Enu_true"].array()
    mode   = infile["FlatTree_VARS;1"]["cc"].array()

    # ----------------------------------------
    # Compute oscillation weights PER EVENT
    # (convert MeV -> GeV for OscProb)
    # ----------------------------------------
    weights = np.array([pmns.Prob(1, 1, E/1000.0, L) for E in Enu_t])  # νμ → νμ survival



    ax.hist(diff_sel, bins=np.arange(-1000, 1000, step=10), histtype='step', weights=np.ones_like(diff_sel), color=color,linewidth=1.5, label = label)
    # Create a matching line handle for legend
    custom_lines.append(Line2D([0], [0], color=color, lw=2, linestyle='-'))
    labels.append(label)

    color = vivid_purple
    ax.hist(diff_sel, bins=np.arange(-1000, 1000, step=10), histtype='step', weights=weights, color=color,linewidth=1.5, label = label, linestyle = '--')
    # Create a matching line handle for legend
    custom_lines.append(Line2D([0], [0], color=color, lw=2, linestyle='--'))
    labels.append(label+" osc")


    return


fig, ax = plt.subplots()
plot_EnuReco_bias(ax, "../flattrees/nuwro/NuWro_Ar40_test.flat.root", r"NuWro SF Argon", dark_blue)

plt.legend(custom_lines, labels)
plt.title("DUNE Enu reco for all channels")
plt.xlabel(r"$E_{\nu}^{\text{true}} - E_{\nu}^{\text{QE}}$ [MeV]")
plt.ylabel("Number of events")
plt.show()



