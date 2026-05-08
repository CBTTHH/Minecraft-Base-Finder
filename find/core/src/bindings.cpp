#include <pybind11/pybind11.h>
#include <pybind11/stl.h> 
#include "detection.hpp"
#include "jsonLoader.hpp"
#include "analyzer.hpp"

using namespace std;
namespace fs = std::filesystem;
namespace py = pybind11;

void start_analysis() {
    const char* appdata = getenv("APPDATA");
    fs::path DIR_DETECTIONS = fs::path(appdata) / ".minecraft" / "minescript" / "find" / "data" / "detections";
    fs::path detection_path = DIR_DETECTIONS / sorted_files_in_dir(DIR_DETECTIONS).back();
        
    auto detections = loadDetections(detection_path.string());
    auto clusters = clustering(detections);
    analyzer(clusters);
}

PYBIND11_MODULE(FinderEngine_cpp, m){
    m.doc() = "C++ Finder Engine for Minecraft Detections";
    m.def("run", &start_analysis, "Runs full C++ clustering and analysis pipeline");
}
