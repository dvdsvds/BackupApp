cmake_minimum_required(VERSION 3.15)
project(BackupTool LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(pybind11_DIR "/home/kundr/miniconda3/envs/backup/lib/python3.12/site-packages/pybind11/share/cmake/pybind11")

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

message(STATUS "✅ pybind11 include dirs: ${pybind11_INCLUDE_DIRS}")

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${pybind11_INCLUDE_DIRS}
)

set(SOURCES
    backend.cpp
)

pybind11_add_module(backend MODULE ${SOURCES})
target_link_libraries(backend PRIVATE pybind11::module)

if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_link_libraries(backend PRIVATE stdc++fs)
endif()

get_filename_component(ROOT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/.." ABSOLUTE)

set(GUI_DIR "${ROOT_DIR}/gui/ui/pyd")

file(MAKE_DIRECTORY "${GUI_DIR}")

set_target_properties(backend PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${GUI_DIR}")

message(STATUS "Backend module will be placed in ${GUI_DIR}")