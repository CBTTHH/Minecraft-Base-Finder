import math
import time

import minescript as m
import find.core.python.minescriptExtra as me
import find.config.constants as C
from find.core.python.logger import logger


def safe_await_loaded_region(x_min, z_min, x_max, z_max):
    start_t = time.perf_counter()
    while True:
        if m.await_loaded_region(x_min, z_min, x_max, z_max):
            return True
        if time.perf_counter() - start_t > C.MAX_TIME_AWAITING_REGION:
            return False
        time.sleep(C.ONE_TIME_TICK)
        
        
def scan(*y_level_thresholds:tuple[tuple[int,int]]) -> set[m.BlockRegion]:
    """
    Docstring for scan
    
    :param y_level_thresholds: y level thresholds of the desire y-axis scan
    :type y_level_scan: *tuple[int]
    :return: set with all partial regions scanned
    of the searching radius. The set is the total scanned region.
    :rtype: set[BlockRegion]
    """
    logger.info("Starting scan...")
    
    searching_r = C.SEARCHING_RADIUS
    x, _, z = map(math.floor, m.player().position)
    
    player_chx = x // C.CHUNK_SIZE
    player_chz = z // C.CHUNK_SIZE
    
    while searching_r > 0:
        
        start_chx = player_chx - searching_r + 1
        start_chz = player_chz - searching_r + 1

        curr_chx = start_chx
        curr_chz = start_chz
        
        end_chx = player_chx + searching_r + 1
        end_chz = player_chz + searching_r + 1
        
        searching_times = math.ceil(searching_r * 2 / C.BATCH_SIZE)
        
        failed = False
        block_region_storage = set()
                    
        for _ in range(searching_times):
            for _ in range(searching_times):
                
                block_x_min = curr_chx * C.CHUNK_SIZE
                block_z_min = curr_chz * C.CHUNK_SIZE
                
                block_x_max = min(curr_chx + C.BATCH_SIZE, end_chx) * C.CHUNK_SIZE 
                block_z_max = min(curr_chz + C.BATCH_SIZE, end_chz) * C.CHUNK_SIZE 
                
                if not safe_await_loaded_region(
                    block_x_min, block_z_min, 
                    block_x_max, block_z_max
                ):
                    logger.warning(f"{me.clr('y')}Batch failed at radius {searching_r}")
                    failed = True
                    break
                
                for dy in y_level_thresholds:
                    
                    block_region = m.get_block_region(
                        (block_x_min, dy[0], block_z_min),
                        (block_x_max, dy[1], block_z_max)
                    )
                    
                    block_region_storage.add(block_region)
                    
                curr_chx += C.BATCH_SIZE 
            
            if failed: break
            
            curr_chz += C.BATCH_SIZE
            curr_chx = start_chx
        
        if not failed:
            logger.info("Scan successfully return block regions")
            return block_region_storage

        searching_r -= 1
        logger.warning(f"Reducing radius to {searching_r}")
        m.echo(f"{me.clr('y')}Reducing radius to {searching_r}")
        
    logger.error("Scan failed completely. No chunks loaded.")
    m.echo(f"{me.clr('r')}Scan failed completely. No chunks loaded.")
    return set()
        