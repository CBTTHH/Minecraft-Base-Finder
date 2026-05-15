from concurrent.futures import ThreadPoolExecutor, as_completed

import minescript as m
from find.core.python.detection import Detection
from find.core.python.logger import logger

INTERESTING_BLOCKS = {
    # Functional Blocks
    "furnace", "blast_furnace", "smoker", "smithing_table", "crafting_table",
    "anvil", "chipped_anvil", "damaged_anvil", "note_block", "jukebox",
    "brewing_stand", "beacon", "ladder", "painting", "scaffolding",
    "bookshelf", "chiseled_bookshelf", "fetching_table", "composter",

    "oak_shelf", "spruce_shelf", "birch_shelf", "jungle_shelf",
    "acacia_shelf", "dark_oak_shelf", "mangrove_shelf", "cherry_shelf",
    "bamboo_shelf", "crimson_shelf", "warped_shelf",

    "enchanting_table", "torch", "wall_torch", "redstone_torch",
    "redstone_wall_torch", "sea_lantern", "glowstone", "end_rod", "lectern",

    "oak_sign", "oak_wall_sign", "spruce_sign", "spruce_wall_sign",
    "birch_sign", "birch_wall_sign", "jungle_sign", "jungle_wall_sign",
    "acacia_sign", "acacia_wall_sign", "dark_oak_sign",
    "dark_oak_wall_sign", "mangrove_sign", "mangrove_wall_sign",
    "cherry_sign", "cherry_wall_sign", "bamboo_sign",
    "bamboo_wall_sign", "crimson_sign", "crimson_wall_sign",
    "warped_sign", "warped_wall_sign",

    "chest", "barrel", "ender_chest",

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

    "whiter_skeleton_skull", "whiter_skeleton_wall_skull",
    "dragon_head", "dragon_wall_head", "dragon_egg", "soul_sand",
    "nether_wart"

    # Building Blocks
    "oak_trapdoor", "spruce_trapdoor", "birch_trapdoor",
    "jungle_trapdoor", "acacia_trapdoor", "dark_oak_trapdoor",
    "mangrove_trapdoor", "cherry_trapdoor", "bamboo_trapdoor",
    "crimson_trapdoor", "warped_trapdoor", "iron_trapdoor",
    
    "iron_block", "emerald_block", "obsidian",
    
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

    # Redstone Blocks
    "redstone_wire", "redstone_block", "repeater", "comparator",
    "lever", "trip_wire_hook", "tripwire", "piston", "sticky_piston",
    "slime_block", "honey_block", "dispenser", "dropper", "hopper",
    "trapped_chest", "observer"
    
    # Rare Blocks
    "nether_portal",
}


def remove_prefix_subfix(block_type:str):
    block_type = block_type.removeprefix("minecraft:")
    block_type = block_type.replace("[", " ")
    block_type = block_type.split(" ")
    return block_type[0]


def process_region(region:m.BlockRegion) -> dict[str, Detection]:
    local_detection: dict[str, Detection] = {}
    
    min_x, min_y, min_z = region.min_pos
    max_x, max_y, max_z = region.max_pos
    
    for bx in range(min_x, max_x + 1):
        for by in range(min_y, max_y + 1):
            for bz in range(min_z, max_z + 1):
                
                block = region.get_block(bx, by, bz)
                
                if not block:
                    continue
                
                block = remove_prefix_subfix(block)
                
                if block not in INTERESTING_BLOCKS:
                    continue
                
                if block not in local_detection:
                    local_detection[block] = Detection(block)
                local_detection[block].add_coords((bx, by, bz))
    
    logger.debug("Successfully colleted local detection blocks") 
    return local_detection


def filter_regions(block_regions:set[m.BlockRegion]) -> dict[str, Detection]:
    """
    Docstring for filtering
    
    :param block_regions: set of all partial regions scanned
    :type block_regions: set[m.BlockRegion]
    :return: dictionary with all the interesting blocks and its Detection class
    :rtype: dict[str, Detection]
    """
    logger.info("Starting filter...")
    
    detection_storage:dict[str, Detection] = {}
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_region, region) for region in block_regions]
        
        for future in as_completed(futures):
            local_detection = future.result()
    
            for block_type, detection in local_detection.items():
                
                if block_type not in detection_storage:
                    detection_storage[block_type] = detection
                else:
                    detection_storage[block_type] += detection
    
    logger.info("Filter successfully return filtered detected blocks")
    return detection_storage 

              
