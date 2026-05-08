from find.core.python import scanning
from find.core.python import logger
from find.core.python import minescriptExtra as me
from find.config import constants as C


# .find radius {number between 4, 12} # Change the constant radius to the specify by the player, if it is more than 12, then set it to 12 and tell 
# the player that it was set to 12 or if thats bellow 4, tell the player it was set to 4. 
def changeRadius(r:int) -> None:
    if not isinstance(r, int):
        print(f"{me.clr('r')}Type Error: Radius needs to be a integer not a {type(r)}")
        return
    
    if r > 12:
        r = 12
        print(f"{me.clr('y')}Searching radius cannot be set more than 12. It might cause memory overload")
    
    if r < 4:
        r = 4
        print(f"{me.clr('y')}Searching radius cannot be set less than 4. The scanning region very small")
    
    C.SEARCHING_RADIUS = r
    print(f"{me.clr('g')}Searching radius is not set to {C.SEARCHING_RADIUS} blocks")

# .find logger {true or false} # Activate or deactivate logger prints in minecraft chat
def DebugModeLogger(b: bool) -> None:
    if not isinstance(b, bool):
        print("Type Error: Boolean needs to be true or false")
    
    if b:
        logger.logger_level = logger.logging.INFO
        print(f"{me.clr('g')}Change to debugging mode")
    else:
        logger.logger_level = logger.logging.WARN
        print(f"{me.clr('g')}Disable debugging mode")
    
    