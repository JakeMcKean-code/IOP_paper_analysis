from FlatTreeMod import *
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

custom_lines = []
labels = []

def plot_osc_bias(ax, ax_ratio, axins, diff_sel, label, color, weights, nominal, counts_nom):
    ax.hist(diff_sel, bins=np.arange(150, 1200, step=50), histtype='step', weights=weights, color=color,linewidth=1.5, label = label, linestyle = '-')
    # Create a matching line handle for legend
    custom_lines.append(Line2D([0], [0], color=color, lw=2, linestyle='-'))
    labels.append(label)
    # axins.hist(diff_sel, bins=np.arange(0, 1200, step=50), histtype='step', weights=weights, color=color,linewidth=1.5, label = label, linestyle = '-')

    if(nominal == True):
        countsn, _ = np.histogram(diff_sel, weights=weights, bins=(np.arange(150, 1200, step=50)))
        ax_ratio.hlines(1, 150, 1200, linestyle='--', color = 'black')
        return countsn
    else:
        counts, edges = np.histogram(diff_sel, weights=weights, bins=(np.arange(150, 1200, step=50)))
        ratio = counts[1:]/counts_nom[1:]
        ax_ratio.step(edges[1:-1], ratio, color=color, linestyle='-', where="mid")
        return



def plot_EnuReco_bias(ax, filename: str, label: str, color: str):

    infile = up.open(filename)
    Enu_t  = 1000*infile["FlatTree_VARS;53"]["Enu_true"].array()
    Enu_QE = 1000*infile["FlatTree_VARS;53"]["Enu_QE"].array()
    mode   = infile["FlatTree_VARS;53"]["cc"].array()
    diff = Enu_t - Enu_QE

    # Select only events with mode == 1
    mask = (mode == 1)
    diff_sel = diff[mask]
    Enu_t_sel = Enu_t[mask]
    Enu_QE_sel = Enu_QE[mask]

    # ----------------------------------------
    # Arrays to hold oscillation probs for
    # different oscillation parameters
    # ----------------------------------------
    prob_default_dm2 = []
    prob_plus_dm2    = []
    prob_minus_dm2   = []

    prob_plus_dcp    = []
    prob_minus_dcp   = []

    # ----------------------------------------
    # Compute oscillation weights PER EVENT
    # (convert MeV -> GeV for OscProb)
    # ----------------------------------------
    prob_default_dm2 = np.array([pmns.Prob(1, 1, E/1000.0, L) for E in Enu_t_sel])  # νμ → νμ survival

    # Increase dm23^2 by +0.4%
    dm32_new = dm32*1.004
    pmns.SetDeltaMsqrs(dm21, dm32_new)
    prob_plus_dm2 = np.array([pmns.Prob(1, 1, E/1000.0, L) for E in Enu_t_sel])  # νμ → νμ survival

    # Decrease dm23^2 by +0.4%
    dm32_new = dm32*0.096
    pmns.SetDeltaMsqrs(dm21, dm32_new)
    prob_minus_dm2 = np.array([pmns.Prob(1, 1, E/1000.0, L) for E in Enu_t_sel])  # νμ → νμ survival

    # Increase dCP by + pi/10
    dCP_new = deltaCP+np.pi/10
    pmns.SetMix(theta12, theta23, theta13, dCP_new)
    prob_plus_dcp = np.array([pmns.Prob(1, 0, E/1000.0, L) for E in Enu_t_sel])  # νμ → νμ survival

    # Decrease dCP by  pi/10
    dCP_new = deltaCP-np.pi/10
    pmns.SetMix(theta12, theta23, theta13, dCP_new)
    prob_minus_dcp = np.array([pmns.Prob(1, 0, E/1000.0, L) for E in Enu_t_sel])  # νμ → νμ survival


    ax.hist(diff_sel, bins=np.arange(-1000, 1000, step=10), histtype='step', weights=np.ones_like(diff_sel), color=color,linewidth=1.5, label = label)
    # Create a matching line handle for legend
    custom_lines.append(Line2D([0], [0], color=color, lw=2, linestyle='-'))
    labels.append(label)

    plot_osc_bias(ax, diff_sel, "default PMNS", vivid_purple, prob_default_dm2)
    plot_osc_bias(ax, diff_sel, "Inc dm32", light_red, prob_plus_dm2)
    plot_osc_bias(ax, diff_sel, "Dec dm32", dark_red, prob_minus_dm2)

    plot_osc_bias(ax, diff_sel, "Inc dCP", light_green, prob_plus_dcp)
    plot_osc_bias(ax, diff_sel, "Dec dm32", dark_green, prob_minus_dcp)

