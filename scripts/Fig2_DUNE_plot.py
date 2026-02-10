from FlatTreeMod import *
from collections import defaultdict
ROOT.gROOT.SetBatch(True)

def plot_Enu_bias_numu(filename, nEvents, plot_name):
    fig, ax = plt.subplots()
    # ---------------------------------
    # Open input file and tree
    # ---------------------------------
    fin = ROOT.TFile.Open(filename)
    tree = fin.Get("FlatTree_VARS")

    bias_wo_list   = []
    bias_with_list = []
    bias_wo_by_n   = defaultdict(list)     # neutron breakdown
    bias_with_by_n = defaultdict(list)
    # ---------------------------------
    # Event loop
    # ---------------------------------
    nentries = tree.GetEntries()
    nevs = 0
    if(nEvents == -1):
        nevs = nentries
    else:
        nevs = nEvents

    for i in range(nevs):
        tree.GetEntry(i)
        has_neutron = False
        ELep     = tree.ELep
        Enu_true = tree.Enu_true
        nfsp     = tree.nfsp
        mode     = tree.Mode

        E  = tree.E
        px = tree.px
        py = tree.py
        pz = tree.pz
        pdg = tree.pdg

        # -------------------------
        # Lepton energy
        # -------------------------
        enuhad_wo   = ELep
        enuhad_with = ELep

        # Loop over final state particles
        for j in range(nfsp):

            apdg = abs(int(pdg[j]))
            Ej   = float(E[j])
            pxj  = float(px[j])
            pyj  = float(py[j])
            pzj  = float(pz[j])

            p2 = pxj*pxj + pyj*pyj + pzj*pzj

            # Check for neutron
            if apdg == 2112:
                has_neutron = True

            # -------------------------
            # Heavy baryons (both defs)
            # -------------------------
            if apdg > 3000: # Remove contribution > 0
                continue
            if apdg > 2300 and apdg < 3000:
                enuhad_wo   += Ej
                enuhad_with += Ej
                continue

            # -------------------------
            # Definition 1 (no pion mass subtraction)
            # -------------------------
            if (apdg == 11 or (apdg > 17 and apdg < 2000)) and (apdg != 211):
                enuhad_wo += Ej

            elif apdg == 2212 or apdg == 211:
                mass2 = Ej*Ej - p2
                if mass2 > 0:
                    mass = np.sqrt(mass2)
                    enuhad_wo += (Ej - mass)

            # -------------------------
            # Definition 2 (with pion masses)
            # -------------------------
            if (apdg == 11 or (apdg > 17 and apdg < 2000)):
                enuhad_with += Ej

            elif apdg == 2212:
                mass2 = Ej*Ej - p2
                if mass2 > 0:
                    mass = np.sqrt(mass2)
                    enuhad_with += (Ej - mass)

        # -------------------------
        # Fill
        # -------------------------
        bias_wo   = enuhad_wo   - Enu_true
        bias_with = enuhad_with - Enu_true

        # Total
        bias_wo_list.append(bias_wo)
        bias_with_list.append(bias_with)

        # By neutron content
        bias_wo_by_n[has_neutron].append(bias_wo)
        bias_with_by_n[has_neutron].append(bias_with)

    # ---------------------------------
    # Write output
    # ---------------------------------
    bias_wo_list = np.array(bias_wo_list)
    bias_with_list = np.array(bias_with_list)
    for k in bias_wo_by_n:
       bias_wo_by_n[k] = np.array(bias_wo_by_n[k])
       bias_with_by_n[k] = np.array(bias_with_by_n[k])

    styles = {
        False: dict(color="green", linestyle="--", label="No neutron"),
        True:  dict(color="purple", linestyle="--",  label="With neutron"),
    }

    ax.hist(bias_with_list, bins=np.arange(-3, 1, step=0.04), histtype='step', weights=np.ones_like(bias_with_list), color=dark_blue,linewidth=1.5, label = "w/o pion mass")

    # Create a matching line handle for legend
    custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
    labels.append("w/o pion mass")

    # ax.hist(bias_with_list, bins=np.arange(-3, 1, step=0.04), histtype='step', weights=np.ones_like(bias_wo_list), color=dark_red,linewidth=1.5, label = "w/ pion mass")
    # custom_lines.append(Line2D([0], [0], color=dark_red, lw=2, linestyle='-'))
    # labels.append("w/ pion mass")

    bins = np.arange(-3, 1, step=0.04)
    # w/o pion mass, by neutron
    vals_no  = bias_with_by_n[False]
    vals_yes = bias_with_by_n[True]

    ax.hist(
        [vals_no, vals_yes],   # list of arrays
        bins=bins,
        stacked=True,
        linewidth=1.5,
        label=["No neutron", "With neutron"],
        color=["green", "purple"]
    )
    ax.legend()

    plt.gca()
    plt.savefig(f"Fig2_plots/Fig2_DUNE_EnuRecoBias_{plot_name}.pdf")
    # plt.show()
    fin.Close()
    Print(f"Done: {filename}")

_events = -1
plot_Enu_bias_numu(filename="../../noFSI/NuWro_Ar40_noFSI_numu.flat.root", nEvents=_events, plot_name="WithPion_noFSI_numu")
plot_Enu_bias_numu(filename="../../noFSI/NuWro_Ar40_noFSI_numubar.flat.root", nEvents=_events, plot_name="WithPion_noFSI_numubar")

# plot_Enu_bias_numu(filename="../../FSI/NuWro_Ar40_numu.flat.root", nEvents=_events, plot_name="FSI_numu")
# plot_Enu_bias_numu(filename="../../FSI/NuWro_Ar40_numubar.flat.root", nEvents=_events, plot_name="FSI_numubar")