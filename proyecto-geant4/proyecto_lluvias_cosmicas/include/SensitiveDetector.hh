#ifndef SENSITIVE_DETECTOR_HH
#define SENSITIVE_DETECTOR_HH

#include "G4VSensitiveDetector.hh"
#include "G4Step.hh"
#include "G4TouchableHistory.hh"

class SensitiveDetector : public G4VSensitiveDetector {
public:
    SensitiveDetector(G4String name);
    virtual ~SensitiveDetector();

    virtual G4bool ProcessHits(G4Step* aStep, G4TouchableHistory* ROhist) override;
};

#endif
