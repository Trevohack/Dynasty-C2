#!/bin/bash


usage() {
    echo "Usage: $0 <ip> <port> <web port>"
    exit 1
}
animation_chars="/-\|"
start_time=$(date +%s)
while true; do
    current_time=$(date +%s)
    elapsed_time=$((current_time - start_time))
    if [ $elapsed_time -ge 10 ]; then
        break
    fi

    for (( i=0; i<${#animation_chars}; i++ )); do
        echo -en "${animation_chars:$i:1} Activating the dynasty...\r"
        sleep 0.1
    done
done

ip="$1"
port="$2" 
web_port="$3" 
log_file="web_app.log" 

if [[ $# -ne 3 ]]; then
    echo "Error: Missing required arguments."
    usage
fi 

cd web_app 
flask run --host="$ip" --port="$web_port" > "$log_file" 2>&1 & 
echo "Flask app running in the background. Logs redirected to $log_file" 

echo "[+] Activating server"
python3 dynasty/server.py $ip $port $web_port
