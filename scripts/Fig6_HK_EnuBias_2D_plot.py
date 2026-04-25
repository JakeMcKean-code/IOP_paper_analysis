from FlatTreeMod import *
ROOT.gROOT.SetBatch(True)

# def plot_Enu_bias_numu(filename, nEvents, plot_name, xbins, ybins):
#   Print(f"Reading: {filename}")
#   fig, ax = plt.subplots()
#   # ---------------------------------
#   # Open input file and tree
#   # ---------------------------------
#   fin = ROOT.TFile.Open(filename)
#   tree = fin.Get("FlatTree_VARS")

#   # ---------------------------------
#   # Event loop
#   # ---------------------------------
#   nentries    = tree.GetEntries()
#   diff_sel    = []
#   Enu_t_sel   = []
#   Enu_QE_sel   = []
#   nevs = 0
#   if(nEvents == -1):
#       nevs = nentries
#   else:
#       nevs = nEvents

#   for i in range(nevs):

#     tree.GetEntry(i)
#     Enu_true = tree.Enu_true*1000
#     Enu_QE   = tree.Enu_QE*1000
#     nfsp     = tree.nfsp
#     pdg      = tree.pdg

#     # -------------------------
#     # CC0pi + Np selection
#     # -------------------------
#     n_proton = 0
#     has_mesons = False

#     for j in range(nfsp):

#         apdg = abs(int(pdg[j]))

#         if apdg == 2212:          # proton
#             n_proton += 1

#         elif apdg in [111,211,221,311,321] or apdg > 3000:
#             has_mesons = True
#             break

#     # For numubar remove proton requirement
#     if has_mesons or n_proton < 1:
#         continue

#     # -------------------------
#     # Fill only if passed
#     # -------------------------
#     diff = Enu_QE - Enu_true

#     diff_sel.append(diff)
#     Enu_t_sel.append(Enu_true)
#     Enu_QE_sel.append(Enu_QE)


#   diff_sel = np.array(diff_sel)
#   Enu_t_sel = np.array(Enu_t_sel)
#   Enu_QE_sel = np.array(Enu_QE_sel)

#   h = ax.hist2d(
#   diff_sel,
#   Enu_t_sel,
#   bins=[xbins, ybins],
#   cmap="viridis"
# )
#   plt.colorbar(h[3], ax=ax, label="Counts")
#   ax.set_title(r"$\nu_{\mu}$")
#   plt.savefig(f"Fig6_plots/Fig6_HK_EnuRecoBias2D_{plot_name}.pdf")
#   fin.Close()
#   Print(f"Done: {filename}")


def plot_Enu_bias(filename, isNub, nEvents, plot_name, xbins, ybins):
  Print(f"Reading: {filename}")
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
    isCC0pi     = tree.flagCC0pi

    if(isCC0pi == True):
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

  h = ax.hist2d(
  diff_sel,
  Enu_t_sel,
  bins=[xbins, ybins],
  cmap="viridis"
)
  plt.colorbar(h[3], ax=ax, label="Counts")
  if(isNub == True):
    ax.set_title(r"$\bar{\nu}_{\mu}$")
  else:
    ax.set_title(r"${\nu}_{\mu}$")
#   plt.savefig(f"Fig6_plots/Fig6_HK_EnuRecoBias2D_{plot_name}.pdf")
  fin.Close()
  plt.show()


_events = 100000
_xbins = np.arange(-1000, 1000, 20)      # bias bins
_ybins = np.linspace(0, 3000, 300)     # Enu bins 

plot_Enu_bias(filename="../../Remade_April26/HK/HK_numu_FSI.flat.root", isNub=True, nEvents=_events, plot_name="FSI_numub", xbins=_xbins, ybins=_ybins)
plot_Enu_bias(filename="../../Remade_April26/HK/HK_numubar_FSI.flat.root", isNub=False, nEvents=_events, plot_name="FSI_numu", xbins=_xbins, ybins=_ybins)