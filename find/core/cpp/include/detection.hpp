#pragma once
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <tuple>
#include <nlohmann/json.hpp>

struct Vec3 {
    int x = 0, y = 0, z = 0;
    Vec3 operator+(const Vec3& other);
    Vec3 operator/(const int n);
    bool operator<(const Vec3& other) const;
    bool operator==(const Vec3& other) const;

    NLOHMANN_DEFINE_TYPE_INTRUSIVE(Vec3, x, y, z);
};

namespace std{
    template<>
    struct hash<Vec3>{
        std::size_t operator()(const Vec3& v) const noexcept{
            std::size_t h1 = std::hash<int>{}(v.x);
            std::size_t h2 = std::hash<int>{}(v.y);
            std::size_t h3 = std::hash<int>{}(v.z);
            return h1 ^ (h2 << 1) ^ (h3 << 2);
        }
    };
}

class Detection {
public:
    std::string type;
    std::unordered_set<Vec3> coords;
    std::unordered_map<std::string, std::string> info; 

    Detection(const std::string& t);
    void addCoord(int x, int y, int z);
};