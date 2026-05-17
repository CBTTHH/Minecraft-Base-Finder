import minescript as m
from find.config import constants as C

def clr(color:str = '') -> str:
    """
    Docstring for text_color
    
    :param color: '0' = black, 'a' = aqua,'b' = blue 'r' = red, 'g' = green, 'y' = yellow, 'p' = purple
    :type color: str
    """
    if (not color):
        return ""
    match color[0]:
        case '0': return "§0"
        case 'a': return "§b"
        case 'r': return "§c"
        case 'g': return "§a"
        case 'y': return "§e"
        case 'b': return "§9"
        case 'p': return "§d"
        case  _ : return "§f"

def kill_jobs(all=False):
    if all: m.echo("Including main script")
    running_scripts = m.job_info()
    
    for job in running_scripts:
        if not(all) and (job.command == ["find\\main"]): 
            continue
        m.execute(f"\\killjob {job.job_id}")


def _help():
    m.echo(f"{clr('p')}=== Finder Engine Help ===")
    m.echo("")
    m.echo(f"{clr('g')}Usage: #finder <command> [arguments]")
    m.echo(f"scan [mode] - Scan area. Modes: default, full, sky, surface, underground.")
    m.echo(f"print [idx/name] [block/coords] [all]{clr()} - Display finding details.")
    m.echo(f"  - {clr('p')}idx: 1-{C.MAX_DETECTIONS} (last scans), name: your saved name.")
    m.echo(f"  - {clr('p')}coords: show all blocks with cluster centers.")
    m.echo(f"  - {clr('p')}all: expand to show every individual coordinate.")
    m.echo(f"  - {clr('a')}Ex: #finder print 1 furnace all")
    m.echo(f"save [name] [idx]{clr()} - Save finding (default index 1) with a custom name.")
    m.echo(f"remove [name]{clr()} - Delete a custom saved finding.")
    m.echo(f"saved{clr()} - List all your saved custom findings.")
    m.echo(f"radius [4-24]{clr()} - Set the scanning radius in blocks.")
    m.echo(f"logger [true/false]{clr()} - Enable or disable debug logs in chat.")
    m.echo(f"stop{clr()} - Stop and deactivate the Finder Engine.")
    m.echo("")
    m.echo(f"{clr('p')}==========================")


