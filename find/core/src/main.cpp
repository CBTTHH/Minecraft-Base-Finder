#include "detection.hpp"
#include "jsonLoader.hpp"
#include "analyzer.hpp"
#include <iostream> 
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

void run_analysis() {
    const char* appdata = getenv("APPDATA");
    if (not appdata) {
        cerr << "Error: APPDATA not found" << endl;
        return;
    }

    fs::path DIR_DETECTIONS = fs::path(appdata) / ".minecraft" / "minescript" / "find" / "data" / "detections";
    
    if (fs::exists(DIR_DETECTIONS)) {
        fs::path detection_path = DIR_DETECTIONS / sorted_files_in_dir(DIR_DETECTIONS).back();
        
        // Loading detections
        unordered_map<string, Detection> detections = loadDetections(detection_path.string());

        // Clustering data
        vector<Cluster> clusters = clustering(detections);

        // Creating json file
        analyzer(clusters);
        
        cout << "Analysis complete. Output written to findings folder." << endl;
    } else {
        cerr << "Detections directory not found at: " << DIR_DETECTIONS << endl;
    }
}

int main() {
    run_analysis();
    return 0;
}