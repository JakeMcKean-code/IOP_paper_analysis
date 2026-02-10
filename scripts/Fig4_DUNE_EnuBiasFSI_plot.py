from FlatTreeMod import *
ROOT.gROOT.SetBatch(True)

def plot_Enu_bias_numu(ax, filename, nEvents, withPion):
  # ---------------------------------
  # Open input file and tree
  # ---------------------------------
  fin = ROOT.TFile.Open(filename)
  tree = fin.Get("FlatTree_VARS")

  bias_wo_list   = []
  bias_with_list = []
  # ---------------------------------
  # Event loop
  # ---------------------------------
  nentries = tree.GetEntries()
  nevs = 0
  fScaleFactor = 0
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
      _fscalefactor = tree.fScaleFactor
      if(_fscalefactor > fScaleFactor):
         fScaleFactor = _fscalefactor

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

      # Check the > 0 contribution
      # if(bias_wo > 0):
      #     print("######")
      #     print("Mode: ", mode)
      #     for j in range(nfsp):
      #         print(f"particle {j}: ", abs(int(pdg[j])) )

      # for j in range(nfsp):
      #      if(abs(int(pdg[j])) == 3222):
      #          print(bias_wo, bias_with)

      bias_wo_list.append(bias_wo)
      bias_with_list.append(bias_with)

  # ---------------------------------
  # Write output
  # ---------------------------------
  bias_wo_list = np.array(bias_wo_list)
  bias_with_list = np.array(bias_with_list)

  bin_width = 0.04
  bins = np.arange(-3, 1, step=bin_width)
  weights_with = fScaleFactor*np.ones_like(bias_with_list)/bin_width
  weights_wo = fScaleFactor*np.ones_like(bias_wo_list)/bin_width

  if(withPion == True):
    if("noFSI" in filename):
      ax.hist(bias_with_list, bins=bins, histtype='step', weights=weights_with, color=dark_red,linewidth=1.5, label = "w/ pion mass noFSI")
      custom_lines.append(Line2D([0], [0], color=dark_red, lw=2, linestyle='-'))
      labels.append("w/ pion mass noFSI")
    else:
      ax.hist(bias_with_list, bins=bins, histtype='step', weights=weights_with, color=dark_blue,linewidth=1.5, label = "w/ pion mass FSI")
      custom_lines.append(Line2D([0], [0], color=dark_red, lw=2, linestyle='-'))
      labels.append("w/ pion mass FSI") 
      
  else:
    if("noFSI" in filename):
      ax.hist(bias_wo_list, bins=bins, histtype='step', weights=weights_wo, color=dark_red,linewidth=1.5, label = "w/o pion mass noFSI")
      custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
      labels.append("w/o pion mass noFSI")
    else:
      ax.hist(bias_wo_list, bins=bins, histtype='step', weights=weights_wo, color=dark_blue,linewidth=1.5, label = "w/o pion mass FSI")
      custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
      labels.append("w/o pion mass FSI")


  fin.Close()
  Print(f"Done: {filename}")


fig, ax = plt.subplots()
_events = -1
_withPion = True
plot_Enu_bias_numu(ax=ax, filename="../../noFSI/NuWro_Ar40_noFSI_numu.flat.root", nEvents=_events, withPion=_withPion)
plot_Enu_bias_numu(ax=ax, filename="../../FSI/NuWro_Ar40_numu.flat.root", nEvents=_events, withPion=_withPion)
ax.legend(loc='best', fontsize=15)
ax.set_xlabel(r"$E_{\nu}^{\text{bias}}$ [MeV]")
ax.set_ylabel(r"$\text{d}\sigma/\text{d}E_{\nu}^{\text{bias}}$ [cm$^{2}$/nucleon MeV]")
plt.savefig("Fig4_plots/Fig4_DUNE_EnuRecoFSIBias_WithPion_numu.pdf")

fig2, ax2 = plt.subplots()
plot_Enu_bias_numu(ax=ax2, filename="../../noFSI/NuWro_Ar40_noFSI_numubar.flat.root", nEvents=_events, withPion=_withPion)
plot_Enu_bias_numu(ax=ax2, filename="../../FSI/NuWro_Ar40_numubar.flat.root", nEvents=_events, withPion=_withPion)
ax2.legend(loc='best', fontsize=15)
ax2.set_xlabel(r"$E_{\nu}^{\text{bias}}$ [MeV]")
ax2.set_ylabel(r"$\text{d}\sigma/\text{d}E_{\nu}^{\text{bias}}$ [cm$^{2}$/nucleon MeV]")
plt.savefig("Fig4_plots/Fig4_DUNE_EnuRecoFSIBias_WithPion_numubar.pdf")


# plot_Enu_bias_numu(ax=ax, filename="../../noFSI/NuWro_Ar40_noFSI_numubar.flat.root", nEvents=_events, withPion=True)
# plot_Enu_bias_numu(ax=ax, filename="../../FSI/NuWro_Ar40_numubar.flat.root", nEvents=_events, withPion=True)
