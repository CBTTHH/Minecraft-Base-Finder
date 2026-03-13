cmake_minimum_required(VERSION 3.12)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(FinderEngine LANGUAGES CXX)

find_package(nlohmann_json REQUIRED)

add_executable(MyApp
    src/detection.cpp
    src/jsonLoader.cpp
    src/analyzer.cpp
    src/main.cpp
)

target_compile_features(MyApp PRIVATE cxx_std_20)

target_include_directories(MyApp PRIVATE include)
target_link_libraries(MyApp PRIVATE nlohmann_json::nlohmann_json)