def plot_EnuReco_bias_ROOT(ax, ax_ratio, filename: str, label: str, color: str):

    fin = ROOT.TFile.Open(filename)
    tree = fin.Get("FlatTree_VARS")

    # ---------------------------------
    # Event loop
    # ---------------------------------
    nentries    = tree.GetEntries()
    diff_sel    = []
    Enu_t_sel   = []
    Enu_QE_sel   = []
    counts_nom  = []

    for i in range(2000000):
        tree.GetEntry(i)

        Enu_true = tree.Enu_true * 1000
        Enu_QE   = tree.Enu_QE * 1000
        pdg = tree.pdg
        nfsp     = tree.nfsp


        for j in range(nfsp):
            apdg = abs(int(pdg[j]))
            if(apdg == 211 or apdg ==111 or apdg == 311 or apdg > 3000):
                continue
            else:
                # print("Particle: ", apdg)
                diff = Enu_QE - Enu_true
                diff_sel.append(diff)
                Enu_t_sel.append(Enu_true)
                Enu_QE_sel.append(Enu_QE)
        # diff = Enu_QE - Enu_true
        # diff_sel.append(diff)
        # Enu_t_sel.append(Enu_true)
        # Enu_QE_sel.append(Enu_QE)


    diff_sel = np.array(diff_sel)
    Enu_t_sel = np.array(Enu_t_sel)
    Enu_QE_sel = np.array(Enu_QE_sel)

    # ----------------------------------------
    # Arrays to hold oscillation probs for
    # different oscillation parameters
    # ----------------------------------------
    prob_default_dm2 = []
    prob_plus_dm2    = []
    prob_minus_dm2   = []

    prob_plus_dcp    = []
    prob_minus_dcp   = []

    # ----------------------------------------
    # Compute oscillation weights PER EVENT
    # (convert MeV -> GeV for OscProb)
    # ----------------------------------------
    prob_default_numu = np.array([pmns.Prob(1, 1, E/1000.0, L) for E in Enu_t_sel])  # νμ → νμ survival
    prob_default_nue = np.array([pmns.Prob(1, 0, E/1000.0, L) for E in Enu_t_sel])  # νμ → νe

    ## Increase dm23^2 by +0.4%
    dm32_new = dm32*1.004
    pmns.SetDeltaMsqrs(dm21, dm32_new)
    prob_plus_dm2 = np.array([pmns.Prob(1, 1, E/1000.0, L) for E in Enu_t_sel])  # νμ → νμ survival

    ## Decrease dm23^2 by +0.4%
    dm32_new = dm32*0.996
    pmns.SetDeltaMsqrs(dm21, dm32_new)
    prob_minus_dm2 = np.array([pmns.Prob(1, 1, E/1000.0, L) for E in Enu_t_sel])  # νμ → νμ survival

    ## Increase dCP by + 20deg
    dCP_new = deltaCP+(20*np.pi/180)
    pmns.SetMix(theta12, theta23, theta13, dCP_new)
    prob_plus_dcp = np.array([pmns.Prob(1, 0, E/1000.0, L) for E in Enu_t_sel])  # νμ → νe

    ## Decrease dCP by  20deg
    dCP_new = deltaCP-(20*np.pi/180)
    pmns.SetMix(theta12, theta23, theta13, dCP_new)
    prob_minus_dcp = np.array([pmns.Prob(1, 0, E/1000.0, L) for E in Enu_t_sel])  # νμ → νe 


    # ax.hist(diff_sel, bins=np.arange(-1000, 1000, step=10), histtype='step', weights=np.ones_like(diff_sel), color=color,linewidth=1.5, label = label)
    # Create a matching line handle for legend
    # custom_lines.append(Line2D([0], [0], color=color, lw=2, linestyle='-'))
    # labels.append(label)

    
    ## Create inset
    # axins = inset_axes(
    #     ax,
    #     width="40%",   # width relative to parent
    #     height="40%",  # height relative to parent
    #     loc="upper right"
    # )
    axins = []
    ## Zoom region (Enu QE)
    # axins.set_xlim(400, 700)
    # axins.set_ylim(2350, 2650)
    ## Zoom region (Enu True)
    # axins.set_xlim(500, 750)
    # axins.set_ylim(bottom = 2350)#, 3325)

    counts_nom = plot_osc_bias(ax, ax_ratio, axins, Enu_QE_sel, "default PMNS", vivid_purple, prob_default_nue, True, counts_nom)
    plot_osc_bias(ax, ax_ratio, axins, Enu_QE_sel, "Inc dCP", light_green, prob_plus_dcp, False, counts_nom)
    plot_osc_bias(ax, ax_ratio, axins, Enu_QE_sel, "Dec dCP", dark_green, prob_minus_dcp, False, counts_nom)
    plot_osc_bias(ax, ax_ratio, axins, Enu_QE_sel+5, "default PMNS, 2MeV shift in EnuQE", dark_blue, prob_default_nue, False, counts_nom)


    # counts_nom = plot_osc_bias(ax, ax_ratio, axins, Enu_t_sel, "default PMNS", vivid_purple, prob_default_numu, True, counts_nom)
    # plot_osc_bias(ax, ax_ratio, axins, Enu_t_sel, "Inc dm32", 'purple', prob_plus_dm2,  False, counts_nom)
    # plot_osc_bias(ax, ax_ratio, axins, Enu_t_sel, "Dec dm32", dark_red, prob_minus_dm2, False, counts_nom)    
    ## Zoom region (Enu QE)
    # axins.set_xlim(500, 900)
    # axins.set_ylim(6800, 8000)
    ## Zoom region (Enu True)
    # axins.set_xlim(500, 700)
    # axins.set_ylim(600, 1200)

    ## Draw rectangle + connecting lines
    # mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")



    return

