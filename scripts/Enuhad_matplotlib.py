from FlatTreeMod import *

ROOT.gROOT.SetBatch(True)

# ---------------------------------
# Open input file and tree
# ---------------------------------
fin = ROOT.TFile.Open("../..//NuWro_Ar40_test.flat.root")
tree = fin.Get("FlatTree_VARS")

bias_wo_list   = []
bias_with_list = []

# ---------------------------------
# Event loop
# ---------------------------------
nentries = tree.GetEntries()
print("Processing", nentries, "events")

for i in range(10000):

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

plt.hist(bias_wo_list, bins=np.arange(-3, 1, step=0.04), histtype='step', weights=np.ones_like(bias_wo_list), color=dark_blue,linewidth=1.5, label = "Enu had w/o pion mass")

# Create a matching line handle for legend
custom_lines.append(Line2D([0], [0], color=dark_blue, lw=2, linestyle='-'))
labels.append("Enu had w/o pion mass")

plt.hist(bias_with_list, bins=np.arange(-3, 1, step=0.04), histtype='step', weights=np.ones_like(bias_wo_list), color=dark_red,linewidth=1.5, label = "Enu had w/ pion mass")
custom_lines.append(Line2D([0], [0], color=dark_red, lw=2, linestyle='-'))
labels.append("Enu had w/ pion mass")
plt.legend()
plt.show()

fin.Close()

print("Done.")
