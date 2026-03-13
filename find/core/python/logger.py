import logging
import os
from datetime import datetime

LOG_DIR = "minescript/find/data/logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
log_file = os.path.join(LOG_DIR, f"run_{logger_timestamp}.log")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s | %(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("FinderEngine")
