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
theta12 = 0.583
theta13 = 0.149
theta23 = 0.857
deltaCP = 3.44

dm21 = 7.41e-5
dm32 = 2.437e-3

pmns.SetMix(theta12, theta23, theta13, deltaCP)
pmns.SetDeltaMsqrs(dm21, dm32)


L = 295.0
pmns.SetPath(L, 2.8)   # 2.8 g/cm3 density for Earth

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


# ----------------------------------------
# Plot standard probability plots
# for numu->numu and numu->nue
# ----------------------------------------
def StandardOscPlots():
    E = np.linspace(200,3200, 1000)
    mumu_prob = np.array([pmns.Prob(1, 1, Ei/1000.0, L) for Ei in E])
    mue_prob = np.array([pmns.Prob(1, 0, Ei/1000.0, L) for Ei in E])
    plt.plot(E, mumu_prob, color = dark_red, label = r"$\nu_{\mu} \rightarrow \nu_{\mu}$")
    plt.plot(E, mue_prob, color = dark_blue, label = r"$\nu_{\mu} \rightarrow \nu_{e}$")

    # ----------------------------------------
    # Plot of flat histogram reweighted to
    # oscillation probabilities
    # ----------------------------------------
    # E_edges   = np.linspace(0, 3000, 201)
    # E_centers = 0.5 * (E_edges[1:] + E_edges[:-1])
    # mumu_prob = np.array([pmns.Prob(1, 1, Ei/1000.0, L) for Ei in E_centers])
    # plt.hist(E_centers,
    #          bins=E_edges,
    #          weights=mumu_prob,
    #          histtype="step",
    #          color=vivid_purple,
    #          linewidth=1.5,
    #          label=r"Flat spectrum weighted by $P_{\mu\mu}$")

    plt.xlabel(r"Neutrino energy, $E_{\nu}$ [MeV]")
    plt.ylabel("Oscillation probability")
    plt.title(r"Baseline $L = 295$ [km], Earth density $\rho = 2.8$ [g$/$cm$^{3}$]")
    plt.legend(loc='best')
    plt.xlim(200, 3200)
    plt.show()

# ----------------------------------------
# Plot numu->nue for different dCP values
# ----------------------------------------
def NuedCPshift(ax: plt.axes, dCP: float, convert_to_rad: bool, color: str, NOorIO: bool):
    if(convert_to_rad == True):
        dCP = dCP * np.pi/180.0
    pmns.SetMix(theta12, theta23, theta13, dCP)

    linestyle = '-'
    if(NOorIO == False):
        linestyle = '--'
        pmns.SetIsNuBar(True)

    E = np.linspace(175,3175, 1000)
    mue_prob = np.array([pmns.Prob(1, 0, Ei/1000.0, L) for Ei in E])
    legend_string = r"$\nu_{\mu} \rightarrow \nu_{e}$"
    dCP_string    = r"$\delta_{CP}$ = " + f"{dCP:.2f}"
    ax.plot(E, mue_prob, color = color, label = f"{legend_string} for {dCP_string}", linestyle=linestyle)
    ax.legend(loc='best')
    ax.set_xlim(175, 3175)
    ax.set_ylim(bottom=0, top = 0.1)
    plt.xlabel(r"Neutrino energy, $E_{\nu}$ [MeV]")
    plt.ylabel("Oscillation probability")
    plt.title(r"Baseline $L = 295$ [km], Earth density $\rho = 2.8$ [g$/$cm$^{3}$]")

fig, ax = plt.subplots()
NuedCPshift(ax, 0, True, 'black', True)
NuedCPshift(ax, 270, True, dark_blue, True)
NuedCPshift(ax, 0, True, 'black', False)
NuedCPshift(ax, 270, True, dark_blue, False)
plt.savefig("Osc_Prob_plot.pdf")
plt.show()

