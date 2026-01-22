from FlatTreeMod import *

custom_lines = []
labels = []

def plot_EnuReco_osc(ax, filename: str, label: str, color: str):

    infile = up.open(filename)
    Enu_t  = 1000*infile["FlatTree_VARS;1"]["Enu_true"].array()
    Enu_QE = 1000*infile["FlatTree_VARS;1"]["Enu_QE"].array()
    # mode   = infile["FlatTree_VARS;1"]["cc"].array()
    mode   = infile["FlatTree_VARS;1"]["Mode"].array()

    # Select only events with mode == 1
    mask = (mode == 1)
    Enu_t_sel = Enu_t[mask]
    Enu_QE_sel = Enu_QE[mask]

    # ----------------------------------------
    # Compute oscillation weights PER EVENT
    # (convert MeV -> GeV for OscProb)
    # ----------------------------------------
    weights = np.array([pmns.Prob(1, 1, E/1000.0, L) for E in Enu_t_sel])  # νμ → νμ survival



    ax.hist(Enu_QE_sel, bins=np.arange(0, 2000, step=10), histtype='step', weights=np.ones_like(Enu_QE_sel), color=color,linewidth=1.5, label = label)
    # Create a matching line handle for legend
    custom_lines.append(Line2D([0], [0], color=color, lw=2, linestyle='-'))
    labels.append(label)

    color = vivid_purple
    ax.hist(Enu_QE_sel, bins=np.arange(0, 2000, step=10), histtype='step', weights=weights, color=color,linewidth=1.5, label = label, linestyle = '--')
    # Create a matching line handle for legend
    custom_lines.append(Line2D([0], [0], color=color, lw=2, linestyle='--'))
    labels.append(label+" osc")


    return


fig, ax = plt.subplots()
plot_EnuReco_osc(ax, "../flattrees/nuwro/NuWro_HK_test.flat.root", r"NuWro SF", dark_blue)

plt.legend(custom_lines, labels)
plt.title("HK oscillated Enu reco for all channels")
plt.xlabel(r"$E_{\nu}^{\text{true}}$ [MeV]")
plt.ylabel("Number of events")
plt.show()



