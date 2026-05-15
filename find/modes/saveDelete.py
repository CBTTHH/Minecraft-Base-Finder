import os
import shutil

import minescript as m
from find.core.python import minescriptExtra as me
from find.config import config
from find.config import constants as C

# .find save {custom name} # Save this list with all the coords 
def save(custom_name:str, index=1):
    if index < 1 or index > C.MAX_DETECTIONS:
        m.echo(f"{me.clr('y')}Out of range error: index should be between 1 and {C.MAX_DETECTIONS}")
        return
    
    findings_list = sorted(os.listdir(config.DIR_FINDINGS))
    saved_finding_list = os.listdir(config.DIR_SAVED_FINDINGS)
    
    finding = findings_list.pop(-index)
    if f"{custom_name}.json" in saved_finding_list:
        m.echo(f"{me.clr('y')}There is already a custom saved file with name '{custom_name}'. Try to save this file with another name or delete the previews one with '.find remove [custom name]'")
        return
    
    shutil.copyfile(os.path.join(config.DIR_FINDINGS, finding), os.path.join(config.DIR_SAVED_FINDINGS, f"{custom_name}.json"))
    m.echo(f"{me.clr('g')}'{custom_name}' is SAVED in findings folder")
    
    
# .find remove {custom name} # Delete custom file (json) with the data
def remove(custom_name:str):
    saved_finding_list = os.listdir(config.DIR_SAVED_FINDINGS)

    if f"{custom_name}.json" in saved_finding_list:
        os.remove(os.path.join(config.DIR_SAVED_FINDINGS, f"{custom_name}.json"))
        m.echo(f"'{me.clr('g')}{custom_name}' was REMOVED from findings folder")
    else: m.echo(f"{me.clr('y')}'{custom_name}' was NOT FOUND in findings folder")
