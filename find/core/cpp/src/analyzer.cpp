#include "analyzer.hpp"

using namespace std;
using json = nlohmann::json;
namespace fs = std::filesystem;

// Constants
const char* appdata = getenv("APPDATA");
fs::path DIR_FINDINGS = fs::path (appdata)/".minecraft"/"minescript"/"find"/"data"/"findings";

const int GROUP_RADIUS = 3;

const unordered_set<string> STRONG_BLOCKS = {
    "beacon", "enchanting_table", "ender_chest", 
    "nether_portal", "shulker_box", "barrel",
    "nether_wart", "soul_sand", "glowstone", 
    "redstone_wire", "redstone_block", "repeater", 
    "comparator", "dispenser", "dropper",
    "brewing_stand",
};


// Class functions
Finding& Finding::operator+=(const Finding& other){
    if (other.type != type){
        throw runtime_error("Types mismatch | block 1: " + other.type + " - block 2: " + type);
    }
    if (category != "strong_blocks" and other.category == "strong_blocks"){
        category = "strong_blocks";
    }
    for (const vector<Vec3>& c_coords: other.clusters_coords){
        clusters_coords.push_back(c_coords);
    }
    for (const Vec3& center: other.centers){
        centers.push_back(center);
    }
    total_size += other.total_size;

    return *this;
}


// Helper functions
Vec3 center_coord(const vector<Vec3>& coords){
    if (coords.empty()) return {0, 0, 0};

    int xs = 0, ys = 0, zs = 0;
    int n = coords.size();

    for (auto& c : coords){
        xs += c.x;
        ys += c.y;
        zs += c.z;
    }
    return {xs / n, ys / n, zs / n};
}


void neighbors(
    const Vec3& coord_main, 
    const unordered_set<Vec3>& coords, 
    unordered_set<Vec3>& coords_seen, 
    Cluster& cluster
){
    int x_main = coord_main.x, y_main = coord_main.y, z_main = coord_main.z;
    coords_seen.insert(coord_main);

    for (int dx = -GROUP_RADIUS; dx <= GROUP_RADIUS; dx++){
        for (int dy = -GROUP_RADIUS; dy <= GROUP_RADIUS; dy++){
            for (int dz = -GROUP_RADIUS; dz <= GROUP_RADIUS; dz++){

                if (dx == 0 and dy == 0 and dz == 0) continue;

                Vec3 coord_neighbor = {x_main + dx, y_main + dy, z_main + dz};

                if (coords.contains(coord_neighbor) and not coords_seen.contains(coord_neighbor)){
                    cluster.coords.push_back(coord_neighbor);
                    coords_seen.insert(coord_neighbor);
                    neighbors(coord_neighbor, coords, coords_seen, cluster);
                }
            }
        }
    }
}


vector<string> sorted_files_in_dir(const fs::path& directory){
    vector<string> files_timestamp;
    for (auto& file: fs::directory_iterator(DIR_FINDINGS)){
        files_timestamp.push_back(file.path().filename().string());
    }
    sort(files_timestamp.begin(), files_timestamp.end());
    return files_timestamp;
}


void toJson(const unordered_map<string, Finding>& blocks){
    json data = {
        {"strong_blocks", json::array()},
        {"grouped_blocks", json::array()}
    };

    for (auto& [block_type, block]: blocks){
        if (block.category == "strong_blocks"){
            data["strong_blocks"].push_back(block);
        }else{
            data["grouped_blocks"].push_back(block);
        }
    }

    chrono::time_point now = chrono::floor<chrono::seconds>(chrono::system_clock::now());
    string timestamp = format("{:%Y%m%d%H%M%S}", now);

    fs::create_directories(DIR_FINDINGS);
    fs::path file_path = DIR_FINDINGS / ("findings_" + timestamp + ".json");

    ofstream json_file(file_path);
    if (json_file.is_open()){
        json_file << data;
        json_file.close();
    }else{
        throw runtime_error("Cannot open file: " + file_path.string());
    }

    while (sorted_files_in_dir(DIR_FINDINGS).size() > 5){
        fs::path oldest_json_path = DIR_FINDINGS / sorted_files_in_dir(DIR_FINDINGS).back();
        if (fs::exists(oldest_json_path)){
            fs::remove(oldest_json_path);
            cout << "File: " << oldest_json_path << " was removed\n";
        }else{
            cout << "File path not found: " << oldest_json_path << "\n";
        }
    }
}


// Functions
vector<Cluster> 
clustering(const unordered_map<string, Detection>& detections){

    vector<Cluster> clusters;
    unordered_set<Vec3> coords_seen;

    for (const auto& [block_type, detection]: detections){
        
        for (const Vec3& coord : detection.coords){
            if (coords_seen.contains(coord)) continue;

            Cluster cluster;
            
            cluster.coords.push_back(coord);
            neighbors(coord, detection.coords, coords_seen, cluster);

            cluster.type = block_type;
            clusters.push_back(cluster);
        }
    }
    return clusters;
}


void analyzer(const vector<Cluster>& clusters){
    unordered_map<string, Finding> blocks_found;

    for (auto& cluster: clusters){
        Finding block;

        block.type = cluster.type;
        if (STRONG_BLOCKS.contains(block.type)) block.category = "strong_blocks";
        block.clusters_coords.push_back(cluster.coords);
        block.centers.push_back(center_coord(cluster.coords));
        
        for (auto& cluster: block.clusters_coords){
            block.total_size += cluster.size();
        }

        if (blocks_found.contains(block.type)){
            blocks_found[block.type] += block;
        }else{
            blocks_found[block.type] = block;
        }
    }
    toJson(blocks_found);
}




