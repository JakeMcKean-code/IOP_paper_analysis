from FlatTreeMod import *
ROOT.gROOT.SetBatch(True)

def plot_Enu_bias_numu_flag(ax, filename, nEvents):
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
  Enu_QE_sel  = []
  flag_arr    = []
  nevs = 0
  if(nEvents == -1):
      nevs = nentries
  else:
      nevs = nEvents

  for i in range(nevs):

    tree.GetEntry(i)

    Enu_true = tree.Enu_true*1000
    Enu_QE   = tree.Enu_QE*1000
    flag     = tree.flagCC0pi

    
    diff = Enu_QE - Enu_true

    diff_sel.append(diff)
    Enu_t_sel.append(Enu_true)
    Enu_QE_sel.append(Enu_QE)
    flag_arr.append(flag)


  diff_sel = np.array(diff_sel)
  Enu_t_sel = np.array(Enu_t_sel)
  Enu_QE_sel = np.array(Enu_QE_sel)
  flag_arr = np.array(flag_arr)

  diff_sel = diff_sel[flag_arr]

  ax.hist(diff_sel, bins=np.arange(-1000, 1000, step=10), histtype='step', weights=np.ones_like(diff_sel), color=dark_red, linestyle = '--', linewidth=1.5, label = "flag")
  custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
  labels.append("flag")

  fin.Close()
  print("Done.")

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
    n_neutron = 0
    has_mesons = False

    for j in range(nfsp):

        apdg = abs(int(pdg[j]))

        if apdg == 2212:          # proton
            n_proton += 1
        elif apdg == 2112:
            n_neutron += 1

        elif apdg in [111,211,221,311,321] or apdg > 3000:
            has_mesons = True
            break

    # For numubar remove proton requirement
    # if has_mesons:# or n_proton < 1:
    if has_mesons or n_neutron < 1:
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

  ax.hist(diff_sel, bins=np.arange(-1000, 1000, step=10), histtype='step', weights=np.ones_like(diff_sel), color=dark_blue,linewidth=1.5, label = "manual")
  custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
  labels.append("manual")

  fin.Close()
  print("Done.")
  return ax

fig, ax = plt.subplots()

# ax = plot_Enu_bias_numu(ax, filename="../../noFSI/NuWro_HK_noFSI_numu.flat.root", nEvents=100000)
# plot_Enu_bias_numu_flag(ax, filename="../../noFSI/NuWro_HK_noFSI_numu.flat.root", nEvents=100000)

ax = plot_Enu_bias_numu(ax, filename="../../noFSI/NuWro_HK_noFSI_numubar.flat.root", nEvents=100000)
plot_Enu_bias_numu_flag(ax, filename="../../noFSI/NuWro_HK_noFSI_numubar.flat.root", nEvents=100000)

plt.legend()
plt.show()