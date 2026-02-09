from FlatTreeMod import *
ROOT.gROOT.SetBatch(True)

def plot_Enu_bias_numu(filename, nEvents, plot_name, withPion, xbins, ybins):
  fig, ax = plt.subplots()
  # ---------------------------------
  # Open input file and tree
  # ---------------------------------
  fin = ROOT.TFile.Open(filename)
  tree = fin.Get("FlatTree_VARS")

  bias_wo_list   = []
  bias_with_list = []
  Enu_t          = []
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

      bias_wo_list.append(bias_wo)
      bias_with_list.append(bias_with)
      Enu_t.append(Enu_true)

  # ---------------------------------
  # Write output
  # ---------------------------------
  bias_wo_list = np.array(bias_wo_list)
  bias_with_list = np.array(bias_with_list)
  Enu_t = np.array(Enu_t)

  if(withPion == True):
    h = ax.hist2d(
    bias_with_list,
    Enu_t,
    bins=[xbins, ybins],
    cmap="viridis"
  )
    plt.colorbar(h[3], ax=ax, label="Counts")
      
  else:
    h = ax.hist2d(
    bias_wo_list,
    Enu_t,
    bins=[xbins, ybins],
    cmap="viridis"
  )
    plt.colorbar(h[3], ax=ax, label="Counts")

  plt.savefig(f"Fig6_plots/Fig6_DUNE_EnuRecoBias2D_{plot_name}.pdf")
  fin.Close()
  Print(f"Done: {filename}")


_events = 100000
_xbins = np.arange(-0.4, 0.4, 0.01)      # bias bins
_ybins = np.linspace(0, 3, 100)     # Enu bins (adjust range!)

plot_Enu_bias_numu(filename="../../noFSI/NuWro_Ar40_noFSI_numu.flat.root", nEvents=_events, plot_name = "noFSI_WithoutPion_numu", withPion=False, xbins=_xbins, ybins=_ybins)
plot_Enu_bias_numu(filename="../../FSI/NuWro_Ar40_numu.flat.root", nEvents=_events, plot_name="FSI_WithoutPion_numu", withPion=False, xbins=_xbins, ybins=_ybins)
plot_Enu_bias_numu(filename="../../noFSI/NuWro_Ar40_noFSI_numubar.flat.root", nEvents=_events, plot_name="noFSI_WithoutPion_numubar", withPion=False, xbins=_xbins, ybins=_ybins)
plot_Enu_bias_numu(filename="../../FSI/NuWro_Ar40_numubar.flat.root", nEvents=_events, plot_name="FSI_WithoutPion_numubar", withPion=False, xbins=_xbins, ybins=_ybins)

plot_Enu_bias_numu(filename="../../noFSI/NuWro_Ar40_noFSI_numu.flat.root", nEvents=_events, plot_name = "noFSI_WithPion_numu", withPion=True, xbins=_xbins, ybins=_ybins)
plot_Enu_bias_numu(filename="../../FSI/NuWro_Ar40_numu.flat.root", nEvents=_events, plot_name="FSI_WithPion_numu", withPion=True, xbins=_xbins, ybins=_ybins)
plot_Enu_bias_numu(filename="../../noFSI/NuWro_Ar40_noFSI_numubar.flat.root", nEvents=_events, plot_name="noFSI_WithPion_numubar", withPion=True, xbins=_xbins, ybins=_ybins)
plot_Enu_bias_numu(filename="../../FSI/NuWro_Ar40_numubar.flat.root", nEvents=_events, plot_name="FSI_WithPion_numubar", withPion=True, xbins=_xbins, ybins=_ybins)