#!/bin/bash
clear

# Colors and style
green="\e[32m"
bold="\e[1m"
reset="\e[0m"
glitch="\e[5m"
divider="${glitch}${green}--===[*]===--${reset}"

# Paths
BASE_DIR="/home/clamytoe/minecraft-server"
DATA_DIR="$BASE_DIR/data"
LOG_FILE="$BASE_DIR/logs/player_logins.json"
BACKUP_DIR="$BASE_DIR/backups"

# Header
echo -e "${green}${bold}🧬 Cobblemon Terminal Dashboard 🧬${reset}"
echo -e "$divider"

# Server Status
status=$(docker inspect -f '{{.State.Status}}' cobblemon-server 2>/dev/null)
echo -e "🖥️ Server Status: ${bold}${status^^}${reset}"

# Uptime
up=$(uptime -p)
echo -e "⏱️ Host Uptime: $up"

# Backups
count=$(ls $BACKUP_DIR/*.zip 2>/dev/null | wc -l)
latest=$(ls -t $BACKUP_DIR/*.zip 2>/dev/null | head -n 1)
echo -e "🗂️ Backups: $count (latest: ${latest##*/})"

echo -e "$divider"

# Recent Players
echo -e "${bold}🧍 Recent Player Logins:${reset}"
jq -c '. | {time: .timestamp, player: .player}' $LOG_FILE | tail -n 3 | while read entry; do
  time=$(echo "$entry" | jq -r '.time')
  player=$(echo "$entry" | jq -r '.player')
  echo -e "🔹 $player @ $time"
done

# Time Earned (example parser)
total_minutes=$(jq -r '. | select(.player=="Steve") | .timestamp' $LOG_FILE | wc -l)
echo -e "\n🎖️ Steve's Earn-A-Minute Count: ${bold}$total_minutes min${reset}"

echo -e "$divider"
echo -e "${green}🔄 Refresh with: watch -n 10 ${BASE_DIR}/scripts/dashboard.sh${reset}"