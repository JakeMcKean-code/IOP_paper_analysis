from FlatTreeMod import *
ROOT.gROOT.SetBatch(True)

def plot_Enu_bias_numu(filename, label, isNuBar, nEvents, plot_name):
  fig, ax = plt.subplots()
  # ---------------------------------
  # Open input file and tree
  # ---------------------------------
  fin = ROOT.TFile.Open(filename)
  tree = fin.Get("FlatTree_VARS")

  # ---------------------------------
  # Event loop
  # ---------------------------------
  nentries    = tree.GetEntries()
  diff_sel    = []
  Enu_t_sel   = []
  Enu_QE_sel   = []
  nevs = 0
  if(nEvents == -1):
      nevs = nentries
  else:
      nevs = nEvents

  for i in range(nevs):

    tree.GetEntry(i)

    Enu_true = tree.Enu_true*1000
    Enu_QE   = tree.Enu_QE*1000
    nfsp     = tree.nfsp
    pdg      = tree.pdg

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
    if(isNuBar == False):
      if has_mesons or n_proton < 1:
          continue
    else:
       if has_mesons:
          continue

    # -------------------------
    # Fill only if passed
    # -------------------------
    diff = Enu_QE - Enu_true

    diff_sel.append(diff)
    Enu_t_sel.append(Enu_true)
    Enu_QE_sel.append(Enu_QE)


  diff_sel = np.array(diff_sel)
  Enu_t_sel = np.array(Enu_t_sel)
  Enu_QE_sel = np.array(Enu_QE_sel)

  ax.hist(diff_sel, bins=np.arange(-1000, 1000, step=10), histtype='step', weights=np.ones_like(diff_sel), color=dark_blue,linewidth=1.5, label = label)
  custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
  labels.append(label)

  ax.legend()
  plt.gca()
  plt.savefig(f"Fig2_plots/Fig2_HK_EnuRecoBias_{plot_name}.pdf")
  # plt.show()

  fin.Close()
  Print(f"Done: {filename}")

_events = 100000
plot_Enu_bias_numu(filename="../../noFSI/NuWro_HK_noFSI_numu.flat.root", label = r"no FSI $\nu_{\mu}$", isNuBar = False, nEvents=_events, plot_name="noFSI_numu")
plot_Enu_bias_numu(filename="../../noFSI/NuWro_HK_noFSI_numubar.flat.root", label = r"no FSI $\bar{\nu}_{\mu}$", isNuBar = True, nEvents=_events, plot_name="noFSI_numubar")

plot_Enu_bias_numu(filename="../../FSI/NuWro_HK_numu.flat.root", label = r"FSI $\nu_{\mu}$", isNuBar = False, nEvents=_events, plot_name="FSI_numu")
plot_Enu_bias_numu(filename="../../FSI/NuWro_HK_numubar.flat.root", label = r"FSI $\bar{\nu}_{\mu}$", isNuBar = True, nEvents=_events, plot_name="FSI_numubar")