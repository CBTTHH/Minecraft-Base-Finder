cmake_minimum_required(VERSION 3.12)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_compile_definitions(_SILENCE_CXX17_CODECVT_FACETS_DEPRECATION_WARNING) 

project(FinderEngine LANGUAGES CXX)


add_subdirectory(external/nlohmann_json)
add_subdirectory(external/pybind11)


add_executable(
    FinderEngine
    core/src/detection.cpp
    core/src/jsonLoader.cpp
    core/src/analyzer.cpp
    core/src/main.cpp
)

target_include_directories(FinderEngine PRIVATE core/include)

target_link_libraries(FinderEngine PRIVATE 
    nlohmann_json::nlohmann_json
    stdc++fs
)


pybind11_add_module(FinderEngine_cpp 
    core/src/main.cpp
    core/src/detection.cpp
    core/src/jsonLoader.cpp
    core/src/analyzer.cpp
    core/src/bindings.cpp
)

target_include_directories(FinderEngine_cpp PRIVATE core/include)

target_link_libraries(FinderEngine_cpp PRIVATE 
    nlohmann_json::nlohmann_json
)
