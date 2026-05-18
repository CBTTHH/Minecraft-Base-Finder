import os
import json

import minescript as m
from find.core.python import minescriptExtra as me
from find.config import config
from find.config import constants as C

# .finder print 1                                        # Print last list (2, the one before the last list, this until 5, 
#                                                        since we are just saving the last 5 findings). 
# .finder print {custom name}                            # Print the saved file with the name 
# .finder print {custom name or number} {specific block} # Print all the coords of that specific block 
# .finder print {custom name or number} coords           # Prints each block with all their coords 

def printList(
    index_or_name:int|str=1, 
    block_or_all:str|bool=False, 
    expanded:bool=False
    ):
    
    dir_findings = ""
    finding_path = ""
    
    if isinstance(index_or_name, int):
        if index_or_name < 1 or index_or_name > 5:
            m.echo(f"{me.clr('r')}Out of range error: index should be between 1 and {C.MAX_DETECTIONS}")
            return

        findings_list = sorted(os.listdir(config.DIR_FINDINGS))
        if len(findings_list) < index_or_name:
            m.echo(f"{me.clr('r')}Out of range error: just {len(findings_list)} findings found. Choose between 1 and {len(findings_list)}.")
            return
        dir_findings = config.DIR_FINDINGS
        finding_path = findings_list.pop(-index_or_name)
        
    else: 
        saved_findings_list = sorted(os.listdir(config.DIR_SAVED_FINDINGS))
        finding_path = index_or_name + ".json"
        if not (finding_path in saved_findings_list):
            m.echo(f"{me.clr('y')}File {index_or_name} not found. Check your saved findings with '#finder saved'")
            m.echo(f"{me.clr('y')}Usage: {me.clr('p')}#finder print [index_or_name] [block or all] [expanded]")
            m.echo(f"{me.clr('y')}Example: {me.clr('p')}#finder print 1 beacon true")
            return
        dir_findings = config.DIR_SAVED_FINDINGS
    
    with open(os.path.join(dir_findings, finding_path), "r") as f:
        finding_data:dict = json.load(f)
    
    block = None
    all_coords = False
    if   isinstance(block_or_all, str):
        block = block_or_all
    elif block_or_all == True:
        all_coords = True
    
    if block or all_coords:
        found = False
        for val in finding_data.values():
            for b in val:
                if b.get("type") != block and not all_coords: 
                    continue
                found = True
                
                m.echo(f"{me.clr('p')}## Block: {b.get('type')}:")
                for i, c_coord in enumerate(b.get('clusters_coords')):
                    cx, cy, cz = b.get('centers')[i].values()
                    m.echo(f"# Center: ({cx}, {cy}, {cz})")
                    
                    if expanded:
                        for coord in c_coord:
                            bx, by, bz = coord.values()
                            m.echo(f"({bx}, {by}, {bz})")
                        m.echo()
                    
        if not found:
            m.echo(f"{me.clr('y')}{block} was not found in the list of blocks")
                
    else:
        for val in finding_data.values():
            for block in val:
                m.echo(f"x{block.get('total_size')} {block.get('type')}")


# .finder saved # Print all the custom names saved by the user 
def printSavedDIR():
    saved_findings_list = sorted(os.listdir(config.DIR_SAVED_FINDINGS))
    
    if not saved_findings_list:
        m.echo(f"{me.clr('y')}Nothing was found in the saving file")
        return
    
    m.echo(f"{me.clr('p')}# Findings:")
    for finding in saved_findings_list:
        m.echo(f"- {finding[:-5]}")