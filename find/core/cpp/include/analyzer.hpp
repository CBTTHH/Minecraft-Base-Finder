#pragma once

#include <iostream>
#include <string>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <fstream>
#include <filesystem>
#include <chrono>
#include <format>
#include <cstdlib>
#include <algorithm>

#include "detection.hpp"
#include "jsonLoader.hpp"

struct Cluster{
    std::string type;
    std::vector<Vec3> coords;
};

struct Finding{
    std::string type = "None";
    std::string category = "grouped_blocks";
    std::vector<std::vector<Vec3>> clusters_coords;
    std::vector<Vec3> centers;
    unsigned int total_size = 0;

    Finding& operator+=(const Finding& other);

    NLOHMANN_DEFINE_TYPE_INTRUSIVE(Finding, type, category, clusters_coords, centers, total_size);
};

// Helper functions
Vec3 center_coord(const std::vector<Vec3>& coords);

void neighbors(
    const Vec3& coord_main, 
    const std::unordered_set<Vec3>& coords, 
    std::unordered_set<Vec3>& coords_seen, 
    Cluster& cluster
);

std::vector<std::string> sorted_files_in_dir(const std::filesystem::path& directory);

void toJson(const std::unordered_map<std::string, Finding>& blocks);


// Functions
std::vector<Cluster> 
clustering(const std::unordered_map<std::string, Detection>& detections);

void analyzer(const std::vector<Cluster>& clusters);

