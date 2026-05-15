#include <pybind11/pybind11.h>
#include <pybind11/stl.h> 
#include "detection.hpp"
#include "jsonLoader.hpp"
#include "analyzer.hpp"

using namespace std;
namespace fs = std::filesystem;
namespace py = pybind11;

void start_analysis(const std::string& minecraft_dir) {
    fs::path DIR_DETECTIONS = fs::path(minecraft_dir) / "minescript" / "find" / "data" / "detections";
    
    if (!fs::exists(DIR_DETECTIONS)) 
        throw std::runtime_error("Detections directory does not exist: " + DIR_DETECTIONS.string());

    auto files = sorted_files_in_dir(DIR_DETECTIONS);
    if (files.empty()) {
        throw std::runtime_error("No detection files found in " + DIR_DETECTIONS.string());
    }

    fs::path detection_path = DIR_DETECTIONS / files.back();
        
    auto detections = loadDetections(detection_path.string());
    auto clusters = clustering(detections);
    analyzer(clusters, minecraft_dir);
}

PYBIND11_MODULE(FinderEngine_cpp, m){
    m.doc() = "C++ Finder Engine for Minecraft Detections";
    m.def("run", &start_analysis, py::arg("minecraft_dir"), "Runs full C++ clustering and analysis pipeline");
}
