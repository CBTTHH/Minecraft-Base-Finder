import os
import json

from find.core.python import minescriptExtra as me
from find.config import config
from find.config import constants as C

# .find print 1                                        # Print last list (2, the one before the last list, this until 5, 
#                                                        since we are just saving the last 5 findings). 
# .find print {custom name}                            # Print the saved file with the name 
# .find print {custom name or number} {specific block} # Print all the coords of that specific block 
# .find print {custom name or number} coords           # Prints each block with all their coords 
def printList(index_or_name:int|str=1, block:str=None, all_coords=False):

    finding_path = ""
    
    if isinstance(index_or_name, int):
        if index_or_name < 1 or index_or_name > 5:
            print(f"{me.clr('r')}Out of range error: index should be between 1 and {C.MAX_DETECTIONS}")
            return

        findings_list = sorted(os.listdir(config.DIR_FINDINGS))
        
        if len(findings_list) < index_or_name:
            print(f"{me.clr('r')}Out of range error: just {len(findings_list)} findings found. Choose between 1 and {len(findings_list)}.")
            return
            
        finding_path = findings_list.pop(-index_or_name)
        
    else: 
        saved_findings_list = sorted(os.listdir(config.DIR_SAVED_FINDINGS))
        
        if not index_or_name in saved_findings_list:
            print(f"{me.clr('y')}File {index_or_name} not found. Check your saved findings with '.find print saved'")
            return

        finding_path = index_or_name
    
    with open(os.path.join(config.DIR_FINDINGS, finding_path), "r") as f:
        finding_data:dict = json.load(f)
        
    if block or all_coords:
        found = False
        for val in finding_data.values():
            for b in val:
                if b.get("type") != block and not all_coords: 
                    continue
                found = True
                
                print(f"{me.clr('p')}## Block: {b.get('type')}:")
                for i, c_coord in enumerate(b.get('clusters_coords')):
                    cx, cy, cz = b.get('centers')[i].values()
                    print(f"# Center: ({cx}, {cy}, {cz})")
                    
                    for coord in c_coord:
                        bx, by, bz = coord.values()
                        print(f"({bx}, {by}, {bz})")
                    print()
                    
        if not found:
            print(f"{me.clr('y')}{block} was not found in the list of blocks")
                
    else:
        for val in finding_data.values():
            for block in val:
                print(f"x{block.get('total_size')} {block.get('type')}")


# .find print saved # Print all the custom names saved by the user 
def printSavedDIR():
    saved_findings_list = sorted(os.listdir(config.DIR_SAVED_FINDINGS))
    
    if not saved_findings_list:
        print("Nothing was found in the saving file")
        return
    
    print("# Findings:")
    for finding in saved_findings_list:
        print(f"- {finding}")
        
printList(block="bookshelf")