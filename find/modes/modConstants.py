import os
import json

import minescript as m
from find.core.python import minescriptExtra as me
from find.config import constants as C
from find.config.config import SETTING_PATH

with open(SETTING_PATH, 'r') as f:
        setting = json.load(f)

# .finder radius {number between 4, 24} # Change the constant radius to the specify by the player, if it is more than 24, then set it to 24 and tell 
# the player that it was set to 24 or if thats bellow 4, tell the player it was set to 4. 
def changeRadius(r:int) -> None:
    if not isinstance(r, int):
        m.echo(f"{me.clr('r')}Type Error: Radius needs to be a integer not a {type(r)}")
        return
    
    if r > C.MAX_SEARCHING_RADIUS:
        r = C.MAX_SEARCHING_RADIUS
        m.echo(f"{me.clr('y')}Searching radius cannot be set more than {C.MAX_SEARCHING_RADIUS}. It might cause memory overload")
    
    if r < C.MIN_SEARCHING_RADIUS:
        r = C.MIN_SEARCHING_RADIUS
        m.echo(f"{me.clr('y')}Searching radius cannot be set less than {C.MIN_SEARCHING_RADIUS}. The scanning region very small")
    
    setting["searching_radius"] = r
    
    with open(SETTING_PATH, 'w') as f:
        json.dump(setting, f, indent=4)
        
    m.echo(f"{me.clr('g')}Searching radius is set to {setting["searching_radius"]} blocks")

# .finder logger {true or false} # Activate or deactivate logger prints in minecraft chat
def DebugModeLogger(b: bool) -> None:
    
    if not isinstance(b, bool):
        m.echo("Type Error: Boolean needs to be true or false")
    
    if b:
        setting["logger_level"] = "info"
        m.echo(f"{me.clr('g')}Change to debugging mode")
    else:
        setting["logger_level"] = "warn"
        m.echo(f"{me.clr('g')}Disable debugging mode")
        
    with open(SETTING_PATH, 'w') as f:
        json.dump(setting, f, indent=4)
        