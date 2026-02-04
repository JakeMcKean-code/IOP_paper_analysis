from FlatTreeMod import *
ROOT.gROOT.SetBatch(True)

Mneutron = 939.565 # MeV

def plot_neutron_energy(ax, filename, nEvents):
    # ---------------------------------
    # Open input file and tree
    # ---------------------------------
    fin = ROOT.TFile.Open(filename)
    tree = fin.Get("FlatTree_VARS")

    neutron_energy_list = []
    # ---------------------------------
    # Event loop
    # ---------------------------------
    nentries = tree.GetEntries()
    nevs = 0
    if(nEvents == -1):
        nevs = nentries
    else:
        nevs = nEvents
    print("Processing", nevs, "events")

    for i in range(nevs):
        tree.GetEntry(i)

        nfsp     = tree.nfsp

        E  = tree.E
        pdg = tree.pdg

        # -------------------------
        # Lepton energy
        # -------------------------
        neutron_energy   = 0

        # Loop over final state particles
        for j in range(nfsp):

            apdg = abs(int(pdg[j]))
            Ej   = float(E[j])*1000


            # -------------------------
            # Get neutron
            # -------------------------
            if apdg == 2112: # Remove contribution > 0
                neutron_energy += Ej

        # -------------------------
        # Fill
        # -------------------------
        neutron_energy_list.append(neutron_energy)

    # ---------------------------------
    # Write output
    # ---------------------------------
    neutron_energy_list = np.array(neutron_energy_list)
    print(neutron_energy_list)
    if("noFSI" in filename):
        ax.hist(neutron_energy_list, bins=np.arange(500, 4000, step=20), histtype='step', weights=np.ones_like(neutron_energy_list), color=dark_red,linewidth=1.5, label = "Neutron energy noFSI")
        custom_lines.append(Line2D([0], [0], color=dark_red, lw=2, linestyle='-'))
        labels.append("Neutron energy noFSI")
    else:
        ax.hist(neutron_energy_list, bins=np.arange(500, 4000, step=20), histtype='step', weights=np.ones_like(neutron_energy_list), color=dark_blue,linewidth=1.5, label = "Neutron energy FSI")
        custom_lines.append(Line2D([0], [0], color=dark_red, lw=2, linestyle='-'))
        labels.append("Neutron energy FSI") 
        
    fin.Close()
    print("Done.")


fig, ax = plt.subplots()
_events = 1000000
# plot_neutron_energy(ax=ax, filename="../../noFSI/NuWro_Ar40_noFSI_numu.flat.root", nEvents=_events)
# plot_neutron_energy(ax=ax, filename="../../FSI/NuWro_Ar40_numu.flat.root", nEvents=_events)

plot_neutron_energy(ax=ax, filename="../../noFSI/NuWro_Ar40_noFSI_numubar.flat.root", nEvents=_events)
plot_neutron_energy(ax=ax, filename="../../FSI/NuWro_Ar40_numubar.flat.root", nEvents=_events)

plt.vlines(x=Mneutron, ymin=0, ymax = ax.get_ylim()[1], color='black', linestyles='--')
plt.vlines(x=2*Mneutron, ymin=0, ymax = ax.get_ylim()[1], color='black', linestyles='--')
plt.vlines(x=3*Mneutron, ymin=0, ymax = ax.get_ylim()[1], color='black', linestyles='--')

plt.ylim(0, ax.get_ylim()[1])
plt.legend(loc='best', fontsize=15)
plt.show()