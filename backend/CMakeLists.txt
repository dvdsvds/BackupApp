cmake_minimum_required(VERSION 3.15)
project(BackupTool LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 REQUIRED)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include ${pybind11_INCLUDE_DIRS})

set(SOURCES
    backend.cpp
)

pybind11_add_module(backend MODULE ${SOURCES})

if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_link_libraries(backend PRIVATE stdc++fs)
endif()

set_target_properties(backend PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/gui
)
