import math
import json

import minescript as m
from find.core.python import minescriptExtra as me
from find.core.python.logger import logger
from find.config import constants as C
from find.config.config import SETTING_PATH


def _safe_await_loaded_region(x_min, z_min, x_max, z_max):
    """
    Waits a snappy 2 ticks (0.1s) for the batch region to be loaded.
    Allows rapid radius fallback if chunks are outside server bounds.
    """
    try:
        m.await_loaded_region.as_async(x_min, z_min, x_max, z_max).wait(timeout=C.ONE_TIME_TICK * 2)
        return True
    except TimeoutError:
        return False
        
        
def scan(*y_level_thresholds: tuple[int, int]) -> set[m.BlockRegion]:
    """
    Scans the configured searching radius in batches. If an outer batch fails to 
    load, dynamically falls back to smaller radii layers.
    """
    logger.info("Starting scan...")
    
    with open(SETTING_PATH, 'r') as f:
        settings = json.load(f)
    
    searching_r = settings["searching_radius"]
    x, _, z = map(math.floor, m.player().position)
    
    player_chx = x // C.CHUNK_SIZE
    player_chz = z // C.CHUNK_SIZE
    
    while searching_r > 0:
        start_chx = player_chx - searching_r + 1
        start_chz = player_chz - searching_r + 1
        end_chx = player_chx + searching_r + 1
        end_chz = player_chz + searching_r + 1
        
        failed = False
        
        logger.debug(f"Verifying radius {searching_r}...")
        for curr_chz in range(start_chz, end_chz, C.BATCH_SIZE):
            for curr_chx in range(start_chx, end_chx, C.BATCH_SIZE):
                
                block_x_min = curr_chx * C.CHUNK_SIZE
                block_z_min = curr_chz * C.CHUNK_SIZE
                
                block_x_max = (min(curr_chx + C.BATCH_SIZE, end_chx) * C.CHUNK_SIZE) - 1
                block_z_max = (min(curr_chz + C.BATCH_SIZE, end_chz) * C.CHUNK_SIZE) - 1
                
                if not _safe_await_loaded_region(
                    block_x_min, block_z_min, 
                    block_x_max, block_z_max
                ):
                    failed = True
                    break 
            if failed: break
        
        if not failed:
            logger.info(f"Verified radius {searching_r}. Collecting block data...")
            m.echo(f"{me.clr('g')}Loading radius {searching_r} chunks...")
            
            block_region_storage = set()
            for curr_chz in range(start_chz, end_chz, C.BATCH_SIZE):
                for curr_chx in range(start_chx, end_chx, C.BATCH_SIZE):
                    
                    block_x_min = curr_chx * C.CHUNK_SIZE
                    block_z_min = curr_chz * C.CHUNK_SIZE
                    block_x_max = (min(curr_chx + C.BATCH_SIZE, end_chx) * C.CHUNK_SIZE) - 1
                    block_z_max = (min(curr_chz + C.BATCH_SIZE, end_chz) * C.CHUNK_SIZE) - 1

                    for dy in y_level_thresholds:
                        block_region = m.get_block_region(
                            (block_x_min, dy[0], block_z_min),
                            (block_x_max, dy[1], block_z_max)
                        )
                        block_region_storage.add(block_region)
            
            logger.info(f"Scan successfully completed at radius: {searching_r}")
            return block_region_storage

        searching_r -= 1
        logger.info(f"Reducing radius to {searching_r}")
        m.echo(f"{me.clr('y')}Reducing radius to {searching_r}")
        
    logger.error("Scan failed completely. No chunks loaded.")
    m.echo(f"{me.clr('r')}Scan failed completely. No chunks loaded.")
    return set()