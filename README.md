

<h1 align="center">Dynasty 2.0 (beta)</h1>

<div align="center">
  Dynasty: A C2 framework inspired by anime, currently supporting <b><i>Linux</i></b>.<br> 
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Trevohack/Dynasty-C2?style=for-the-badge&labelColor=blue&color=violet">
  <img alt="Static Badge" src="https://img.shields.io/badge/Tested--on-Linux-violet?style=for-the-badge&logo=linux&logoColor=black&labelColor=blue">
  <img alt="Static Badge" src="https://img.shields.io/badge/Bash-violet?style=for-the-badge&logo=gnubash&logoColor=black&labelColor=blue">
  <p></p>
  <a href="https://github.com/Trevohack/Dynasty-C2?tab=readme-ov-file#">Install</a>
  <span> • </span>
  <a href="https://github.com/Trevohack/Dynasty-C2?tab=readme-ov-file#">Documentation</a>
  <span> • </span>
  <a href="https://github.com/Trevohack/Dynasty-C2?tab=readme-ov-file#">Usage</a>
  <p></p>
</div> 

```bash
❯ ./dynasty.sh 0.0.0.0 9999 9090
Flask app running in the background. Logs redirected to web_app.log
[+] Activating server

    
    ____                                                       _       _
  /  __    _       _______        ___                       _| |_  _ | |
 |   \ \__| |_    |____   |_ _   /  /                      |_  __|| || |
 |   /  __    \   ___/  _/|_|_| |  |___  __   ___________   / // \| || |
    /  _\/ /\  | |___  _____|   |   _  \|  | |___________| /__  /_| || |
    | |/ _/_/  |   /  /____     |  | |  |  |                / _/ /|_|| |
    \___/  \__/    \_______|   /__/   \___/                /_/  / ___| |  |
                                                            \_/\_\____|  |
                                                                    ____/
     
       __
     /
       Dynasty C2 | Version 1.0 (beta) | [ treveen:anonymous ]
                   __/
                        Made by Trevohack

   [ "Dyansty" inspired by ANIME                    ]
   [  Anime-inspired C2 framework for digital heros ]

  Try help! 

  OPEN PORTS
  0.0.0.0:9999................TCP Listener For Agents
  0.0.0.0:9090................Web Server 


-------------------------------------------------------------------------- 

[treveen@dynasty]~# 
``` 


## Introduction

Welcome to Dynasty-C2, an advanced Command and Control (C2) framework inspired by anime and meticulously crafted to provide powerful capabilities for digital operations, currently supporting Linux environments.

## Features Overview

- **Web Server**: Dynasty-C2 hosts its own web server for distributing required payloads, ensuring seamless communication.
- **Convenient Startup**: With a simple one-liner command, start the console and web server effortlessly.
- **Agent Interaction**: Facilitates interaction with multiple agents, allowing for effective management of sessions.
- **Cross-Platform Compatibility**: While currently focused on Linux environments, future releases aim to support Windows compatibility.
- **Persistence Payloads**: Planned future enhancements include the integration of persistence payloads for extended control.
- **Unique Agent Identification**: Generates a unique key for each agent, enabling efficient tracking and management.
- **User-Friendly Interface**: Offers a streamlined interface for ease of use, simplifying complex operations.
- **File Upload Functionality**: Allows for seamless file uploads to selected agents, enhancing operational flexibility.
- **Payload Generation**: Empowers users to generate customized payloads to specific requirements.

## Documentation Highlights

### Commands Overview

- **Console Commands**:
  - `agents`: Lists all active connections.
  - `use [agent]`: Initiates interaction with a selected agent, providing access to a shell.
  - `kill [key]`: Terminates a selected agent using its unique key.
  - `generate payloads lhost=<lhost> lport=<lport> shell=<shell>`: Generates payloads based on specified parameters.
  - `show privesc-payloads`: Displays all available privilege escalation payloads.
  - `server status`: Provides status information about the web server.

- **Agent Commands**:
  - `set privesc-payload [num]`: Activates a selected privilege escalation payload on the target system.
  - `troll`: Sends commands to all terminal sessions on the target system.
  - `upload [url]`: Facilitates file uploads to the agent.
  - `quit`: Backgrounds the selected agent for later interaction.

## Installation Instructions

* To install Dynasty-C2, follow these steps:

* Clone the repository using `git`:
```bash
$ git clone https://github.com/Trevohack/Dynasty-C2 
$ cd Dynasty-C2 
$ chmod +x dynasty.sh
``` 

## Usage 

* Execute the script with appropriate parameters:
```bash
$ ./dynasty.sh <lhost> <lport> <web_port>
``` 

* Ensure that the lhost denotes the listener host, the lport specifies the port for the C2 server, and the web_port designates the port for hosting payloads.

* This command will initiate Dynasty-C2 with two open ports: lport and web_port.


### Thank You! 
