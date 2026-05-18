import os
import json
import logging
from datetime import datetime

from find.config.config import SETTING_PATH, DIR_LOGS

os.makedirs(DIR_LOGS, exist_ok=True)

logger = logging.getLogger("FinderEngine")

def _cleanup_logger():
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
        

def setup_logger():
    logger.setLevel(logging.DEBUG)

    with open(SETTING_PATH, 'r') as f:
            setting = json.load(f)

    if setting.get("logger_level", "info").startswith('w'):
        chat_level = logging.WARNING
    else:
        chat_level = logging.INFO
        
    logger_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_file = os.path.join(DIR_LOGS, f"run_{logger_timestamp}.log")

    _cleanup_logger()

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG) 
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(chat_level) 
    
    formatter = logging.Formatter("[%(asctime)s | %(levelname)s]: %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


