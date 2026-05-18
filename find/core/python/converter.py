import os
import json
from datetime import datetime

from find.config import constants as C
from find.config.config import DIR_DETECTIONS, DIR_LOGS
from find.core.python.detection import Detection
from find.core.python.logger import logger


os.makedirs(DIR_DETECTIONS, exist_ok=True)

def _oldest(files: list[str], file_type="json") -> str:
    db = {}
    if file_type == "json":
        for file_name in files:
            if file_name.startswith("detection"):
                db[file_name.removeprefix("detection").removesuffix(".json")] = file_name
    else:
        for file_name in files:
            if file_name.startswith("run_"):
                db[file_name.removeprefix("run_").removesuffix(".log")] = file_name
    
    if not db: return None
    oldest_timestamp = min(db.keys(), key=int)
    return db.get(str(oldest_timestamp))

def _remove_oldest(oldest_file: str, file_type_list: list, file_type="json") -> None:
    for file_name in file_type_list:
        if file_name.startswith(oldest_file):
            if file_type == "json": 
                path = os.path.join(DIR_DETECTIONS, file_name) 
            else: 
                path = os.path.join(DIR_LOGS, file_name)
            
            if os.path.exists(path): 
                logger.debug(f"Deleting: {oldest_file}")
                os.remove(path)


def to_json(detections:dict[str,Detection]) -> None:
    """
    Docstring for to_json
    
    :param detections: Convert all detected types of block into a json
    :type detections: dict[str, Detection]
    """
    logger.info("Converting detected blocks into json...")
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    total_detections = []

    for detection in detections.values():
        total_detections.append(detection.to_dict())
    
    total_detections_json = json.dumps(total_detections)
    logger.debug("Successfully converted into json file")
    
    json_file = f"detection{timestamp}.json" 
    with open(os.path.join(DIR_DETECTIONS, json_file), "w") as f:
        f.write(total_detections_json)
        logger.info(f"Converter successfully stored detections in {json_file}")

    while True:
        detections_json_list = os.listdir(DIR_DETECTIONS)
        detections_log_list = os.listdir(DIR_LOGS)

        if len(detections_json_list) <= C.MAX_DETECTIONS and len(detections_log_list) <= C.MAX_DETECTIONS:
            break

        if len(detections_json_list) > C.MAX_DETECTIONS:
            oldest_json_f = _oldest(detections_json_list)
            _remove_oldest(oldest_json_f, detections_json_list)

        if len(detections_log_list) > C.MAX_DETECTIONS:
            oldest_log_f = _oldest(detections_log_list, "log")
            _remove_oldest(oldest_log_f, detections_log_list, "log")
