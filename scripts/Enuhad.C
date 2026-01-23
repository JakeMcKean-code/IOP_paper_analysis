#include <TFile.h>
#include <TTree.h>
#include <TH1D.h>
#include <TCanvas.h>
#include <cmath>
#include <iostream>

void compute_enuhad_variants() {

    // -----------------------------
    // Open file and tree
    // -----------------------------
    TFile *file = new TFile("../flattrees/nuwro/NuWro_Ar40_test.flat.root", "READ");
    TTree *tree = (TTree*)file->Get("FlatTree_VARS");

    TFile *fout = new TFile("Fig1_SF_Dune_EnuReco.root", "RECREATE");
    fout->cd();


    // -----------------------------
    // Branch variables
    // -----------------------------
    const int nmax = 10000;

    float E[nmax];
    float px[nmax];
    float py[nmax];
    float pz[nmax];
    int   pdg[nmax];

    float ELep;
    float Enu_true;
    int   nfsp;

    tree->SetBranchAddress("E", &E);
    tree->SetBranchAddress("px", &px);
    tree->SetBranchAddress("py", &py);
    tree->SetBranchAddress("pz", &pz);
    tree->SetBranchAddress("pdg", &pdg);

    tree->SetBranchAddress("ELep", &ELep);
    tree->SetBranchAddress("Enu_true", &Enu_true);
    tree->SetBranchAddress("nfsp", &nfsp);

    // -----------------------------
    // Histograms
    // -----------------------------
    TH1D *h_bias_wo = new TH1D("h_bias_wo",
    "No pion mass subtraction; (E_{vis}-E_{true}) [GeV];Events",
    100, -3, 1);

    TH1D *h_bias_with = new TH1D("h_bias_with",
    "With pion masses; (E_{vis}-E_{true}) [GeV];Events",
    100, -3, 1);

    // -----------------------------
    // Event loop
    // -----------------------------
    Long64_t nentries = tree->GetEntries();

    for (Long64_t i = 0; i < nentries; ++i) {

    tree->GetEntry(i);

    // -------------------------
    // Definition 1:
    // enuhad_wo_pion_mass
    // -------------------------
    double enuhad_wo = ELep;

    // -------------------------
    // Definition 2:
    // enuhad_with_pion_masses
    // -------------------------
    double enuhad_with = ELep;

    for (int j = 0; j < nfsp; ++j) {

        int apdg = std::abs(pdg[j]);
        double Ej  = E[j];
        double pxj = px[j];
        double pyj = py[j];
        double pzj = pz[j];

        double p2 = pxj*pxj + pyj*pyj + pzj*pzj;

        // -------------------------
        // Common pieces
        // -------------------------

        // Term: heavy baryons (same in both)
        if (apdg > 2300 && apdg < 10000) {
        enuhad_wo   += Ej;
        enuhad_with += Ej;
        continue;
        }

        // -------------------------
        // Definition 1 logic
        // -------------------------

        // (abs(pdg)==11 || (abs(pdg)>17 && abs(pdg)<2000)) && (abs(pdg)!=211)
        if ( (apdg == 11 || (apdg > 17 && apdg < 2000)) && (apdg != 211) ) {
        enuhad_wo += Ej;
        }
        // (abs(pdg)==2212 || abs(pdg)==211) → KE
        else if (apdg == 2212 || apdg == 211) {
        double mass2 = Ej*Ej - p2;
        if (mass2 > 0) {
            double mass = std::sqrt(mass2);
            enuhad_wo += (Ej - mass);
        }
        }

        // -------------------------
        // Definition 2 logic
        // -------------------------

        // (abs(pdg)==11 || (abs(pdg)>17 && abs(pdg)<2000))  → full E (pions INCLUDED)
        if ( (apdg == 11 || (apdg > 17 && apdg < 2000)) ) {
        enuhad_with += Ej;
        }
        // (abs(pdg)==2212) → proton KE only
        else if (apdg == 2212) {
        double mass2 = Ej*Ej - p2;
        if (mass2 > 0) {
            double mass = std::sqrt(mass2);
            enuhad_with += (Ej - mass);
        }
        }
    }

    // -----------------------------
    // Fill bias histograms
    // -----------------------------
    double bias_wo   = enuhad_wo   - Enu_true;
    double bias_with = enuhad_with - Enu_true;

    h_bias_wo->Fill(bias_wo);
    h_bias_with->Fill(bias_with);
    }

    h_bias_with->Write();
    h_bias_wo->Write();

    fout->Write();
    fout->Close();
    delete fout;
    delete file;

std::cout << "Done. Processed " << nentries << " events." << std::endl;
}
