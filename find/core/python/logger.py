import os
import json
import logging
from datetime import datetime

from find.config.config import SETTING_PATH

LOG_DIR = os.path.join("minescript", "find", "data", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("FinderEngine")

def setup_logger():
    with open(SETTING_PATH, 'r') as f:
            setting = json.load(f)

    if setting["logger_level"][0] == 'w':
        logger_level = logging.WARN
    else:
        logger_level = logging.DEBUG
        
    logger_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_file = os.path.join(LOG_DIR, f"run_{logger_timestamp}.log")

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logger_level)
    
    file_handler = logging.FileHandler(log_file)
    stream_handler = logging.StreamHandler()
    
    formatter = logging.Formatter("[%(asctime)s | %(levelname)s]: %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

def cleanup_logger():
    logger.handlers.clear()
