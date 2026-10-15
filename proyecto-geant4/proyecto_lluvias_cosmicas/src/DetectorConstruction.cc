#include "DetectorConstruction.hh"
#include "SensitiveDetector.hh"
#include "G4SDManager.hh"
#include "G4VisAttributes.hh"
#include "G4Colour.hh"

DetectorConstruction::DetectorConstruction() : logicGroundDetector(nullptr) {}
DetectorConstruction::~DetectorConstruction() {}

G4VPhysicalVolume* DetectorConstruction::Construct() {
    G4NistManager* nist = G4NistManager::Instance();

    // Materiales
    G4Material* airMaterial = nist->FindOrBuildMaterial("G4_AIR");
    G4Material* detectorMaterial = nist->FindOrBuildMaterial("G4_Si");

    // 1. Volumen Mundo (Más grande para acomodar todas las capas)
    G4double worldSizeXY = 5.0 * km;
    G4double worldSizeZ = 20.0 * km; // 40 km de alto en total

    G4Box* solidWorld = new G4Box("World", worldSizeXY, worldSizeXY, worldSizeZ);
    G4LogicalVolume* logicWorld = new G4LogicalVolume(solidWorld, airMaterial, "World");
    G4VPhysicalVolume* physWorld = new G4PVPlacement(0, G4ThreeVector(), logicWorld, "World", 0, false, 0);

    // 2. Capas de la Atmósfera (Representando distintas alturas)
    G4double layerThickness = 5.0 * km; // Cada capa medirá 10 km de alto (la mitad es 5)
    G4Box* solidLayer = new G4Box("AtmoLayer", worldSizeXY, worldSizeXY, layerThickness);

    // - Capa Alta (10 km a 20 km)
    G4LogicalVolume* logicLayerHigh = new G4LogicalVolume(solidLayer, airMaterial, "LayerHigh");
    new G4PVPlacement(0, G4ThreeVector(0, 0, 10.0 * km), logicLayerHigh, "LayerHigh", logicWorld, false, 0);

    // - Capa Media (0 km a 10 km)
    G4LogicalVolume* logicLayerMid = new G4LogicalVolume(solidLayer, airMaterial, "LayerMid");
    new G4PVPlacement(0, G4ThreeVector(0, 0, 0.0 * km), logicLayerMid, "LayerMid", logicWorld, false, 0);

    // - Capa Baja (Suelo hasta 0 km)
    G4LogicalVolume* logicLayerLow = new G4LogicalVolume(solidLayer, airMaterial, "LayerLow");
    new G4PVPlacement(0, G4ThreeVector(0, 0, -10.0 * km), logicLayerLow, "LayerLow", logicWorld, false, 0);

    // 3. Detector a Nivel del Suelo
    G4double detectorSizeXY = 100.0 * m;
    G4double detectorThickness = 0.5 * m;

    G4Box* solidGroundDetector = new G4Box("GroundDetector", detectorSizeXY, detectorSizeXY, detectorThickness);
    logicGroundDetector = new G4LogicalVolume(solidGroundDetector, detectorMaterial, "GroundDetector");
    new G4PVPlacement(0, G4ThreeVector(0, 0, -15.1 * km), logicGroundDetector, "GroundDetector", logicWorld, false, 0);

    // 4. Visualización
    logicWorld->SetVisAttributes(G4VisAttributes::GetInvisible()); // Ocultar los bordes del mundo exterior

    G4VisAttributes* visHigh = new G4VisAttributes(G4Colour(0.0, 0.2, 0.8, 0.1)); // Azul suave
    logicLayerHigh->SetVisAttributes(visHigh);

    G4VisAttributes* visMid = new G4VisAttributes(G4Colour(0.0, 0.4, 0.8, 0.2)); // Azul intermedio
    logicLayerMid->SetVisAttributes(visMid);

    G4VisAttributes* visLow = new G4VisAttributes(G4Colour(0.0, 0.6, 0.8, 0.3)); // Azul denso
    logicLayerLow->SetVisAttributes(visLow);

    G4VisAttributes* detectorVis = new G4VisAttributes(G4Colour(1.0, 0.0, 0.0, 0.9)); // Rojo
    logicGroundDetector->SetVisAttributes(detectorVis);

    return physWorld;
}

void DetectorConstruction::ConstructSDandField() {
    SensitiveDetector* sensDet = new SensitiveDetector("GroundDetectorSD");
    G4SDManager::GetSDMpointer()->AddNewDetector(sensDet);
    SetSensitiveDetector(logicGroundDetector, sensDet);
}
