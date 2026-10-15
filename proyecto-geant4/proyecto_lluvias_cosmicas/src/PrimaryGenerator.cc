#include "PrimaryGenerator.hh"

PrimaryGenerator::PrimaryGenerator() {
    fParticleGun = new G4ParticleGun(1);

    // Partícula primaria de origen cósmico (Protón de alta energía)
    G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();
    G4ParticleDefinition* particle = particleTable->FindParticle("proton");

    fParticleGun->SetParticleDefinition(particle);
    fParticleGun->SetParticleEnergy(10.0 * GeV); // Energía del rayo cósmico primario
    fParticleGun->SetParticleMomentumDirection(G4ThreeVector(0., 0., -1.)); // Apuntando hacia abajo
    fParticleGun->SetParticlePosition(G4ThreeVector(0.0 * m, 0.0 * m, 14.5 * km)); // En la parte superior de la atmósfera
}

PrimaryGenerator::~PrimaryGenerator() {
    delete fParticleGun;
}

void PrimaryGenerator::GeneratePrimaries(G4Event* anEvent) {
    fParticleGun->GeneratePrimaryVertex(anEvent);
}
