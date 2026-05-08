#include "detection.hpp"

using namespace std;

Vec3 Vec3::operator+(const Vec3& other){
    return {x + other.x, y + other.y, z + other.z};
}

Vec3 Vec3::operator/(const int n){
    return {x /= n, y /= n, z /= n};
}

bool Vec3::operator<(const Vec3& other) const{
    return tie(x, y, z) < tie(other.x, other.y, other.z);
}

bool Vec3::operator==(const Vec3& other) const{
        return x == other.x and y == other.y and z == other.z;
}

Detection::Detection(const string& t) : type(t){}

void Detection::addCoord(int x, int y, int z) {
    coords.insert({x, y, z});
}
