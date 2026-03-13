#include <iostream>
#include "detection.hpp"
#include "jsonLoader.hpp"
#include "analyzer.hpp"

using namespace std;
namespace fs = std::filesystem;

int main(){
    const char* appdata = getenv("APPDATA");
    fs::path DIR_DETECTIONS = fs::path (appdata)/".minecraft"/"minescript"/"find"/"data"/"detections";
    string path = sorted_files_in_dir(DIR_DETECTIONS).back();

    // Loading detections
    unordered_map<string, Detection> detections = loadDetections(path);

    // Clustering data
    vector<Cluster> clusters = clustering(detections);

    // Creating json file
    analyzer(clusters); 

    return 0;
}