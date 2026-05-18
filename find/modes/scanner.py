import os
import minescript as m 

from core.python import FinderEngine_cpp
from core.python import scanning
from core.python import filtering
from core.python.logger import logger, setup_logger, _cleanup_logger
from core.python import converter
from core.python import minescriptExtra as me

from config import constants as C

def runScanner(mode:str="default") -> None:
    """
    Full scan of minecraft environment.

    Args:
        mode (str): Choose between "default", "full", "sky", "surface", "underground". 
        Defaults to "full".
    """
    # Initialize logger with fresh settings and a new log file
    setup_logger()
    
    if   mode == "sky":
        args = (C.Y_LEVEL_SEARCHING_SKY_TH,)
    elif mode == "surface":
        args = (C.Y_LEVEL_SEARCHING_SURFACE_TH,)
    elif mode == "underground":
        args = (C.Y_LEVEL_SEARCHING_UNDERGROUND_TH,)
    elif mode == "full":
        args = (C.Y_LEVEL_SEARCHING_SURFACE_TH, C.Y_LEVEL_SEARCHING_SKY_TH, C.Y_LEVEL_SEARCHING_UNDERGROUND_TH)
    else:
        args = (C.Y_LEVEL_SEARCHING_SURFACE_TH, C.Y_LEVEL_SEARCHING_UNDERGROUND_TH)
        
    m.echo(f"{me.clr('g')}Initiating {mode} scan...")
    # Collect coords the current region
    block_regions = scanning.scan(*args)
    logger.info("Finished scanning...")
    
    # Filtering blocks to keep just common blocks in real bases
    interesting_blocks = filtering.filter_regions(block_regions)
    logger.info("Finished filtering...")
    
    # Create a json to bridge python with C++ -> detections.json
    converter.to_json(interesting_blocks)
    logger.info("Converted to json file (detections)...")
    
    # C++ analysis and clustering of blocks -> findings.json
    minecraft_dir = os.getcwd()
    FinderEngine_cpp.run(minecraft_dir)
    logger.info("Finished C++ analysis, clustering and converting to json file (findings)...")
    
    # Remove handlers so the logger "ends" until the next scan
    _cleanup_logger()
    m.echo(f"{me.clr('g')}Finished scanning successfully")