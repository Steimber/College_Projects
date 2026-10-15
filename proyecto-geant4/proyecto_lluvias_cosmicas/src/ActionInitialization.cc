#include "ActionInitialization.hh"
#include "PrimaryGenerator.hh"

ActionInitialization::ActionInitialization() : G4VUserActionInitialization() {}

ActionInitialization::~ActionInitialization() {}

void ActionInitialization::BuildForMaster() const {}

void ActionInitialization::Build() const {
    SetUserAction(new PrimaryGenerator());
}
