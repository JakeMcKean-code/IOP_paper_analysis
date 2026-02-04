from FlatTreeMod import *
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

custom_lines = []
labels = []

bin_width = 20

def plot_osc_reco(ax, ax_ratio, diff_sel, label, color, weights, nominal, counts_nom):
    ax.hist(diff_sel, bins=np.arange(0, 2000, step=bin_width), histtype='step', weights=weights, color=color,linewidth=1.5, label = label, linestyle = '-')
    custom_lines.append(Line2D([0], [0], color=color, lw=2, linestyle='-'))
    labels.append(label)

    if(nominal == True):
        countsn, _ = np.histogram(diff_sel, weights=weights, bins=(np.arange(0, 2000, step=bin_width)))
        ax_ratio.hlines(1, 0, 2000, linestyle='--', color = 'black')
        return countsn
    else:
        counts, edges = np.histogram(diff_sel, weights=weights, bins=(np.arange(0, 2000, step=bin_width)))
        ratio = counts[1:]/counts_nom[1:]
        ax_ratio.step(edges[1:-1], ratio, color=color, linestyle='-', where="mid")
        return
        

def plot_osc_true(ax, ax_ratio, diff_sel, label, color, weights, nominal, counts_nom):
    ax.hist(diff_sel, bins=np.arange(0, 2000, step=bin_width), histtype='step', weights=weights, color=color,linewidth=1.5, label = label, linestyle = '-')
    custom_lines.append(Line2D([0], [0], color=color, lw=2, linestyle='-'))
    labels.append(label)

    if(nominal == True):
        countsn, _ = np.histogram(diff_sel, weights=weights, bins=(np.arange(0, 2000, step=bin_width)))
        ax_ratio.hlines(1, 0, 2000, linestyle='--', color = 'black')
        return countsn
    else:
        counts, edges = np.histogram(diff_sel, weights=weights, bins=(np.arange(0, 2000, step=bin_width)))
        ratio = counts[1:]/counts_nom[1:]
        ax_ratio.step(edges[1:-1], ratio, color=color, linestyle='-', where="mid")
        return
   


def plot_EnuReco(nEvents: int, IsReco: bool):
    ## Set axis
    fig = plt.figure()
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1], hspace=0.07)
    ax = fig.add_subplot(gs[0])
    ax_ratio = fig.add_subplot(gs[1], sharex=ax)
    plt.sca(ax)
    plt.setp(ax.get_xticklabels(), visible=False)

    filename = "../../FSI/NuWro_HK_numu.flat.root"
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
    nevs = 0
    if(nEvents == -1):
        nevs = nentries
    else:
        nevs = nEvents

    for i in range(nevs):
        tree.GetEntry(i)

        Enu_true = tree.Enu_true * 1000
        Enu_QE   = tree.Enu_QE * 1000
        pdg = tree.pdg
        nfsp     = tree.nfsp


        # -------------------------
        # CC0pi + Np selection
        # -------------------------
        n_proton = 0
        has_mesons = False

        for j in range(nfsp):

            apdg = abs(int(pdg[j]))

            if apdg == 2212:          # proton
                n_proton += 1

            elif apdg in [111,211,221,311,321] or apdg > 3000:
                has_mesons = True
                break

        # For numubar remove proton requirement
        if has_mesons or n_proton < 1:
            continue

        diff = Enu_QE - Enu_true
        diff_sel.append(diff)
        Enu_t_sel.append(Enu_true)
        Enu_QE_sel.append(Enu_QE)



    diff_sel = np.array(diff_sel)
    Enu_t_sel = np.array(Enu_t_sel)
    Enu_QE_sel = np.array(Enu_QE_sel)

    # ----------------------------------------
    # Arrays to hold oscillation probs for
    # different oscillation parameters
    # ----------------------------------------
    prob_plus_dm2    = []
    prob_minus_dm2   = []

    # ----------------------------------------
    # Compute oscillation weights PER EVENT
    # (convert MeV -> GeV for OscProb)
    # ----------------------------------------
    prob_default_numu = np.array([pmns.Prob(1, 1, E/1000.0, L) for E in Enu_t_sel])  # νμ → νe

    ## Increase dm23^2 by +0.4%
    dm32_new = dm32*1.004
    pmns.SetDeltaMsqrs(dm21, dm32_new)
    prob_plus_dm2 = np.array([pmns.Prob(1, 1, E/1000.0, L) for E in Enu_t_sel])  # νμ → νμ survival

    ## Decrease dm23^2 by +0.4%
    dm32_new = dm32*0.996
    pmns.SetDeltaMsqrs(dm21, dm32_new)
    prob_minus_dm2 = np.array([pmns.Prob(1, 1, E/1000.0, L) for E in Enu_t_sel])  # νμ → νμ survival

    if(IsReco == True):
        counts_nom = plot_osc_reco(ax, ax_ratio, Enu_QE_sel, "default PMNS", vivid_purple, prob_default_numu, True, counts_nom)
        plot_osc_reco(ax, ax_ratio, Enu_QE_sel, "Inc dm32", light_green, prob_plus_dm2, False, counts_nom)
        plot_osc_reco(ax, ax_ratio, Enu_QE_sel, "Dec dm32", dark_green, prob_minus_dm2, False, counts_nom)
        plot_osc_reco(ax, ax_ratio, Enu_QE_sel+2, "default PMNS, 5MeV shift in EnuQE", dark_blue, prob_default_numu, False, counts_nom)

        ax.legend(custom_lines, labels, loc = 'lower right')
        ax_ratio.set_xlabel(r"$E_{\nu}^{\text{\text{QE}}}$ [MeV]")
        ax.set_ylabel("Number of events")

        ax.set_xlim(150,1200)
        ax_ratio.set_xlim(150,1200)
        ax_ratio.set_ylim(0.96,1.04)
        # plt.savefig("Fig1_plots/Fig1_EnuQE_dm32.pdf")

    else:
        counts_nom = plot_osc_true(ax, ax_ratio, Enu_t_sel, "default PMNS", vivid_purple, prob_default_numu, True, counts_nom)
        plot_osc_true(ax, ax_ratio, Enu_t_sel, "Inc dm32", light_green, prob_plus_dm2, False, counts_nom)
        plot_osc_true(ax, ax_ratio, Enu_t_sel, "Dec dm32", dark_green, prob_minus_dm2, False, counts_nom)

        ax.legend(custom_lines, labels, loc = 'lower right')
        ax_ratio.set_xlabel(r"$E_{\nu}^{\text{\text{True}}}$ [MeV]")
        ax.set_ylabel("Number of events")
        ax.set_xlim(300,1200)
        ax_ratio.set_xlim(300,1200)
        ax_ratio.set_ylim(0.96,1.04)
        # plt.savefig("Fig1_plots/Fig1_EnuTrue_dm32.pdf")
    plt.show()

    return



plot_EnuReco(nEvents = 200000, IsReco = False)





