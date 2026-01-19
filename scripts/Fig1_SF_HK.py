from FlatTreeMod import *

custom_lines = []
labels = []

def plot_EnuReco_bias(ax, filename: str, label: str, color: str):

    infile = up.open(filename)
    Enu_t = 1000*infile["FlatTree_VARS;1"]["Enu_true"].array()
    Enu_QE = 1000*infile["FlatTree_VARS;1"]["Enu_QE"].array()

    diff = []


    for index, val in enumerate(Enu_t):
        diff.append((Enu_t[index] - Enu_QE[index]))
    diff = np.array(diff)

    ax.hist(diff, bins=np.arange(-1000, 1000, step=10), histtype='step', weights=np.ones_like(diff), color=color,linewidth=1.5, label = label)
    # Create a matching line handle for legend
    custom_lines.append(Line2D([0], [0], color=color, lw=2))
    labels.append(label)


    return


fig, ax = plt.subplots()
plot_EnuReco_bias(ax, "../flattrees/nuwro/NuWro_HK_test.flat.root", r"NuWro SF", dark_blue)

plt.legend(custom_lines, labels)
plt.title("HK unoscillated Enu reco for all channels")
plt.xlabel(r"$E_{\nu}^{\text{true}} - E_{\nu}^{\text{QE}}$ [MeV]")
plt.ylabel("Number of events")
plt.show()