# fig = plt.figure(figsize=(10, 10))
#
# gs = GridSpec(2, 3, figure=fig)
#
# # Define the subplots
# ax1 = fig.add_subplot(gs[0, 0])  # Top left
# ax2 = fig.add_subplot(gs[0, 1])  # Top right
# ax3 = fig.add_subplot(gs[0, 2])  # Bottom left
# ax4 = fig.add_subplot(gs[1, 0])  # Bottom right
# ax5 = fig.add_subplot(gs[1, 1])  # Bottom right

## Set axis
fig = plt.figure()
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1], hspace=0.07)
ax = fig.add_subplot(gs[0])
ax_ratio = fig.add_subplot(gs[1], sharex=ax)
ax_ratio.set_ylim(0.96,1.04)
plt.sca(ax)
plt.setp(ax.get_xticklabels(), visible=False)
plot_EnuReco_bias_ROOT(ax, ax_ratio, "../../FSI/NuWro_HK_test.flat.root", r"NuWro SF", dark_blue)

ax.legend(custom_lines, labels, loc = 'lower right')
# plt.title("HK Enu reco for all channels")
ax_ratio.set_xlabel(r"$E_{\nu}^{\text{\text{QE}}}$ [MeV]")
ax.set_ylabel("Number of events")
# plt.savefig("plots/Fig1_HK_EnuQE_dCP_shifts_ratio.pdf")
plt.show()



