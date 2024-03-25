
<h1 align="center">Dynasty 1.0 (beta)</h1>

<div align="center">
  Dynasty: A C2 framework inspired by anime, currently supporting <b><i>Linux</i></b>.<br> 
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Trevohack/Dynasty-C2?style=for-the-badge&labelColor=blue&color=violet">
  <img alt="Static Badge" src="https://img.shields.io/badge/Tested--on-Linux-violet?style=for-the-badge&logo=linux&logoColor=black&labelColor=blue">
  <img alt="Static Badge" src="https://img.shields.io/badge/Bash-violet?style=for-the-badge&logo=gnubash&logoColor=black&labelColor=blue">
  <p></p>
  <a href="https://github.com/Trevohack/Dynasty-C2?tab=readme-ov-file#installation">Install</a>
  <span> • </span>
  <a href="https://github.com/Trevohack/Dynasty-C2?tab=readme-ov-file#documentation">Documentation</a>
  <span> • </span>
  <a href="https://github.com/Trevohack/Dynasty-C2?tab=readme-ov-file#usage">Usage</a>
  <p></p>
</div>

## Installation

* Traditional `git`:

```bash
git clone https://github.com/Trevohack/Dynasty-C2 
cd Dynasty-C2 
chmod +x dynasty.sh
./dynasty.sh <lhost> <lport> <web_port>
``` 


## Documentation

> `Dynasty` is a powerful C2 framework that can handle multiple sessions (agents), entirely coded in Python. 

> Please note that this project is currently in beta, meaning it's under active development and may have some issues.

### [ FEATURES ] 

- [X] Own web server for hosting required payloads
- [X] One-liner to start console and web server 
- [X] Agent interaction 
- [X] Support for multiple connections
- [ ] Windows compatibility
- [ ] Persistence payloads
- [X] Generates a unique key for each agent as a unique ID 
- [X] Provides a user-friendly interface 


### [ COMMANDS ]

| Command | Description |
| :-------- | :-------   | 
| **`agents`** |  List all active connections |
| **`use [agent]`** | Interact with a selected agent (opens a shell) |
| **`kill [key]`** | Terminate a selected agent using its key |
| **`show payloads`** | Display all available payloads | 
| **`use payload [num]`** | Activate a selected payload on the target |
| **`troll`** | Send commands to all ttys on the target |
| **`server status`** | Show the status of the web server |


## Usage 

* Run the `dynasty.sh` script to set up environment: start console and the web server on desired ports: `./dynasty.sh 0.0.0.0 9999 9090` 

* This will pop up a loading screen and the console after a while. 

* All logs of the web server will be saved at `web_app/web_app.log`. 

* The console can be used independently as well: `python3 server.py <lhost> <lport> <web_port>`. 


```bash
[dev@dynasty]~# Dynasty-C2 is still under development, it may have some issues. A more stable version of it will be out soon
```




