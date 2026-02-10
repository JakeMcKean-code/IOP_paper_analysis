from FlatTreeMod import *
ROOT.gROOT.SetBatch(True)

def plot_Enu_bias_numu(ax, filename, nEvents):
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
  fScaleFactor = 0
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
    _fscalefactor = tree.fScaleFactor
    if(_fscalefactor > fScaleFactor):
       fScaleFactor = _fscalefactor

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

  bin_width = 10
  bins = np.arange(-1000, 1000, step=bin_width)
  weights = fScaleFactor*np.ones_like(diff_sel)/bin_width

  if("noFSI" in filename):  
    ax.hist(diff_sel, bins=bins, histtype='step', weights=weights, color=dark_blue,linewidth=1.5, label = "noFSI")
    custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
    labels.append("noFSI")
  else:
    ax.hist(diff_sel, bins=bins, histtype='step', weights=weights, color=dark_red,linewidth=1.5, label = "FSI")
    custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
    labels.append("FSI")

  ax.set_title(r"$\nu_{\mu}$")
  fin.Close()
  Print(f"Done: {filename}")

def plot_Enu_bias_numubar(ax, filename, nEvents):
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
  fScaleFactor = 0
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
    _fscalefactor = tree.fScaleFactor
    if(_fscalefactor > fScaleFactor):
       fScaleFactor = _fscalefactor

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
    if has_mesons:# or n_proton < 1:
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

  bin_width = 10
  bins = np.arange(-1000, 1000, step=bin_width)
  weights = fScaleFactor*np.ones_like(diff_sel)/bin_width
  if("noFSI" in filename):  
    ax.hist(diff_sel, bins=bins, histtype='step', weights=weights, color=dark_blue,linewidth=1.5, label = "noFSI")
    custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
    labels.append("noFSI")
  else:
    ax.hist(diff_sel, bins=bins, histtype='step', weights=fScaleFactor*np.ones_like(diff_sel)/bin_width, color=dark_red,linewidth=1.5, label = "FSI")
    custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
    labels.append("FSI")

  ax.set_title(r"$\bar{\nu}_{\mu}$")
  fin.Close()
  Print(f"Done: {filename}")


# fig, ax = plt.subplots()
_events = -1
# plot_Enu_bias_numu(ax, filename="../../noFSI/NuWro_HK_noFSI_numu.flat.root", nEvents=_events)
# plot_Enu_bias_numu(ax, filename="../../FSI/NuWro_HK_numu.flat.root", nEvents=_events)
# ax.vlines(x=0, ymin=0, ymax = ax.get_ylim()[1], color='black', linestyles='--')
# ax.legend(loc = 'best', fontsize=15)
# ax.set_xlabel(r"$E_{\nu}^{\text{bias}}$ [MeV]")
# ax.set_ylabel(r"$\text{d}\sigma/\text{d}E_{\nu}^{\text{bias}}$ [cm$^{2}$/nucleon MeV]")
# plt.show()
# plt.savefig("Fig3_plots/Fig3_HK_EnuRecoFSIBias_numu.pdf")

fig2, ax2 = plt.subplots()
plot_Enu_bias_numubar(ax2, filename="../../noFSI/NuWro_HK_noFSI_numubar.flat.root", nEvents=_events)
plot_Enu_bias_numubar(ax2, filename="../../FSI/NuWro_HK_numubar.flat.root", nEvents=_events)
ax2.vlines(x=0, ymin=0, ymax = ax2.get_ylim()[1], color='black', linestyles='--')
ax2.legend(loc = 'best', fontsize=15)
ax2.set_xlabel(r"$E_{\nu}^{\text{bias}}$ [MeV]")
ax2.set_ylabel(r"$\text{d}\sigma/\text{d}E_{\nu}^{\text{bias}}$ [cm$^{2}$/nucleon MeV]")
# plt.show()
plt.savefig("Fig3_plots/Fig3_HK_EnuRecoFSIBias_numubar.pdf")
