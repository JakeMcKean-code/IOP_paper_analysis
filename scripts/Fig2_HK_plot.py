from FlatTreeMod import *
ROOT.gROOT.SetBatch(True)

def plot_Enu_bias_numu(filename, nEvents):
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

    Enu_true = tree.Enu_true * 1000
    Enu_QE   = tree.Enu_QE * 1000
    pdg = tree.pdg
    diff = Enu_QE - Enu_true
    Enu_QE_sel.append(Enu_QE)
    Enu_t_sel.append(Enu_true)
    diff_sel.append(diff)


  diff_sel = np.array(diff_sel)
  Enu_t_sel = np.array(Enu_t_sel)
  Enu_QE_sel = np.array(Enu_QE_sel)

  plt.hist(diff_sel, bins=np.arange(-1000, 1000, step=10), histtype='step', weights=np.ones_like(diff_sel), color=dark_blue,linewidth=1.5, label = "")
  custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
  labels.append("")

  plt.legend()
  plt.savefig("Fig2_plots/Fig2_HK_EnuReco_bias.pdf")
  plt.show()

  fin.Close()
  print("Done.")


plot_Enu_bias_numu(filename="../../noFSI/NuWro_HK_noFSI_numu.flat.root", nEvents=1000000)