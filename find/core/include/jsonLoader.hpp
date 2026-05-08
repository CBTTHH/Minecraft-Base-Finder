#pragma once
#include "detection.hpp"

#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <set>
#include <fstream>
#include <nlohmann/json.hpp>

std::string variant_simplified(const std::string& b_variant);

std::unordered_map<std::string, Detection>
loadDetections(const std::string& path);
