from FlatTreeMod import *
ROOT.gROOT.SetBatch(True)

def plot_Enu_bias_numu(ax, filename, isNub, nEvents):
  # ---------------------------------
  # Open input file and tree
  # ---------------------------------
  Print(f"Reading: {filename}")
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


  pass_flag = 0
  fail_flag = 0
  for i in range(nevs):

    tree.GetEntry(i)
    nfsp     = tree.nfsp
    pdg      = tree.pdg
    mode      = tree.Mode
    isCC0pi     = tree.flagCC0pi

    _fscalefactor = tree.fScaleFactor
    if(_fscalefactor > fScaleFactor):
       fScaleFactor = _fscalefactor

    if(i==1):
      Log(f"Scale factor: {fScaleFactor}")
 
    if(isCC0pi == True):
      pass_flag += 1
      Enu_true = tree.Enu_true*1000
      Enu_QE   = tree.Enu_QE*1000
      # -------------------------
      # Fill only if passed
      # -------------------------
      diff = Enu_QE - Enu_true
      # if(abs(diff) < 1000):
      diff_sel.append(diff)
      Enu_t_sel.append(Enu_true)
      Enu_QE_sel.append(Enu_QE)
    else:
       fail_flag += 1

  Log(f"Flag stats: pass {pass_flag}, fail {fail_flag}")
  Log(f"Flag*fScaleFactor stats: pass {pass_flag*fScaleFactor}, fail {fail_flag*fScaleFactor}")
  diff_sel = np.array(diff_sel)
  Enu_t_sel = np.array(Enu_t_sel)
  Enu_QE_sel = np.array(Enu_QE_sel)

  bin_width = 10
  # bins = 100
  bins = np.arange(-1000, 1000, step=bin_width)
  weights = fScaleFactor*np.ones_like(diff_sel)/bin_width

  if("noFSI" in filename):  
    ax.hist(diff_sel, bins=bins, histtype='step', weights=weights, color=dark_blue, linewidth=1.8, label = "noFSI")
    custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
    labels.append("noFSI")
  else:
    ax.hist(diff_sel, bins=bins, histtype='step', weights=weights, color=dark_red, linewidth=1.8, label = "FSI")
    custom_lines.append(Line2D([0], [0], color=dark_red, lw=2, linestyle='-'))
    labels.append("FSI")

  if(isNub == False):
    ax.set_title(r"$\nu_{\mu}$")
  else:
    ax.set_title(r"$\bar{\nu}_{\mu}$")
  
  fin.Close()
  return ax


fig, ax = plt.subplots()
_events = 100000
# plot_Enu_bias_numu(ax, filename="../../Remade_April26/HK/HK_numu_noFSI.flat.root", isNub=False, nEvents=_events)
# ax = plot_Enu_bias_numu(ax, filename="../../Remade_April26/HK/HK_numu_FSI.flat.root", isNub=False, nEvents=_events)

plot_Enu_bias_numu(ax, filename="../../Remade_April26/HK/HK_numubar_noFSI.flat.root", isNub=True, nEvents=_events)
ax = plot_Enu_bias_numu(ax, filename="../../Remade_April26/HK/HK_numubar_FSI.flat.root", isNub=True, nEvents=_events)

ax.vlines(x=0, ymin=0, ymax = ax.get_ylim()[1], color='black', linestyles='--')
ax.legend(loc = 'best', fontsize=15)
ax.set_xlabel(r"$E_{\nu}^{\text{bias}}$ [MeV]")
ax.set_ylabel(r"$\text{d}\sigma/\text{d}E_{\nu}^{\text{bias}}$ [cm$^{2}$/nucleon MeV]")
plt.show()
