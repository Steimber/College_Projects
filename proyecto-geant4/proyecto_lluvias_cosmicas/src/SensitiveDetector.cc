#include "SensitiveDetector.hh"
#include "G4Track.hh"
#include "G4Step.hh"
#include "G4SystemOfUnits.hh"
#include "G4ios.hh"

SensitiveDetector::SensitiveDetector(G4String name) : G4VSensitiveDetector(name) {}

SensitiveDetector::~SensitiveDetector() {}

G4bool SensitiveDetector::ProcessHits(G4Step* aStep, G4TouchableHistory*) {
    G4Track* track = aStep->GetTrack();

    // Registrar solo el primer paso de la partícula en el detector
    if (aStep->IsFirstStepInVolume()) {
        G4String particleName = track->GetDefinition()->GetParticleName();
        G4double kinEnergy = track->GetKineticEnergy();
        G4double edep = aStep->GetTotalEnergyDeposit();

        G4cout << "[Detector Nivel Suelo] Particula: " << particleName 
               << " | Energia Cinetica: " << kinEnergy / MeV << " MeV"
               << " | Energia Depositada: " << edep / MeV << " MeV" << G4endl;
    }

    return true;
}
