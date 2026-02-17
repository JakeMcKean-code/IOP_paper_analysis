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
    fScaleFactor = 0
    if(nEvents == -1):
        nevs = nentries
    else:
        nevs = nEvents

    for i in range(nevs):
        tree.GetEntry(i)
        bad_event = False
        nfsp     = tree.nfsp

        E  = tree.E
        pdg = tree.pdg
        Enu = tree.Enu_true
        ELep = tree.ELep
        q0 = (Enu - ELep)*1000
        _fscalefactor = tree.fScaleFactor
        if(_fscalefactor > fScaleFactor):
            fScaleFactor = _fscalefactor
        # -------------------------
        # neutron kinetic energy
        # -------------------------
        neutron_KE   = 0
        # Loop over final state particles
        for j in range(nfsp):

            apdg = abs(int(pdg[j]))
            Ej   = float(E[j])*1000

            if(apdg>3000):
                bad_event = True
                continue
            # -------------------------
            # Get neutron
            # -------------------------
            if apdg == 2112: 
                neutron_KE += (Ej - Mneutron) # T_neutron

        # -------------------------
        # Fill
        # -------------------------
        if(bad_event == False):
            if(neutron_KE != 0):
                neutron_energy_list.append(neutron_KE/q0)
        else:
            continue
    # ---------------------------------
    # Write output
    # ---------------------------------
    neutron_energy_list = np.array(neutron_energy_list)
    bin_width = 0.01
    bins = np.arange(0, 1, step=bin_width)
    weights = fScaleFactor*np.ones_like(neutron_energy_list)/bin_width
    print(neutron_energy_list)
    if("noFSI" in filename):
        ax.hist(neutron_energy_list, bins=bins, histtype='step', weights=weights, color=dark_red,linewidth=1.5, label = "noFSI")
        custom_lines.append(Line2D([0], [0], color=dark_red, lw=2, linestyle='-'))
        labels.append("Neutron energy noFSI")
    else:
        ax.hist(neutron_energy_list, bins=bins, histtype='step', weights=weights, color=dark_blue,linewidth=1.5, label = "FSI")
        custom_lines.append(Line2D([0], [0], color=dark_red, lw=2, linestyle='-'))
        labels.append("Neutron energy FSI") 
        
    fin.Close()
    Print(f"Done: {filename}")


_events = -1

fig2, ax2 = plt.subplots()
# plot_neutron_energy(ax=ax2, filename="../../noFSI/NuWro_Ar40_noFSI_numu.flat.root", nEvents=_events)
# plot_neutron_energy(ax=ax2, filename="../../FSI/NuWro_Ar40_numu.flat.root", nEvents=_events)
# ax2.set_xlabel(r"$\sum T_{n}/q_{0}$")
# ax2.set_ylabel(r"$\text{d}\sigma/(\text{d} \sum T_{n}/q_{0})$ [cm$^{2}$/nucleon MeV]")
# ax2.set_ylim(0, ax2.get_ylim()[1])
# ax2.legend(loc='best', fontsize=15)
# plt.savefig("Fig5_plots/Fig5_DUNE_EnergyFromNeutrons_numu.pdf")


ax2.clear()
plot_neutron_energy(ax=ax2, filename="../../noFSI/NuWro_Ar40_noFSI_numubar.flat.root", nEvents=_events)
plot_neutron_energy(ax=ax2, filename="../../FSI/NuWro_Ar40_numubar.flat.root", nEvents=_events)
ax2.set_xlabel(r"$\sum T_{n}/q_{0}$")
ax2.set_ylabel(r"$\text{d}\sigma/(\text{d} \sum T_{n}/q_{0})$ [cm$^{2}$/nucleon MeV]")
ax2.set_ylim(0, ax2.get_ylim()[1])
ax2.legend(loc='best', fontsize=15)
plt.savefig("Fig5_plots/Fig5_DUNE_EnergyFromNeutrons_numubar.pdf")
