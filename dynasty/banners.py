from rich.table import Table 
from colors import NiceColors


class characters:
    naruto = f"[{NiceColors.red}Naruto{NiceColors.reset}]"
    goku = f"[{NiceColors.yellow}Son Goku{NiceColors.reset}]"
    sakura = f"[{NiceColors.green}Sakura{NiceColors.reset}]"
    monkey = f"[{NiceColors.blue}Monkey D. Luffy{NiceColors.reset}]" 
    yagmi = f"[{NiceColors.cyan}Light Yagmi{NiceColors.reset}]"

    agent_chars = [naruto, goku, sakura, monkey, yagmi] 

class banners:
    alien = f"""
{NiceColors.blue}	
_________________________________________________________                                                  
{NiceColors.reset}
{NiceColors.magenta}
                         ,------------. 
            ///////      |huahahahaha!|   /`., , 
           || -  _|      `------------'  /'/''<
           |/ O  o|              |    _.'   /_'\.
           (-   `\|              |   (_ oOo __) |
            |  `-'|               \    `\:/'    `\ 
       ____/  --- |___             `-   /`       |____ 
      /  `\  .___/ |  \                /'\__(()\_/ _  `\ 
     /    `\      /'   \              |  |  (\\\)__/    | 
    /   /   `\___/'  |  \             |  |   \         / 
{NiceColors.blue} 
_________________________________________________________
{NiceColors.reset}
 
    """ 


    help = f""" 
   {NiceColors.blue} 
   ------------------------------------------------------------------------------------ 
   {NiceColors.reset}
                                  
                                  {NiceColors.yellow}Dynasty - Help Menu{NiceColors.reset}

   {NiceColors.magenta}Command{NiceColors.reset}                                                                 {NiceColors.magenta}Usage{NiceColors.reset} 
   -------                                                                ------  

   "help".......................................................................{NiceColors.cyan}Displays this help message{NiceColors.reset}
   "kill (key)".....................................................................{NiceColors.cyan}Kill active characters{NiceColors.reset}
   "agents".....................................................................{NiceColors.cyan}List all characters beaten{NiceColors.reset}
   "use (agent num)".........................................................{NiceColors.cyan}Get a shell to selected agent{NiceColors.reset}
   "generate payloads lhost=<lhost> lport=<lport> shell=<shell_type>"....................{NiceColors.cyan}Generate payloads{NiceColors.reset}


   {NiceColors.yellow}Dynasty - In Agent{NiceColors.reset}

   
   "background"..................................................................{NiceColors.cyan}Background selected agent{NiceColors.reset}
   "troll"............................................................{NiceColors.cyan}Send commands to tty shells in agent{NiceColors.reset}
   "show privesc-check"..................................................................{NiceColors.cyan}View all payloads{NiceColors.reset}
   "set privesc-check (num)"...................................................{NiceColors.cyan}Activate a payload on agent{NiceColors.reset} 
   "server status"...............................................{NiceColors.cyan}Check server status and web server status{NiceColors.reset}
   "upload [filename]......................................................{NiceColors.cyan}Upload a file to selected agent{NiceColors.reset}

   "exit"................................................................................{NiceColors.cyan}Exit the Dynasty!{NiceColors.reset} 

   

    The Dynasty! 

    
   Made with ❤️  by Trevohack 
   """ 
