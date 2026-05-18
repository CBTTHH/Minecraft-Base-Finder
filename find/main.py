import time
import threading

import minescript as m 
from core.python import minescriptExtra as me

from modes import printer
from modes import saveDelete
from modes import modConstants
from modes import scanner

MODES = { 
    "scan"   : (scanner.runScanner,           0,  1),
    "print"  : (printer.printList,            0,  3),
    "save"   : (saveDelete.save,              1,  2),
    "remove" : (saveDelete.remove,            1,  1),
    "saved"  : (printer.printSavedDIR,        0,  0),
    "radius" : (modConstants.changeRadius,    1,  1),
    "logger" : (modConstants.DebugModeLogger, 1,  1),
    "-help"  : (me._help,                     0,  0),
}


def main_running() -> bool:
    running_jobs = m.job_info()
    n_running_jobs = len(running_jobs) - 1
    
    if (not n_running_jobs):
        return False
    
    for job in running_jobs:
        if (job.command == ["find\\main"]):
            m.echo(f"{me.clr('y')}\nFinder Engine is already running...\n")
            return True
    return False


def commands(argv:str) -> None:
    if (not argv.startswith("#finder")):
        return
    
    argv = argv.replace(".", " ").split()
    argc = len(argv)
    
    cmd = argv[1].lower()
    
    if cmd in MODES:
        executor, min_num_param, max_num_param = MODES[cmd]
        if not(min_num_param <= argc - 2 <= max_num_param):
            m.echo(f"{me.clr('y')}This function require at least {min_num_param} parameters or at most {max_num_param}...")
            m.echo(f"{me.clr('y')}Get help typing: #finder -help")
            return
            
        for i in range(2, argc):
            if   argv[i].isdigit():
                argv[i] = int(argv[i])
            elif argv[i].lower() == "true" or argv[i].lower() == "all":
                argv[i] = True
            elif argv[i].lower() == "false":
                argv[i] = False
            
        executor(*argv[2:])
            
    else: 
        m.echo(f"{me.clr('y')}Unrecognizable mode: {cmd}")
        m.echo(f"{me.clr('y')}Get help typing: #finder -help")


def main():
    if main_running():
        return
        
    stop_flag = False
    
    m.echo(f"{me.clr('g')}Finder Engine ACTIVATED\nUse: '#finder <mode>'")
    
    with m.EventQueue() as events:
        events.register_outgoing_chat_interceptor(prefix="#finder")
        m.echo(f"{me.clr('g')}Type '#finder stop' to STOP the Engine")
    
        while (not stop_flag):
            event = events.get()
            
            if event.type == m.EventType.OUTGOING_CHAT_INTERCEPT:
                message = event.message.strip().lower()
                                
                if "#finder stop" == message:
                    m.echo(f"{me.clr('g')}STOPPING ENGINE...")
                    stop_flag = True
                    break
                
                m.echo("=== BEGINNING ====================================")

                threading.Thread(target=commands,
                                 args=(message,),
                                 daemon=True).start()
                
        time.sleep(0.1)
            
    
if __name__ == "__main__":
    main()

