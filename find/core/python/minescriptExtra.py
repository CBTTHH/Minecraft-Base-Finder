import minescript as m

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


    
