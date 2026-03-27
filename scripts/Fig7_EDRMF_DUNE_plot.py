from FlatTreeMod import *
ROOT.gROOT.SetBatch(True)

def plot_Enu_bias_numu(ax, filename, label, nEvents, withPion):
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

  bin_width = 0.05
  bins = np.arange(-0.7, 0+bin_width, step=bin_width)
  weights_with = fScaleFactor*np.ones_like(bias_with_list)/bin_width
  weights_wo = fScaleFactor*np.ones_like(bias_wo_list)/bin_width

  if(withPion == True):
    if(label == "ED-RMF"):
      ax.hist(bias_with_list, bins=bins, histtype='step', weights=weights_with, color=dark_red,linewidth=1.5, label = f"{label} w/ pion mass")
      custom_lines.append(Line2D([0], [0], color=dark_red, lw=2, linestyle='-'))
      labels.append(f"{label} w/ pion mass")
    elif (label == "RPWIA"):
      ax.hist(bias_with_list, bins=bins, histtype='step', weights=weights_with, color=dark_blue,linewidth=1.5, label = f"{label} w/ pion mass")
      custom_lines.append(Line2D([0], [0], color=dark_red, lw=2, linestyle='-'))
      labels.append(f"{label} w/ pion mass") 
      
  else:
    if(label == "ED-RMF"):
      ax.hist(bias_wo_list, bins=bins, histtype='step', weights=weights_wo, color=dark_red,linewidth=1.5, label = f"{label} w/o pion mass")
      custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
      labels.append(f"{label}w/o pion mass")
    elif (label == "RPWIA"):
      ax.hist(bias_wo_list, bins=bins, histtype='step', weights=weights_wo, color=dark_blue,linewidth=1.5, label = f"{label} w/o pion mass")
      custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
      labels.append(f"{label}w/o pion mass")


  fin.Close()
  Print(f"Done: {filename}")


fig, ax = plt.subplots(1,2)
_events = 10000
_withPion = False
plot_Enu_bias_numu(ax=ax[0], filename="../../FSI/NEUT_Ar40_EDRMF_numu.flat.root", label="ED-RMF", nEvents=_events, withPion=_withPion)
plot_Enu_bias_numu(ax=ax[0], filename="../../FSI/RPWIA_1M_Cas_numu_Ar40.flat.root", label="RPWIA", nEvents=_events, withPion=_withPion)
ax[0].legend(loc='best', fontsize=15)
ax[0].set_xlabel(r"$E_{\nu}^{\text{bias}}$ [MeV]")
ax[0].set_ylabel(r"$\text{d}\sigma/\text{d}E_{\nu}^{\text{bias}}$ [cm$^{2}$/nucleon MeV]")

_events = 10000
_withPion = True
plot_Enu_bias_numu(ax=ax[1], filename="../../FSI/NEUT_Ar40_EDRMF_numu.flat.root", label="ED-RMF", nEvents=_events, withPion=_withPion)
plot_Enu_bias_numu(ax=ax[1], filename="../../FSI/RPWIA_1M_Cas_numu_Ar40.flat.root", label="RPWIA", nEvents=_events, withPion=_withPion)
ax[1].legend(loc='best', fontsize=15)
ax[1].set_xlabel(r"$E_{\nu}^{\text{bias}}$ [MeV]")
ax[1].set_ylabel(r"$\text{d}\sigma/\text{d}E_{\nu}^{\text{bias}}$ [cm$^{2}$/nucleon MeV]")
plt.show()



