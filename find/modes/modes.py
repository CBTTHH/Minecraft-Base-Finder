import os
import time
import threading

import minescript as m
import find.core.python.minescriptExtra as m_extra

DIR_FINDINGS = os.path.join("minescript", "find", "data", "findings")
DIR_SAVED = os.path.join("minescript", "find", "data", "findings_saved")
DIR_LOGS = os.path.join("minescript", "find", "data", "findings")



MODES = { 
    "print": (m.execute, "\\bot\\modes\\descend"),
    "radius": (m.execute, "\\bot\\modes\\auto_miner"),
    "save": (m.execute, "\\bot\\modes\\scan_only"),
    "delete": (m_extra.kill_jobs, None),
    "scan": (m_extra.kill_jobs, True),
    "logger": (m_extra._help, None),
    "stop": (m_extra.kill_jobs, True),
}


def main_running() -> bool:
    running_jobs = m.job_info()
    n_running_jobs = len(running_jobs) - 1
    
    if (not n_running_jobs):
        return False
    
    for job in running_jobs:
        if (job.command == ["find\\main"]):
            m.echo(f"{m_extra.txt_clr('y')}\nMain script is already running\n")
            return True
    return False


def commands(msg:str):
    if (not msg.startswith(".bot")):
        return
    
    msg = msg.replace(".", " ").replace("_", " ").split()
    
    if len(msg) > 3:
        m.echo(f"{m_extra.txt_clr('y')}Get help typing: .bot help")
        return
    
    cmd = msg[1].lower()
    
    if cmd in MODES:
        m.echo(f"Running mode: {m_extra.txt_clr('p')}{cmd}")
        try:
            executor, cmd = MODES[cmd]
            executor(cmd) if cmd else executor()
        except BaseException as e:
            m.echo(f"Error: {e}")
            executor, cmd = MODES["stop all"]
            executor(cmd) if cmd else executor()
            
            
    else: 
        m.echo(f"Unrecognizable mode: {cmd}")
        m.echo(f"{m_extra.txt_clr('y')}Get help typing: .bot help")


def main():
    stop_flag = False
    
    m.echo(f"{m_extra.txt_clr('g')}Bot ACTIVATED\nUse: '.bot <mode>'")
    
    with m.EventQueue() as events:
        events.register_outgoing_chat_interceptor(prefix=".bot")
        m.echo(f"{m_extra.txt_clr('g')}Type '.bot stop' to STOP the program")
    
        while (not stop_flag):
            event = events.get()
            
            if event.type == m.EventType.OUTGOING_CHAT_INTERCEPT:
                message = event.message.strip().lower()
                
                if ".find stop" == message:
                    m.echo(f"{m_extra.txt_clr('g')}STOPPING SCRIPT...")
                    stop_flag = True

                threading.Thread(target=commands,
                                 args=(message,),
                                 daemon=True).start()
            
        time.sleep(0.1)
        

if __name__ == "__main__":
    running = main_running()
    if (not running):
        main()


# .find print # To print the last list again 


# .find print 1 # Print last list (2, the one before the last list, this until 5, since we are just saving the last 5 findings). 


# .find save {custom name} # Save this list with all the coords 


# .find print {custom name} # Print the saved file with the name 


# .find print {custom name or number} {specific block} # Print all the coords of that specific block 


# .find print saved # Print all the custom names saved by the user 


# .find delete {custom name} # Delete custom file (json) with the data 


# .find print all {custom name or number} # Prints each block with all their coords 


# .find radius {number between 4, 12} # Change the constant radius to the specify by the player, if it is more than 12, then set it to 12 and tell 
# the player that it was set to 12 or if thats bellow 4, tell the player it was set to 4. 


# .find search {initial y level} {final y level} # Custom search for the specific y levels ask for the player 


# .find logger {true or false} # Activate or deactivate logger prints in minecraft chat
