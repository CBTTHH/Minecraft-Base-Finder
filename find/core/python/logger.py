import os
import json
import logging
from datetime import datetime

from find.config.config import SETTING_PATH

LOG_DIR      = os.path.join("minescript", "find", "data", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

with open(SETTING_PATH, 'r') as f:
        setting = json.load(f)

if setting["logger_level"][0] == 'w':
    logger_level = logging.WARN
else:
    logger_level = logging.INFO
    

logger_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
log_file = os.path.join(LOG_DIR, f"run_{logger_timestamp}.log")

logging.basicConfig(
    level=logger_level,
    format="[%(asctime)s | %(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("FinderEngine")
