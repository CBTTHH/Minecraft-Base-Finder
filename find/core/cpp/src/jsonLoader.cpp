#include "jsonLoader.hpp"

using json = nlohmann::json;
using namespace std;


unordered_set<string> blocks_variants = {
    "oak_shelf", "spruce_shelf", "birch_shelf", "jungle_shelf",
    "acacia_shelf", "dark_oak_shelf", "mangrove_shelf", "cherry_shelf",
    "bamboo_shelf", "crimson_shelf", "warped_shelf",

    "oak_sign", "oak_wall_sign", "spruce_sign", "spruce_wall_sign",
    "birch_sign", "birch_wall_sign", "jungle_sign", "jungle_wall_sign",
    "acacia_sign", "acacia_wall_sign", "dark_oak_sign",
    "dark_oak_wall_sign", "mangrove_sign", "mangrove_wall_sign",
    "cherry_sign", "cherry_wall_sign", "bamboo_sign",
    "bamboo_wall_sign", "crimson_sign", "crimson_wall_sign",
    "warped_sign", "warped_wall_sign",

    "shulker_box", "white_shulker_box", "light_gray_shulker_box",
    "gray_shulker_box", "black_shulker_box", "brown_shulker_box",
    "red_shulker_box", "orange_shulker_box", "yellow_shulker_box",
    "lime_shulker_box", "green_shulker_box", "cyan_shulker_box",
    "light_blue_shulker_box", "blue_shulker_box", "purple_shulker_box",
    "magenta_shulker_box", "pink_shulker_box",

    "white_bed", "light_gray_bed", "gray_bed", "black_bed", "brown_bed",
    "red_bed", "orange_bed", "yellow_bed", "lime_bed", "green_bed",
    "cyan_bed", "light_blue_bed", "blue_bed", "purple_bed",
    "magenta_bed", "pink_bed",

    "oak_trapdoor", "spruce_trapdoor", "birch_trapdoor",
    "jungle_trapdoor", "acacia_trapdoor", "dark_oak_trapdoor",
    "mangrove_trapdoor", "cherry_trapdoor", "bamboo_trapdoor",
    "crimson_trapdoor", "warped_trapdoor", "iron_trapdoor",

    "glass", "tinted_glass", "white_stained_glass", 
    "light_gray_stained_glass", "gray_stained_glass", "black_stained_glass", 
    "brown_stained_glass", "red_stained_glass", "orange_stained_glass", 
    "yellow_stained_glass", "lime_stained_glass", "green_stained_glass", 
    "cyan_stained_glass", "light_blue_stained_glass", "blue_stained_glass", 
    "pink_stained_glass", "magenta_stained_glass", "purple_stained_glass",
    "glass_pane", "light_gray_stained_glass_pane", 

    "white_stained_glass_pane", "gray_stained_glass_pane", 
    "black_stained_glass_pane", "brown_stained_glass_pane",
    "red_stained_glass_pane", "orange_stained_glass_pane",
    "yellow_stained_glass_pane", "lime_stained_glass_pane",
    "green_stained_glass_pane", "cyan_stained_glass_pane",
    "light_blue_stained_glass_pane", "blue_stained_glass_pane",
    "purple_stained_glass_pane", "magenta_stained_glass_pane", 
    "pink_stained_glass_pane",
    
    "white_carpet", "light_gray_carpet", "gray_carpet", "black_carpet", 
    "brown_carpet", "red_carpet", "orange_carpet", "yellow_carpet", 
    "lime_carpet", "green_carpet", "cyan_carpet", "light_blue_carpet", 
    "blue_carpet", "purple_carpet", "magenta_carpet", "pink_carpet",

    "anvil", "chipped_anvil", "damaged_anvil",
};


string variant_simplified(const string& b_variant){
    if (not blocks_variants.contains(b_variant)) return b_variant;

    static const set<string> blocks_simplified = {
        "bed", "sign", "shulker_box", "trapdoor", 
        "glass_pane", "glass", "carpet", "anvil", "shelf"
    };

    for (const auto& block_suffix: blocks_simplified){
        if (b_variant.ends_with(block_suffix)){
            return block_suffix;
        }
    }
    return b_variant;
}


unordered_map<string, Detection>
loadDetections(const string& path){
        std::ifstream file(path);
    
    if (not file.is_open()){
        cerr << "Failed to open JSON file\n";
        return {};
    }

    json detections_json;
    file >> detections_json;

    unordered_map<string, Detection> detections;
    
    for (const auto &detection : detections_json){

        string block_type = variant_simplified(detection["type"]);
        Detection block(block_type);

        for (const auto& coord: detection["coords"]){

            int x = coord[0];
            int y = coord[1];
            int z = coord[2];

            block.addCoord(x, y, z);
        }

        detections.insert({block_type, block});
    }
    
    return detections;
}





