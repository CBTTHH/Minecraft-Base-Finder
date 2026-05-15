cmake_minimum_required(VERSION 3.12)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

project(FinderEngine LANGUAGES CXX)

if(MSVC)
    add_compile_options(/D_CRT_SECURE_NO_WARNINGS)
    set(variables 
        CMAKE_CXX_FLAGS_RELEASE 
        CMAKE_CXX_FLAGS_DEBUG
    )
    foreach(variable ${variables})
        if(${variable} MATCHES "/MD")
            string(REGEX REPLACE "/MD" "/MT" ${variable} "${${variable}}")
        endif()
    endforeach()
endif()

# Dependencies
add_subdirectory(external/nlohmann_json)
add_subdirectory(external/pybind11)

# --- TARGET 1: The Executable ---
add_executable(FinderEngine_exe
    core/src/main.cpp
    core/src/detection.cpp
    core/src/jsonLoader.cpp
    core/src/analyzer.cpp
)
target_include_directories(FinderEngine_exe PRIVATE core/include)
target_link_libraries(FinderEngine_exe PRIVATE nlohmann_json::nlohmann_json)

# --- TARGET 2: The Python Module ---
pybind11_add_module(FinderEngine_cpp 
    core/src/bindings.cpp
    core/src/detection.cpp
    core/src/jsonLoader.cpp
    core/src/analyzer.cpp
)
target_include_directories(FinderEngine_cpp PRIVATE core/include)
target_link_libraries(FinderEngine_cpp PRIVATE 
    nlohmann_json::nlohmann_json 
    pybind11::pybind11
)

# Compiler-Specific Linker Logic
if(NOT MSVC)
    target_link_libraries(FinderEngine_exe PRIVATE stdc++fs)
    target_link_libraries(FinderEngine_cpp PRIVATE stdc++fs)
    set_target_properties(FinderEngine_cpp PROPERTIES 
        LINK_FLAGS "-static -static-libgcc -static-libstdc++"
    )
endif()