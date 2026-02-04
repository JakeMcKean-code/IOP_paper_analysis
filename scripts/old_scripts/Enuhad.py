import ROOT
import numpy as np
import math

ROOT.gROOT.SetBatch(True)

# ---------------------------------
# Open input file and tree
# ---------------------------------
fin = ROOT.TFile.Open("../flattrees/nuwro/NuWro_Ar40_test.flat.root")
tree = fin.Get("FlatTree_VARS")

# ---------------------------------
# Output file
# ---------------------------------
fout = ROOT.TFile("Fig1_SF_Dune_EnuRecoPy.root", "RECREATE")

# ---------------------------------
# Histograms
# ---------------------------------
h_bias_wo = ROOT.TH1D(
    "h_bias_wo",
    "No pion mass subtraction; (E_{vis}-E_{true}) [GeV];Events",
    100, -3, 1
)

h_bias_with = ROOT.TH1D(
    "h_bias_with",
    "With pion masses; (E_{vis}-E_{true}) [GeV];Events",
    100, -3, 1
)

bias_wo_list   = []
bias_with_list = []

# ---------------------------------
# Event loop
# ---------------------------------
nentries = tree.GetEntries()
print("Processing", nentries, "events")

for i in range(nentries):

    tree.GetEntry(i)

    ELep     = tree.ELep
    Enu_true = tree.Enu_true
    nfsp     = tree.nfsp

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
        if apdg > 2300 and apdg < 10000:
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
                mass = math.sqrt(mass2)
                enuhad_wo += (Ej - mass)

        # -------------------------
        # Definition 2 (with pion masses)
        # -------------------------
        if (apdg == 11 or (apdg > 17 and apdg < 2000)):
            enuhad_with += Ej

        elif apdg == 2212:
            mass2 = Ej*Ej - p2
            if mass2 > 0:
                mass = math.sqrt(mass2)
                enuhad_with += (Ej - mass)

    # -------------------------
    # Fill
    # -------------------------
    bias_wo   = enuhad_wo   - Enu_true
    bias_with = enuhad_with - Enu_true

    h_bias_wo.Fill(bias_wo)
    h_bias_with.Fill(bias_with)

    bias_wo_list.append(bias_wo)
    bias_with_list.append(bias_with)

# ---------------------------------
# Write output
# ---------------------------------
fout.cd()
h_bias_wo.Write()
h_bias_with.Write()
fout.Write()
fout.Close()
fin.Close()

print("Done.")
