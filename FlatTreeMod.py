try:
    import uproot
except ImportError:
    Err("Uproot not installed. Cannot perform analysis.")

import uproot as up
import warnings

try:
    import matplotlib.pyplot as plt
except ImportError:
    Err("Matplotlib not installed. Cannot create plots.")

import numpy as np
from matplotlib import gridspec
plt.style.use(["science", "notebook"])#, "grid"])
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"]})

def Log(string):
    print("\033[94m[LOG]\033[0m :: ", string)

def Warn(string):
    print("\033[93m[WARNING]\033[0m :: ", string)

def Err(string):
    print("\033[91m[ERROR]\033[0m :: ", string)

def Print(string):
    print("\033[92m[OUTPUT]\033[0m :: ", string)





def plot_flattree_diff_xsec(filename: str, label: str, bin_edges, outfile_name: str):

    outfile_name = outfile_name + "_pred.csv"

    infile = up.open(filename)
    mode = infile["FlatTree_VARS;1"]["cc"].array()
    Elep = 1000*infile["FlatTree_VARS;1"]["ELep"].array()

    Enu = 235.5
    Mp = 938.2721
    Mmu = 105.6584

    Ep, pdg = [], []
    if("noFSI" in filename):
        Ep = 1000*infile["FlatTree_VARS;1"]["E_vert"].array()
        pdg = infile["FlatTree_VARS;1"]["pdg_vert"].array()

    else:
        Ep = 1000*infile["FlatTree_VARS;1"]["E"].array()
        pdg = infile["FlatTree_VARS;1"]["pdg"].array()

    
    Emiss = []
    Evis  = []
    # NucDeEx_counter = 0
    # Proton_counter = 0
    # Neutron_counter = 0
    for index, val in enumerate(mode):
        T_mu = Elep[index] - Mmu # Classical E_tot = T + M
        if(mode[index] == 1):
            sum_Tp = 0
            sum_Gamma = 0
            # if(2212 not in pdg[index]):
            #     Neutron_counter += 1
            # else:
            #     Proton_counter += 1
            for particle in range(0, len(pdg[index])):
                if(pdg[index][particle] == 2212):
                    Tp = Ep[index][particle] - Mp # Classical
                    sum_Tp += Tp
                if(pdg[index][particle] == 22):
                    E_Gamma = Ep[index][particle]
                    if(E_Gamma > 0):
                        sum_Gamma += E_Gamma
                        # NucDeEx_counter += 1

            if(sum_Gamma != 0):
                Emiss_val = Enu - Elep[index] - sum_Tp - sum_Gamma
            else:
                Emiss_val = Enu - Elep[index] - sum_Tp
            Evis_val = T_mu + sum_Tp

            Evis.append(Evis_val)
            Emiss.append(Emiss_val)

    # Compute histogram and integral
    counts, _ = np.histogram(Emiss, bins=bin_edges)
    bin_widths = np.diff(bin_edges)
    integral = np.sum(counts * bin_widths)

    # compute bin centres
    edges = np.array(Evis_bins)
    centres = 0.5 * (edges[:-1] + edges[1:])

    ## Plotting area

    return













