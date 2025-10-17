cmake_minimum_required(VERSION 3.15)
project(BackupTool LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

set(SOURCES
    backend.cpp
    main.cpp
)

add_executable(backup ${SOURCES})

if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_link_libraries(backup stdc++fs)
endif()

set_target_properties(backup PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/build
)