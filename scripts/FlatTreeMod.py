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
from matplotlib.lines import Line2D

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


# ----------------------------------------
# Colour schemes
# ----------------------------------------
light_blue = '#56B4E9'
medium_blue = '#0072B2'
dark_blue = '#084594'
light_red = '#E69F00'
dark_red = '#D55E00'
light_green = '#009E73'
dark_green = '#007D4B'
vivid_purple = '#CC79A7'
bright_yellow = '#F0E442'

# ----------------------------------------
# Load OscProb shared library
# ----------------------------------------
import ROOT
ROOT.gSystem.Load('/home/jm721/Desktop/PhDWork/FirstYear/Minoo_Project/UCM_codes/precomputed_tables/Graphs/Full_EDRMF_RNG_check/IOP_paper/OscProb/build/lib64/libOscProb.so')

# ----------------------------------------
# Create global PMNS_Fast object
# ----------------------------------------
pmns = ROOT.OscProb.PMNS_Fast()

# ----------------------------------------
# Set oscillation parameters (PDG-ish)
# ----------------------------------------
theta12 = 0.584 #7
theta13 = 0.15 #49
theta23 = 0.859 #0.785
deltaCP = 3.4

dm21 = 7.42e-5 #53e-5
dm32 = 2.44e-3 #50e-3

pmns.SetMix(theta12, theta23, theta13, deltaCP)
pmns.SetDeltaMsqrs(dm21, dm32)

# ----------------------------------------
# Set T2K baseline (km)
# ----------------------------------------
L = 295.0
pmns.SetPath(L, 2.8)   # 2.8 g/cm3 density for Earth

# ----------------------------------------
# Arrays for custom legend lines
# ----------------------------------------

custom_lines = []
labels = []

# ----------------------------------------
# Functions to oscillate given energy
# input: neutrino energy
# output: oscillation probability
# ----------------------------------------
# Flavour codes:
# 0: nue
# 1: numu
# 2: nutau
# ----------------------------------------

def OscProb_mumu(E_in: float) -> float:
    return pmns.Prob(1, 1, E_in, L)  # νμ → νμ

def OscProb_mue(E_in: float) -> float:
    return pmns.Prob(1, 0, E_in, L)  # νμ → νe


def plot_branch(ax_main, filename: str, kinematic: str, bin_width: float, label: str, color: str):
    infile = up.open(filename)
    TBranch_kinematic = infile["FlatTree_VARS;1"][kinematic].array()
    XSec_scale_factor = max(infile["FlatTree_VARS;1"]["fScaleFactor"].array())


    bins = np.arange(0, 10, step=bin_width)
    weights = XSec_scale_factor * np.ones_like(TBranch_kinematic) / bin_width

    counts, edges = np.histogram(TBranch_kinematic, bins=bins, weights=weights)
    sumw2, _      = np.histogram(TBranch_kinematic, bins=bins, weights=weights**2)

    errors  = np.sqrt(sumw2)
    centers = 0.5 * (edges[1:] + edges[:-1])
    ax_main.hist(TBranch_kinematic, bins=np.arange(0, 10, step=bin_width), histtype='step', weights=XSec_scale_factor*np.ones_like(TBranch_kinematic)/(bin_width), color=color,linewidth=1.2, label = label)
    # counts, edges  = np.histogram(TBranch_kinematic, bins=(np.arange(0, 10, step=bin_width)), weights=(XSec_scale_factor*np.ones_like(TBranch_kinematic)/(bin_width)))
    # errors = np.sqrt(np.histogram(TBranch_kinematic, bins=(np.arange(0, 10, step=bin_width)), weights=(XSec_scale_factor*np.ones_like(TBranch_kinematic)/(bin_width))**2)[0])
    # centers = 0.5 * (edges[1:] + edges[:-1])
    ax_main.errorbar(centers, counts, yerr=errors, color=color, linestyle='')
    ax_main.legend(loc = "upper right")

    # Create a matching line handle for legend
    custom_lines.append(Line2D([0], [0], color=color, lw=2))
    labels.append(label)
    return


def plot_flattree_diff_xsec(filename: str, label: str, bin_edges, outfile_name: str):

    infile = up.open(filename)
    Elep = 1000*infile["FlatTree_VARS;1"]["ELep"].array()

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













