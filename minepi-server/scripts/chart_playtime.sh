#!/bin/bash
# Paths
BASE_DIR="/home/clamytoe/minecraft-server"
DATA_DIR="$BASE_DIR/data"
LOG_FILE="$BASE_DIR/logs/player_logins.json"

echo "📊 Playtime Report"
echo "-------------------------"

jq -r '.player' "$LOG_FILE" | sort | uniq | while read player; do
  count=$(jq -r --arg p "$player" '. | select(.player==$p)' "$LOG_FILE" | wc -l)
  minutes=$((count))  # 1 event = 1 Earn-A-Minute token
  echo "🧍 $player: $minutes min earned"
done