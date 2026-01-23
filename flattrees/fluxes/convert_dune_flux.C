#include <TFile.h>
#include <TH1.h>
#include <iostream>

void convert_flux_perGeV()
{
    // ----------------------------
    // Input / output files
    // ----------------------------
    TFile *infile  = TFile::Open("Dune-numu-flux.root", "READ");
    TFile *outfile = TFile::Open("output_dune_flux.root", "RECREATE");

    if (!infile || infile->IsZombie()) {
        std::cerr << "Error opening input file!" << std::endl;
        return;
    }

    // ----------------------------
    // Get the histogram
    // ----------------------------
    TH1 *h = (TH1*) infile->Get("numu_flux");   // <-- change name if needed

    if (!h) {
        std::cerr << "Histogram not found!" << std::endl;
        return;
    }

    // Clone so we don’t overwrite the original
    TH1 *h_new = (TH1*) h->Clone("numu_flux");
    h_new->SetTitle("Flux per GeV");

    h_new->Scale(1.0, "width");
    // ----------------------------
    // Write output
    // ----------------------------
    outfile->cd();
    h_new->Write();

    outfile->Close();
    infile->Close();

    std::cout << "Saved flux per GeV to output_flux_perGeV.root" << std::endl;
}
