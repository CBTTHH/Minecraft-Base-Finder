import os
import json
from datetime import datetime

import minescript as m
import find.config.constants as C
from find.core.python.detection import Detection
from find.core.python.logger import logger, logger_timestamp


DETECTIONS_DIR = os.path.join("minescript", "find", "data", "detections")
LOGS_DIR = os.path.join("minescript", "find", "data", "logs")


def oldest(files:str, file_type="json") -> str:
    db = {}
    
    if file_type == "json":
        for file_name in files:
            db[file_name.removeprefix("detection").removesuffix(".json")] = file_name
    else:
        for file_name in files:
            db[file_name.removeprefix("run_").removesuffix(".log")] = file_name

    oldest_timestamp = min({int(timestamp) for timestamp in db.keys()})
    return db.get(str(oldest_timestamp))
    
        

def remove_oldest(oldest_file:str, file_type_list:list, file_type="json") -> None:
    for file_name in file_type_list:
        if file_name.startswith(oldest_file):
            
            if file_type == "json": 
                path = os.path.join(DETECTIONS_DIR, file_name) 
            else: 
                path = os.path.join(LOGS_DIR, file_name)
            
            if os.path.exists(path): 
                logger.warning(f"Deleting: {oldest_file}")
                os.remove(path)
            
            file_type_list.remove(oldest_file)


def to_json(detections:dict[str,Detection]) -> None:
    """
    Docstring for to_json
    
    :param detections: Convert all detected types of block into a json
    :type detections: dict[str, Detection]
    """
    logger.info("Converting detected blocks into json...")
    
    timestamp = logger_timestamp
    total_detections = []

    for detection in detections.values():
        total_detections.append(detection.to_dict())
    
    total_detections_json = json.dumps(total_detections)
    logger.debug("Successfully converted into json file")
    
    json_file = f"detection{timestamp}.json" 
    with open(os.path.join(DETECTIONS_DIR, json_file), "w") as f:
        f.write(total_detections_json)
        logger.info(f"Converter successfully stored detections in {json_file}")
        
    detections_json_list = os.listdir(DETECTIONS_DIR)
    detections_log_list = os.listdir(LOGS_DIR)
    files_number = max(len(detections_json_list), len(detections_log_list))

    while files_number > C.MAX_DETECTIONS:
        
        if len(detections_json_list) > C.MAX_DETECTIONS:
            oldest_json_f = oldest(detections_json_list)
            remove_oldest(oldest_json_f, detections_json_list)
        
        if len(detections_log_list) > C.MAX_DETECTIONS:
            oldest_log_f = oldest(detections_log_list, "log")
            remove_oldest(oldest_log_f, detections_log_list, "log")
            
        files_number = max(len(detections_json_list), len(detections_log_list))
        

