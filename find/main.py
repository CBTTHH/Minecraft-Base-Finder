import os
import time
import threading

import minescript as m 
# from core. python import FinderEngine_cpp 
from core.python import minescriptExtra as me
from core.python import scanning
from core.python import filtering
from core.python import converter
from config import constants as C



MODES = { 
    "print": (m.execute, "\\bot\\modes\\descend"),
    "radius": (m.execute, "\\bot\\modes\\auto_miner"),
    "save": (m.execute, "\\bot\\modes\\scan_only"),
    "delete": (me.kill_jobs, None),
    "scan": (me.kill_jobs, True),
    "logger": (me._help, None),
    "stop": (me.kill_jobs, True),
}


def main_running() -> bool:
    running_jobs = m.job_info()
    n_running_jobs = len(running_jobs) - 1
    
    if (not n_running_jobs):
        return False
    
    for job in running_jobs:
        if (job.command == ["find\\main"]):
            m.echo(f"{me.clr('y')}\nMain script is already running\n")
            return True
    return False


def commands(msg:str):
    if (not msg.startswith(".bot")):
        return
    
    msg = msg.replace(".", " ").replace("_", " ").split()
    
    cmd = msg[1].lower()
    
    if cmd in MODES:
        m.echo(f"Running mode: {me.clr('p')}{cmd}")
        try:
            executor, cmd = MODES[cmd]
            executor(cmd) if cmd else executor()
        except BaseException as e:
            m.echo(f"Error: {e}")
            executor, cmd = MODES["stop all"]
            executor(cmd) if cmd else executor()
            
            
    else: 
        m.echo(f"Unrecognizable mode: {cmd}")
        m.echo(f"{me.clr('y')}Get help typing: .bot help")


def main():
    stop_flag = False
    
    m.echo(f"{me.clr('g')}Bot ACTIVATED\nUse: '.bot <mode>'")
    
    with m.EventQueue() as events:
        events.register_outgoing_chat_interceptor(prefix=".bot")
        m.echo(f"{me.clr('g')}Type '.bot stop' to STOP the current process")
    
        while (not stop_flag):
            event = events.get()
            
            if event.type == m.EventType.OUTGOING_CHAT_INTERCEPT:
                message = event.message.strip().lower()
                
                if ".find stop" == message:
                    m.echo(f"{me.clr('g')}STOPPING SCRIPT...")
                    stop_flag = True

                threading.Thread(target=commands,
                                 args=(message),
                                 daemon=True).start()
            
        time.sleep(0.1)
        
           
def main2():
    block_regions = scanning.scan(C.Y_LEVEL_SEARCHING_SURFACE_TH, C.Y_LEVEL_SEARCHING_SKY_TH, C.Y_LEVEL_SEARCHING_UNDERGROUND_TH)
    interesting_blocks = filtering.filter_regions(block_regions)
    converter.to_json(interesting_blocks)
    
if __name__ == "__main__":
    main2()

