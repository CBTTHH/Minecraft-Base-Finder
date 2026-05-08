import os
import shutil
from find.config import config
from find.config import constants as C

# .find save {custom name} # Save this list with all the coords 
def save(cname:str, index=1):
    if index < 1 or index > 5:
        print(f"Out of range error: index should be between 1 and {C.MAX_DETECTIONS}")
        return
    
    findings_list = sorted(os.listdir(config.DIR_FINDINGS))
    saved_finding_list = os.listdir(config.DIR_SAVED_FINDINGS)
    
    finding = findings_list.pop(index)
    if f"{cname}.json" in saved_finding_list:
        print(f"There is already a custom saved file with name '{cname}'. Try to save this file with another name or delete the previews one with '.find remove [custom name]'")
        return
    
    shutil.copyfile(os.path.join(config.DIR_FINDINGS, finding), os.path.join(config.DIR_SAVED_FINDINGS, f"{cname}.json"))
    print(f"'{cname}' is SAVED in findings folder")
    
    
# .find remove {custom name} # Delete custom file (json) with the data
def remove(cname:str):
    saved_finding_list = os.listdir(config.DIR_SAVED_FINDINGS)

    if f"{cname}.json" in saved_finding_list:
        os.remove(os.path.join(config.DIR_SAVED_FINDINGS, f"{cname}.json"))
        print(f"'{cname}' was REMOVED from findings folder")
    else: print(f"'{cname}' was NOT FOUND in findings folder")
