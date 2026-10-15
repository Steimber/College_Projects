cmake_minimum_required(VERSION 3.16)
project(proyecto_lluvias_cosmicas)

find_package(Geant4 REQUIRED ui_all vis_all)
include(${Geant4_USE_FILE})

include_directories(${PROJECT_SOURCE_DIR}/include)

file(GLOB SOURCES 
    ${PROJECT_SOURCE_DIR}/sim.cc 
    ${PROJECT_SOURCE_DIR}/src/*.cc
)

add_executable(sim ${SOURCES})
target_link_libraries(sim ${Geant4_LIBRARIES})
